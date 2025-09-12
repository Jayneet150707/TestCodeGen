"""
Interactive Loan Application Workflow Example
Demonstrates real-time processing of a loan application through the Agent Fabric system.
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


class LoanApplicationWorkflow:
    """
    Interactive loan application workflow that processes a real application
    through all agents in the Agent Fabric system.
    """
    
    def __init__(self):
        self.application_data = None
        self.workflow_state = {
            'current_step': 'intake',
            'completed_steps': [],
            'results': {},
            'errors': []
        }
    
    async def start_interactive_workflow(self):
        """Start an interactive loan application workflow."""
        print("\n🏦 Agent Fabric - Interactive Loan Application Workflow")
        print("=" * 60)
        print("This workflow will guide you through processing a loan application")
        print("using the Google ADK-powered Agent Fabric system.\n")
        
        # Collect application data
        self.application_data = await self._collect_application_data()
        
        # Process through workflow
        await self._execute_workflow()
        
        # Display final results
        await self._display_final_results()
    
    async def _collect_application_data(self) -> Dict[str, Any]:
        """Collect loan application data interactively."""
        print("📝 Step 1: Collecting Application Information")
        print("-" * 40)
        
        # For demo purposes, we'll use predefined data
        # In a real system, this would collect from user input or API
        
        application_data = {
            "applicant_info": {
                "first_name": input("First Name [John]: ") or "John",
                "last_name": input("Last Name [Doe]: ") or "Doe",
                "email": input("Email [john.doe@email.com]: ") or "john.doe@email.com",
                "phone": input("Phone [+1-555-0123]: ") or "+1-555-0123",
                "ssn": input("SSN [123-45-6789]: ") or "123-45-6789",
                "date_of_birth": input("Date of Birth [1990-01-15]: ") or "1990-01-15"
            },
            "loan_details": {
                "amount": float(input("Loan Amount [50000]: ") or "50000"),
                "purpose": input("Loan Purpose [Personal]: ") or "Personal",
                "term_months": int(input("Term in Months [60]: ") or "60")
            },
            "employment_info": {
                "employer": input("Employer [ABC Corp]: ") or "ABC Corp",
                "position": input("Position [Manager]: ") or "Manager",
                "annual_income": float(input("Annual Income [75000]: ") or "75000"),
                "employment_length_months": int(input("Employment Length (months) [24]: ") or "24")
            }
        }
        
        print(f"\n✅ Application data collected for {application_data['applicant_info']['first_name']} {application_data['applicant_info']['last_name']}")
        return application_data
    
    async def _execute_workflow(self):
        """Execute the complete loan application workflow."""
        print(f"\n🚀 Starting Workflow Processing")
        print("=" * 60)
        
        workflow_steps = [
            ("intake", "Application Intake", self._process_intake),
            ("kyc", "KYC Verification", self._process_kyc),
            ("fraud", "Fraud Detection", self._process_fraud),
            ("enrichment", "Data Enrichment", self._process_enrichment),
            ("credit", "Credit Assessment", self._process_credit),
            ("decision", "Final Decision", self._make_decision)
        ]
        
        for step_id, step_name, step_function in workflow_steps:
            print(f"\n📍 Processing: {step_name}")
            print("-" * 40)
            
            try:
                self.workflow_state['current_step'] = step_id
                result = await step_function()
                
                self.workflow_state['results'][step_id] = result
                self.workflow_state['completed_steps'].append(step_id)
                
                print(f"✅ {step_name} completed successfully")
                
                # Check if we need to stop (e.g., application rejected)
                if result.get('status') == 'rejected' or result.get('decision') == 'declined':
                    print(f"⏹️ Workflow stopped: {result.get('reason', 'Application declined')}")
                    break
                    
            except Exception as e:
                error_msg = f"Error in {step_name}: {str(e)}"
                self.workflow_state['errors'].append(error_msg)
                logger.error(error_msg)
                
                # Ask user if they want to continue
                continue_workflow = input(f"\n❌ {step_name} failed. Continue anyway? (y/N): ").lower() == 'y'
                if not continue_workflow:
                    break
    
    async def _process_intake(self) -> Dict[str, Any]:
        """Process application through Intake Agent."""
        print("  → Validating application data...")
        await asyncio.sleep(1)
        
        # Simulate intake validation
        validation_errors = []
        
        # Check required fields
        applicant = self.application_data['applicant_info']
        if not applicant.get('first_name') or not applicant.get('last_name'):
            validation_errors.append("Missing applicant name")
        
        if not applicant.get('email') or '@' not in applicant.get('email', ''):
            validation_errors.append("Invalid email address")
        
        loan_details = self.application_data['loan_details']
        if loan_details.get('amount', 0) < 1000:
            validation_errors.append("Minimum loan amount is $1,000")
        
        if validation_errors:
            return {
                'status': 'rejected',
                'reason': 'Validation failed',
                'validation_errors': validation_errors
            }
        
        application_id = str(uuid.uuid4())
        
        print(f"  → Application ID generated: {application_id}")
        print(f"  → Loan amount: ${loan_details['amount']:,.2f}")
        print(f"  → Purpose: {loan_details['purpose']}")
        
        return {
            'status': 'accepted',
            'application_id': application_id,
            'validation_score': 0.95,
            'next_steps': ['kyc_verification', 'fraud_screening', 'credit_assessment']
        }
    
    async def _process_kyc(self) -> Dict[str, Any]:
        """Process KYC verification."""
        print("  → Verifying identity information...")
        await asyncio.sleep(1.5)
        
        applicant = self.application_data['applicant_info']
        
        # Simulate KYC checks
        identity_score = 0.0
        
        # Name validation
        if applicant.get('first_name') and applicant.get('last_name'):
            identity_score += 0.3
            print("    ✓ Name validation passed")
        
        # SSN validation (basic format check)
        ssn = applicant.get('ssn', '').replace('-', '')
        if len(ssn) == 9 and ssn.isdigit():
            identity_score += 0.3
            print("    ✓ SSN format validation passed")
        
        # Email validation
        if applicant.get('email') and '@' in applicant.get('email', ''):
            identity_score += 0.2
            print("    ✓ Email validation passed")
        
        # Date of birth validation
        try:
            dob = datetime.strptime(applicant.get('date_of_birth', ''), '%Y-%m-%d')
            age = (datetime.now() - dob).days // 365
            if 18 <= age <= 100:
                identity_score += 0.2
                print(f"    ✓ Age validation passed (Age: {age})")
        except:
            print("    ⚠ Date of birth format invalid")
        
        verification_level = 'basic' if identity_score >= 0.6 else 'failed'
        
        return {
            'identity_score': identity_score,
            'verification_level': verification_level,
            'identity_verified': identity_score >= 0.6,
            'risk_level': 'low' if identity_score >= 0.8 else 'medium'
        }
    
    async def _process_fraud(self) -> Dict[str, Any]:
        """Process fraud detection."""
        print("  → Running fraud detection algorithms...")
        await asyncio.sleep(1.2)
        
        # Simulate fraud scoring
        fraud_indicators = []
        fraud_score = 0.0
        
        # Check for suspicious patterns
        applicant = self.application_data['applicant_info']
        loan_amount = self.application_data['loan_details']['amount']
        annual_income = self.application_data['employment_info']['annual_income']
        
        # Income to loan ratio check
        if loan_amount > annual_income * 5:
            fraud_indicators.append("High loan-to-income ratio")
            fraud_score += 0.3
        
        # Email domain check (simplified)
        email = applicant.get('email', '')
        suspicious_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
        if any(domain in email for domain in suspicious_domains):
            fraud_indicators.append("Suspicious email domain")
            fraud_score += 0.4
        
        # Name consistency check
        first_name = applicant.get('first_name', '').lower()
        last_name = applicant.get('last_name', '').lower()
        if first_name == last_name:
            fraud_indicators.append("Identical first and last name")
            fraud_score += 0.5
        
        print(f"    → Fraud score: {fraud_score:.2f}")
        if fraud_indicators:
            print(f"    ⚠ Indicators found: {', '.join(fraud_indicators)}")
        else:
            print("    ✓ No fraud indicators detected")
        
        decision = 'clear' if fraud_score < 0.3 else 'review' if fraud_score < 0.7 else 'decline'
        
        return {
            'fraud_score': fraud_score,
            'decision': decision,
            'risk_indicators': fraud_indicators,
            'confidence': 0.85
        }
    
    async def _process_enrichment(self) -> Dict[str, Any]:
        """Process data enrichment."""
        print("  → Enriching application data...")
        await asyncio.sleep(1.0)
        
        employment = self.application_data['employment_info']
        loan_details = self.application_data['loan_details']
        
        # Calculate additional metrics
        monthly_income = employment['annual_income'] / 12
        estimated_monthly_payment = self._calculate_monthly_payment(
            loan_details['amount'], 
            loan_details['term_months']
        )
        
        debt_to_income = estimated_monthly_payment / monthly_income
        
        print(f"    → Monthly income: ${monthly_income:,.2f}")
        print(f"    → Estimated payment: ${estimated_monthly_payment:,.2f}")
        print(f"    → Debt-to-income ratio: {debt_to_income:.2%}")
        
        # Employment stability score
        employment_months = employment.get('employment_length_months', 0)
        stability_score = min(1.0, employment_months / 24)  # 2 years = full score
        
        return {
            'monthly_income': monthly_income,
            'estimated_monthly_payment': estimated_monthly_payment,
            'debt_to_income_ratio': debt_to_income,
            'employment_stability_score': stability_score,
            'data_quality_score': 0.88
        }
    
    def _calculate_monthly_payment(self, loan_amount: float, term_months: int, 
                                 annual_rate: float = 0.08) -> float:
        """Calculate estimated monthly payment."""
        monthly_rate = annual_rate / 12
        if monthly_rate == 0:
            return loan_amount / term_months
        
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / \
                 ((1 + monthly_rate) ** term_months - 1)
        return payment
    
    async def _process_credit(self) -> Dict[str, Any]:
        """Process credit assessment."""
        print("  → Performing credit assessment...")
        await asyncio.sleep(1.8)
        
        # Simulate credit scoring based on available data
        base_score = 650  # Starting point
        
        employment = self.application_data['employment_info']
        enrichment = self.workflow_state['results']['enrichment']
        
        # Adjust score based on income
        if employment['annual_income'] >= 75000:
            base_score += 50
            print("    ✓ High income bonus: +50 points")
        elif employment['annual_income'] >= 50000:
            base_score += 25
            print("    ✓ Good income bonus: +25 points")
        
        # Adjust for employment stability
        stability_score = enrichment['employment_stability_score']
        stability_bonus = int(stability_score * 30)
        base_score += stability_bonus
        print(f"    ✓ Employment stability bonus: +{stability_bonus} points")
        
        # Adjust for debt-to-income ratio
        dti = enrichment['debt_to_income_ratio']
        if dti < 0.3:
            base_score += 30
            print("    ✓ Low DTI bonus: +30 points")
        elif dti > 0.5:
            base_score -= 40
            print("    ⚠ High DTI penalty: -40 points")
        
        credit_score = max(300, min(850, base_score))  # Clamp to valid range
        
        # Determine decision
        if credit_score >= 700:
            decision = 'approve'
            risk_level = 'low'
            interest_rate = 6.5
        elif credit_score >= 650:
            decision = 'approve'
            risk_level = 'medium'
            interest_rate = 8.5
        elif credit_score >= 600:
            decision = 'conditional'
            risk_level = 'medium'
            interest_rate = 12.0
        else:
            decision = 'decline'
            risk_level = 'high'
            interest_rate = None
        
        print(f"    → Credit score: {credit_score}")
        print(f"    → Risk level: {risk_level}")
        print(f"    → Decision: {decision}")
        
        return {
            'credit_score': credit_score,
            'decision': decision,
            'risk_level': risk_level,
            'interest_rate': interest_rate,
            'confidence': 0.82
        }
    
    async def _make_decision(self) -> Dict[str, Any]:
        """Make final loan decision."""
        print("  → Making final decision...")
        await asyncio.sleep(0.8)
        
        # Gather results from all steps
        kyc_result = self.workflow_state['results']['kyc']
        fraud_result = self.workflow_state['results']['fraud']
        credit_result = self.workflow_state['results']['credit']
        
        # Decision logic
        decision_factors = []
        
        # KYC check
        if not kyc_result['identity_verified']:
            decision = 'declined'
            decision_factors.append('KYC verification failed')
        # Fraud check
        elif fraud_result['decision'] == 'decline':
            decision = 'declined'
            decision_factors.append('High fraud risk')
        # Credit check
        elif credit_result['decision'] == 'decline':
            decision = 'declined'
            decision_factors.append('Credit assessment failed')
        # Conditional approval
        elif credit_result['decision'] == 'conditional':
            decision = 'conditional_approval'
            decision_factors.append('Requires additional verification')
        # Full approval
        else:
            decision = 'approved'
            decision_factors.append('All checks passed')
        
        loan_terms = None
        if decision in ['approved', 'conditional_approval']:
            loan_amount = self.application_data['loan_details']['amount']
            term_months = self.application_data['loan_details']['term_months']
            interest_rate = credit_result['interest_rate']
            
            monthly_payment = self._calculate_monthly_payment(
                loan_amount, term_months, interest_rate / 100
            )
            
            loan_terms = {
                'loan_amount': loan_amount,
                'interest_rate': interest_rate,
                'term_months': term_months,
                'monthly_payment': monthly_payment,
                'total_interest': (monthly_payment * term_months) - loan_amount
            }
        
        return {
            'decision': decision,
            'decision_factors': decision_factors,
            'loan_terms': loan_terms,
            'processing_time': '3.2 minutes',
            'confidence': 0.89
        }
    
    async def _display_final_results(self):
        """Display comprehensive final results."""
        print("\n" + "=" * 60)
        print("📊 LOAN APPLICATION PROCESSING RESULTS")
        print("=" * 60)
        
        # Application summary
        applicant = self.application_data['applicant_info']
        loan_details = self.application_data['loan_details']
        
        print(f"\n👤 APPLICANT: {applicant['first_name']} {applicant['last_name']}")
        print(f"📧 Email: {applicant['email']}")
        print(f"💰 Requested Amount: ${loan_details['amount']:,.2f}")
        print(f"🎯 Purpose: {loan_details['purpose']}")
        print(f"📅 Term: {loan_details['term_months']} months")
        
        # Processing results
        print(f"\n📋 PROCESSING SUMMARY:")
        print("-" * 30)
        
        for step in self.workflow_state['completed_steps']:
            result = self.workflow_state['results'][step]
            if step == 'intake':
                print(f"✅ Intake: {result['status']}")
            elif step == 'kyc':
                print(f"✅ KYC: Score {result['identity_score']:.2f}")
            elif step == 'fraud':
                print(f"✅ Fraud: {result['decision']} (Score: {result['fraud_score']:.2f})")
            elif step == 'enrichment':
                print(f"✅ Enrichment: DTI {result['debt_to_income_ratio']:.1%}")
            elif step == 'credit':
                print(f"✅ Credit: Score {result['credit_score']} ({result['decision']})")
            elif step == 'decision':
                print(f"✅ Decision: {result['decision'].upper()}")
        
        # Final decision
        if 'decision' in self.workflow_state['results']:
            decision_result = self.workflow_state['results']['decision']
            decision = decision_result['decision']
            
            print(f"\n🎯 FINAL DECISION: {decision.upper()}")
            print("-" * 30)
            
            if decision == 'approved':
                terms = decision_result['loan_terms']
                print(f"✅ LOAN APPROVED!")
                print(f"💰 Amount: ${terms['loan_amount']:,.2f}")
                print(f"📈 Interest Rate: {terms['interest_rate']:.1f}%")
                print(f"💳 Monthly Payment: ${terms['monthly_payment']:,.2f}")
                print(f"💸 Total Interest: ${terms['total_interest']:,.2f}")
                
            elif decision == 'conditional_approval':
                print(f"⚠️ CONDITIONAL APPROVAL")
                print(f"📋 Additional requirements needed")
                
            else:
                print(f"❌ LOAN DECLINED")
                print(f"📋 Reasons: {', '.join(decision_result['decision_factors'])}")
        
        # Errors (if any)
        if self.workflow_state['errors']:
            print(f"\n⚠️ PROCESSING ERRORS:")
            print("-" * 30)
            for error in self.workflow_state['errors']:
                print(f"❌ {error}")
        
        print(f"\n⏱️ Total Processing Time: {decision_result.get('processing_time', 'N/A')}")
        print(f"🎯 Overall Confidence: {decision_result.get('confidence', 0) * 100:.1f}%")
        
        print("\n" + "=" * 60)
        print("🎉 WORKFLOW COMPLETED!")
        print("=" * 60)


async def main():
    """Main execution function."""
    workflow = LoanApplicationWorkflow()
    
    try:
        await workflow.start_interactive_workflow()
        
        print("\n💡 What happened here:")
        print("  • Interactive data collection")
        print("  • Multi-agent processing pipeline")
        print("  • Real-time decision making")
        print("  • Comprehensive risk assessment")
        print("  • Automated loan terms calculation")
        
        print("\n🔗 Try next:")
        print("  • Run the full demo: python examples/demo_runner.py")
        print("  • Explore agent APIs individually")
        print("  • Review processing logs and metrics")
        
    except KeyboardInterrupt:
        print("\n⏹️ Workflow interrupted by user")
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
