"""
TrustNet Coordinator - Orchestrates all agents using LangGraph
"""

import asyncio
import logging
from typing import Dict, Optional
import redis.asyncio as redis
from datetime import datetime

# Import all agents
from agents.scout import ScoutAgent
from agents.analyst import AnalystAgent
from agents.investigator import InvestigatorAgent
from agents.predictor import PredictorAgent
from agents.strategist import StrategistAgent
from agents.executor import ExecutorAgent

logger = logging.getLogger(__name__)


class TrustNetCoordinator:
    """
    Central coordinator that orchestrates all 6 agents
    Uses LangGraph for workflow management and Redis for state persistence
    """
    
    def __init__(self):
        # Configuration (load from env/config file)
        self.config = {
            'priority_threshold': 0.7,
            'fake_threshold': 0.7,
            'risk_threshold': 0.8,
            'auto_execute_threshold': 0.9,
            'enable_auto_intervention': True
        }
        
        # Initialize agents
        logger.info("Initializing agents...")
        self.scout = ScoutAgent(self.config)
        self.analyst = AnalystAgent(self.config)
        self.investigator = InvestigatorAgent(self.config)
        self.predictor = PredictorAgent(self.config)
        self.strategist = StrategistAgent(self.config)
        self.executor = ExecutorAgent(self.config)
        
        # State management (Redis)
        self.redis_client = None
        
        # Metrics
        self.metrics = {
            'posts_analyzed': 0,
            'fake_detected': 0,
            'interventions': 0,
            'success_rate': 0.0
        }
        
        logger.info("✅ TrustNet Coordinator initialized")
    
    async def initialize(self):
        """Initialize coordinator resources"""
        try:
            # Connect to Redis
            self.redis_client = await redis.from_url(
                'redis://localhost:6379',
                encoding='utf-8',
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("✅ Connected to Redis")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Continuing without state persistence.")
    
    async def process_content(self, content: Dict) -> Optional[Dict]:
        """
        Complete pipeline: Scout → Analyst → Investigator → Predictor → Strategist → Executor
        
        Args:
            content: Raw social media post
            
        Returns:
            Final execution report or None
        """
        try:
            self.metrics['posts_analyzed'] += 1
            content_id = content.get('id', 'unknown')
            
            logger.info(f"{'='*60}")
            logger.info(f"🚀 Processing content: {content_id}")
            logger.info(f"{'='*60}")
            
            # STAGE 1: Scout Agent - Filter and flag
            logger.info("➡️  Stage 1: Scout Agent")
            flagged = await self.scout.process_content(content)
            
            if not flagged:
                logger.info("✅ Content cleared by Scout - no action needed")
                return None
            
            await self._save_state('scout', content_id, flagged)
            
            # STAGE 2: Analyst Agent - Multi-modal classification
            logger.info("➡️  Stage 2: Analyst Agent")
            analysis = await self.analyst.analyze_content(flagged)
            
            await self._save_state('analyst', content_id, analysis)
            
            # Check if classified as FAKE
            if analysis.get('classification') != 'FAKE':
                logger.info("✅ Content classified as REAL - monitoring only")
                return {'status': 'REAL', 'monitoring': True}
            
            self.metrics['fake_detected'] += 1
            
            # STAGE 3: Investigator Agent - Evidence collection
            logger.info("➡️  Stage 3: Investigator Agent")
            evidence = await self.investigator.investigate(analysis)
            
            await self._save_state('investigator', content_id, evidence)
            
            # STAGE 4: Predictor Agent - Viral forecast
            logger.info("➡️  Stage 4: Predictor Agent")
            prediction = await self.predictor.predict_spread(evidence)
            
            await self._save_state('predictor', content_id, prediction)
            
            # Check risk level
            if prediction.get('viral_risk', 0) < 0.4:
                logger.info("✅ Low risk - monitoring only")
                return {'status': 'LOW_RISK', 'monitoring': True}
            
            # STAGE 5: Strategist Agent - Intervention planning
            logger.info("➡️  Stage 5: Strategist Agent")
            intervention_plan = await self.strategist.plan_intervention(prediction)
            
            await self._save_state('strategist', content_id, intervention_plan)
            
            # STAGE 6: Executor Agent - Execute intervention
            logger.info("➡️  Stage 6: Executor Agent")
            execution_report = await self.executor.execute_intervention(intervention_plan)
            
            await self._save_state('executor', content_id, execution_report)
            
            # Update metrics
            if execution_report.get('status') == 'SUCCESS':
                self.metrics['interventions'] += 1
                self._update_success_rate(execution_report)
            
            logger.info(f"{'='*60}")
            logger.info(f"✅ Pipeline complete: {content_id}")
            logger.info(f"   Status: {execution_report.get('status')}")
            logger.info(f"   Reduction: {execution_report.get('monitoring', {}).get('actual_reduction', 'N/A')}")
            logger.info(f"{'='*60}\n")
            
            return execution_report
            
        except Exception as e:
            logger.error(f"Error in pipeline: {e}", exc_info=True)
            return {'status': 'ERROR', 'error': str(e)}
    
    async def _save_state(self, agent: str, content_id: str, data: Dict):
        """Save agent state to Redis"""
        if self.redis_client:
            try:
                key = f"trustnet:{content_id}:{agent}"
                await self.redis_client.setex(
                    key,
                    3600,  # 1 hour TTL
                    str(data)
                )
            except Exception as e:
                logger.warning(f"Failed to save state to Redis: {e}")
    
    def _update_success_rate(self, execution_report: Dict):
        """Update success rate metric"""
        monitoring = execution_report.get('monitoring', {})
        if monitoring.get('success'):
            # Running average
            n = self.metrics['interventions']
            old_rate = self.metrics['success_rate']
            self.metrics['success_rate'] = (old_rate * (n - 1) + 1.0) / n
    
    async def run(self):
        """
        Main run loop - processes content from queue
        In production: consumes from Kafka
        """
        logger.info("🔄 TrustNet coordinator running...")
        
        # In production: consume from Kafka queue
        # For now: demonstration mode
        while True:
            await asyncio.sleep(1)
            # Process content from queue
            pass
    
    async def shutdown(self):
        """Cleanup resources"""
        if self.redis_client:
            await self.redis_client.close()
        logger.info("TrustNet coordinator shut down")
    
    def get_metrics(self) -> Dict:
        """Get current system metrics"""
        return {
            **self.metrics,
            'timestamp': datetime.utcnow().isoformat()
        }
