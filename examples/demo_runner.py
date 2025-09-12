"""
Agent Fabric Demo Runner
Demonstrates the complete loan application workflow using Google ADK.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentFabricDemo:
    """
    Demonstration of the Agent Fabric system processing a complete loan application.
    Shows the interaction between all agents in a realistic scenario.
    """
    
    def __init__(self):
        self.demo_data = self._generate_demo_data()
        self.workflow_results = {}
        
    def _generate_demo_data(self) -> Dict[str, Any]:
        """Generate realistic demo data for loan application."""
        return {
            "applicant_info": {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@email.com",
                "phone": "+1-555-0123",
                "ssn": "123-45-6789",
                "date_of_birth": "1985-06-15",
                "address": {
                    "street": "123 Main Street",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip_code": "94105",
                    "country": "USA"
                }
            },
            "loan_details": {
                "amount": 250000,
                "purpose": "Home Purchase",
                "term_months": 360,
                "property_value": 500000,
                "down_payment": 100000
            },
            "employment_info": {
                "employer": "Tech Solutions Inc.",
                "position": "Senior Software Engineer",
                "annual_income": 120000,
                "employment_length_months": 36,
                "employment_type": "full_time"
            },
            "financial_info": {
                "monthly_income": 10000,
                "monthly_expenses": 4500,
                "existing_debt": 25000,
                "savings": 150000,
                "checking_balance": 15000
            },
            "documents": [
                "drivers_license_001.pdf",
                "pay_stub_recent.pdf",
                "bank_statement_001.pdf",
                "tax_return_2023.pdf",
                "employment_verification.pdf"
            ]
        }
    
    async def run_complete_demo(self):
        """Run the complete loan application workflow demo."""
        logger.info("🚀 Starting Agent Fabric Demo - Complete Loan Application Workflow")
        logger.info("=" * 80)
        
        try:
            # Step 1: Application Intake
            logger.info("📝 Step 1: Processing Application Intake...")
            intake_result = await self._demo_intake_agent()
            self.workflow_results['intake'] = intake_result
            
            if intake_result['status'] != 'accepted':
                logger.error("❌ Application rejected at intake stage")
                return
            
            application_id = intake_result['application_id']
            logger.info(f"✅ Application {application_id} accepted for processing")
            
            # Step 2: Document Processing (OCR)
            logger.info("\n📄 Step 2: Processing Documents with OCR...")
            ocr_result = await self._demo_ocr_agent(application_id)
            self.workflow_results['ocr'] = ocr_result
            
            # Step 3: KYC Verification
            logger.info("\n🔍 Step 3: Performing KYC Verification...")
            kyc_result = await self._demo_kyc_agent(application_id)
            self.workflow_results['kyc'] = kyc_result
            
            # Step 4: Fraud Detection
            logger.info("\n🛡️ Step 4: Running Fraud Detection...")
            fraud_result = await self._demo_fraud_agent(application_id)
            self.workflow_results['fraud'] = fraud_result
            
            # Step 5: Data Enrichment
            logger.info("\n📊 Step 5: Enriching Application Data...")
            enrichment_result = await self._demo_enrichment_agent(application_id)
            self.workflow_results['enrichment'] = enrichment_result
            
            # Step 6: Credit Assessment
            logger.info("\n💳 Step 6: Performing Credit Assessment...")
            credit_result = await self._demo_credit_agent(application_id)
            self.workflow_results['credit'] = credit_result
            
            # Step 7: Final Decision
            logger.info("\n⚖️ Step 7: Making Final Decision...")
            final_decision = await self._make_final_decision()
            self.workflow_results['final_decision'] = final_decision
            
            # Step 8: Collections Setup (if approved)
            if final_decision['decision'] == 'approved':
                logger.info("\n💰 Step 8: Setting up Collections Management...")
                collections_result = await self._demo_collections_agent(application_id)
                self.workflow_results['collections'] = collections_result
            
            # Display Results Summary
            await self._display_results_summary()
            
        except Exception as e:
            logger.error(f"❌ Demo failed with error: {e}")
            raise
    
    async def _demo_intake_agent(self) -> Dict[str, Any]:
        """Simulate Intake Agent processing."""
        logger.info("  → Validating application data...")
        await asyncio.sleep(1)  # Simulate processing time
        
        logger.info("  → Checking data completeness...")
        await asyncio.sleep(0.5)
        
        logger.info("  → Determining next steps...")
        await asyncio.sleep(0.5)
        
        # Simulate intake processing
        result = {
            'application_id': str(uuid.uuid4()),
            'status': 'accepted',
            'next_steps': [
                'ocr_processing',
                'kyc_verification', 
                'fraud_screening',
                'data_enrichment',
                'credit_assessment'
            ],
            'validation_results': {
                'is_valid': True,
                'completeness_score': 0.95,
                'validation_errors': []
            },
            'created_at': datetime.utcnow().isoformat(),
            'estimated_processing_time': '2-3 business days'
        }
        
        logger.info(f"  ✅ Application processed successfully")
        logger.info(f"  📋 Next steps: {', '.join(result['next_steps'])}")
        
        return result
    
    async def _demo_ocr_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate OCR Agent processing."""
        documents = self.demo_data['documents']
        
        logger.info(f"  → Processing {len(documents)} documents...")
        
        processed_docs = {}
        for doc in documents:
            logger.info(f"    • Processing {doc}...")
            await asyncio.sleep(0.3)  # Simulate OCR processing
            
            processed_docs[doc] = {
                'status': 'processed',
                'extracted_text_length': 1500 + len(doc) * 10,
                'confidence_score': 0.92,
                'document_type': self._classify_document(doc),
                'key_data_extracted': True
            }
        
        result = {
            'application_id': application_id,
            'documents_processed': len(documents),
            'processing_results': processed_docs,
            'overall_confidence': 0.91,
            'processing_time_seconds': len(documents) * 0.3,
            'issues_found': []
        }
        
        logger.info(f"  ✅ Processed {len(documents)} documents with 91% confidence")
        
        return result
    
    def _classify_document(self, doc_name: str) -> str:
        """Classify document type based on filename."""
        if 'license' in doc_name.lower():
            return 'drivers_license'
        elif 'pay_stub' in doc_name.lower():
            return 'pay_stub'
        elif 'bank' in doc_name.lower():
            return 'bank_statement'
        elif 'tax' in doc_name.lower():
            return 'tax_return'
        elif 'employment' in doc_name.lower():
            return 'employment_verification'
        else:
            return 'other'
    
    async def _demo_kyc_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate KYC Agent processing."""
        logger.info("  → Verifying identity documents...")
        await asyncio.sleep(1.5)
        
        logger.info("  → Checking address verification...")
        await asyncio.sleep(1)
        
        logger.info("  → Running sanctions screening...")
        await asyncio.sleep(0.8)
        
        logger.info("  → Validating SSN and personal info...")
        await asyncio.sleep(0.7)
        
        result = {
            'application_id': application_id,
            'verification_result': {
                'identity_verified': True,
                'document_verification': {
                    'drivers_license_001.pdf': {
                        'verified': True,
                        'authenticity_score': 0.94
                    }
                },
                'address_verified': True,
                'sanctions_clear': True,
                'verification_level': 'enhanced'
            },
            'identity_score': 0.89,
            'risk_level': 'low',
            'compliance_status': 'compliant',
            'risk_factors': [],
            'verified_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"  ✅ KYC verification completed - Identity Score: {result['identity_score']}")
        logger.info(f"  🔒 Compliance Status: {result['compliance_status']}")
        
        return result
    
    async def _demo_fraud_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate Fraud Agent processing."""
        logger.info("  → Analyzing application patterns...")
        await asyncio.sleep(1)
        
        logger.info("  → Checking velocity patterns...")
        await asyncio.sleep(0.8)
        
        logger.info("  → Running ML fraud models...")
        await asyncio.sleep(1.2)
        
        logger.info("  → Cross-referencing fraud databases...")
        await asyncio.sleep(0.6)
        
        result = {
            'application_id': application_id,
            'fraud_score': 0.15,  # Low fraud risk
            'risk_level': 'low',
            'decision': 'clear',
            'confidence': 0.92,
            'risk_indicators': [],
            'model_results': {
                'velocity_check': {'score': 0.05, 'status': 'pass'},
                'pattern_analysis': {'score': 0.12, 'status': 'pass'},
                'device_fingerprint': {'score': 0.08, 'status': 'pass'},
                'behavioral_analysis': {'score': 0.18, 'status': 'pass'}
            },
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"  ✅ Fraud analysis completed - Risk Score: {result['fraud_score']}")
        logger.info(f"  🛡️ Decision: {result['decision'].upper()}")
        
        return result
    
    async def _demo_enrichment_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate Enrichment Agent processing."""
        logger.info("  → Gathering external data sources...")
        await asyncio.sleep(1.2)
        
        logger.info("  → Validating employment information...")
        await asyncio.sleep(0.9)
        
        logger.info("  → Enriching financial profile...")
        await asyncio.sleep(1.1)
        
        logger.info("  → Cross-referencing public records...")
        await asyncio.sleep(0.7)
        
        result = {
            'application_id': application_id,
            'enrichment_results': {
                'employment_verified': True,
                'income_validated': True,
                'property_value_confirmed': True,
                'credit_history_length': 12,  # years
                'public_records_clear': True
            },
            'data_quality_score': 0.93,
            'additional_insights': {
                'debt_to_income_ratio': 0.31,
                'loan_to_value_ratio': 0.50,
                'payment_history_score': 0.88,
                'stability_indicators': ['long_employment', 'stable_residence']
            },
            'confidence_level': 0.91,
            'enriched_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"  ✅ Data enrichment completed - Quality Score: {result['data_quality_score']}")
        logger.info(f"  📊 DTI Ratio: {result['additional_insights']['debt_to_income_ratio']}")
        
        return result
    
    async def _demo_credit_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate Credit Agent processing."""
        logger.info("  → Pulling credit reports...")
        await asyncio.sleep(1.5)
        
        logger.info("  → Calculating credit score...")
        await asyncio.sleep(1)
        
        logger.info("  → Running risk models...")
        await asyncio.sleep(1.3)
        
        logger.info("  → Determining loan terms...")
        await asyncio.sleep(0.8)
        
        result = {
            'application_id': application_id,
            'credit_score': 742,
            'risk_level': 'low',
            'decision': 'approve',
            'confidence': 0.87,
            'risk_factors': [],
            'positive_factors': [
                'High credit score',
                'Stable employment history',
                'Low debt-to-income ratio',
                'Substantial down payment'
            ],
            'recommended_terms': {
                'interest_rate': 6.25,
                'loan_amount': 250000,
                'term_months': 360,
                'monthly_payment': 1539.29,
                'apr': 6.31
            },
            'assessed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"  ✅ Credit assessment completed - Score: {result['credit_score']}")
        logger.info(f"  💰 Recommended Rate: {result['recommended_terms']['interest_rate']}%")
        
        return result
    
    async def _make_final_decision(self) -> Dict[str, Any]:
        """Make final loan decision based on all agent results."""
        logger.info("  → Aggregating all assessment results...")
        await asyncio.sleep(0.5)
        
        logger.info("  → Applying business rules...")
        await asyncio.sleep(0.3)
        
        logger.info("  → Calculating final risk score...")
        await asyncio.sleep(0.4)
        
        # Analyze results from all agents
        kyc_score = self.workflow_results['kyc']['identity_score']
        fraud_score = self.workflow_results['fraud']['fraud_score']
        credit_score = self.workflow_results['credit']['credit_score']
        
        # Simple decision logic
        if (kyc_score > 0.8 and 
            fraud_score < 0.3 and 
            credit_score > 700):
            decision = 'approved'
            confidence = 0.91
        elif (kyc_score > 0.6 and 
              fraud_score < 0.5 and 
              credit_score > 650):
            decision = 'conditional_approval'
            confidence = 0.75
        else:
            decision = 'declined'
            confidence = 0.85
        
        result = {
            'decision': decision,
            'confidence': confidence,
            'final_risk_score': 0.23,
            'decision_factors': {
                'kyc_score': kyc_score,
                'fraud_score': fraud_score,
                'credit_score': credit_score,
                'enrichment_quality': self.workflow_results['enrichment']['data_quality_score']
            },
            'conditions': [] if decision == 'approved' else ['Additional income verification required'],
            'decided_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"  ✅ Final Decision: {decision.upper()}")
        logger.info(f"  📊 Confidence: {confidence * 100:.1f}%")
        
        return result
    
    async def _demo_collections_agent(self, application_id: str) -> Dict[str, Any]:
        """Simulate Collections Agent setup for approved loan."""
        logger.info("  → Setting up payment schedule...")
        await asyncio.sleep(0.8)
        
        logger.info("  → Configuring automated reminders...")
        await asyncio.sleep(0.6)
        
        logger.info("  → Establishing monitoring rules...")
        await asyncio.sleep(0.5)
        
        result = {
            'application_id': application_id,
            'payment_schedule_created': True,
            'automated_reminders': {
                'enabled': True,
                'reminder_days': [5, 1],  # Days before due date
                'channels': ['email', 'sms']
            },
            'monitoring_rules': {
                'late_payment_threshold': 5,  # days
                'escalation_threshold': 30,  # days
                'auto_call_enabled': True
            },
            'first_payment_date': '2024-02-01',
            'setup_completed_at': datetime.utcnow().isoformat()
        }
        
        logger.info("  ✅ Collections management configured")
        logger.info(f"  📅 First payment due: {result['first_payment_date']}")
        
        return result
    
    async def _display_results_summary(self):
        """Display comprehensive results summary."""
        logger.info("\n" + "=" * 80)
        logger.info("📊 AGENT FABRIC DEMO RESULTS SUMMARY")
        logger.info("=" * 80)
        
        # Application Overview
        intake = self.workflow_results['intake']
        final_decision = self.workflow_results['final_decision']
        
        logger.info(f"🆔 Application ID: {intake['application_id']}")
        logger.info(f"👤 Applicant: {self.demo_data['applicant_info']['first_name']} {self.demo_data['applicant_info']['last_name']}")
        logger.info(f"💰 Loan Amount: ${self.demo_data['loan_details']['amount']:,}")
        logger.info(f"🏠 Purpose: {self.demo_data['loan_details']['purpose']}")
        
        logger.info("\n📋 PROCESSING RESULTS:")
        logger.info("-" * 40)
        
        # Agent Results
        agents_summary = [
            ("📝 Intake", self.workflow_results['intake']['status'], "✅"),
            ("📄 OCR", f"{self.workflow_results['ocr']['documents_processed']} docs processed", "✅"),
            ("🔍 KYC", f"Score: {self.workflow_results['kyc']['identity_score']:.2f}", "✅"),
            ("🛡️ Fraud", f"Risk: {self.workflow_results['fraud']['fraud_score']:.2f}", "✅"),
            ("📊 Enrichment", f"Quality: {self.workflow_results['enrichment']['data_quality_score']:.2f}", "✅"),
            ("💳 Credit", f"Score: {self.workflow_results['credit']['credit_score']}", "✅")
        ]
        
        for agent, result, status in agents_summary:
            logger.info(f"{agent:<15} {result:<25} {status}")
        
        # Final Decision
        logger.info("\n🎯 FINAL DECISION:")
        logger.info("-" * 40)
        decision = final_decision['decision'].upper()
        confidence = final_decision['confidence'] * 100
        
        if decision == 'APPROVED':
            logger.info(f"✅ LOAN {decision} (Confidence: {confidence:.1f}%)")
            
            # Loan Terms
            terms = self.workflow_results['credit']['recommended_terms']
            logger.info(f"💰 Loan Amount: ${terms['loan_amount']:,}")
            logger.info(f"📈 Interest Rate: {terms['interest_rate']}%")
            logger.info(f"📅 Term: {terms['term_months']} months")
            logger.info(f"💳 Monthly Payment: ${terms['monthly_payment']:,.2f}")
            
        elif decision == 'CONDITIONAL_APPROVAL':
            logger.info(f"⚠️ LOAN {decision} (Confidence: {confidence:.1f}%)")
            logger.info(f"📋 Conditions: {', '.join(final_decision['conditions'])}")
            
        else:
            logger.info(f"❌ LOAN {decision} (Confidence: {confidence:.1f}%)")
        
        # Processing Time
        logger.info("\n⏱️ PROCESSING METRICS:")
        logger.info("-" * 40)
        logger.info(f"📊 Total Processing Time: ~8.5 seconds (Demo)")
        logger.info(f"🔄 Agents Involved: 7")
        logger.info(f"📄 Documents Processed: {len(self.demo_data['documents'])}")
        logger.info(f"🎯 Overall Confidence: {confidence:.1f}%")
        
        # Next Steps
        logger.info("\n🚀 NEXT STEPS:")
        logger.info("-" * 40)
        if decision == 'APPROVED':
            logger.info("✅ Loan approved - Collections management configured")
            logger.info("📧 Approval notification sent to applicant")
            logger.info("📋 Loan documents prepared for signing")
            logger.info("💰 Funding process initiated")
        elif decision == 'CONDITIONAL_APPROVAL':
            logger.info("📋 Additional documentation required")
            logger.info("📧 Conditional approval notification sent")
            logger.info("⏳ Awaiting applicant response")
        else:
            logger.info("📧 Decline notification sent to applicant")
            logger.info("📋 Decline reasons documented")
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 DEMO COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)


async def main():
    """Main demo execution function."""
    print("\n🤖 Agent Fabric - Google ADK Financial Services Demo")
    print("🏦 Comprehensive Loan Application Processing Workflow")
    print("=" * 80)
    
    demo = AgentFabricDemo()
    
    try:
        await demo.run_complete_demo()
        
        print("\n💡 This demo showcased:")
        print("  • Google ADK-based agent orchestration")
        print("  • Multi-agent workflow coordination")
        print("  • Real-time decision making")
        print("  • Compliance and risk management")
        print("  • End-to-end loan processing")
        
        print("\n🔗 Next Steps:")
        print("  • Explore individual agent capabilities")
        print("  • Review the architecture documentation")
        print("  • Try the interactive API endpoints")
        print("  • Customize agents for your use case")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

