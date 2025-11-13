"""
TrustNet 2.0 - RSS Feed Collector
Monitors news sites via RSS feeds (100% FREE, no API needed)
"""

import feedparser
import logging
from typing import List, Dict
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class RSSCollector:
    """Collect posts from RSS feeds (news sites, blogs, etc.)"""
    
    def __init__(self, feeds: List[str] = None):
        # Popular news RSS feeds (EXPANDED LIST!)
        self.feeds = feeds or [
            # Major News
            "http://feeds.bbci.co.uk/news/rss.xml",  # BBC News
            "http://rss.cnn.com/rss/cnn_topstories.rss",  # CNN
            "https://feeds.reuters.com/reuters/topNews",  # Reuters
            "https://www.aljazeera.com/xml/rss/all.xml",  # Al Jazeera
            "https://feeds.npr.org/1001/rss.xml",  # NPR News
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",  # New York Times
            
            # Tech News
            "https://www.theverge.com/rss/index.xml",  # The Verge
            "https://techcrunch.com/feed/",  # TechCrunch
            "https://www.wired.com/feed/rss",  # Wired
            "https://feeds.arstechnica.com/arstechnica/index",  # Ars Technica
            
            # Health/Science
            "https://www.sciencedaily.com/rss/all.xml",  # Science Daily
            "https://www.medicalnewstoday.com/rss/news.xml",  # Medical News
            "https://www.sciencenews.org/feed",  # Science News
            
            # Politics
            "https://www.politico.com/rss/politics08.xml",  # Politico
            "https://thehill.com/feed/",  # The Hill
            
            # Business
            "https://feeds.bloomberg.com/markets/news.rss",  # Bloomberg
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",  # CNBC
        ]
        
        logger.info(f"📰 RSS Collector initialized")
        logger.info(f"   Monitoring {len(self.feeds)} feeds")
    
    
    def get_recent_posts(self, limit: int = 10) -> List[Dict]:
        """Get recent posts from all RSS feeds"""
        
        all_posts = []
        
        for feed_url in self.feeds:
            try:
                logger.info(f"🔍 Fetching feed: {feed_url}")
                
                feed = feedparser.parse(feed_url)
                
                if feed.bozo:
                    logger.warning(f"⚠️  Error parsing feed: {feed_url}")
                    continue
                
                feed_name = feed.feed.get('title', 'Unknown')
                
                for entry in feed.entries[:limit]:
                    post_data = {
                        'id': entry.get('id', entry.get('link', str(time.time()))),
                        'title': entry.get('title', 'No title'),
                        'text': entry.get('summary', entry.get('description', '')),
                        'url': entry.get('link', ''),
                        'created_at': self._parse_date(entry.get('published', entry.get('updated', ''))),
                        'author': {
                            'username': entry.get('author', feed_name),
                            'verified': True  # RSS feeds are from verified sources
                        },
                        'source': feed_name,
                        'platform': 'rss',
                        'metrics': {
                            'score': 0,  # RSS doesn't have engagement metrics
                            'comments': 0
                        }
                    }
                    
                    all_posts.append(post_data)
                    
                    # Log post
                    logger.info("="*80)
                    logger.info(f"📰 NEW RSS POST COLLECTED")
                    logger.info(f"   Source: {feed_name}")
                    logger.info(f"   Title: {entry.get('title', '')[:80]}...")
                    logger.info(f"   URL: {entry.get('link', '')}")
                    logger.info("="*80)
                
                logger.info(f"✅ Collected {len(feed.entries[:limit])} posts from {feed_name}")
                
            except Exception as e:
                logger.error(f"❌ Error fetching feed {feed_url}: {e}")
                continue
        
        logger.info(f"✅ Total collected: {len(all_posts)} posts from {len(self.feeds)} feeds")
        return all_posts
    
    
    def _parse_date(self, date_string: str) -> str:
        """Parse date from RSS feed"""
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_string)
            return dt.isoformat()
        except:
            return datetime.now().isoformat()
    
    
    def stream_posts(self, on_post_callback, check_interval: int = 300):
        """Monitor feeds continuously (check every 5 minutes)"""
        
        logger.info(f"📡 Starting RSS stream (checking every {check_interval}s)")
        seen_ids = set()
        
        while True:
            try:
                posts = self.get_recent_posts(limit=5)
                
                # Only process unseen posts
                new_posts = [p for p in posts if p['id'] not in seen_ids]
                
                for post in new_posts:
                    seen_ids.add(post['id'])
                    on_post_callback(post)
                
                if new_posts:
                    logger.info(f"📬 Processed {len(new_posts)} new posts")
                
                # Keep seen_ids from growing too large
                if len(seen_ids) > 1000:
                    seen_ids = set(list(seen_ids)[-500:])
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("⏹️  Stopped RSS stream")
                break
            except Exception as e:
                logger.error(f"❌ Error in stream: {e}")
                time.sleep(check_interval)


# Example usage
if __name__ == "__main__":
    import os
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    # Create collector
    collector = RSSCollector()
    
    # Get recent posts
    print("\n🔍 Fetching recent news posts...")
    posts = collector.get_recent_posts(limit=5)
    
    print(f"\n✅ Found {len(posts)} posts!")
    
    for i, post in enumerate(posts, 1):
        print(f"\n{i}. {post['source']}")
        print(f"   {post['title'][:80]}...")
        print(f"   🔗 {post['url']}")
