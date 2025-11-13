"""
TrustNet 2.0 - Reddit Collector
Monitors Reddit in real-time for misinformation
"""

import praw
import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class RedditCollector:
    """Collect posts from Reddit in real-time"""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str = "TrustNet:v2.0 (by /u/your_username)",
        subreddits: List[str] = None
    ):
        self.subreddits = subreddits or [
            "news",
            "worldnews",
            "politics",
            "conspiracy",
            "CovidVaccinated",
            "skeptic"
        ]
        
        # Initialize Reddit API
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        logger.info(f"🤖 Reddit Collector initialized")
        logger.info(f"   Monitoring subreddits: {', '.join(self.subreddits)}")
    
    
    def get_hot_posts(self, limit: int = 10) -> List[Dict]:
        """Get hot/trending posts from monitored subreddits"""
        
        all_posts = []
        
        try:
            subreddit = self.reddit.subreddit('+'.join(self.subreddits))
            
            logger.info(f"🔍 Fetching hot posts from r/{'+'.join(self.subreddits)}")
            
            for submission in subreddit.hot(limit=limit):
                # Skip stickied posts
                if submission.stickied:
                    continue
                
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'url': submission.url,
                    'created_at': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'author': {
                        'username': str(submission.author) if submission.author else '[deleted]',
                        'verified': False  # Reddit doesn't have verification
                    },
                    'subreddit': submission.subreddit.display_name,
                    'metrics': {
                        'score': submission.score,
                        'upvote_ratio': submission.upvote_ratio,
                        'num_comments': submission.num_comments,
                        'awards': submission.total_awards_received
                    },
                    'platform': 'reddit',
                    'reddit_url': f"https://reddit.com{submission.permalink}"
                }
                
                all_posts.append(post_data)
                
                # Log post
                logger.info("="*80)
                logger.info(f"🤖 NEW REDDIT POST COLLECTED")
                logger.info(f"   ID: {submission.id}")
                logger.info(f"   Subreddit: r/{submission.subreddit.display_name}")
                logger.info(f"   Author: u/{post_data['author']['username']}")
                logger.info(f"   Title: {submission.title[:80]}...")
                logger.info(f"   Score: {submission.score} | "
                          f"Comments: {submission.num_comments} | "
                          f"Ratio: {submission.upvote_ratio:.0%}")
                logger.info("="*80)
            
            logger.info(f"✅ Collected {len(all_posts)} Reddit posts")
            return all_posts
            
        except Exception as e:
            logger.error(f"❌ Error collecting Reddit posts: {e}")
            return []
    
    
    def get_new_posts(self, limit: int = 10) -> List[Dict]:
        """Get newest posts (better for real-time monitoring)"""
        
        all_posts = []
        
        try:
            subreddit = self.reddit.subreddit('+'.join(self.subreddits))
            
            logger.info(f"🔍 Fetching new posts from r/{'+'.join(self.subreddits)}")
            
            for submission in subreddit.new(limit=limit):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'url': submission.url,
                    'created_at': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'author': {
                        'username': str(submission.author) if submission.author else '[deleted]',
                        'verified': False
                    },
                    'subreddit': submission.subreddit.display_name,
                    'metrics': {
                        'score': submission.score,
                        'upvote_ratio': submission.upvote_ratio,
                        'num_comments': submission.num_comments,
                        'awards': submission.total_awards_received
                    },
                    'platform': 'reddit',
                    'reddit_url': f"https://reddit.com{submission.permalink}"
                }
                
                all_posts.append(post_data)
                
                logger.info(f"🤖 r/{submission.subreddit.display_name}: {submission.title[:60]}...")
            
            logger.info(f"✅ Collected {len(all_posts)} new Reddit posts")
            return all_posts
            
        except Exception as e:
            logger.error(f"❌ Error collecting Reddit posts: {e}")
            return []
    
    
    def stream_posts(self, on_post_callback, check_interval: int = 60):
        """Monitor subreddits continuously"""
        
        import time
        
        logger.info(f"📡 Starting Reddit stream (checking every {check_interval}s)")
        seen_ids = set()
        
        while True:
            try:
                posts = self.get_new_posts(limit=25)
                
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
                logger.info("⏹️  Stopped Reddit stream")
                break
            except Exception as e:
                logger.error(f"❌ Error in stream: {e}")
                time.sleep(check_interval)


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    # Get API credentials from environment
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not all([client_id, client_secret]):
        print("❌ Missing Reddit API credentials!")
        print("\nAdd to your .env file:")
        print("REDDIT_CLIENT_ID=your_client_id")
        print("REDDIT_CLIENT_SECRET=your_client_secret")
        print("\nGet them from: https://www.reddit.com/prefs/apps")
        exit(1)
    
    # Create collector
    collector = RedditCollector(
        client_id=client_id,
        client_secret=client_secret,
        subreddits=["news", "worldnews", "conspiracy"]
    )
    
    # Get hot posts
    print("\n🔍 Fetching hot posts...")
    posts = collector.get_hot_posts(limit=10)
    
    print(f"\n✅ Found {len(posts)} posts!")
    
    for i, post in enumerate(posts, 1):
        print(f"\n{i}. r/{post['subreddit']} - u/{post['author']['username']}")
        print(f"   {post['title'][:80]}...")
        print(f"   ⬆️ {post['metrics']['score']} | 💬 {post['metrics']['num_comments']}")
