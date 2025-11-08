"""
Intelligent Test Management AI System for Solar PV Testing Labs
MODULE_ID: TEST_MANAGEMENT_AI_SESSION2

This package provides comprehensive test management functionality including:
- AI-powered test protocol library
- Smart test scheduling
- Advanced sample tracking with QR/Barcode
- Test execution management
- Data ingestion and validation
- Equipment integration
"""

__version__ = "1.0.0"
__module_id__ = "TEST_MANAGEMENT_AI_SESSION2"

from .models import *
from .protocols import ProtocolLibrary
from .scheduling import AIScheduler
from .sample_tracking import SampleTracker
from .test_execution import TestExecutor
from .data_ingestion import DataIngestor
from .equipment import EquipmentManager
from .ai_engine import AIEngine

__all__ = [
    'ProtocolLibrary',
    'AIScheduler',
    'SampleTracker',
    'TestExecutor',
    'DataIngestor',
    'EquipmentManager',
    'AIEngine'
]
