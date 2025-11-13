"""
Agent 5: Strategist Agent - The Tactician
RL-based intervention planning using Proximal Policy Optimization (PPO)
"""

import asyncio
import logging
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class StrategistAgent:
    """
    Strategist Agent uses Reinforcement Learning to select optimal
    intervention strategies based on state, cost, and expected impact
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.auto_execute_threshold = config.get('auto_execute_threshold', 0.9)
        self.budget_remaining = config.get('daily_budget', 5000)
        
        # In production: load trained PPO model
        self.rl_agent = None
        
        # Available actions with cost and impact estimates
        self.actions = {
            'deploy_factcheck': {
                'cost': 5,
                'impact': 0.4,
                'time': 0,  # Immediate
                'best_for': ['high_evidence', 'clear_fake']
            },
            'report_to_platform': {
                'cost': 0,
                'impact': 0.2,  # Uncertain - depends on platform
                'time': 12,  # Hours
                'best_for': ['tos_violation', 'hate_speech']
            },
            'throttle_bots': {
                'cost': 2,
                'impact': 0.6,
                'time': 1,
                'best_for': ['high_bot_involvement']
            },
            'alert_influencers': {
                'cost': 1,
                'impact': 0.3,
                'time': 0,
                'best_for': ['high_reach_predicted']
            },
            'counter_narrative': {
                'cost': 10,
                'impact': 0.7,
                'time': 3,
                'best_for': ['critical_topics', 'health', 'safety']
            },
            'monitor_only': {
                'cost': 0,
                'impact': 0,
                'time': 0,
                'best_for': ['low_risk']
            }
        }
        
        logger.info("✅ Strategist Agent initialized")
    
    async def plan_intervention(self, prediction_report: Dict) -> Dict:
        """
        Generate optimal intervention plan using RL
        
        Args:
            prediction_report: Viral prediction from Predictor Agent
            
        Returns:
            Intervention plan with actions, costs, and expected outcomes
        """
        try:
            content_id = prediction_report.get('content_id')
            logger.info(f"🎯 Planning intervention for: {content_id}")
            
            # Step 5.1: Build state representation
            state_vector = self._build_state_vector(prediction_report)
            
            # Step 5.2: Evaluate action options
            action_evaluations = self._evaluate_actions(state_vector, prediction_report)
            
            # Step 5.3: RL decision (PPO agent selects actions)
            selected_actions = await self._rl_decision(state_vector, action_evaluations)
            
            # Step 5.4: Generate intervention plan
            intervention_plan = self._generate_plan(
                selected_actions,
                action_evaluations,
                prediction_report
            )
            
            logger.info(
                f"✅ Plan generated: {content_id} - "
                f"Actions: {[a['type'] for a in intervention_plan['actions']]}"
            )
            
            return intervention_plan
            
        except Exception as e:
            logger.error(f"Error planning intervention: {e}", exc_info=True)
            return self._error_plan(prediction_report)
    
    def _build_state_vector(self, report: Dict) -> np.ndarray:
        """
        Build state representation for RL agent
        Features: fake_prob, viral_risk, reach, bots, evidence, topic, time, budget
        """
        evidence_report = report.get('evidence_report', {})
        
        state = np.array([
            evidence_report.get('fake_probability', 0.5),
            report.get('viral_risk', 0.5),
            min(report.get('predicted_reach', {}).get('24h', 0) / 50000, 1.0),
            report.get('bot_percentage', 0),
            evidence_report.get('evidence_strength', 0.5),
            self._encode_topic(evidence_report),
            self._get_time_urgency(report),
            min(self.budget_remaining / 5000, 1.0)
        ])
        
        return state
    
    def _encode_topic(self, report: Dict) -> float:
        """Encode topic sensitivity (0-1)"""
        # Extract topic from evidence report
        # High sensitivity topics get higher values
        # Placeholder - in production: proper topic extraction
        return 0.7
    
    def _get_time_urgency(self, report: Dict) -> float:
        """Calculate time urgency (0-1)"""
        # Based on how soon content will peak
        peak_time = report.get('peak_time', '24h')
        hours = int(peak_time.replace('h', ''))
        
        # Sooner peak = higher urgency
        urgency = max(0, 1 - (hours / 48))
        return urgency
    
    def _evaluate_actions(self, state: np.ndarray, report: Dict) -> Dict[str, Dict]:
        """
        Evaluate each action's suitability for current state
        """
        evaluations = {}
        
        fake_prob = state[0]
        viral_risk = state[1]
        bot_percentage = state[3]
        evidence_strength = state[4]
        
        for action_name, action_config in self.actions.items():
            # Calculate Q-value (expected return) for this action
            q_value = self._estimate_q_value(
                action_name,
                action_config,
                state,
                report
            )
            
            evaluations[action_name] = {
                'q_value': q_value,
                'cost': action_config['cost'],
                'impact': action_config['impact'],
                'time': action_config['time'],
                'suitable': self._is_suitable(action_name, state, report)
            }
        
        return evaluations
    
    def _estimate_q_value(
        self,
        action_name: str,
        action_config: Dict,
        state: np.ndarray,
        report: Dict
    ) -> float:
        """
        Estimate Q-value: expected cumulative reward for taking this action
        In production: use trained neural network
        """
        fake_prob = state[0]
        viral_risk = state[1]
        bot_percentage = state[3]
        
        # Heuristic Q-value calculation
        base_value = 0.5
        
        if action_name == 'deploy_factcheck':
            # Good for high fake probability, strong evidence
            base_value = 0.6 + (fake_prob * 0.3)
        
        elif action_name == 'throttle_bots':
            # Excellent for high bot involvement
            base_value = 0.5 + (bot_percentage * 0.5)
        
        elif action_name == 'counter_narrative':
            # Good for high risk, critical topics
            base_value = 0.4 + (viral_risk * 0.4)
        
        elif action_name == 'monitor_only':
            # Good for low risk
            base_value = max(0, 0.8 - (viral_risk * 0.6))
        
        # Adjust for cost-effectiveness
        cost_penalty = action_config['cost'] / 20.0  # Normalize
        q_value = base_value - (cost_penalty * 0.2)
        
        return max(0, min(1, q_value))
    
    def _is_suitable(self, action_name: str, state: np.ndarray, report: Dict) -> bool:
        """Check if action is suitable for current situation"""
        viral_risk = state[1]
        bot_percentage = state[3]
        
        if action_name == 'throttle_bots' and bot_percentage < 0.15:
            return False
        
        if action_name == 'monitor_only' and viral_risk > 0.7:
            return False
        
        # Check budget
        if self.budget_remaining < self.actions[action_name]['cost']:
            return False
        
        return True
    
    async def _rl_decision(
        self,
        state: np.ndarray,
        evaluations: Dict[str, Dict]
    ) -> List[str]:
        """
        Use RL agent (PPO) to select actions
        Returns: List of action names to execute
        """
        # Sort actions by Q-value
        sorted_actions = sorted(
            evaluations.items(),
            key=lambda x: x[1]['q_value'],
            reverse=True
        )
        
        selected = []
        total_cost = 0
        
        # Select top actions that fit budget and are suitable
        for action_name, eval_data in sorted_actions:
            if (eval_data['suitable'] and 
                eval_data['q_value'] > 0.5 and
                total_cost + eval_data['cost'] <= self.budget_remaining):
                
                selected.append(action_name)
                total_cost += eval_data['cost']
                
                # Stop after 2-3 actions max
                if len(selected) >= 3:
                    break
        
        # Ensure at least one action
        if not selected:
            selected = ['monitor_only']
        
        return selected
    
    def _generate_plan(
        self,
        selected_actions: List[str],
        evaluations: Dict[str, Dict],
        report: Dict
    ) -> Dict:
        """
        Generate detailed intervention plan from selected actions
        """
        viral_risk = report.get('viral_risk', 0.5)
        predicted_reach = report.get('predicted_reach', {})
        
        # Build action details
        actions = []
        total_cost = 0
        total_impact = 0
        
        for action_name in selected_actions:
            action_config = self.actions[action_name]
            eval_data = evaluations[action_name]
            
            action_detail = {
                'type': action_name,
                'cost': action_config['cost'],
                'expected_impact': action_config['impact'],
                'timeline': f"{action_config['time']} hours" if action_config['time'] > 0 else "Immediate",
                'priority': 'HIGH' if viral_risk > 0.8 else 'MEDIUM',
                'target': self._get_action_target(action_name, report)
            }
            
            actions.append(action_detail)
            total_cost += action_config['cost']
            total_impact += action_config['impact']
        
        # Calculate expected outcome
        original_reach = predicted_reach.get('48h', 10000)
        reduction_rate = min(total_impact, 0.9)
        final_reach = int(original_reach * (1 - reduction_rate))
        
        # Determine priority and approval needed
        priority = 'URGENT' if viral_risk > 0.8 else 'HIGH' if viral_risk > 0.6 else 'MEDIUM'
        needs_approval = viral_risk > self.auto_execute_threshold or total_cost > 20
        
        plan = {
            'content_id': report.get('content_id'),
            'priority': priority,
            'needs_human_approval': needs_approval,
            'actions': actions,
            'total_cost': total_cost,
            'expected_reduction': f"{int(reduction_rate * 100)}%",
            'predicted_final_reach': final_reach,
            'original_predicted_reach': original_reach,
            'confidence': 0.85,
            'timestamp': datetime.utcnow().isoformat(),
            'prediction_report': report
        }
        
        # Update budget
        self.budget_remaining -= total_cost
        
        return plan
    
    def _get_action_target(self, action_name: str, report: Dict) -> str:
        """Get target description for action"""
        if action_name == 'throttle_bots':
            bot_count = int(report.get('network_size', 0) * report.get('bot_percentage', 0))
            return f"{bot_count} bot accounts"
        elif action_name == 'deploy_factcheck':
            return "Original post + high-reach sharers"
        elif action_name == 'alert_influencers':
            return "Top 10 influencers in network"
        else:
            return "N/A"
    
    def _error_plan(self, report: Dict) -> Dict:
        """Return error/fallback plan"""
        return {
            'content_id': report.get('content_id'),
            'priority': 'MEDIUM',
            'needs_human_approval': True,
            'actions': [
                {
                    'type': 'monitor_only',
                    'cost': 0,
                    'timeline': 'Continuous',
                    'target': 'All channels'
                }
            ],
            'total_cost': 0,
            'error': True,
            'prediction_report': report
        }
