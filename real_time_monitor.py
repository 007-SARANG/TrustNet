"""
TrustNet 2.0 - Real-Time Social Media Monitor
Collects and analyzes posts from multiple platforms in real-time
"""

import asyncio
import logging
from typing import Dict, List
import os
from dotenv import load_dotenv

# Import collectors
try:
    from agents.collectors.twitter_collector import TwitterCollector
except:
    TwitterCollector = None

try:
    from agents.collectors.reddit_collector import RedditCollector
except:
    RedditCollector = None

from agents.collectors.rss_collector import RSSCollector

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
)
logger = logging.getLogger(__name__)


class RealTimeMonitor:
    """Orchestrates real-time collection and analysis from multiple platforms"""
    
    def __init__(self, socketio_instance=None):
        self.sio = socketio_instance
        self.collectors = {}
        self.analyzed_posts = []
        
        # Initialize available collectors
        self._init_twitter()
        self._init_reddit()
        self._init_rss()
        
        logger.info("🚀 Real-Time Monitor initialized")
        logger.info(f"   Active platforms: {list(self.collectors.keys())}")
    
    
    def _init_twitter(self):
        """Initialize Twitter collector if credentials available"""
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_SECRET")
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        if all([api_key, api_secret, bearer_token]):
            try:
                self.collectors['twitter'] = TwitterCollector(
                    api_key=api_key,
                    api_secret=api_secret,
                    bearer_token=bearer_token
                )
                logger.info("✅ Twitter collector ready")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Twitter: {e}")
        else:
            logger.warning("⚠️  Twitter API credentials not configured")
            logger.info("   Add to .env: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_BEARER_TOKEN")
    
    
    def _init_reddit(self):
        """Initialize Reddit collector if credentials available"""
        if not RedditCollector:
            return
            
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        
        if all([client_id, client_secret]):
            try:
                self.collectors['reddit'] = RedditCollector(
                    client_id=client_id,
                    client_secret=client_secret
                )
                logger.info("✅ Reddit collector ready")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Reddit: {e}")
        else:
            logger.warning("⚠️  Reddit API credentials not configured")
            logger.info("   Add to .env: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET")
    
    
    def _init_rss(self):
        """Initialize RSS collector (always available, no API needed)"""
        try:
            self.collectors['rss'] = RSSCollector()
            logger.info("✅ RSS collector ready (FREE, unlimited)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize RSS: {e}")
    
    
    async def analyze_post(self, post: Dict) -> Dict:
        """Analyze a collected post for misinformation"""
        
        platform = post['platform']
        content = post.get('text') or post.get('title', '')
        
        logger.info("="*80)
        logger.info(f"📝 ANALYZING {platform.upper()} POST")
        logger.info(f"   ID: {post['id']}")
        logger.info(f"   Author: @{post['author']['username']}")
        logger.info(f"   Content: {content[:100]}...")
        logger.info("="*80)
        
        # Simple keyword-based detection for demo
        fake_keywords = [
            'miracle', 'shocking', 'doctors hate', 'cure', 'breaking',
            'unbelievable', 'secret', 'they dont want you to know',
            'banned', 'censored', 'wake up', 'sheep'
        ]
        
        content_lower = content.lower()
        suspicious_count = sum(1 for keyword in fake_keywords if keyword in content_lower)
        is_suspicious = suspicious_count >= 2
        
        # Calculate risk score
        risk_score = min(suspicious_count * 0.25, 0.95)
        
        result = {
            **post,
            'analysis': {
                'is_suspicious': is_suspicious,
                'risk_score': risk_score,
                'classification': 'FAKE' if is_suspicious else 'REAL',
                'confidence': 0.85 if is_suspicious else 0.92,
                'red_flags': suspicious_count,
                'timestamp': post['created_at']
            }
        }
        
        # Log result
        logger.info(f"✅ ANALYSIS COMPLETE")
        logger.info(f"   Classification: {result['analysis']['classification']}")
        logger.info(f"   Risk Score: {risk_score:.0%}")
        logger.info(f"   Red Flags: {suspicious_count}")
        logger.info("="*80 + "\n")
        
        # Send to dashboard via WebSocket
        if self.sio:
            await self.sio.emit('new_post', {
                'platform': platform,
                'content': content[:200],
                'author': post['author']['username'],
                'classification': result['analysis']['classification'],
                'risk_score': risk_score,
                'url': post.get('url') or post.get('reddit_url'),
                'metrics': post.get('metrics', {})
            })
        
        self.analyzed_posts.append(result)
        return result
    
    
    async def collect_twitter(self):
        """Collect tweets continuously"""
        if 'twitter' not in self.collectors:
            return
        
        collector = self.collectors['twitter']
        
        while True:
            try:
                logger.info("🐦 Fetching tweets...")
                tweets = collector.search_recent_tweets(max_results=10)
                
                for tweet in tweets:
                    await self.analyze_post(tweet)
                
                # Wait 2 minutes (Twitter rate limits)
                await asyncio.sleep(120)
                
            except Exception as e:
                logger.error(f"❌ Twitter collection error: {e}")
                await asyncio.sleep(120)
    
    
    async def collect_reddit(self):
        """Collect Reddit posts continuously"""
        if 'reddit' not in self.collectors:
            return
        
        collector = self.collectors['reddit']
        seen_ids = set()
        
        while True:
            try:
                logger.info("🤖 Fetching Reddit posts...")
                posts = collector.get_new_posts(limit=10)
                
                # Only analyze new posts
                new_posts = [p for p in posts if p['id'] not in seen_ids]
                
                for post in new_posts:
                    seen_ids.add(post['id'])
                    await self.analyze_post(post)
                
                # Keep seen_ids manageable
                if len(seen_ids) > 1000:
                    seen_ids = set(list(seen_ids)[-500:])
                
                # Wait 1 minute
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"❌ Reddit collection error: {e}")
                await asyncio.sleep(60)
    
    
    async def start(self):
        """Start monitoring all configured platforms"""
        
        if not self.collectors:
            logger.error("❌ No collectors configured! Add API credentials to .env")
            return
        
        logger.info("="*80)
        logger.info("🚀 STARTING REAL-TIME MONITORING")
        logger.info(f"   Platforms: {', '.join(self.collectors.keys())}")
        logger.info("="*80)
        
        # Start all collectors concurrently
        tasks = []
        
        if 'twitter' in self.collectors:
            tasks.append(asyncio.create_task(self.collect_twitter()))
        
        if 'reddit' in self.collectors:
            tasks.append(asyncio.create_task(self.collect_reddit()))
        
        if 'rss' in self.collectors:
            tasks.append(asyncio.create_task(self.collect_rss()))
        
        # Run forever
        await asyncio.gather(*tasks)
    
    
    async def collect_rss(self):
        """Collect RSS posts continuously"""
        if 'rss' not in self.collectors:
            return
        
        collector = self.collectors['rss']
        seen_ids = set()
        
        while True:
            try:
                logger.info("📰 Fetching RSS posts...")
                posts = collector.get_recent_posts(limit=10)
                
                # Only analyze new posts
                new_posts = [p for p in posts if p['id'] not in seen_ids]
                
                for post in new_posts:
                    seen_ids.add(post['id'])
                    await self.analyze_post(post)
                
                # Keep seen_ids manageable
                if len(seen_ids) > 1000:
                    seen_ids = set(list(seen_ids)[-500:])
                
                # Wait 5 minutes (RSS feeds update slowly)
                await asyncio.sleep(300)
                
            except Exception as e:
                logger.error(f"❌ RSS collection error: {e}")
                await asyncio.sleep(300)


# Standalone mode for testing
if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("🚀 TrustNet 2.0 - Real-Time Social Media Monitor")
    print("="*80)
    print("\n📋 Checking API credentials...")
    
    # Check what APIs are configured
    configured = []
    missing = []
    
    if all([os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"), os.getenv("TWITTER_BEARER_TOKEN")]):
        configured.append("✅ Twitter")
    else:
        missing.append("❌ Twitter")
    
    if all([os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET")]):
        configured.append("✅ Reddit")
    else:
        missing.append("❌ Reddit")
    
    print("\nConfigured APIs:")
    for api in configured:
        print(f"  {api}")
    
    if missing:
        print("\nMissing APIs:")
        for api in missing:
            print(f"  {api}")
        print("\n💡 See REQUIRED_APIS.md for setup instructions")
    
    if not configured:
        print("\n❌ No APIs configured! Cannot start monitoring.")
        print("\n📖 Read REQUIRED_APIS.md to get started")
        exit(1)
    
    print("\n" + "="*80)
    print("🎬 Starting real-time monitoring...")
    print("="*80)
    
    # Create and start monitor
    monitor = RealTimeMonitor()
    
    try:
        asyncio.run(monitor.start())
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped")
        print(f"📊 Total posts analyzed: {len(monitor.analyzed_posts)}")
