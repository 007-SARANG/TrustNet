"""
Agent 4: Predictor Agent - The Oracle
GNN-based viral spread forecasting, bot detection, and risk assessment
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
import networkx as nx
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PredictorAgent:
    """
    Predictor Agent forecasts viral spread using Graph Neural Networks,
    detects bot networks, and calculates viral risk scores
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.risk_threshold = config.get('risk_threshold', 0.8)
        
        # In production: load pre-trained GraphSAGE model
        self.gnn_model = None
        
        logger.info("✅ Predictor Agent initialized")
    
    async def predict_spread(self, evidence_report: Dict) -> Dict:
        """
        Predict viral spread and assess risk
        
        Args:
            evidence_report: Evidence from Investigator Agent
            
        Returns:
            Viral forecast with risk score and bot detection
        """
        try:
            content_id = evidence_report.get('content_id')
            logger.info(f"📈 Predicting spread for: {content_id}")
            
            # Step 4.1: Build social network graph
            network_graph = await self._build_network_graph(evidence_report)
            
            # Step 4.2: Bot detection
            bot_analysis = await self._detect_bots(network_graph, evidence_report)
            
            # Step 4.3: Propagation prediction using GNN
            spread_forecast = await self._predict_propagation(
                network_graph,
                evidence_report,
                bot_analysis
            )
            
            # Step 4.4: Calculate viral risk score
            risk_assessment = self._calculate_risk_score(
                spread_forecast,
                bot_analysis,
                evidence_report
            )
            
            prediction_report = {
                'content_id': content_id,
                'network_size': network_graph['node_count'],
                'bot_percentage': bot_analysis['bot_percentage'],
                'predicted_reach': spread_forecast['predictions'],
                'peak_time': spread_forecast['peak_time'],
                'viral_risk': risk_assessment['viral_risk'],
                'risk_level': risk_assessment['risk_level'],
                'bot_networks': bot_analysis['bot_networks'],
                'recommendation': risk_assessment['recommendation'],
                'evidence_report': evidence_report
            }
            
            logger.info(
                f"✅ Prediction complete: {content_id} - "
                f"Risk: {risk_assessment['viral_risk']:.2f}"
            )
            
            return prediction_report
            
        except Exception as e:
            logger.error(f"Error predicting spread: {e}", exc_info=True)
            return self._error_report(evidence_report)
    
    async def _build_network_graph(self, report: Dict) -> Dict:
        """
        Build social network graph from engagement data
        """
        # Extract network data from source
        source_data = report.get('analysis_report', {}).get('source_data', {})
        metadata = source_data.get('metadata', {})
        
        # Create NetworkX graph
        G = nx.DiGraph()
        
        # Add seed node (original poster)
        author = metadata.get('author', {})
        seed_id = author.get('id', 'unknown')
        
        G.add_node(seed_id, **{
            'followers': author.get('followers', 0),
            'verified': author.get('verified', False),
            'account_age': author.get('account_age_days', 365),
            'influence_score': self._calculate_influence(author)
        })
        
        # In production: fetch actual network data from social media APIs
        # For now, simulate network structure
        
        return {
            'graph': G,
            'node_count': G.number_of_nodes(),
            'edge_count': G.number_of_edges(),
            'seed_node': seed_id
        }
    
    def _calculate_influence(self, user: Dict) -> float:
        """Calculate user influence score (0-1)"""
        followers = user.get('followers', 0)
        verified = user.get('verified', False)
        
        # Logarithmic scale for followers
        follower_score = min(np.log10(followers + 1) / 7, 1.0)
        
        # Verification bonus
        influence = follower_score + (0.2 if verified else 0)
        
        return min(influence, 1.0)
    
    async def _detect_bots(self, network: Dict, report: Dict) -> Dict:
        """
        Detect bots and coordinated inauthentic behavior
        """
        G = network['graph']
        
        # Bot detection features for each node
        bot_scores = {}
        bot_count = 0
        
        for node in G.nodes():
            node_data = G.nodes[node]
            
            # Bot indicators
            features = {
                'default_profile': not node_data.get('has_custom_profile', True),
                'high_frequency': node_data.get('tweets_per_day', 0) > 50,
                'low_followers': node_data.get('followers', 100) < 50,
                'suspicious_username': self._check_suspicious_username(node),
                'new_account': node_data.get('account_age', 365) < 30
            }
            
            # Simple bot score (in production: use Random Forest classifier)
            bot_score = sum(features.values()) / len(features)
            bot_scores[node] = bot_score
            
            if bot_score > 0.6:
                bot_count += 1
        
        # Detect coordinated networks (clusters of bots)
        bot_networks = self._detect_coordinated_behavior(G, bot_scores)
        
        total_nodes = G.number_of_nodes()
        bot_percentage = (bot_count / total_nodes) if total_nodes > 0 else 0
        
        return {
            'bot_count': bot_count,
            'bot_percentage': bot_percentage,
            'bot_scores': bot_scores,
            'bot_networks': bot_networks,
            'inauthentic_amplification': bot_percentage > 0.15
        }
    
    def _check_suspicious_username(self, username: str) -> bool:
        """Check for suspicious username patterns"""
        # Patterns: random chars, many numbers
        digit_ratio = sum(c.isdigit() for c in username) / len(username) if username else 0
        return digit_ratio > 0.5
    
    def _detect_coordinated_behavior(
        self,
        G: nx.DiGraph,
        bot_scores: Dict[str, float]
    ) -> List[Dict]:
        """
        Detect clusters of bots acting in coordination
        """
        # Find communities using Louvain algorithm (simplified)
        # In production: implement proper community detection
        
        bot_networks = []
        
        # Identify high-bot-score communities
        high_bot_nodes = [node for node, score in bot_scores.items() if score > 0.6]
        
        if len(high_bot_nodes) > 5:
            bot_networks.append({
                'size': len(high_bot_nodes),
                'coordination_score': 0.8,
                'description': 'Suspected bot network detected'
            })
        
        return bot_networks
    
    async def _predict_propagation(
        self,
        network: Dict,
        report: Dict,
        bot_analysis: Dict
    ) -> Dict:
        """
        Use GNN to predict viral spread over time
        """
        # Current engagement
        source_data = report.get('analysis_report', {}).get('source_data', {})
        current_engagement = source_data.get('metadata', {}).get('engagement', {})
        current_reach = sum(current_engagement.values())
        
        # Simulate spread (in production: use trained GraphSAGE model)
        predictions = self._monte_carlo_simulation(
            network,
            current_reach,
            bot_analysis
        )
        
        # Find peak time
        peak_idx = np.argmax(list(predictions.values()))
        peak_time = list(predictions.keys())[peak_idx]
        
        return {
            'current_reach': current_reach,
            'predictions': predictions,
            'peak_time': peak_time,
            'method': 'Monte Carlo simulation'
        }
    
    def _monte_carlo_simulation(
        self,
        network: Dict,
        current_reach: int,
        bot_analysis: Dict,
        num_simulations: int = 100
    ) -> Dict[str, int]:
        """
        Monte Carlo simulation of viral spread
        """
        # Growth rate based on bot involvement
        bot_boost = 1 + (bot_analysis['bot_percentage'] * 0.5)
        
        # Predict reach at different time points
        time_points = {
            '6h': int(current_reach * 2.5 * bot_boost),
            '12h': int(current_reach * 5.0 * bot_boost),
            '24h': int(current_reach * 12.0 * bot_boost),
            '48h': int(current_reach * 25.0 * bot_boost),
        }
        
        return time_points
    
    def _calculate_risk_score(
        self,
        forecast: Dict,
        bot_analysis: Dict,
        evidence_report: Dict
    ) -> Dict:
        """
        Calculate viral risk score (0-1) and generate recommendation
        """
        # Risk factors
        reach_24h = forecast['predictions'].get('24h', 0)
        bot_percentage = bot_analysis['bot_percentage']
        fake_prob = evidence_report.get('fake_probability', 0.5)
        
        # Get topic sensitivity
        topic = self._extract_topic(evidence_report)
        topic_sensitivity = self._get_topic_sensitivity(topic)
        
        # Weights
        w = {'reach': 0.3, 'velocity': 0.25, 'bots': 0.2, 'topic': 0.25}
        
        # Normalize reach (log scale)
        reach_score = min(np.log10(reach_24h + 1) / 5, 1.0)
        
        # Velocity (how fast it's growing)
        velocity_score = min(reach_24h / 50000, 1.0)
        
        # Bot involvement
        bot_score = bot_percentage
        
        # Calculate risk
        viral_risk = (
            w['reach'] * reach_score +
            w['velocity'] * velocity_score +
            w['bots'] * bot_score +
            w['topic'] * topic_sensitivity
        )
        
        # Risk level
        if viral_risk >= 0.8:
            risk_level = 'CRITICAL'
            recommendation = 'URGENT INTERVENTION NEEDED'
        elif viral_risk >= 0.6:
            risk_level = 'HIGH'
            recommendation = 'INTERVENTION RECOMMENDED'
        elif viral_risk >= 0.4:
            risk_level = 'MEDIUM'
            recommendation = 'MONITOR CLOSELY'
        else:
            risk_level = 'LOW'
            recommendation = 'CONTINUE MONITORING'
        
        return {
            'viral_risk': viral_risk,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'factors': {
                'reach_score': reach_score,
                'velocity_score': velocity_score,
                'bot_score': bot_score,
                'topic_sensitivity': topic_sensitivity
            }
        }
    
    def _extract_topic(self, report: Dict) -> str:
        """Extract main topic from content"""
        # Simplified - in production: use topic modeling
        text = report.get('analysis_report', {}).get('source_data', {}).get('text', '').lower()
        
        if any(word in text for word in ['vaccine', 'covid', 'health', 'medical']):
            return 'health'
        elif any(word in text for word in ['election', 'vote', 'political', 'government']):
            return 'politics'
        else:
            return 'general'
    
    def _get_topic_sensitivity(self, topic: str) -> float:
        """Get sensitivity multiplier for topic"""
        sensitivity = {
            'health': 0.9,
            'politics': 0.7,
            'general': 0.5
        }
        return sensitivity.get(topic, 0.5)
    
    def _error_report(self, report: Dict) -> Dict:
        """Return error report if prediction fails"""
        return {
            'content_id': report.get('content_id'),
            'viral_risk': 0.5,
            'risk_level': 'MEDIUM',
            'recommendation': 'MONITOR - PREDICTION ERROR',
            'error': True,
            'evidence_report': report
        }
