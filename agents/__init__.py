"""
Agent Fabric - Agents Module
Contains all specialized agents for the financial services platform.
"""

from .base_agent import BaseAgent
from .intake_agent import IntakeAgent
from .kyc_agent import KYCAgent
from .credit_agent import CreditAgent
from .fraud_agent import FraudAgent
from .collections_agent import CollectionsAgent
from .ocr_agent import OCRAgent
from .enrichment_agent import EnrichmentAgent

__all__ = [
    'BaseAgent',
    'IntakeAgent',
    'KYCAgent', 
    'CreditAgent',
    'FraudAgent',
    'CollectionsAgent',
    'OCRAgent',
    'EnrichmentAgent'
]

