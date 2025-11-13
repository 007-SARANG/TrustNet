"""
Configuration Management
"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Environment
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
    GOOGLE_FACTCHECK_API_KEY = os.getenv('GOOGLE_FACT_CHECK_API_KEY', '')
    
    # Database
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'trustnet')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'trustnet_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    # Agent Configuration
    SCOUT_PRIORITY_THRESHOLD = float(os.getenv('SCOUT_PRIORITY_THRESHOLD', '0.7'))
    ANALYST_FAKE_THRESHOLD = float(os.getenv('ANALYST_FAKE_THRESHOLD', '0.7'))
    PREDICTOR_RISK_THRESHOLD = float(os.getenv('PREDICTOR_RISK_THRESHOLD', '0.8'))
    
    @classmethod
    def get_agent_config(cls) -> Dict:
        """Get configuration for agents"""
        return {
            'priority_threshold': cls.SCOUT_PRIORITY_THRESHOLD,
            'fake_threshold': cls.ANALYST_FAKE_THRESHOLD,
            'risk_threshold': cls.PREDICTOR_RISK_THRESHOLD,
            'google_factcheck_api_key': cls.GOOGLE_FACTCHECK_API_KEY,
            'tineye_api_key': os.getenv('TINEYE_API_KEY', ''),
            'auto_execute_threshold': 0.9,
            'enable_auto_intervention': True,
            'daily_budget': 5000
        }


config = Config()
