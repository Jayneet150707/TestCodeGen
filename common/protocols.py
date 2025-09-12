"""
Common protocols and interfaces for Agent Fabric system.
Defines the communication standards between agents using Google ADK.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class MessageType(Enum):
    """Types of messages that can be exchanged between agents."""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class AgentStatus(Enum):
    """Status of an agent in the system."""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class WorkflowStatus(Enum):
    """Status of a workflow execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REQUIRES_HUMAN = "requires_human"


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.REQUEST
    sender_id: str = ""
    recipient_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    priority: int = 5  # 1-10, where 1 is highest priority
    ttl: Optional[int] = None  # Time to live in seconds


@dataclass
class AgentCapability:
    """Describes what an agent can do."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    required_permissions: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # seconds


@dataclass
class AgentMetadata:
    """Metadata about an agent instance."""
    id: str
    name: str
    version: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    last_heartbeat: datetime
    load_factor: float = 0.0  # 0.0 to 1.0
    error_count: int = 0
    total_requests: int = 0


@dataclass
class WorkflowStep:
    """Represents a single step in a workflow."""
    id: str
    agent_id: str
    capability: str
    input_data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    timeout: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class WorkflowDefinition:
    """Defines a complete workflow with multiple steps."""
    id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    version: str = "1.0"


@dataclass
class WorkflowExecution:
    """Tracks the execution of a workflow instance."""
    id: str
    workflow_id: str
    status: WorkflowStatus
    current_step: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


class AgentProtocol(ABC):
    """Abstract base class defining the agent protocol interface."""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent and register with the orchestrator."""
        pass
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """Process an incoming message and return a response."""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> List[AgentCapability]:
        """Return the list of capabilities this agent provides."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Return the current health status of the agent."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Gracefully shutdown the agent."""
        pass


class OrchestratorProtocol(ABC):
    """Abstract base class for the orchestrator interface."""
    
    @abstractmethod
    async def register_agent(self, agent_metadata: AgentMetadata) -> bool:
        """Register a new agent with the orchestrator."""
        pass
    
    @abstractmethod
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the orchestrator."""
        pass
    
    @abstractmethod
    async def route_message(self, message: AgentMessage) -> bool:
        """Route a message to the appropriate agent."""
        pass
    
    @abstractmethod
    async def execute_workflow(self, workflow: WorkflowDefinition, 
                             context: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow and return the execution instance."""
        pass
    
    @abstractmethod
    async def get_agent_status(self, agent_id: str) -> Optional[AgentMetadata]:
        """Get the current status of a specific agent."""
        pass


class PolicyProtocol(ABC):
    """Abstract base class for policy enforcement."""
    
    @abstractmethod
    async def validate_request(self, message: AgentMessage) -> bool:
        """Validate if a request complies with policies."""
        pass
    
    @abstractmethod
    async def audit_log(self, event: Dict[str, Any]) -> bool:
        """Log an event for audit purposes."""
        pass
    
    @abstractmethod
    async def check_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check data compliance and return validation results."""
        pass


class HiTLProtocol(ABC):
    """Abstract base class for Human-in-the-Loop functionality."""
    
    @abstractmethod
    async def requires_human_review(self, context: Dict[str, Any]) -> bool:
        """Determine if human review is required."""
        pass
    
    @abstractmethod
    async def escalate_to_human(self, case: Dict[str, Any]) -> str:
        """Escalate a case to human review and return case ID."""
        pass
    
    @abstractmethod
    async def get_human_decision(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get the human decision for a case."""
        pass


# Common data structures for financial services
@dataclass
class LoanApplication:
    """Standard loan application data structure."""
    id: str
    applicant_id: str
    loan_amount: float
    loan_purpose: str
    employment_info: Dict[str, Any]
    financial_info: Dict[str, Any]
    documents: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"


@dataclass
class CreditAssessment:
    """Credit assessment result structure."""
    application_id: str
    credit_score: int
    risk_level: str  # low, medium, high
    decision: str  # approve, decline, review
    confidence: float
    factors: List[str]
    assessed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class FraudAnalysis:
    """Fraud analysis result structure."""
    application_id: str
    fraud_score: float  # 0.0 to 1.0
    risk_indicators: List[str]
    decision: str  # clear, suspicious, fraudulent
    confidence: float
    analyzed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class KYCResult:
    """KYC verification result structure."""
    applicant_id: str
    identity_verified: bool
    document_verification: Dict[str, bool]
    address_verified: bool
    sanctions_check: bool
    verification_level: str  # basic, enhanced, premium
    verified_at: datetime = field(default_factory=datetime.utcnow)

