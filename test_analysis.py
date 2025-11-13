"""
Test script to analyze posts and see them in real-time on the dashboard
"""

import requests
import json
import time

API_URL = "http://localhost:8000/api/analyze"

# Test posts
test_posts = [
    {
        "content": "BREAKING: Scientists discover miracle cure that doctors don't want you to know about!",
        "author": "test_user_1",
        "platform": "twitter"
    },
    {
        "content": "New study from Harvard Medical School shows promising results for cancer treatment.",
        "author": "test_user_2", 
        "platform": "twitter"
    },
    {
        "content": "OMG! Celebrities reveal shocking secret to weight loss! Click here now!!!",
        "author": "test_user_3",
        "platform": "facebook"
    },
    {
        "content": "The weather forecast for tomorrow shows a chance of rain in the afternoon.",
        "author": "test_user_4",
        "platform": "twitter"
    },
    {
        "content": "Bill Gates wants to microchip everyone with 5G vaccines! Share before they delete this!",
        "author": "test_user_5",
        "platform": "facebook"
    }
]

def analyze_post(post):
    """Send a post for analysis"""
    try:
        print(f"\n{'='*80}")
        print(f"📝 Analyzing post from @{post['author']} on {post['platform']}")
        print(f"Content: {post['content'][:60]}...")
        print(f"{'='*80}")
        
        response = requests.post(
            API_URL,
            json={
                "content": post['content'],
                "content_type": "text",
                "metadata": {
                    "author": post['author'],
                    "platform": post['platform'],
                    "timestamp": time.time()
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis Complete!")
            print(f"   Trust Score: {result.get('trust_score', 'N/A')}")
            print(f"   Risk Level: {result.get('risk_level', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
            
            if 'analysis' in result:
                analysis = result['analysis']
                if 'sentiment' in analysis:
                    print(f"   Sentiment: {analysis['sentiment']}")
                if 'credibility_score' in analysis:
                    print(f"   Credibility: {analysis['credibility_score']}")
            
            print(f"\n💡 Check your dashboard at http://localhost:3000 to see this analysis!")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Is the server running?")
        print("   Run: python quick_start.py")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    print("\n" + "="*80)
    print("🚀 TrustNet 2.0 - Post Analysis Test")
    print("="*80)
    print("\n📊 Make sure your dashboard is open at: http://localhost:3000")
    print("You'll see posts appear in real-time as they're analyzed!\n")
    
    input("Press Enter to start analyzing posts...")
    
    for i, post in enumerate(test_posts, 1):
        print(f"\n\n🔍 Analyzing post {i}/{len(test_posts)}...")
        analyze_post(post)
        
        if i < len(test_posts):
            print("\n⏳ Waiting 3 seconds before next post...")
            time.sleep(3)
    
    print("\n\n" + "="*80)
    print("✅ All posts analyzed!")
    print("="*80)
    print("\n📊 Check your dashboard to see all the analysis results!")
    print("   Dashboard: http://localhost:3000")
    print("   - Activity Feed: See all analyzed posts")
    print("   - Network View: See connections between posts")
    print("   - Analytics: See statistics and trends")
    print("\n")


if __name__ == "__main__":
    main()
