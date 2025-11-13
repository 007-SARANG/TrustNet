"""
Agent 1: Scout Agent - The Sentinel
Monitors social media streams, detects anomalies, and flags suspicious content
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class ScoutAgent:
    """
    Scout Agent monitors incoming social media content and flags suspicious posts
    Processing: 10,000 posts/minute with real-time anomaly detection
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.priority_threshold = config.get('priority_threshold', 0.7)
        
        # Suspicious keywords (health misinformation, conspiracy theories)
        self.suspicious_keywords = [
            'vaccine', 'infertility', 'microchip', '5g', 'conspiracy',
            'cover-up', 'hidden truth', 'they don\'t want you to know',
            'breaking', 'urgent', 'share immediately', 'banned', 'censored'
        ]
        
        logger.info("✅ Scout Agent initialized")
    
    async def process_content(self, content: Dict) -> Optional[Dict]:
        """
        Process incoming content and determine if it should be flagged
        
        Args:
            content: Raw social media post with text, metadata, engagement
            
        Returns:
            Flagged content dict if suspicious, None otherwise
        """
        try:
            text = content.get('text', '')
            
            # Step 1: Language detection (English only for MVP)
            if not self._is_english(text):
                return None
            
            # Step 2: Remove spam/ads
            if self._is_spam(content):
                return None
            
            # Step 3: Anomaly detection
            anomaly_score = await self._detect_anomalies(content)
            
            # Step 4: Priority scoring
            priority_score = self._calculate_priority(content, anomaly_score)
            
            if priority_score >= self.priority_threshold:
                flagged = {
                    'content_id': content.get('id'),
                    'text': text,
                    'images': content.get('images', []),
                    'videos': content.get('videos', []),
                    'metadata': self._extract_metadata(content),
                    'priority_score': priority_score,
                    'anomaly_score': anomaly_score,
                    'priority_level': self._get_priority_level(priority_score),
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': content.get('source', 'unknown')
                }
                
                logger.info(f"🚨 Flagged content: {content.get('id')} (priority: {priority_score:.2f})")
                return flagged
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing content: {e}", exc_info=True)
            return None
    
    def _is_english(self, text: str) -> bool:
        """Simple English language detection"""
        # Basic check - can be enhanced with langdetect library
        english_chars = sum(c.isascii() for c in text)
        return (english_chars / len(text)) > 0.8 if text else False
    
    def _is_spam(self, content: Dict) -> bool:
        """Detect spam and advertisements"""
        text = content.get('text', '').lower()
        
        # Spam indicators
        spam_keywords = ['buy now', 'click here', 'limited offer', 'act fast', 'discount']
        has_spam_keywords = any(keyword in text for keyword in spam_keywords)
        
        # Excessive links
        links = content.get('urls', [])
        has_too_many_links = len(links) > 3
        
        return has_spam_keywords or has_too_many_links
    
    async def _detect_anomalies(self, content: Dict) -> float:
        """
        Detect anomalies in content using multiple signals
        Returns: anomaly score (0-1)
        """
        text = content.get('text', '')
        scores = []
        
        # 1. Suspicious keyword detection
        keyword_score = self._check_suspicious_keywords(text)
        scores.append(keyword_score)
        
        # 2. Engagement velocity check
        velocity_score = self._check_viral_velocity(content)
        scores.append(velocity_score)
        
        # 3. Emotional language detection
        emotion_score = self._check_emotional_language(text)
        scores.append(emotion_score)
        
        # Aggregate scores
        anomaly_score = np.mean(scores)
        return float(anomaly_score)
    
    def _check_suspicious_keywords(self, text: str) -> float:
        """Check for predefined suspicious keywords"""
        text_lower = text.lower()
        matches = sum(1 for keyword in self.suspicious_keywords if keyword in text_lower)
        return min(matches / 3.0, 1.0)  # Normalize
    
    def _check_viral_velocity(self, content: Dict) -> float:
        """Check if content is spreading unusually fast"""
        engagement = content.get('engagement', {})
        likes = engagement.get('likes', 0)
        retweets = engagement.get('retweets', 0)
        comments = engagement.get('comments', 0)
        
        # Calculate engagement rate (simplified)
        total_engagement = likes + retweets * 2 + comments * 3
        time_since_post = content.get('time_since_post_hours', 1)
        
        engagement_rate = total_engagement / max(time_since_post, 0.1)
        
        # High velocity threshold
        if engagement_rate > 100:
            return 0.9
        elif engagement_rate > 50:
            return 0.7
        elif engagement_rate > 20:
            return 0.5
        else:
            return 0.2
    
    def _check_emotional_language(self, text: str) -> float:
        """Detect highly emotional or manipulative language using VADER"""
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        
        # High negative or positive compound scores indicate emotional content
        compound = abs(sentiment_scores['compound'])
        
        # Check for urgency markers
        urgency_words = ['breaking', 'urgent', 'immediately', 'now', 'alert', 'warning']
        has_urgency = any(word in text.lower() for word in urgency_words)
        
        emotion_score = compound
        if has_urgency:
            emotion_score = min(emotion_score + 0.3, 1.0)
        
        return emotion_score
    
    def _calculate_priority(self, content: Dict, anomaly_score: float) -> float:
        """
        Calculate overall priority score for the content
        Returns: priority score (0-1)
        """
        # Factors that influence priority
        engagement = content.get('engagement', {})
        author_followers = content.get('author', {}).get('followers', 0)
        
        # Weighted combination
        weights = {
            'anomaly': 0.4,
            'engagement': 0.3,
            'influence': 0.2,
            'recency': 0.1
        }
        
        # Normalize engagement (log scale)
        total_engagement = sum(engagement.values()) if engagement else 0
        engagement_score = min(np.log10(total_engagement + 1) / 5, 1.0)
        
        # Normalize influence
        influence_score = min(np.log10(author_followers + 1) / 7, 1.0)
        
        # Recency bonus (newer = higher priority)
        time_since_post = content.get('time_since_post_hours', 24)
        recency_score = max(0, 1 - (time_since_post / 24))
        
        # Calculate weighted priority
        priority = (
            weights['anomaly'] * anomaly_score +
            weights['engagement'] * engagement_score +
            weights['influence'] * influence_score +
            weights['recency'] * recency_score
        )
        
        return float(priority)
    
    def _get_priority_level(self, score: float) -> str:
        """Convert numeric score to priority level"""
        if score >= 0.8:
            return 'HIGH'
        elif score >= 0.6:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _extract_metadata(self, content: Dict) -> Dict:
        """Extract relevant metadata from content"""
        return {
            'author': content.get('author', {}),
            'timestamp': content.get('timestamp'),
            'platform': content.get('source'),
            'url': content.get('url'),
            'engagement': content.get('engagement', {}),
            'has_media': bool(content.get('images') or content.get('videos'))
        }
