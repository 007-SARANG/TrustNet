"""
Instagram Image Collector with Offline AI Analysis
Detects informative images, generates comparisons using local models
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib

# Image processing
from PIL import Image
import requests
from io import BytesIO

# Instagram scraping (optional)
try:
    import instaloader
    INSTALOADER_AVAILABLE = True
except ImportError:
    INSTALOADER_AVAILABLE = False

# Local AI Models
try:
    import torch
    from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("⚠️ Install transformers and torch for full functionality")

# Optional: Stable Diffusion (not required for CLIP)
try:
    from diffusers import StableDiffusionPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

logger = logging.getLogger(__name__)


class InstagramImageAnalyzer:
    """Offline image analysis using local AI models"""
    
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Initialize models
        self.clip_model = None
        self.clip_processor = None
        self.sd_pipeline = None
        
        if MODELS_AVAILABLE:
            self._load_models()
    
    def _load_models(self):
        """Load CLIP and Stable Diffusion models for offline use"""
        try:
            logger.info("📦 Loading CLIP model for image-text similarity...")
            self.clip_model = CLIPModel.from_pretrained(
                "openai/clip-vit-base-patch32",
                cache_dir=str(self.models_dir)
            )
            self.clip_processor = CLIPProcessor.from_pretrained(
                "openai/clip-vit-base-patch32",
                cache_dir=str(self.models_dir)
            )
            logger.info("✅ CLIP model loaded")
            
            # Optional: Load Stable Diffusion for image generation
            # logger.info("📦 Loading Stable Diffusion for image generation...")
            # self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
            #     "runwayml/stable-diffusion-v1-5",
            #     cache_dir=str(self.models_dir),
            #     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            # )
            # self.sd_pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
            # logger.info("✅ Stable Diffusion loaded")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
    
    def classify_informative(self, image: Image.Image, caption: str) -> Dict:
        """
        Classify if image and caption are informative using CLIP
        
        Returns:
            Dict with classification results
        """
        if not MODELS_AVAILABLE or not self.clip_model:
            logger.warning("⚠️ CLIP models not available - using fallback classification")
            return {
                'is_informative': True,
                'category': 'unknown',
                'confidence': 0.5,
                'reasoning': 'Models not available - defaulting to informative (install transformers, torch for AI classification)',
                'scores': {
                    'informative': 0.5,
                    'entertainment': 0.25,
                    'advertisement': 0.15,
                    'misinformation': 0.1
                }
            }
        
        try:
            # Define informative vs non-informative labels
            labels = [
                "educational content, informative, news, facts, data, statistics",
                "entertainment, meme, selfie, personal photo, casual content",
                "advertisement, promotional, marketing, sponsored content",
                "misinformation, fake news, misleading content"
            ]
            
            # Prepare inputs
            inputs = self.clip_processor(
                text=labels,
                images=image,
                return_tensors="pt",
                padding=True
            )
            
            # Get predictions
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
            
            # Analyze results
            probs_list = probs[0].tolist()
            informative_score = probs_list[0]
            entertainment_score = probs_list[1]
            ad_score = probs_list[2]
            misinfo_score = probs_list[3]
            
            # Classification logic
            is_informative = informative_score > 0.35 and misinfo_score < 0.3
            confidence = informative_score
            
            # Determine reasoning and category
            if misinfo_score > 0.4:
                category = "misinformation"
                reasoning = "Potentially misleading content detected"
            elif ad_score > 0.5:
                category = "advertisement"
                reasoning = "Advertisement/promotional content"
            elif entertainment_score > 0.5:
                category = "entertainment"
                reasoning = "Entertainment/casual content"
            elif informative_score > 0.4:
                category = "informative"
                reasoning = "Educational/informative content"
            else:
                category = "mixed"
                reasoning = "Mixed content type"
            
            return {
                'is_informative': is_informative,
                'category': category,
                'confidence': float(confidence),
                'reasoning': reasoning,
                'scores': {
                    'informative': float(informative_score),
                    'entertainment': float(entertainment_score),
                    'advertisement': float(ad_score),
                    'misinformation': float(misinfo_score)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Classification error: {e}")
            return {
                'is_informative': True,
                'category': 'unknown',
                'confidence': 0.5,
                'reasoning': f'Error during classification: {str(e)}',
                'scores': {
                    'informative': 0.5,
                    'entertainment': 0.25,
                    'advertisement': 0.15,
                    'misinformation': 0.1
                }
            }
    
    def verify_image_caption_match(self, image: Image.Image, caption: str) -> Dict:
        """
        Check if image content matches the caption (KEY MISINFORMATION DETECTOR)
        Example: If caption says "BMW car" but image shows a cat -> MISMATCH!
        
        Returns:
            Dict with match score and detailed analysis
        """
        if not MODELS_AVAILABLE or not self.clip_model:
            logger.warning("⚠️ CLIP models not available - cannot verify image-caption match")
            return {
                'similarity': 0.5,
                'matches': True,
                'confidence': 0.0,
                'reasoning': 'Models not available - install transformers and torch for verification'
            }
        
        try:
            # Prepare inputs for CLIP
            inputs = self.clip_processor(
                text=[caption],
                images=image,
                return_tensors="pt",
                padding=True
            )
            
            # Get image-text similarity
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                
                # Get the image and text embeddings
                image_embeds = outputs.image_embeds
                text_embeds = outputs.text_embeds
                
                # Normalize embeddings to unit vectors
                image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
                text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)
                
                # Calculate cosine similarity (dot product of normalized vectors)
                # This gives us a value between -1 and 1, where 1 is perfect match
                similarity_score = (image_embeds @ text_embeds.T).item()
                
                # Normalize to 0-1 range for easier interpretation
                # cosine similarity of -1 to 1 becomes 0 to 1
                similarity_score = (similarity_score + 1) / 2
            
            # Determine if they match
            # Cosine similarity interpretation: >0.75 = strong match, 0.6-0.75 = moderate, <0.6 = mismatch
            matches = similarity_score > 0.6  # Threshold for matching
            confidence = float(similarity_score)
            
            # Detailed reasoning
            if similarity_score > 0.75:
                reasoning = "✅ Strong match: Image content aligns well with caption"
                mismatch_type = None
            elif similarity_score > 0.6:
                reasoning = "⚠️ Moderate match: Some alignment between image and caption"
                mismatch_type = None
            else:
                reasoning = "🚨 MISMATCH DETECTED: Image content does NOT match caption!"
                mismatch_type = "image_caption_mismatch"
            
            return {
                'similarity': float(similarity_score),
                'matches': matches,
                'confidence': confidence,
                'reasoning': reasoning,
                'mismatch_type': mismatch_type
            }
            
        except Exception as e:
            logger.error(f"❌ Image-caption verification error: {e}")
            return {
                'similarity': 0.5,
                'matches': True,
                'confidence': 0.0,
                'reasoning': f'Error during verification: {str(e)}',
                'mismatch_type': None
            }
    
    def compare_images(self, image1: Image.Image, image2: Image.Image, caption: str) -> Dict:
        """
        Compare two images using CLIP embeddings
        
        Returns:
            Dict with similarity score and analysis
        """
        if not MODELS_AVAILABLE or not self.clip_model:
            return {
                'similarity': 0.5,
                'match': 'unknown',
                'reasoning': 'Models not available'
            }
        
        try:
            # Get image embeddings
            inputs1 = self.clip_processor(images=image1, return_tensors="pt")
            inputs2 = self.clip_processor(images=image2, return_tensors="pt")
            
            with torch.no_grad():
                image1_features = self.clip_model.get_image_features(**inputs1)
                image2_features = self.clip_model.get_image_features(**inputs2)
                
                # Normalize features
                image1_features = image1_features / image1_features.norm(dim=-1, keepdim=True)
                image2_features = image2_features / image2_features.norm(dim=-1, keepdim=True)
                
                # Calculate cosine similarity
                similarity = (image1_features @ image2_features.T).item()
            
            # Determine match level
            if similarity > 0.85:
                match = 'high'
                reasoning = "Images are very similar"
            elif similarity > 0.70:
                match = 'medium'
                reasoning = "Images have significant similarities"
            elif similarity > 0.50:
                match = 'low'
                reasoning = "Images have some similarities"
            else:
                match = 'none'
                reasoning = "Images are quite different"
            
            return {
                'similarity': float(similarity),
                'match': match,
                'reasoning': reasoning
            }
            
        except Exception as e:
            logger.error(f"❌ Comparison error: {e}")
            return {
                'similarity': 0.0,
                'match': 'error',
                'reasoning': f'Error during comparison: {str(e)}'
            }
    
    def generate_image_from_caption(self, caption: str) -> Optional[Image.Image]:
        """Generate image from caption using Stable Diffusion (if available)"""
        if not self.sd_pipeline:
            logger.warning("⚠️ Stable Diffusion not loaded - cannot generate images")
            return None
        
        try:
            logger.info(f"🎨 Generating image for: {caption[:50]}...")
            image = self.sd_pipeline(
                caption,
                num_inference_steps=30,
                guidance_scale=7.5
            ).images[0]
            
            logger.info("✅ Image generated successfully")
            return image
            
        except Exception as e:
            logger.error(f"❌ Image generation error: {e}")
            return None


class InstagramCollector:
    """
    Instagram post collector with image analysis
    Supports multiple sources:
    1. Manual image paths/URLs (simulated)
    2. Instaloader (unofficial scraper)
    3. Instagram Graph API (official, requires setup)
    """
    
    def __init__(self, samples_dir: str = "./data/instagram_samples", instagram_username: str = None, instagram_password: str = None):
        self.samples_dir = Path(samples_dir)
        self.samples_dir.mkdir(parents=True, exist_ok=True)
        
        self.analyzer = InstagramImageAnalyzer()
        self.flagged_posts = []
        
        # Instaloader setup (optional)
        self.loader = None
        if INSTALOADER_AVAILABLE and (instagram_username or instagram_password):
            try:
                self.loader = instaloader.Instaloader()
                if instagram_username and instagram_password:
                    self.loader.login(instagram_username, instagram_password)
                    logger.info("✅ Logged into Instagram via Instaloader")
            except Exception as e:
                logger.warning(f"⚠️ Instaloader login failed: {e}")
                self.loader = instaloader.Instaloader()  # Continue without login
        
    def fetch_sample_post(self, image_path: str, caption: str) -> Dict:
        """
        Simulate fetching an Instagram post
        In production, this would use Instagram API
        """
        try:
            # Load image
            if image_path.startswith('http'):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path)
            
            # Generate post ID
            post_id = hashlib.md5(f"{image_path}{caption}".encode()).hexdigest()[:16]
            
            return {
                'id': post_id,
                'platform': 'instagram',
                'image': image,
                'image_path': image_path,
                'caption': caption,
                'author': {'username': 'sample_user'},
                'created_at': datetime.now().isoformat(),
                'metrics': {
                    'likes': 0,
                    'comments': 0,
                    'shares': 0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching post: {e}")
            return None
    
    def fetch_from_instagram(self, profile_name: str, max_posts: int = 10) -> List[Dict]:
        """
        Fetch real posts from Instagram using Instaloader
        
        Args:
            profile_name: Instagram username/profile
            max_posts: Maximum number of posts to fetch
            
        Returns:
            List of post dictionaries
        """
        if not INSTALOADER_AVAILABLE:
            logger.error("❌ Instaloader not installed. Run: pip install instaloader")
            return []
        
        if not self.loader:
            self.loader = instaloader.Instaloader()
        
        try:
            logger.info(f"📸 Fetching posts from @{profile_name}...")
            profile = instaloader.Profile.from_username(self.loader.context, profile_name)
            
            posts = []
            for idx, post in enumerate(profile.get_posts()):
                if idx >= max_posts:
                    break
                
                # Skip videos
                if post.is_video:
                    continue
                
                # Download image
                image_url = post.url
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                
                # Create post dict
                post_data = {
                    'id': post.shortcode,
                    'platform': 'instagram',
                    'image': image,
                    'image_path': image_url,
                    'caption': post.caption or '',
                    'author': {'username': profile_name},
                    'created_at': post.date_utc.isoformat(),
                    'metrics': {
                        'likes': post.likes,
                        'comments': post.comments,
                        'shares': 0
                    },
                    'url': f"https://instagram.com/p/{post.shortcode}/"
                }
                
                posts.append(post_data)
                logger.info(f"✅ Fetched post {idx+1}/{max_posts}: {post.shortcode}")
            
            logger.info(f"📊 Successfully fetched {len(posts)} posts from @{profile_name}")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Error fetching from Instagram: {e}")
            return []
    
    def fetch_specific_post(self, post_url: str) -> Optional[Dict]:
        """
        Fetch a specific Instagram post by URL
        
        Args:
            post_url: Full Instagram post URL (e.g., https://instagram.com/p/ABC123/)
            
        Returns:
            Post dictionary or None
        """
        if not INSTALOADER_AVAILABLE:
            logger.error("❌ Instaloader not installed. Run: pip install instaloader")
            return None
        
        if not self.loader:
            self.loader = instaloader.Instaloader()
        
        try:
            # Extract shortcode from URL
            shortcode = post_url.split('/p/')[-1].strip('/')
            
            logger.info(f"📸 Fetching specific post: {shortcode}...")
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            
            # Skip videos
            if post.is_video:
                logger.warning("⚠️ Post is a video, skipping...")
                return None
            
            # Download image
            response = requests.get(post.url)
            image = Image.open(BytesIO(response.content))
            
            post_data = {
                'id': post.shortcode,
                'platform': 'instagram',
                'image': image,
                'image_path': post.url,
                'caption': post.caption or '',
                'author': {'username': post.owner_username},
                'created_at': post.date_utc.isoformat(),
                'metrics': {
                    'likes': post.likes,
                    'comments': post.comments,
                    'shares': 0
                },
                'url': f"https://instagram.com/p/{post.shortcode}/"
            }
            
            logger.info(f"✅ Successfully fetched post: {shortcode}")
            return post_data
            
        except Exception as e:
            logger.error(f"❌ Error fetching specific post: {e}")
            logger.info("💡 Tip: Instagram may be blocking direct post requests. Use fetch_from_instagram() instead.")
            return None
    
    def analyze_post(self, post: Dict) -> Dict:
        """
        Full analysis pipeline for Instagram post
        1. Verify image-caption match (CRITICAL for misinformation detection)
        2. Classify if informative
        3. Generate comparison image (optional)
        4. Compare images
        5. Apply prevention rules
        """
        image = post['image']
        caption = post['caption']
        
        logger.info(f"🔍 Analyzing Instagram post: {caption[:50]}...")
        
        # Step 1: VERIFY IMAGE-CAPTION MATCH (KEY FEATURE!)
        image_caption_match = self.analyzer.verify_image_caption_match(image, caption)
        logger.info(f"📊 Image-Caption Match: {image_caption_match['similarity']:.2f} - {image_caption_match['reasoning']}")
        
        # Step 2: Classify if informative
        classification = self.analyzer.classify_informative(image, caption)
        
        # Step 3 & 4: Generate and compare (optional)
        generated_image = None
        comparison = None
        if self.analyzer.sd_pipeline:
            generated_image = self.analyzer.generate_image_from_caption(caption)
            if generated_image:
                comparison = self.analyzer.compare_images(image, generated_image, caption)
        
        # Step 5: Prevention algorithm (includes image-caption match check)
        prevention_result = self._apply_prevention_rules(classification, comparison, image_caption_match)
        
        # Compile results
        analysis = {
            'post_id': post['id'],
            'image_caption_match': image_caption_match,  # NEW: Key misinformation indicator
            'classification': classification,
            'comparison': comparison,
            'prevention': prevention_result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Log if flagged
        if prevention_result['flagged']:
            self.flagged_posts.append(analysis)
            logger.warning(f"🚨 POST FLAGGED: {prevention_result['reason']}")
        
        # Special log for image-caption mismatch
        if not image_caption_match.get('matches', True):
            logger.error(f"🚨 IMAGE-CAPTION MISMATCH: {image_caption_match['reasoning']}")
        
        return analysis
    
    def _apply_prevention_rules(self, classification: Dict, comparison: Optional[Dict], image_caption_match: Optional[Dict] = None) -> Dict:
        """
        Business rules for flagging/blocking non-informative content
        """
        flagged = False
        reasons = []
        rules_triggered = []
        action = "allow"
        
        # Rule 0: IMAGE-CAPTION MISMATCH (HIGHEST PRIORITY - CRITICAL FOR MISINFORMATION!)
        if image_caption_match and not image_caption_match.get('matches', True):
            flagged = True
            mismatch_severity = 1.0 - image_caption_match.get('similarity', 0.5)
            if mismatch_severity > 0.7:
                reasons.append(f"🚨 CRITICAL MISMATCH: Image does NOT match caption! (Similarity: {image_caption_match.get('similarity', 0):.2f})")
                rules_triggered.append("Rule 0: Critical image-caption mismatch (MISINFORMATION)")
                action = "block"
            else:
                reasons.append(f"⚠️ Image-caption mismatch detected (Similarity: {image_caption_match.get('similarity', 0):.2f})")
                rules_triggered.append("Rule 0: Image-caption mismatch")
                action = "review"
        
        # Rule 1: High misinformation score
        if classification.get('scores', {}).get('misinformation', 0) > 0.5:
            flagged = True
            reasons.append("High misinformation probability")
            rules_triggered.append("Rule 1: Misinformation > 0.5")
            if action != "block":
                action = "block"
        
        # Rule 2: Low informative score
        if not classification.get('is_informative', True):
            if classification.get('confidence', 0) < 0.3:
                flagged = True
                reasons.append("Low informative value")
                rules_triggered.append("Rule 2: Low informative score")
                if action == "allow":
                    action = "review"
        
        # Rule 3: Advertisement content
        if classification.get('scores', {}).get('advertisement', 0) > 0.6:
            flagged = True
            reasons.append("Promotional content")
            rules_triggered.append("Rule 3: Advertisement > 0.6")
            if action == "allow":
                action = "flag"
        
        # Rule 4: Generated image comparison mismatch (if available)
        if comparison and comparison.get('similarity', 1.0) < 0.3:
            flagged = True
            reasons.append("Generated image comparison mismatch")
            rules_triggered.append("Rule 4: Generated image mismatch")
            if action == "allow":
                action = "review"
        
        return {
            'flagged': flagged,
            'reason': '; '.join(reasons) if reasons else "Content approved",
            'action': action,
            'rules_triggered': rules_triggered,
            'confidence': classification.get('confidence', 0.5)
        }
    
    def get_sample_posts(self) -> List[Dict]:
        """
        Get list of sample posts for testing
        Returns sample Instagram posts with images and captions
        """
        samples = [
            {
                'image_url': 'https://via.placeholder.com/600x600.png?text=Climate+Change+Data',
                'caption': 'New climate data shows 2025 temperature records. Key findings from latest research.'
            },
            {
                'image_url': 'https://via.placeholder.com/600x600.png?text=Selfie',
                'caption': 'Having a great day! #blessed #happy'
            },
            {
                'image_url': 'https://via.placeholder.com/600x600.png?text=Health+Tip',
                'caption': 'SHOCKING cure doctors don\'t want you to know! Buy now!'
            }
        ]
        
        posts = []
        for sample in samples:
            try:
                response = requests.get(sample['image_url'], timeout=5)
                image = Image.open(BytesIO(response.content))
                
                post = {
                    'id': hashlib.md5(sample['caption'].encode()).hexdigest()[:16],
                    'platform': 'instagram',
                    'image': image,
                    'image_path': sample['image_url'],
                    'caption': sample['caption'],
                    'author': {'username': 'sample_user'},
                    'created_at': datetime.now().isoformat(),
                    'metrics': {'likes': 0, 'comments': 0, 'shares': 0}
                }
                posts.append(post)
            except Exception as e:
                logger.error(f"Error loading sample: {e}")
        
        return posts
    
    def save_analysis_log(self, analyses: List[Dict], output_path: str = "./instagram_analysis_log.json"):
        """Save analysis results to JSON log"""
        try:
            with open(output_path, 'w') as f:
                json.dump(analyses, f, indent=2, default=str)
            logger.info(f"📝 Analysis log saved to {output_path}")
        except Exception as e:
            logger.error(f"❌ Error saving log: {e}")


def main():
    """Test the Instagram collector"""
    logging.basicConfig(level=logging.INFO)
    
    collector = InstagramCollector()
    
    logger.info("🚀 Starting Instagram Image Analysis Test")
    logger.info("=" * 60)
    
    # Get sample posts
    posts = collector.get_sample_posts()
    
    # Analyze each post
    analyses = []
    for post in posts:
        logger.info(f"\n📸 Processing: {post['caption'][:50]}...")
        analysis = collector.analyze_post(post)
        analyses.append(analysis)
        
        # Print results
        logger.info(f"✅ Classification: {analysis['classification']['reasoning']}")
        logger.info(f"   Informative: {analysis['classification']['is_informative']}")
        logger.info(f"   Confidence: {analysis['classification']['confidence']:.2f}")
        logger.info(f"   Prevention: {analysis['prevention']['action']}")
    
    # Save results
    collector.save_analysis_log(analyses)
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 SUMMARY:")
    logger.info(f"   Total posts analyzed: {len(analyses)}")
    logger.info(f"   Posts flagged: {len(collector.flagged_posts)}")
    logger.info(f"   Log saved: instagram_analysis_log.json")


if __name__ == "__main__":
    main()
