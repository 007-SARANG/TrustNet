"""
Agent 6: Executor Agent - The Operator
Executes interventions, monitors outcomes, and logs results
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp

logger = logging.getLogger(__name__)


class ExecutorAgent:
    """
    Executor Agent carries out intervention actions, monitors progress,
    and feeds outcomes back to learning system
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.twitter_api = config.get('twitter_api')  # Twitter API client
        self.enable_auto_intervention = config.get('enable_auto_intervention', True)
        
        logger.info("✅ Executor Agent initialized")
    
    async def execute_intervention(self, intervention_plan: Dict) -> Dict:
        """
        Execute intervention plan and monitor outcomes
        
        Args:
            intervention_plan: Plan from Strategist Agent
            
        Returns:
            Execution report with outcomes and metrics
        """
        try:
            content_id = intervention_plan.get('content_id')
            logger.info(f"⚡ Executing intervention for: {content_id}")
            
            # Step 6.1: Human-in-loop approval (if needed)
            if intervention_plan.get('needs_human_approval'):
                approval = await self._request_human_approval(intervention_plan)
                if not approval:
                    logger.info(f"❌ Intervention rejected by human operator: {content_id}")
                    return self._rejected_report(intervention_plan)
            
            # Step 6.2: Execute actions
            execution_results = await self._execute_actions(intervention_plan)
            
            # Step 6.3: Monitor and log
            monitoring_data = await self._monitor_intervention(
                intervention_plan,
                execution_results
            )
            
            # Step 6.4: Alert stakeholders
            await self._alert_stakeholders(intervention_plan, monitoring_data)
            
            execution_report = {
                'content_id': content_id,
                'status': 'SUCCESS',
                'actions_executed': execution_results,
                'monitoring': monitoring_data,
                'actual_reduction': monitoring_data.get('actual_reduction'),
                'timestamp': datetime.utcnow().isoformat(),
                'intervention_plan': intervention_plan
            }
            
            logger.info(
                f"✅ Intervention complete: {content_id} - "
                f"Reduction: {monitoring_data.get('actual_reduction', 'N/A')}"
            )
            
            return execution_report
            
        except Exception as e:
            logger.error(f"Error executing intervention: {e}", exc_info=True)
            return self._error_report(intervention_plan)
    
    async def _request_human_approval(self, plan: Dict) -> bool:
        """
        Request human approval for high-risk interventions
        Returns: True if approved, False otherwise
        """
        logger.info(
            f"🚨 Requesting human approval for: {plan.get('content_id')} "
            f"(Priority: {plan.get('priority')})"
        )
        
        # In production: send to dashboard, wait for response via WebSocket
        # For now: auto-approve after timeout (simulated)
        await asyncio.sleep(0.5)  # Simulated wait
        
        # Auto-approve for demo (in production: wait for real response)
        return True
    
    async def _execute_actions(self, plan: Dict) -> List[Dict]:
        """
        Execute all actions in the intervention plan
        """
        actions = plan.get('actions', [])
        results = []
        
        for action in actions:
            action_type = action.get('type')
            logger.info(f"🔧 Executing action: {action_type}")
            
            if action_type == 'throttle_bots':
                result = await self._throttle_bots(action, plan)
            elif action_type == 'deploy_factcheck':
                result = await self._deploy_factcheck(action, plan)
            elif action_type == 'report_to_platform':
                result = await self._report_to_platform(action, plan)
            elif action_type == 'alert_influencers':
                result = await self._alert_influencers(action, plan)
            elif action_type == 'counter_narrative':
                result = await self._deploy_counter_narrative(action, plan)
            elif action_type == 'monitor_only':
                result = await self._setup_monitoring(action, plan)
            else:
                result = {'action': action_type, 'status': 'UNKNOWN_ACTION'}
            
            results.append(result)
            
            # Brief pause between actions
            await asyncio.sleep(0.2)
        
        return results
    
    async def _throttle_bots(self, action: Dict, plan: Dict) -> Dict:
        """
        Report bot accounts to platform
        """
        target = action.get('target', '')
        logger.info(f"🤖 Throttling bots: {target}")
        
        # In production: use Twitter API to report bot accounts
        # For now: simulate
        
        return {
            'action': 'throttle_bots',
            'status': 'SUCCESS',
            'accounts_reported': target,
            'expected_suspension_rate': '60-70%',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _deploy_factcheck(self, action: Dict, plan: Dict) -> Dict:
        """
        Generate and post fact-check content
        """
        logger.info("📝 Deploying fact-check...")
        
        # Step 1: Generate fact-check content using GPT-4
        factcheck_text = await self._generate_factcheck_content(plan)
        
        # Step 2: Post to Twitter (reply to original)
        # In production: use Twitter API
        # response = await self.twitter_api.post_tweet(factcheck_text, reply_to=...)
        
        # Step 3: Distribute to fact-check partners
        await self._distribute_to_partners(factcheck_text, plan)
        
        return {
            'action': 'deploy_factcheck',
            'status': 'SUCCESS',
            'content': factcheck_text[:100] + '...',
            'channels': ['Twitter', 'Fact-check database'],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _generate_factcheck_content(self, plan: Dict) -> str:
        """
        Generate fact-check content using GPT-4
        """
        evidence_report = plan.get('prediction_report', {}).get('evidence_report', {})
        debunks = evidence_report.get('debunks', [])
        
        # Simplified - in production: use GPT-4 API
        if debunks:
            source = debunks[0].get('source', 'fact-checkers')
            factcheck = (
                f"⚠️ This claim is FALSE. According to {source}, "
                f"this has been debunked. See full details: [link]"
            )
        else:
            factcheck = (
                "⚠️ This claim is unverified and shows signs of misinformation. "
                "Please verify before sharing."
            )
        
        return factcheck
    
    async def _distribute_to_partners(self, content: str, plan: Dict) -> None:
        """
        Distribute fact-check to partner organizations
        """
        # In production: send to Snopes, PolitiFact, etc.
        logger.info("📤 Distributing fact-check to partners...")
    
    async def _report_to_platform(self, action: Dict, plan: Dict) -> Dict:
        """
        Report content to platform for TOS violation
        """
        logger.info("🚩 Reporting to platform...")
        
        # In production: use platform reporting APIs
        
        return {
            'action': 'report_to_platform',
            'status': 'SUCCESS',
            'platform': 'Twitter',
            'report_id': 'RPT_' + datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _alert_influencers(self, action: Dict, plan: Dict) -> Dict:
        """
        Alert high-reach users about misinformation
        """
        logger.info("📢 Alerting influencers...")
        
        # In production: send DMs or emails to top influencers
        
        return {
            'action': 'alert_influencers',
            'status': 'SUCCESS',
            'influencers_contacted': 10,
            'method': 'Email + DM',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _deploy_counter_narrative(self, action: Dict, plan: Dict) -> Dict:
        """
        Create and boost counter-narrative content
        """
        logger.info("🎬 Deploying counter-narrative...")
        
        # In production: create content + paid promotion
        
        return {
            'action': 'counter_narrative',
            'status': 'SUCCESS',
            'content_created': True,
            'boost_budget': '$10',
            'expected_reach': 5000,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _setup_monitoring(self, action: Dict, plan: Dict) -> Dict:
        """
        Set up continuous monitoring
        """
        logger.info("👁️ Setting up monitoring...")
        
        return {
            'action': 'monitor_only',
            'status': 'ACTIVE',
            'monitoring_interval': '30 minutes',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _monitor_intervention(
        self,
        plan: Dict,
        execution_results: List[Dict]
    ) -> Dict:
        """
        Monitor intervention progress and measure effectiveness
        """
        logger.info("📊 Monitoring intervention progress...")
        
        # In production: track actual spread metrics over time
        # For now: simulate monitoring
        
        predicted_reduction = float(plan.get('expected_reduction', '50%').rstrip('%')) / 100
        
        # Simulate actual outcome (slight variance from prediction)
        import random
        variance = random.uniform(-0.1, 0.1)
        actual_reduction = max(0, min(1, predicted_reduction + variance))
        
        original_reach = plan.get('original_predicted_reach', 10000)
        final_reach = int(original_reach * (1 - actual_reduction))
        
        success = actual_reduction >= (predicted_reduction * 0.8)  # Within 80% of target
        
        return {
            'predicted_reduction': f"{int(predicted_reduction * 100)}%",
            'actual_reduction': f"{int(actual_reduction * 100)}%",
            'original_predicted_reach': original_reach,
            'final_actual_reach': final_reach,
            'success': success,
            'monitoring_points': [
                {'time': '30m', 'reach': int(final_reach * 0.3)},
                {'time': '1h', 'reach': int(final_reach * 0.5)},
                {'time': '6h', 'reach': int(final_reach * 0.8)},
                {'time': '24h', 'reach': final_reach}
            ]
        }
    
    async def _alert_stakeholders(self, plan: Dict, monitoring: Dict) -> None:
        """
        Send alerts and updates to stakeholders
        """
        logger.info("📧 Alerting stakeholders...")
        
        # In production: WebSocket push, email, SMS
        # For now: just log
        
        logger.info(
            f"Intervention {plan.get('content_id')}: "
            f"{monitoring.get('actual_reduction')} reduction achieved"
        )
    
    def _rejected_report(self, plan: Dict) -> Dict:
        """Return report for rejected intervention"""
        return {
            'content_id': plan.get('content_id'),
            'status': 'REJECTED',
            'reason': 'Human operator declined intervention',
            'timestamp': datetime.utcnow().isoformat(),
            'intervention_plan': plan
        }
    
    def _error_report(self, plan: Dict) -> Dict:
        """Return error report if execution fails"""
        return {
            'content_id': plan.get('content_id'),
            'status': 'FAILED',
            'error': True,
            'timestamp': datetime.utcnow().isoformat(),
            'intervention_plan': plan
        }
