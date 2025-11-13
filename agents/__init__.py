"""Agents Package - All 6 TrustNet Agents"""

from .scout import ScoutAgent
from .analyst import AnalystAgent
from .investigator import InvestigatorAgent
from .predictor import PredictorAgent
from .strategist import StrategistAgent
from .executor import ExecutorAgent

__all__ = [
    'ScoutAgent',
    'AnalystAgent',
    'InvestigatorAgent',
    'PredictorAgent',
    'StrategistAgent',
    'ExecutorAgent'
]

__version__ = '2.0.0'
