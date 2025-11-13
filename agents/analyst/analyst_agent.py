"""
Agent 2: Analyst Agent - The Detective
Multi-modal classification: Text + Image + Video analysis
"""

import asyncio
import logging
from typing import Dict, List, Optional
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from PIL import Image
import numpy as np
import os
from groq import Groq

logger = logging.getLogger(__name__)


class AnalystAgent:
    """
    Analyst Agent performs deep multi-modal analysis of flagged content
    Uses RoBERTa for text, CNNs for images, and GPT-4 for advanced analysis
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.fake_threshold = config.get('fake_threshold', 0.7)
        
        # Initialize models
        logger.info("Loading RoBERTa model...")
        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        # In production, load fine-tuned model on FakeNewsNet
        self.text_classifier = RobertaForSequenceClassification.from_pretrained(
            'roberta-base',
            num_labels=2
        )
        
        # Initialize Groq client (FREE and FASTER than OpenAI!)
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Clickbait and urgency markers
        self.clickbait_words = [
            'shocking', 'unbelievable', 'you won\'t believe',
            'doctors hate', 'this one trick', 'number 7 will shock you'
        ]
        
        self.urgency_markers = [
            'breaking', 'urgent', 'share now', 'before it\'s deleted',
            'act fast', 'limited time', 'they don\'t want you to know'
        ]
        
        logger.info("✅ Analyst Agent initialized")
    
    async def analyze_content(self, flagged_content: Dict) -> Dict:
        """
        Comprehensive multi-modal analysis of flagged content
        
        Args:
            flagged_content: Content flagged by Scout Agent
            
        Returns:
            Analysis report with classification, confidence, and reasoning
        """
        try:
            content_id = flagged_content.get('content_id')
            logger.info(f"🔍 Analyzing content: {content_id}")
            
            # Step 2.1: Text Analysis
            text_analysis = await self._analyze_text(flagged_content.get('text', ''))
            
            # Step 2.2: Image Analysis (if present)
            image_analysis = None
            if flagged_content.get('images'):
                image_analysis = await self._analyze_images(flagged_content.get('images'))
            
            # Step 2.3: Video Analysis (if present)
            video_analysis = None
            if flagged_content.get('videos'):
                video_analysis = await self._analyze_videos(flagged_content.get('videos'))
            
            # Step 2.4: Cross-modal verification
            cross_modal_score = await self._cross_modal_verification(
                text_analysis, image_analysis, video_analysis
            )
            
            # Step 2.5: Aggregate all scores
            final_report = self._aggregate_scores(
                text_analysis,
                image_analysis,
                video_analysis,
                cross_modal_score
            )
            
            final_report['content_id'] = content_id
            final_report['source_data'] = flagged_content
            
            logger.info(
                f"✅ Analysis complete: {content_id} - "
                f"Fake prob: {final_report['fake_probability']:.2f}"
            )
            
            return final_report
            
        except Exception as e:
            logger.error(f"Error analyzing content: {e}", exc_info=True)
            return self._error_report(flagged_content)
    
    async def _analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis using multiple techniques
        """
        # A. RoBERTa Classification
        roberta_score = await self._roberta_classification(text)
        
        # B. Linguistic Feature Analysis
        clickbait_score = self._detect_clickbait(text)
        urgency_score = self._detect_urgency(text)
        emotional_score = self._detect_emotional_manipulation(text)
        
        # C. GPT-4 Advanced Analysis
        gpt4_analysis = await self._gpt4_analysis(text)
        
        # Combine scores
        text_score = (
            roberta_score * 0.4 +
            clickbait_score * 0.15 +
            urgency_score * 0.15 +
            emotional_score * 0.15 +
            gpt4_analysis['fake_score'] * 0.15
        )
        
        return {
            'text_fake_probability': text_score,
            'roberta_score': roberta_score,
            'clickbait_detected': clickbait_score > 0.5,
            'urgency_detected': urgency_score > 0.5,
            'emotional_manipulation': emotional_score > 0.6,
            'gpt4_insights': gpt4_analysis['insights'],
            'key_claims': gpt4_analysis['claims']
        }
    
    async def _roberta_classification(self, text: str) -> float:
        """RoBERTa-based fake news classification"""
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                max_length=512,
                truncation=True,
                padding=True,
                return_tensors='pt'
            )
            
            # Inference
            with torch.no_grad():
                outputs = self.text_classifier(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                fake_prob = probabilities[0][1].item()  # Probability of class 1 (fake)
            
            return fake_prob
        except Exception as e:
            logger.error(f"RoBERTa classification error: {e}")
            return 0.5  # Neutral if error
    
    def _detect_clickbait(self, text: str) -> float:
        """Detect clickbait patterns"""
        text_lower = text.lower()
        matches = sum(1 for word in self.clickbait_words if word in text_lower)
        return min(matches / 2.0, 1.0)
    
    def _detect_urgency(self, text: str) -> float:
        """Detect urgency markers"""
        text_lower = text.lower()
        matches = sum(1 for marker in self.urgency_markers if marker in text_lower)
        
        # Also check for excessive punctuation
        exclamations = text.count('!')
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        urgency_score = min(matches / 2.0 + exclamations / 10.0 + caps_ratio, 1.0)
        return urgency_score
    
    def _detect_emotional_manipulation(self, text: str) -> float:
        """Detect fear, anger, and emotional triggers"""
        fear_words = ['danger', 'threat', 'warning', 'scary', 'terrifying', 'deadly']
        anger_words = ['outrage', 'betrayal', 'corruption', 'scandal', 'attack']
        
        text_lower = text.lower()
        fear_count = sum(1 for word in fear_words if word in text_lower)
        anger_count = sum(1 for word in anger_words if word in text_lower)
        
        emotion_score = min((fear_count + anger_count) / 3.0, 1.0)
        return emotion_score
    
    async def _gpt4_analysis(self, text: str) -> Dict:
        """Advanced analysis using GPT-4"""
        try:
            prompt = f"""Analyze this social media post for misinformation:

"{text}"

Provide:
1. Fake probability (0-1)
2. Key claims made
3. Logical consistency issues
4. Signs of AI-generated content

Respond in JSON format."""

            # Use Groq with Llama 3 (faster and free!)
            response = await asyncio.to_thread(
                self.groq_client.chat.completions.create,
                model="llama-3.1-70b-versatile",  # Fast and accurate
                messages=[
                    {"role": "system", "content": "You are a fact-checking expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024
            )
            
            # Parse response (simplified - add proper JSON parsing)
            content = response.choices[0].message.content
            
            return {
                'fake_score': 0.6,  # Placeholder - parse from GPT-4 response
                'insights': content,
                'claims': []  # Extract claims from response
            }
        except Exception as e:
            logger.error(f"GPT-4 analysis error: {e}")
            return {'fake_score': 0.5, 'insights': '', 'claims': []}
    
    async def _analyze_images(self, images: List[str]) -> Dict:
        """
        Image analysis: deepfake detection, forensics, object detection
        """
        # Placeholder for actual implementation
        # In production: Use EfficientNet, ELA, EXIF analysis
        
        return {
            'image_fake_probability': 0.5,
            'deepfake_detected': False,
            'manipulation_detected': False,
            'reverse_search_results': []
        }
    
    async def _analyze_videos(self, videos: List[str]) -> Dict:
        """
        Video analysis: frame extraction, temporal consistency, lip-sync
        """
        # Placeholder for actual implementation
        # In production: Use Wav2Lip, frame-by-frame CNN analysis
        
        return {
            'video_fake_probability': 0.5,
            'lipsync_inconsistency': False,
            'temporal_inconsistency': False
        }
    
    async def _cross_modal_verification(
        self,
        text_analysis: Dict,
        image_analysis: Optional[Dict],
        video_analysis: Optional[Dict]
    ) -> float:
        """
        Verify consistency between text claims and visual content
        """
        # Placeholder - implement CLIP-based verification
        return 0.0
    
    def _aggregate_scores(
        self,
        text_analysis: Dict,
        image_analysis: Optional[Dict],
        video_analysis: Optional[Dict],
        cross_modal_score: float
    ) -> Dict:
        """
        Aggregate all analysis scores into final classification
        """
        # Weighted ensemble
        weights = {'text': 0.4, 'image': 0.3, 'video': 0.2, 'cross_modal': 0.1}
        
        text_score = text_analysis['text_fake_probability']
        image_score = image_analysis['image_fake_probability'] if image_analysis else 0.5
        video_score = video_analysis['video_fake_probability'] if video_analysis else 0.5
        
        # Only weight media if present
        if not image_analysis and not video_analysis:
            final_prob = text_score
        else:
            final_prob = (
                weights['text'] * text_score +
                weights['image'] * image_score +
                weights['video'] * video_score +
                weights['cross_modal'] * cross_modal_score
            )
        
        classification = 'FAKE' if final_prob >= self.fake_threshold else 'REAL'
        confidence = 'HIGH' if abs(final_prob - 0.5) > 0.3 else 'MEDIUM' if abs(final_prob - 0.5) > 0.15 else 'LOW'
        
        # Generate reason
        reasons = []
        if text_analysis.get('clickbait_detected'):
            reasons.append("Clickbait language detected")
        if text_analysis.get('urgency_detected'):
            reasons.append("Urgency markers present")
        if image_analysis and image_analysis.get('manipulation_detected'):
            reasons.append("Image manipulation detected")
        
        reason = " + ".join(reasons) if reasons else "Multiple weak signals"
        
        return {
            'fake_probability': final_prob,
            'classification': classification,
            'confidence': confidence,
            'reason': reason,
            'text_analysis': text_analysis,
            'image_analysis': image_analysis,
            'video_analysis': video_analysis
        }
    
    def _error_report(self, content: Dict) -> Dict:
        """Return error report if analysis fails"""
        return {
            'content_id': content.get('content_id'),
            'fake_probability': 0.5,
            'classification': 'UNKNOWN',
            'confidence': 'LOW',
            'reason': 'Analysis error occurred',
            'error': True
        }
