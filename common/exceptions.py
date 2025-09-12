"""
Custom exceptions for the Agent Fabric system.
Provides specific error types for different failure scenarios.
"""

from typing import Any, Dict, Optional


class AgentFabricException(Exception):
    """Base exception for all Agent Fabric errors."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}


class AgentException(AgentFabricException):
    """Base exception for agent-related errors."""
    pass


class AgentNotFoundError(AgentException):
    """Raised when an agent cannot be found."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            f"Agent with ID '{agent_id}' not found",
            "AGENT_NOT_FOUND",
            {"agent_id": agent_id}
        )


class AgentUnavailableError(AgentException):
    """Raised when an agent is unavailable for processing."""
    
    def __init__(self, agent_id: str, reason: str = "Unknown"):
        super().__init__(
            f"Agent '{agent_id}' is unavailable: {reason}",
            "AGENT_UNAVAILABLE",
            {"agent_id": agent_id, "reason": reason}
        )


class AgentTimeoutError(AgentException):
    """Raised when an agent operation times out."""
    
    def __init__(self, agent_id: str, timeout: int):
        super().__init__(
            f"Agent '{agent_id}' operation timed out after {timeout} seconds",
            "AGENT_TIMEOUT",
            {"agent_id": agent_id, "timeout": timeout}
        )


class WorkflowException(AgentFabricException):
    """Base exception for workflow-related errors."""
    pass


class WorkflowNotFoundError(WorkflowException):
    """Raised when a workflow cannot be found."""
    
    def __init__(self, workflow_id: str):
        super().__init__(
            f"Workflow with ID '{workflow_id}' not found",
            "WORKFLOW_NOT_FOUND",
            {"workflow_id": workflow_id}
        )


class WorkflowExecutionError(WorkflowException):
    """Raised when workflow execution fails."""
    
    def __init__(self, workflow_id: str, step_id: str = None, reason: str = "Unknown"):
        message = f"Workflow '{workflow_id}' execution failed"
        if step_id:
            message += f" at step '{step_id}'"
        message += f": {reason}"
        
        super().__init__(
            message,
            "WORKFLOW_EXECUTION_ERROR",
            {"workflow_id": workflow_id, "step_id": step_id, "reason": reason}
        )


class WorkflowValidationError(WorkflowException):
    """Raised when workflow validation fails."""
    
    def __init__(self, workflow_id: str, validation_errors: list):
        super().__init__(
            f"Workflow '{workflow_id}' validation failed: {', '.join(validation_errors)}",
            "WORKFLOW_VALIDATION_ERROR",
            {"workflow_id": workflow_id, "validation_errors": validation_errors}
        )


class PolicyException(AgentFabricException):
    """Base exception for policy-related errors."""
    pass


class PolicyViolationError(PolicyException):
    """Raised when a policy violation is detected."""
    
    def __init__(self, policy_name: str, violation_details: str):
        super().__init__(
            f"Policy violation detected in '{policy_name}': {violation_details}",
            "POLICY_VIOLATION",
            {"policy_name": policy_name, "violation_details": violation_details}
        )


class ComplianceError(PolicyException):
    """Raised when compliance requirements are not met."""
    
    def __init__(self, requirement: str, details: str = ""):
        super().__init__(
            f"Compliance requirement not met: {requirement}. {details}",
            "COMPLIANCE_ERROR",
            {"requirement": requirement, "details": details}
        )


class DataException(AgentFabricException):
    """Base exception for data-related errors."""
    pass


class DataValidationError(DataException):
    """Raised when data validation fails."""
    
    def __init__(self, field: str, value: Any, reason: str):
        super().__init__(
            f"Data validation failed for field '{field}' with value '{value}': {reason}",
            "DATA_VALIDATION_ERROR",
            {"field": field, "value": str(value), "reason": reason}
        )


class DataNotFoundError(DataException):
    """Raised when required data cannot be found."""
    
    def __init__(self, data_type: str, identifier: str):
        super().__init__(
            f"{data_type} with identifier '{identifier}' not found",
            "DATA_NOT_FOUND",
            {"data_type": data_type, "identifier": identifier}
        )


class ExternalServiceException(AgentFabricException):
    """Base exception for external service errors."""
    pass


class ExternalServiceUnavailableError(ExternalServiceException):
    """Raised when an external service is unavailable."""
    
    def __init__(self, service_name: str, status_code: int = None):
        message = f"External service '{service_name}' is unavailable"
        if status_code:
            message += f" (HTTP {status_code})"
        
        super().__init__(
            message,
            "EXTERNAL_SERVICE_UNAVAILABLE",
            {"service_name": service_name, "status_code": status_code}
        )


class ExternalServiceTimeoutError(ExternalServiceException):
    """Raised when an external service call times out."""
    
    def __init__(self, service_name: str, timeout: int):
        super().__init__(
            f"External service '{service_name}' timed out after {timeout} seconds",
            "EXTERNAL_SERVICE_TIMEOUT",
            {"service_name": service_name, "timeout": timeout}
        )


class AuthenticationError(AgentFabricException):
    """Raised when authentication fails."""
    
    def __init__(self, reason: str = "Invalid credentials"):
        super().__init__(
            f"Authentication failed: {reason}",
            "AUTHENTICATION_ERROR",
            {"reason": reason}
        )


class AuthorizationError(AgentFabricException):
    """Raised when authorization fails."""
    
    def __init__(self, resource: str, action: str):
        super().__init__(
            f"Access denied: insufficient permissions to {action} {resource}",
            "AUTHORIZATION_ERROR",
            {"resource": resource, "action": action}
        )


class ConfigurationError(AgentFabricException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, config_key: str, reason: str = "Invalid or missing"):
        super().__init__(
            f"Configuration error for '{config_key}': {reason}",
            "CONFIGURATION_ERROR",
            {"config_key": config_key, "reason": reason}
        )


class ResourceExhaustionError(AgentFabricException):
    """Raised when system resources are exhausted."""
    
    def __init__(self, resource_type: str, limit: Any = None):
        message = f"Resource exhaustion: {resource_type}"
        if limit:
            message += f" (limit: {limit})"
        
        super().__init__(
            message,
            "RESOURCE_EXHAUSTION",
            {"resource_type": resource_type, "limit": str(limit) if limit else None}
        )


# Financial Services Specific Exceptions

class FinancialServiceException(AgentFabricException):
    """Base exception for financial service errors."""
    pass


class CreditAssessmentError(FinancialServiceException):
    """Raised when credit assessment fails."""
    
    def __init__(self, applicant_id: str, reason: str):
        super().__init__(
            f"Credit assessment failed for applicant '{applicant_id}': {reason}",
            "CREDIT_ASSESSMENT_ERROR",
            {"applicant_id": applicant_id, "reason": reason}
        )


class FraudDetectionError(FinancialServiceException):
    """Raised when fraud detection fails."""
    
    def __init__(self, application_id: str, reason: str):
        super().__init__(
            f"Fraud detection failed for application '{application_id}': {reason}",
            "FRAUD_DETECTION_ERROR",
            {"application_id": application_id, "reason": reason}
        )


class KYCVerificationError(FinancialServiceException):
    """Raised when KYC verification fails."""
    
    def __init__(self, applicant_id: str, verification_type: str, reason: str):
        super().__init__(
            f"KYC {verification_type} verification failed for applicant '{applicant_id}': {reason}",
            "KYC_VERIFICATION_ERROR",
            {"applicant_id": applicant_id, "verification_type": verification_type, "reason": reason}
        )


class DocumentProcessingError(FinancialServiceException):
    """Raised when document processing fails."""
    
    def __init__(self, document_id: str, processing_type: str, reason: str):
        super().__init__(
            f"Document {processing_type} failed for document '{document_id}': {reason}",
            "DOCUMENT_PROCESSING_ERROR",
            {"document_id": document_id, "processing_type": processing_type, "reason": reason}
        )


class InsufficientDataError(FinancialServiceException):
    """Raised when insufficient data is available for processing."""
    
    def __init__(self, required_data: str, context: str = ""):
        message = f"Insufficient data: {required_data}"
        if context:
            message += f" (context: {context})"
        
        super().__init__(
            message,
            "INSUFFICIENT_DATA",
            {"required_data": required_data, "context": context}
        )


def handle_exception(func):
    """Decorator to handle and log exceptions consistently."""
    import functools
    import logging
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AgentFabricException as e:
            logging.error(f"Agent Fabric Exception in {func.__name__}: {e.message}", 
                         extra={"error_code": e.error_code, "details": e.details})
            raise
        except Exception as e:
            logging.error(f"Unexpected exception in {func.__name__}: {str(e)}")
            raise AgentFabricException(
                f"Unexpected error in {func.__name__}: {str(e)}",
                "UNEXPECTED_ERROR",
                {"function": func.__name__, "original_error": str(e)}
            )
    
    return wrapper

