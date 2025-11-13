"""
TrustNet 2.0 - Twitter Collector
Monitors Twitter in real-time for misinformation
"""

import tweepy
import logging
from typing import List, Dict
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class TwitterCollector:
    """Collect tweets in real-time based on keywords/hashtags"""
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        bearer_token: str,
        keywords: List[str] = None
    ):
        self.keywords = keywords or [
            "breaking news",
            "vaccine",
            "covid",
            "election",
            "conspiracy",
            "miracle cure"
        ]
        
        # Initialize Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            wait_on_rate_limit=True
        )
        
        logger.info(f"🐦 Twitter Collector initialized")
        logger.info(f"   Monitoring keywords: {', '.join(self.keywords)}")
    
    
    def search_recent_tweets(self, max_results: int = 10) -> List[Dict]:
        """
        Search for recent tweets matching keywords
        
        Twitter API v2 Basic (FREE):
        - 500K tweets/month
        - Last 7 days only
        - 100 tweets per request
        """
        
        all_tweets = []
        
        try:
            # Build search query
            query = " OR ".join(self.keywords)
            query += " -is:retweet lang:en"  # Exclude retweets, English only
            
            logger.info(f"🔍 Searching Twitter for: {query}")
            
            # Search tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'text'],
                expansions=['author_id'],
                user_fields=['username', 'verified', 'public_metrics']
            )
            
            if not response.data:
                logger.warning("No tweets found")
                return []
            
            # Process tweets
            users = {user.id: user for user in response.includes.get('users', [])}
            
            for tweet in response.data:
                author = users.get(tweet.author_id)
                
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'author': {
                        'id': tweet.author_id,
                        'username': author.username if author else 'unknown',
                        'verified': author.verified if author else False,
                        'followers': author.public_metrics['followers_count'] if author else 0
                    },
                    'metrics': {
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count'],
                        'replies': tweet.public_metrics['reply_count'],
                        'views': tweet.public_metrics.get('impression_count', 0)
                    },
                    'platform': 'twitter',
                    'url': f"https://twitter.com/{author.username}/status/{tweet.id}" if author else None
                }
                
                all_tweets.append(tweet_data)
                
                # Log tweet
                logger.info("="*80)
                logger.info(f"🐦 NEW TWEET COLLECTED")
                logger.info(f"   ID: {tweet.id}")
                logger.info(f"   Author: @{tweet_data['author']['username']}")
                logger.info(f"   Text: {tweet.text[:100]}...")
                logger.info(f"   Likes: {tweet_data['metrics']['likes']} | "
                          f"RTs: {tweet_data['metrics']['retweets']} | "
                          f"Replies: {tweet_data['metrics']['replies']}")
                logger.info("="*80)
            
            logger.info(f"✅ Collected {len(all_tweets)} tweets")
            return all_tweets
            
        except tweepy.TweepyException as e:
            logger.error(f"❌ Twitter API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error collecting tweets: {e}")
            return []
    
    
    def stream_tweets(self, on_tweet_callback):
        """
        Stream tweets in real-time (requires Twitter API v2 Elevated)
        
        For Basic tier, use search_recent_tweets() in a loop instead
        """
        logger.warning("⚠️  Real-time streaming requires Twitter API v2 Elevated ($100/month)")
        logger.info("💡 Using polling mode instead (search every 60 seconds)")
        
        # Polling mode for Basic tier
        while True:
            tweets = self.search_recent_tweets(max_results=10)
            
            for tweet in tweets:
                on_tweet_callback(tweet)
            
            logger.info("⏳ Waiting 60 seconds before next search...")
            asyncio.sleep(60)


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
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not all([api_key, api_secret, bearer_token]):
        print("❌ Missing Twitter API credentials!")
        print("\nAdd to your .env file:")
        print("TWITTER_API_KEY=your_api_key")
        print("TWITTER_API_SECRET=your_api_secret")
        print("TWITTER_BEARER_TOKEN=your_bearer_token")
        print("\nGet them from: https://developer.twitter.com/en/portal/dashboard")
        exit(1)
    
    # Create collector
    collector = TwitterCollector(
        api_key=api_key,
        api_secret=api_secret,
        bearer_token=bearer_token,
        keywords=["vaccine", "covid", "breaking news", "miracle cure"]
    )
    
    # Search recent tweets
    print("\n🔍 Searching for recent tweets...")
    tweets = collector.search_recent_tweets(max_results=10)
    
    print(f"\n✅ Found {len(tweets)} tweets!")
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n{i}. @{tweet['author']['username']}")
        print(f"   {tweet['text'][:100]}...")
        print(f"   👍 {tweet['metrics']['likes']} | 🔁 {tweet['metrics']['retweets']}")
