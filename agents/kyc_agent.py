"""
KYC Agent - Handles Know Your Customer verification and compliance checks.
Ensures regulatory compliance and identity verification.
"""

import re
from typing import Any, Dict, List
from datetime import datetime, date
import hashlib

from .base_agent import BaseAgent
from common.protocols import AgentCapability, AgentMessage, KYCResult
from common.exceptions import KYCVerificationError, handle_exception


class KYCAgent(BaseAgent):
    """
    KYC Agent responsible for:
    - Identity verification
    - Document validation
    - Address verification
    - Sanctions screening
    - Regulatory compliance checks
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="kyc-agent",
            name="KYC Agent",
            version="1.0.0",
            config=config
        )
        
        # KYC verification thresholds
        self.verification_thresholds = {
            'basic': {'min_score': 0.6, 'required_docs': 1},
            'enhanced': {'min_score': 0.8, 'required_docs': 2},
            'premium': {'min_score': 0.95, 'required_docs': 3}
        }
    
    async def _load_capabilities(self) -> List[AgentCapability]:
        """Load capabilities specific to the KYC Agent."""
        return [
            AgentCapability(
                name="verify_identity",
                description="Perform comprehensive identity verification",
                input_schema={
                    "type": "object",
                    "properties": {
                        "applicant_id": {"type": "string"},
                        "personal_info": {
                            "type": "object",
                            "properties": {
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "date_of_birth": {"type": "string", "format": "date"},
                                "ssn": {"type": "string"},
                                "address": {"type": "object"}
                            }
                        },
                        "documents": {"type": "array", "items": {"type": "string"}},
                        "verification_level": {"type": "string", "enum": ["basic", "enhanced", "premium"]}
                    },
                    "required": ["applicant_id", "personal_info", "verification_level"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verification_result": {"type": "object"},
                        "identity_score": {"type": "number"},
                        "risk_level": {"type": "string"},
                        "compliance_status": {"type": "string"}
                    }
                },
                estimated_duration=120
            ),
            AgentCapability(
                name="verify_documents",
                description="Verify authenticity of provided documents",
                input_schema={
                    "type": "object",
                    "properties": {
                        "documents": {"type": "array", "items": {"type": "string"}},
                        "document_types": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["documents"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "document_results": {"type": "object"},
                        "authenticity_score": {"type": "number"},
                        "issues_found": {"type": "array"}
                    }
                },
                estimated_duration=60
            ),
            AgentCapability(
                name="sanctions_screening",
                description="Screen against sanctions and watchlists",
                input_schema={
                    "type": "object",
                    "properties": {
                        "personal_info": {"type": "object"},
                        "screening_level": {"type": "string", "enum": ["standard", "enhanced"]}
                    },
                    "required": ["personal_info"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "screening_result": {"type": "string"},
                        "matches_found": {"type": "array"},
                        "risk_score": {"type": "number"}
                    }
                },
                estimated_duration=30
            )
        ]
    
    @handle_exception
    async def _process_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Process incoming KYC requests."""
        capability = message.payload.get('capability')
        data = message.payload.get('data', {})
        
        if capability == 'verify_identity':
            return await self._verify_identity(data)
        elif capability == 'verify_documents':
            return await self._verify_documents(data)
        elif capability == 'sanctions_screening':
            return await self._sanctions_screening(data)
        else:
            raise ValueError(f"Unknown capability: {capability}")
    
    async def _verify_identity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive identity verification."""
        try:
            applicant_id = data.get('applicant_id')
            personal_info = data.get('personal_info', {})
            documents = data.get('documents', [])
            verification_level = data.get('verification_level', 'basic')
            
            # Initialize verification result
            verification_result = {
                'identity_verified': False,
                'document_verification': {},
                'address_verified': False,
                'sanctions_clear': False,
                'verification_level': verification_level
            }
            
            identity_score = 0.0
            risk_factors = []
            
            # 1. Basic identity checks
            basic_score = await self._perform_basic_identity_checks(personal_info)
            identity_score += basic_score * 0.3
            
            if basic_score < 0.5:
                risk_factors.append("Failed basic identity validation")
            
            # 2. Document verification
            if documents:
                doc_result = await self._verify_documents({'documents': documents})
                verification_result['document_verification'] = doc_result['document_results']
                identity_score += doc_result['authenticity_score'] * 0.4
                
                if doc_result['authenticity_score'] < 0.7:
                    risk_factors.append("Document authenticity concerns")
            else:
                risk_factors.append("No documents provided for verification")
            
            # 3. Address verification
            address_score = await self._verify_address(personal_info.get('address', {}))
            verification_result['address_verified'] = address_score > 0.7
            identity_score += address_score * 0.2
            
            if not verification_result['address_verified']:
                risk_factors.append("Address verification failed")
            
            # 4. Sanctions screening
            sanctions_result = await self._sanctions_screening({
                'personal_info': personal_info,
                'screening_level': 'enhanced' if verification_level == 'premium' else 'standard'
            })
            verification_result['sanctions_clear'] = sanctions_result['screening_result'] == 'clear'
            identity_score += (1.0 if verification_result['sanctions_clear'] else 0.0) * 0.1
            
            if not verification_result['sanctions_clear']:
                risk_factors.append("Sanctions screening concerns")
            
            # 5. Determine overall verification status
            threshold = self.verification_thresholds[verification_level]['min_score']
            verification_result['identity_verified'] = identity_score >= threshold
            
            # Determine risk level
            risk_level = self._calculate_risk_level(identity_score, risk_factors)
            
            # Determine compliance status
            compliance_status = self._determine_compliance_status(
                verification_result, verification_level, identity_score
            )
            
            # Create KYC result object
            kyc_result = KYCResult(
                applicant_id=applicant_id,
                identity_verified=verification_result['identity_verified'],
                document_verification=verification_result['document_verification'],
                address_verified=verification_result['address_verified'],
                sanctions_check=verification_result['sanctions_clear'],
                verification_level=verification_level
            )
            
            # Store KYC result
            await self._store_kyc_result(kyc_result)
            
            # Log audit event
            await self.log_audit_event('kyc_verification_completed', {
                'applicant_id': applicant_id,
                'verification_level': verification_level,
                'identity_score': identity_score,
                'risk_level': risk_level,
                'compliance_status': compliance_status,
                'risk_factors': risk_factors
            })
            
            return {
                'verification_result': verification_result,
                'identity_score': round(identity_score, 3),
                'risk_level': risk_level,
                'compliance_status': compliance_status,
                'risk_factors': risk_factors,
                'verified_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in identity verification: {e}")
            raise KYCVerificationError(data.get('applicant_id', 'unknown'), 'identity', str(e))
    
    async def _perform_basic_identity_checks(self, personal_info: Dict[str, Any]) -> float:
        """Perform basic identity validation checks."""
        score = 0.0
        checks_passed = 0
        total_checks = 5
        
        # Check 1: Name validation
        first_name = personal_info.get('first_name', '').strip()
        last_name = personal_info.get('last_name', '').strip()
        if first_name and last_name and len(first_name) > 1 and len(last_name) > 1:
            checks_passed += 1
        
        # Check 2: SSN validation
        ssn = personal_info.get('ssn', '').replace('-', '').replace(' ', '')
        if self._validate_ssn(ssn):
            checks_passed += 1
        
        # Check 3: Date of birth validation
        dob = personal_info.get('date_of_birth')
        if self._validate_date_of_birth(dob):
            checks_passed += 1
        
        # Check 4: Address completeness
        address = personal_info.get('address', {})
        if self._validate_address_completeness(address):
            checks_passed += 1
        
        # Check 5: Data consistency
        if self._check_data_consistency(personal_info):
            checks_passed += 1
        
        score = checks_passed / total_checks
        return score
    
    def _validate_ssn(self, ssn: str) -> bool:
        """Validate SSN format and basic rules."""
        if not ssn or len(ssn) != 9 or not ssn.isdigit():
            return False
        
        # Check for invalid SSN patterns
        invalid_patterns = [
            '000000000', '111111111', '222222222', '333333333',
            '444444444', '555555555', '666666666', '777777777',
            '888888888', '999999999'
        ]
        
        if ssn in invalid_patterns:
            return False
        
        # Check area number (first 3 digits)
        area_number = ssn[:3]
        if area_number in ['000', '666'] or area_number.startswith('9'):
            return False
        
        return True
    
    def _validate_date_of_birth(self, dob: str) -> bool:
        """Validate date of birth."""
        if not dob:
            return False
        
        try:
            birth_date = datetime.strptime(dob, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            # Must be between 18 and 120 years old
            return 18 <= age <= 120
        except ValueError:
            return False
    
    def _validate_address_completeness(self, address: Dict[str, Any]) -> bool:
        """Validate address completeness."""
        required_fields = ['street', 'city', 'state', 'zip_code']
        return all(address.get(field, '').strip() for field in required_fields)
    
    def _check_data_consistency(self, personal_info: Dict[str, Any]) -> bool:
        """Check for data consistency and red flags."""
        # Simple consistency checks
        first_name = personal_info.get('first_name', '').lower()
        last_name = personal_info.get('last_name', '').lower()
        
        # Check for suspicious patterns
        if first_name == last_name:
            return False
        
        # Check for common test/fake names
        fake_names = ['test', 'fake', 'john doe', 'jane doe', 'mickey mouse']
        full_name = f"{first_name} {last_name}"
        if full_name in fake_names:
            return False
        
        return True
    
    async def _verify_documents(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify document authenticity and extract information."""
        documents = data.get('documents', [])
        document_types = data.get('document_types', [])
        
        document_results = {}
        total_score = 0.0
        issues_found = []
        
        for i, doc_id in enumerate(documents):
            doc_type = document_types[i] if i < len(document_types) else 'unknown'
            
            # Simulate document verification
            doc_result = await self._verify_single_document(doc_id, doc_type)
            document_results[doc_id] = doc_result
            
            total_score += doc_result['authenticity_score']
            if doc_result['issues']:
                issues_found.extend(doc_result['issues'])
        
        avg_score = total_score / len(documents) if documents else 0.0
        
        return {
            'document_results': document_results,
            'authenticity_score': round(avg_score, 3),
            'issues_found': issues_found
        }
    
    async def _verify_single_document(self, doc_id: str, doc_type: str) -> Dict[str, Any]:
        """Verify a single document."""
        # Simulate document verification logic
        # In real implementation, this would integrate with OCR and document verification services
        
        authenticity_score = 0.85  # Simulated score
        issues = []
        
        # Simulate various document checks
        checks = {
            'format_valid': True,
            'security_features': True,
            'data_extraction': True,
            'tampering_detected': False
        }
        
        if doc_type == 'drivers_license':
            # Specific checks for driver's license
            if not self._check_dl_format(doc_id):
                issues.append("Invalid driver's license format")
                authenticity_score -= 0.2
        elif doc_type == 'passport':
            # Specific checks for passport
            if not self._check_passport_format(doc_id):
                issues.append("Invalid passport format")
                authenticity_score -= 0.2
        
        return {
            'document_id': doc_id,
            'document_type': doc_type,
            'authenticity_score': max(0.0, authenticity_score),
            'checks': checks,
            'issues': issues,
            'verified_at': datetime.utcnow().isoformat()
        }
    
    def _check_dl_format(self, doc_id: str) -> bool:
        """Check driver's license format."""
        # Simplified format check
        return len(doc_id) >= 8
    
    def _check_passport_format(self, doc_id: str) -> bool:
        """Check passport format."""
        # Simplified format check
        return len(doc_id) >= 9
    
    async def _verify_address(self, address: Dict[str, Any]) -> float:
        """Verify address information."""
        if not address:
            return 0.0
        
        score = 0.0
        
        # Check address completeness
        required_fields = ['street', 'city', 'state', 'zip_code']
        completeness = sum(1 for field in required_fields if address.get(field, '').strip()) / len(required_fields)
        score += completeness * 0.4
        
        # Validate ZIP code format
        zip_code = address.get('zip_code', '')
        if re.match(r'^\d{5}(-\d{4})?$', zip_code):
            score += 0.3
        
        # Validate state code
        state = address.get('state', '').upper()
        valid_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        if state in valid_states:
            score += 0.3
        
        return min(1.0, score)
    
    async def _sanctions_screening(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Screen against sanctions and watchlists."""
        personal_info = data.get('personal_info', {})
        screening_level = data.get('screening_level', 'standard')
        
        # Extract screening data
        first_name = personal_info.get('first_name', '').lower()
        last_name = personal_info.get('last_name', '').lower()
        full_name = f"{first_name} {last_name}"
        
        # Simulate sanctions screening
        # In real implementation, this would query actual sanctions databases
        matches_found = []
        risk_score = 0.0
        
        # Check against simulated watchlists
        high_risk_names = ['john smith', 'jane doe']  # Simplified for demo
        
        if full_name in high_risk_names:
            matches_found.append({
                'list_name': 'OFAC SDN',
                'match_score': 0.95,
                'match_type': 'exact'
            })
            risk_score = 0.95
        
        # Determine screening result
        if risk_score > 0.8:
            screening_result = 'high_risk'
        elif risk_score > 0.5:
            screening_result = 'medium_risk'
        elif matches_found:
            screening_result = 'requires_review'
        else:
            screening_result = 'clear'
        
        return {
            'screening_result': screening_result,
            'matches_found': matches_found,
            'risk_score': risk_score,
            'screening_level': screening_level,
            'screened_at': datetime.utcnow().isoformat()
        }
    
    def _calculate_risk_level(self, identity_score: float, risk_factors: List[str]) -> str:
        """Calculate overall risk level."""
        if identity_score >= 0.9 and not risk_factors:
            return 'low'
        elif identity_score >= 0.7 and len(risk_factors) <= 1:
            return 'medium'
        else:
            return 'high'
    
    def _determine_compliance_status(self, verification_result: Dict[str, Any], 
                                   verification_level: str, identity_score: float) -> str:
        """Determine compliance status based on verification results."""
        threshold = self.verification_thresholds[verification_level]['min_score']
        
        if identity_score >= threshold and verification_result['sanctions_clear']:
            return 'compliant'
        elif identity_score >= threshold * 0.8:
            return 'requires_review'
        else:
            return 'non_compliant'
    
    async def _store_kyc_result(self, kyc_result: KYCResult):
        """Store KYC result in Firestore."""
        try:
            doc_ref = self.firestore_client.collection('kyc_results').document(kyc_result.applicant_id)
            doc_ref.set({
                'applicant_id': kyc_result.applicant_id,
                'identity_verified': kyc_result.identity_verified,
                'document_verification': kyc_result.document_verification,
                'address_verified': kyc_result.address_verified,
                'sanctions_check': kyc_result.sanctions_check,
                'verification_level': kyc_result.verification_level,
                'verified_at': kyc_result.verified_at
            })
            
            self.logger.info(f"Stored KYC result for applicant {kyc_result.applicant_id}")
            
        except Exception as e:
            self.logger.error(f"Error storing KYC result: {e}")
            raise

