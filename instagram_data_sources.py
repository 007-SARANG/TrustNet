"""
Real Instagram Data Collection Examples
Shows 3 different ways to get Instagram posts and captions
"""

from agents.collectors.instagram_collector import InstagramCollector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_manual_sample():
    """
    METHOD 1: Manual/Simulated (No API needed)
    - Use downloaded images or URLs
    - Manually provide captions
    - Good for: Testing, demo, specific posts
    """
    print("\n" + "="*80)
    print("METHOD 1: Manual/Simulated Posts")
    print("="*80)
    
    collector = InstagramCollector()
    
    # Example with placeholder image URL
    post = collector.fetch_sample_post(
        image_path='https://via.placeholder.com/600x600.png?text=Climate+Data',
        caption='New research shows climate change accelerating. Key findings: temperatures up 2°C globally.'
    )
    
    if post:
        analysis = collector.analyze_post(post)
        print(f"\n✅ Analyzed: {post['caption'][:60]}...")
        print(f"   Classification: {analysis['classification']['reasoning']}")
        print(f"   Flagged: {analysis['prevention']['flagged']}")


def example_2_instaloader_profile():
    """
    METHOD 2: Instaloader - Scrape Public Profiles (No API key)
    - Scrapes public Instagram profiles
    - No authentication needed for public posts
    - Can login for private accounts
    - Good for: Research, analysis, monitoring specific accounts
    
    Install: pip install instaloader
    """
    print("\n" + "="*80)
    print("METHOD 2: Instaloader - Scrape Public Profile")
    print("="*80)
    
    try:
        # Initialize collector (no credentials needed for public posts)
        collector = InstagramCollector()
        
        # Fetch posts from a public profile (e.g., news organizations)
        profile_name = "nasa"  # Change to any public Instagram profile
        posts = collector.fetch_from_instagram(profile_name, max_posts=3)
        
        if posts:
            print(f"\n✅ Fetched {len(posts)} posts from @{profile_name}")
            
            # Analyze first post
            analysis = collector.analyze_post(posts[0])
            print(f"\n📊 Analysis of first post:")
            print(f"   Caption: {posts[0]['caption'][:60]}...")
            print(f"   Likes: {posts[0]['metrics']['likes']}")
            print(f"   Classification: {analysis['classification']['reasoning']}")
            print(f"   Informative: {analysis['classification']['is_informative']}")
        else:
            print("⚠️ No posts fetched. Check if Instaloader is installed:")
            print("   pip install instaloader")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure to install: pip install instaloader")


def example_3_instaloader_specific_post():
    """
    METHOD 3: Instaloader - Fetch Specific Post by URL
    - Fetch a single post by its URL
    - No authentication needed for public posts
    - Good for: Analyzing reported posts, specific investigations
    """
    print("\n" + "="*80)
    print("METHOD 3: Instaloader - Fetch Specific Post URL")
    print("="*80)
    
    try:
        collector = InstagramCollector()
        
        # Example Instagram post URL (replace with any public post URL)
        post_url = "https://www.instagram.com/p/C5wR7gRPQHl/"  # NASA post example
        
        post = collector.fetch_specific_post(post_url)
        
        if post:
            print(f"\n✅ Fetched post: {post['id']}")
            print(f"   Caption: {post['caption'][:100]}...")
            print(f"   Likes: {post['metrics']['likes']}")
            print(f"   Comments: {post['metrics']['comments']}")
            
            # Analyze it
            analysis = collector.analyze_post(post)
            print(f"\n📊 Analysis:")
            print(f"   Classification: {analysis['classification']['reasoning']}")
            print(f"   Confidence: {analysis['classification']['confidence']:.2%}")
            print(f"   Action: {analysis['prevention']['action']}")
        else:
            print("⚠️ Could not fetch post. Check if Instaloader is installed:")
            print("   pip install instaloader")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure to install: pip install instaloader")


def example_4_instagram_graph_api():
    """
    METHOD 4: Official Instagram Graph API (Requires Setup)
    - Official Facebook/Instagram API
    - Requires: Facebook Developer account, Instagram Business account
    - Good for: Production apps, commercial use, official integrations
    
    Setup Steps:
    1. Create Facebook Developer account
    2. Create an App
    3. Add Instagram Graph API product
    4. Get Access Token
    5. Connect Instagram Business Account
    
    Install: pip install facebook-sdk
    """
    print("\n" + "="*80)
    print("METHOD 4: Instagram Graph API (Official)")
    print("="*80)
    
    print("\n⚠️ This method requires setup:")
    print("1. Facebook Developer Account: https://developers.facebook.com/")
    print("2. Instagram Business Account")
    print("3. Access Token with permissions:")
    print("   - instagram_basic")
    print("   - instagram_manage_comments")
    print("   - pages_read_engagement")
    
    print("\n📝 Example code (after setup):")
    print("""
import facebook

# Your access token from Facebook Developer portal
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
INSTAGRAM_ACCOUNT_ID = 'YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID'

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN)

# Get recent posts
posts = graph.get_connections(
    id=INSTAGRAM_ACCOUNT_ID,
    connection_name='media',
    fields='id,caption,media_type,media_url,permalink,timestamp'
)

for post in posts['data']:
    if post['media_type'] == 'IMAGE':
        image_url = post['media_url']
        caption = post.get('caption', '')
        
        # Pass to TrustNet analyzer
        collector = InstagramCollector()
        post_data = collector.fetch_sample_post(image_url, caption)
        analysis = collector.analyze_post(post_data)
        print(f"Analyzed: {caption[:50]}...")
    """)


def comparison_table():
    """Show comparison of all methods"""
    print("\n" + "="*80)
    print("COMPARISON: Instagram Data Collection Methods")
    print("="*80)
    
    print("""
┌─────────────────────┬──────────────┬────────────┬──────────────┬─────────────┐
│ Method              │ API Key Req? │ Auth Req?  │ Rate Limits  │ Best For    │
├─────────────────────┼──────────────┼────────────┼──────────────┼─────────────┤
│ 1. Manual/Simulated │ ❌ No        │ ❌ No      │ None         │ Testing     │
│ 2. Instaloader      │ ❌ No        │ ⚠️ Optional│ IP-based     │ Research    │
│ 3. Graph API        │ ✅ Yes       │ ✅ Yes     │ App-based    │ Production  │
│ 4. Apify Scraper    │ ✅ Yes       │ ❌ No      │ Credit-based │ Scale       │
└─────────────────────┴──────────────┴────────────┴──────────────┴─────────────┘

RECOMMENDED FOR TRUSTNET:
- Development/Testing: Method 1 (Manual)
- Research/Analysis: Method 2 (Instaloader) ⭐ EASIEST
- Production: Method 3 (Graph API) - Requires business setup
    """)


if __name__ == "__main__":
    print("\n🔬 INSTAGRAM DATA COLLECTION EXAMPLES FOR TRUSTNET")
    print("="*80)
    
    # Show comparison first
    comparison_table()
    
    # Run examples
    print("\n\n📋 Running Examples...\n")
    
    # Method 1: Always works
    example_1_manual_sample()
    
    # Method 2: Works if instaloader installed
    example_2_instaloader_profile()
    
    # Method 3: Works if instaloader installed
    example_3_instaloader_specific_post()
    
    # Method 4: Just show instructions
    example_4_instagram_graph_api()
    
    print("\n" + "="*80)
    print("✅ Examples complete!")
    print("\nTo install Instaloader (recommended): pip install instaloader")
    print("To start analyzing: Modify the examples above with real profile names/URLs")
    print("="*80 + "\n")
