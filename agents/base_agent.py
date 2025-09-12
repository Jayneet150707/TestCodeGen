"""
Base Agent class for the Agent Fabric system using Google ADK.
All specialized agents inherit from this base class.
"""

import asyncio
import logging
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from google.cloud import aiplatform
from google.cloud import pubsub_v1
from google.cloud import firestore

from common.protocols import (
    AgentProtocol, AgentMessage, AgentCapability, AgentMetadata, 
    AgentStatus, MessageType
)
from common.exceptions import (
    AgentException, AgentTimeoutError, AgentUnavailableError,
    handle_exception
)


class BaseAgent(AgentProtocol):
    """
    Base agent class implementing Google ADK integration and common functionality.
    All specialized agents should inherit from this class.
    """
    
    def __init__(self, agent_id: str, name: str, version: str = "1.0.0", config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.name = name
        self.version = version
        self.config = config or {}
        self.status = AgentStatus.INITIALIZING
        self.capabilities: List[AgentCapability] = []
        self.last_heartbeat = datetime.utcnow()
        self.load_factor = 0.0
        self.error_count = 0
        self.total_requests = 0
        
        # Google Cloud clients
        self.project_id = self.config.get('google_adk', {}).get('project_id')
        self.region = self.config.get('google_adk', {}).get('region', 'us-central1')
        
        # Initialize Google Cloud clients
        self._init_google_clients()
        
        # Message queue for processing
        self.message_queue = asyncio.Queue()
        self.processing_task: Optional[asyncio.Task] = None
        
        # Logger
        self.logger = logging.getLogger(f"agent.{self.name}")
        
    def _init_google_clients(self):
        """Initialize Google Cloud clients for ADK integration."""
        try:
            # AI Platform client for ML operations
            aiplatform.init(project=self.project_id, location=self.region)
            
            # Pub/Sub client for messaging
            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()
            
            # Firestore client for state management
            self.firestore_client = firestore.Client(project=self.project_id)
            
            # Topic and subscription names
            self.topic_name = f"projects/{self.project_id}/topics/agent-{self.agent_id}"
            self.subscription_name = f"projects/{self.project_id}/subscriptions/agent-{self.agent_id}-sub"
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Cloud clients: {e}")
            raise AgentException(f"Google Cloud initialization failed: {e}")
    
    @handle_exception
    async def initialize(self) -> bool:
        """Initialize the agent and register with the orchestrator."""
        try:
            self.logger.info(f"Initializing agent {self.name} ({self.agent_id})")
            
            # Create Pub/Sub topic and subscription
            await self._setup_pubsub()
            
            # Load agent-specific capabilities
            self.capabilities = await self._load_capabilities()
            
            # Register with orchestrator
            await self._register_with_orchestrator()
            
            # Start message processing
            self.processing_task = asyncio.create_task(self._process_messages())
            
            # Start heartbeat
            asyncio.create_task(self._heartbeat_loop())
            
            self.status = AgentStatus.READY
            self.logger.info(f"Agent {self.name} initialized successfully")
            return True
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.logger.error(f"Agent initialization failed: {e}")
            raise
    
    async def _setup_pubsub(self):
        """Set up Pub/Sub topic and subscription for the agent."""
        try:
            # Create topic
            try:
                self.publisher.create_topic(request={"name": self.topic_name})
                self.logger.info(f"Created topic: {self.topic_name}")
            except Exception:
                # Topic might already exist
                pass
            
            # Create subscription
            try:
                self.subscriber.create_subscription(
                    request={
                        "name": self.subscription_name,
                        "topic": self.topic_name
                    }
                )
                self.logger.info(f"Created subscription: {self.subscription_name}")
            except Exception:
                # Subscription might already exist
                pass
                
        except Exception as e:
            self.logger.error(f"Failed to setup Pub/Sub: {e}")
            raise
    
    @abstractmethod
    async def _load_capabilities(self) -> List[AgentCapability]:
        """Load the capabilities this agent provides. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    async def _process_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Process a specific request. Must be implemented by subclasses."""
        pass
    
    async def _register_with_orchestrator(self):
        """Register this agent with the orchestrator."""
        try:
            metadata = AgentMetadata(
                id=self.agent_id,
                name=self.name,
                version=self.version,
                status=self.status,
                capabilities=self.capabilities,
                last_heartbeat=self.last_heartbeat,
                load_factor=self.load_factor,
                error_count=self.error_count,
                total_requests=self.total_requests
            )
            
            # Store agent metadata in Firestore
            doc_ref = self.firestore_client.collection('agents').document(self.agent_id)
            doc_ref.set({
                'id': metadata.id,
                'name': metadata.name,
                'version': metadata.version,
                'status': metadata.status.value,
                'capabilities': [
                    {
                        'name': cap.name,
                        'description': cap.description,
                        'input_schema': cap.input_schema,
                        'output_schema': cap.output_schema,
                        'required_permissions': cap.required_permissions,
                        'estimated_duration': cap.estimated_duration
                    } for cap in metadata.capabilities
                ],
                'last_heartbeat': metadata.last_heartbeat,
                'load_factor': metadata.load_factor,
                'error_count': metadata.error_count,
                'total_requests': metadata.total_requests
            })
            
            self.logger.info(f"Registered agent {self.agent_id} with orchestrator")
            
        except Exception as e:
            self.logger.error(f"Failed to register with orchestrator: {e}")
            raise
    
    async def _process_messages(self):
        """Main message processing loop."""
        while self.status != AgentStatus.OFFLINE:
            try:
                # Pull messages from Pub/Sub
                response = self.subscriber.pull(
                    request={
                        "subscription": self.subscription_name,
                        "max_messages": 10
                    },
                    timeout=30.0
                )
                
                for received_message in response.received_messages:
                    try:
                        # Parse message
                        message_data = json.loads(received_message.message.data.decode('utf-8'))
                        agent_message = AgentMessage(**message_data)
                        
                        # Process message
                        response_message = await self.process_message(agent_message)
                        
                        # Send response if needed
                        if response_message and agent_message.sender_id:
                            await self._send_message(response_message, agent_message.sender_id)
                        
                        # Acknowledge message
                        self.subscriber.acknowledge(
                            request={
                                "subscription": self.subscription_name,
                                "ack_ids": [received_message.ack_id]
                            }
                        )
                        
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                        self.error_count += 1
                        
            except Exception as e:
                if "timeout" not in str(e).lower():
                    self.logger.error(f"Error in message processing loop: {e}")
                await asyncio.sleep(1)
    
    @handle_exception
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """Process an incoming message and return a response."""
        try:
            self.status = AgentStatus.BUSY
            self.total_requests += 1
            self.last_heartbeat = datetime.utcnow()
            
            self.logger.info(f"Processing message {message.id} from {message.sender_id}")
            
            # Process the request
            result = await self._process_request(message)
            
            # Create response message
            response = AgentMessage(
                type=MessageType.RESPONSE,
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                correlation_id=message.id,
                payload=result
            )
            
            self.status = AgentStatus.READY
            return response
            
        except Exception as e:
            self.error_count += 1
            self.status = AgentStatus.ERROR
            self.logger.error(f"Error processing message {message.id}: {e}")
            
            # Create error response
            error_response = AgentMessage(
                type=MessageType.ERROR,
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                correlation_id=message.id,
                payload={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            
            return error_response
    
    async def _send_message(self, message: AgentMessage, recipient_topic: str):
        """Send a message to another agent via Pub/Sub."""
        try:
            topic_path = f"projects/{self.project_id}/topics/agent-{recipient_topic}"
            message_data = json.dumps({
                'id': message.id,
                'type': message.type.value,
                'sender_id': message.sender_id,
                'recipient_id': message.recipient_id,
                'timestamp': message.timestamp.isoformat(),
                'payload': message.payload,
                'correlation_id': message.correlation_id,
                'priority': message.priority,
                'ttl': message.ttl
            }).encode('utf-8')
            
            future = self.publisher.publish(topic_path, message_data)
            future.result()  # Wait for publish to complete
            
            self.logger.debug(f"Sent message {message.id} to {recipient_topic}")
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            raise
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats to maintain agent registration."""
        while self.status != AgentStatus.OFFLINE:
            try:
                self.last_heartbeat = datetime.utcnow()
                
                # Update agent status in Firestore
                doc_ref = self.firestore_client.collection('agents').document(self.agent_id)
                doc_ref.update({
                    'status': self.status.value,
                    'last_heartbeat': self.last_heartbeat,
                    'load_factor': self.load_factor,
                    'error_count': self.error_count,
                    'total_requests': self.total_requests
                })
                
                await asyncio.sleep(30)  # Heartbeat every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Heartbeat failed: {e}")
                await asyncio.sleep(5)
    
    async def get_capabilities(self) -> List[AgentCapability]:
        """Return the list of capabilities this agent provides."""
        return self.capabilities
    
    async def health_check(self) -> Dict[str, Any]:
        """Return the current health status of the agent."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status.value,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "load_factor": self.load_factor,
            "error_count": self.error_count,
            "total_requests": self.total_requests,
            "uptime": (datetime.utcnow() - self.last_heartbeat).total_seconds()
        }
    
    async def shutdown(self) -> bool:
        """Gracefully shutdown the agent."""
        try:
            self.logger.info(f"Shutting down agent {self.name}")
            self.status = AgentStatus.OFFLINE
            
            # Cancel processing task
            if self.processing_task:
                self.processing_task.cancel()
                try:
                    await self.processing_task
                except asyncio.CancelledError:
                    pass
            
            # Unregister from orchestrator
            doc_ref = self.firestore_client.collection('agents').document(self.agent_id)
            doc_ref.update({'status': AgentStatus.OFFLINE.value})
            
            self.logger.info(f"Agent {self.name} shutdown complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False
    
    def update_load_factor(self, factor: float):
        """Update the current load factor of the agent."""
        self.load_factor = max(0.0, min(1.0, factor))
    
    async def log_audit_event(self, event_type: str, details: Dict[str, Any]):
        """Log an audit event for compliance tracking."""
        try:
            audit_doc = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'event_type': event_type,
                'timestamp': datetime.utcnow(),
                'details': details
            }
            
            self.firestore_client.collection('audit_logs').add(audit_doc)
            
        except Exception as e:
            self.logger.error(f"Failed to log audit event: {e}")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.agent_id}, name={self.name}, status={self.status.value})>"

