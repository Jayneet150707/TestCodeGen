"""
Intake Agent - Handles loan application intake and initial processing.
First point of contact for new loan applications.
"""

import uuid
from typing import Any, Dict, List
from datetime import datetime

from .base_agent import BaseAgent
from common.protocols import AgentCapability, AgentMessage, LoanApplication
from common.exceptions import DataValidationError, handle_exception


class IntakeAgent(BaseAgent):
    """
    Intake Agent responsible for:
    - Receiving new loan applications
    - Initial data validation
    - Application preprocessing
    - Routing to appropriate next steps
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="intake-agent",
            name="Intake Agent",
            version="1.0.0",
            config=config
        )
    
    async def _load_capabilities(self) -> List[AgentCapability]:
        """Load capabilities specific to the Intake Agent."""
        return [
            AgentCapability(
                name="process_application",
                description="Process a new loan application",
                input_schema={
                    "type": "object",
                    "properties": {
                        "applicant_info": {
                            "type": "object",
                            "properties": {
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "email": {"type": "string", "format": "email"},
                                "phone": {"type": "string"},
                                "ssn": {"type": "string"},
                                "date_of_birth": {"type": "string", "format": "date"}
                            },
                            "required": ["first_name", "last_name", "email", "ssn"]
                        },
                        "loan_details": {
                            "type": "object",
                            "properties": {
                                "amount": {"type": "number", "minimum": 1000},
                                "purpose": {"type": "string"},
                                "term_months": {"type": "integer", "minimum": 12, "maximum": 360}
                            },
                            "required": ["amount", "purpose", "term_months"]
                        },
                        "employment_info": {
                            "type": "object",
                            "properties": {
                                "employer": {"type": "string"},
                                "position": {"type": "string"},
                                "annual_income": {"type": "number", "minimum": 0},
                                "employment_length_months": {"type": "integer", "minimum": 0}
                            },
                            "required": ["employer", "annual_income"]
                        },
                        "documents": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["applicant_info", "loan_details", "employment_info"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string"},
                        "status": {"type": "string"},
                        "next_steps": {"type": "array", "items": {"type": "string"}},
                        "validation_results": {"type": "object"},
                        "created_at": {"type": "string", "format": "date-time"}
                    }
                },
                estimated_duration=30
            ),
            AgentCapability(
                name="validate_application",
                description="Validate application data completeness and format",
                input_schema={
                    "type": "object",
                    "properties": {
                        "application_data": {"type": "object"}
                    },
                    "required": ["application_data"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "is_valid": {"type": "boolean"},
                        "validation_errors": {"type": "array", "items": {"type": "string"}},
                        "completeness_score": {"type": "number", "minimum": 0, "maximum": 1}
                    }
                },
                estimated_duration=10
            ),
            AgentCapability(
                name="get_application_status",
                description="Retrieve the current status of an application",
                input_schema={
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string"}
                    },
                    "required": ["application_id"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "string"},
                        "status": {"type": "string"},
                        "current_stage": {"type": "string"},
                        "last_updated": {"type": "string", "format": "date-time"}
                    }
                },
                estimated_duration=5
            )
        ]
    
    @handle_exception
    async def _process_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Process incoming requests based on the capability requested."""
        capability = message.payload.get('capability')
        data = message.payload.get('data', {})
        
        if capability == 'process_application':
            return await self._process_application(data)
        elif capability == 'validate_application':
            return await self._validate_application(data)
        elif capability == 'get_application_status':
            return await self._get_application_status(data)
        else:
            raise ValueError(f"Unknown capability: {capability}")
    
    async def _process_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a new loan application."""
        try:
            # Generate unique application ID
            application_id = str(uuid.uuid4())
            
            # Extract and validate data
            applicant_info = data.get('applicant_info', {})
            loan_details = data.get('loan_details', {})
            employment_info = data.get('employment_info', {})
            documents = data.get('documents', [])
            
            # Validate required fields
            validation_result = await self._validate_application_data({
                'applicant_info': applicant_info,
                'loan_details': loan_details,
                'employment_info': employment_info
            })
            
            if not validation_result['is_valid']:
                return {
                    'application_id': application_id,
                    'status': 'rejected',
                    'reason': 'Validation failed',
                    'validation_errors': validation_result['validation_errors'],
                    'created_at': datetime.utcnow().isoformat()
                }
            
            # Create loan application object
            loan_application = LoanApplication(
                id=application_id,
                applicant_id=applicant_info.get('email', ''),  # Using email as temp ID
                loan_amount=loan_details.get('amount', 0),
                loan_purpose=loan_details.get('purpose', ''),
                employment_info=employment_info,
                financial_info={
                    'annual_income': employment_info.get('annual_income', 0),
                    'requested_amount': loan_details.get('amount', 0),
                    'debt_to_income_ratio': None  # To be calculated later
                },
                documents=documents,
                status='intake_complete'
            )
            
            # Store application in Firestore
            await self._store_application(loan_application)
            
            # Determine next steps based on application characteristics
            next_steps = await self._determine_next_steps(loan_application)
            
            # Log audit event
            await self.log_audit_event('application_processed', {
                'application_id': application_id,
                'applicant_email': applicant_info.get('email'),
                'loan_amount': loan_details.get('amount'),
                'next_steps': next_steps
            })
            
            return {
                'application_id': application_id,
                'status': 'accepted',
                'next_steps': next_steps,
                'validation_results': validation_result,
                'created_at': datetime.utcnow().isoformat(),
                'estimated_processing_time': '2-5 business days'
            }
            
        except Exception as e:
            self.logger.error(f"Error processing application: {e}")
            raise
    
    async def _validate_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate application data completeness and format."""
        return await self._validate_application_data(data.get('application_data', {}))
    
    async def _validate_application_data(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to validate application data."""
        errors = []
        completeness_score = 0.0
        total_fields = 0
        completed_fields = 0
        
        # Validate applicant info
        applicant_info = application_data.get('applicant_info', {})
        required_applicant_fields = ['first_name', 'last_name', 'email', 'ssn']
        
        for field in required_applicant_fields:
            total_fields += 1
            if field in applicant_info and applicant_info[field]:
                completed_fields += 1
                
                # Specific validations
                if field == 'email' and '@' not in applicant_info[field]:
                    errors.append(f"Invalid email format: {applicant_info[field]}")
                elif field == 'ssn' and len(applicant_info[field].replace('-', '')) != 9:
                    errors.append("SSN must be 9 digits")
            else:
                errors.append(f"Missing required field: {field}")
        
        # Validate loan details
        loan_details = application_data.get('loan_details', {})
        required_loan_fields = ['amount', 'purpose', 'term_months']
        
        for field in required_loan_fields:
            total_fields += 1
            if field in loan_details and loan_details[field]:
                completed_fields += 1
                
                # Specific validations
                if field == 'amount':
                    amount = loan_details[field]
                    if not isinstance(amount, (int, float)) or amount < 1000:
                        errors.append("Loan amount must be at least $1,000")
                    elif amount > 1000000:
                        errors.append("Loan amount cannot exceed $1,000,000")
                elif field == 'term_months':
                    term = loan_details[field]
                    if not isinstance(term, int) or term < 12 or term > 360:
                        errors.append("Loan term must be between 12 and 360 months")
            else:
                errors.append(f"Missing required field: {field}")
        
        # Validate employment info
        employment_info = application_data.get('employment_info', {})
        required_employment_fields = ['employer', 'annual_income']
        
        for field in required_employment_fields:
            total_fields += 1
            if field in employment_info and employment_info[field]:
                completed_fields += 1
                
                # Specific validations
                if field == 'annual_income':
                    income = employment_info[field]
                    if not isinstance(income, (int, float)) or income < 0:
                        errors.append("Annual income must be a positive number")
            else:
                errors.append(f"Missing required field: {field}")
        
        # Calculate completeness score
        if total_fields > 0:
            completeness_score = completed_fields / total_fields
        
        return {
            'is_valid': len(errors) == 0,
            'validation_errors': errors,
            'completeness_score': completeness_score
        }
    
    async def _get_application_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get the current status of an application."""
        application_id = data.get('application_id')
        
        if not application_id:
            raise DataValidationError('application_id', None, 'Application ID is required')
        
        try:
            # Retrieve application from Firestore
            doc_ref = self.firestore_client.collection('applications').document(application_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return {
                    'application_id': application_id,
                    'status': 'not_found',
                    'message': 'Application not found'
                }
            
            app_data = doc.to_dict()
            
            return {
                'application_id': application_id,
                'status': app_data.get('status', 'unknown'),
                'current_stage': app_data.get('current_stage', 'intake'),
                'last_updated': app_data.get('last_updated', datetime.utcnow().isoformat()),
                'progress_percentage': self._calculate_progress(app_data.get('status', 'unknown'))
            }
            
        except Exception as e:
            self.logger.error(f"Error retrieving application status: {e}")
            raise
    
    async def _store_application(self, application: LoanApplication):
        """Store the loan application in Firestore."""
        try:
            doc_ref = self.firestore_client.collection('applications').document(application.id)
            doc_ref.set({
                'id': application.id,
                'applicant_id': application.applicant_id,
                'loan_amount': application.loan_amount,
                'loan_purpose': application.loan_purpose,
                'employment_info': application.employment_info,
                'financial_info': application.financial_info,
                'documents': application.documents,
                'status': application.status,
                'created_at': application.created_at,
                'last_updated': datetime.utcnow(),
                'current_stage': 'intake'
            })
            
            self.logger.info(f"Stored application {application.id} in Firestore")
            
        except Exception as e:
            self.logger.error(f"Error storing application: {e}")
            raise
    
    async def _determine_next_steps(self, application: LoanApplication) -> List[str]:
        """Determine the next processing steps based on application characteristics."""
        next_steps = []
        
        # Always start with document processing if documents are provided
        if application.documents:
            next_steps.append('ocr_processing')
        
        # Always require KYC verification
        next_steps.append('kyc_verification')
        
        # Determine if enhanced fraud screening is needed
        if application.loan_amount > 100000:  # High-value loans
            next_steps.append('enhanced_fraud_screening')
        else:
            next_steps.append('standard_fraud_screening')
        
        # Credit assessment is always required
        next_steps.append('credit_assessment')
        
        # Data enrichment for better decision making
        next_steps.append('data_enrichment')
        
        return next_steps
    
    def _calculate_progress(self, status: str) -> int:
        """Calculate progress percentage based on current status."""
        status_progress = {
            'intake_complete': 10,
            'documents_processed': 20,
            'kyc_verified': 40,
            'fraud_cleared': 60,
            'credit_assessed': 80,
            'approved': 100,
            'declined': 100,
            'requires_review': 75
        }
        
        return status_progress.get(status, 0)

