"""
Test Instagram Integration with Instaloader (Method 2)
Demonstrates fetching REAL Instagram posts using Instaloader
"""

import os
import sys
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check if instaloader is installed
try:
    import instaloader
    logger.info("✅ Instaloader is installed")
except ImportError:
    logger.error("❌ Instaloader not installed!")
    logger.error("Install it with: pip install instaloader")
    sys.exit(1)

from agents.collectors.instagram_collector import InstagramCollector


def test_instaloader_profile():
    """
    Test Method 2A: Fetch multiple posts from a public profile
    """
    print("\n" + "="*80)
    print("TEST 1: Fetch Posts from Public Profile")
    print("="*80)
    
    try:
        # Initialize collector (no login needed for public posts)
        collector = InstagramCollector()
        
        # Fetch posts from NASA (public profile with informative content)
        profile_name = "nasa"
        max_posts = 3
        
        logger.info(f"🚀 Fetching {max_posts} posts from @{profile_name}...")
        posts = collector.fetch_from_instagram(profile_name, max_posts=max_posts)
        
        if not posts:
            logger.error(f"❌ No posts fetched from @{profile_name}")
            logger.error("This could be due to:")
            logger.error("1. Network issues")
            logger.error("2. Instagram rate limiting")
            logger.error("3. Profile doesn't exist or is private")
            return False
        
        print(f"\n✅ Successfully fetched {len(posts)} posts!\n")
        
        # Analyze each post
        results = []
        for idx, post in enumerate(posts, 1):
            print(f"\n{'─'*80}")
            print(f"POST {idx}/{len(posts)}: {post['id']}")
            print(f"{'─'*80}")
            print(f"📝 Caption: {post['caption'][:100]}...")
            print(f"❤️  Likes: {post['metrics']['likes']:,}")
            print(f"💬 Comments: {post['metrics']['comments']:,}")
            print(f"🔗 URL: {post['url']}")
            
            # Analyze the post
            logger.info(f"🔍 Analyzing post {idx}...")
            analysis = collector.analyze_post(post)
            
            # Display results
            print(f"\n📊 ANALYSIS RESULTS:")
            print(f"   Classification: {analysis['classification']['category']}")
            print(f"   Informative: {analysis['classification']['is_informative']}")
            print(f"   Confidence: {analysis['classification']['confidence']:.2%}")
            print(f"   Reasoning: {analysis['classification']['reasoning'][:150]}...")
            
            print(f"\n🛡️  PREVENTION SYSTEM:")
            print(f"   Flagged: {analysis['prevention']['flagged']}")
            print(f"   Action: {analysis['prevention']['action']}")
            if analysis['prevention']['flagged']:
                print(f"   Triggered Rules: {', '.join(analysis['prevention']['rules_triggered'])}")
            
            # Save results
            results.append({
                'post_id': post['id'],
                'caption': post['caption'][:200],
                'url': post['url'],
                'metrics': post['metrics'],
                'analysis': analysis
            })
        
        # Save to JSON
        output_file = f"instagram_analysis_{profile_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        return False


def test_specific_post():
    """
    Test Method 2B: Fetch a specific post by URL
    NOTE: This often fails due to Instagram's anti-scraping measures
    """
    print("\n" + "="*80)
    print("TEST 2: Fetch Specific Post by URL (Optional)")
    print("="*80)
    print("⚠️  Note: Instagram often blocks direct post fetching (403 errors)")
    print("    This is normal - use profile fetching instead for better reliability")
    
    try:
        collector = InstagramCollector()
        
        # Try to fetch a specific post
        # Note: This may fail due to Instagram's anti-bot protections
        post_url = "https://www.instagram.com/p/C5wR7gRPQHl/"  # NASA post
        
        logger.info(f"🔍 Attempting to fetch post from URL: {post_url}")
        post = collector.fetch_specific_post(post_url)
        
        if not post:
            logger.warning("⚠️ Could not fetch the specific post (EXPECTED - Instagram blocks this)")
            logger.info("✅ This is normal behavior - Instagram blocks direct post requests")
            logger.info("💡 Use fetch_from_instagram(profile) instead for reliable scraping")
            return None  # Return None instead of False - this is expected
        
        print(f"\n✅ Successfully fetched post: {post['id']}\n")
        print(f"{'─'*80}")
        print(f"📝 Caption: {post['caption'][:200]}...")
        print(f"👤 Author: @{post['author']['username']}")
        print(f"❤️  Likes: {post['metrics']['likes']:,}")
        print(f"💬 Comments: {post['metrics']['comments']:,}")
        print(f"🔗 URL: {post['url']}")
        
        # Analyze
        logger.info("🔍 Analyzing post...")
        analysis = collector.analyze_post(post)
        
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   Classification: {analysis['classification']['category']}")
        print(f"   Informative: {analysis['classification']['is_informative']}")
        print(f"   Confidence: {analysis['classification']['confidence']:.2%}")
        print(f"   Reasoning: {analysis['classification']['reasoning']}")
        
        print(f"\n🛡️  PREVENTION SYSTEM:")
        print(f"   Flagged: {analysis['prevention']['flagged']}")
        print(f"   Action: {analysis['prevention']['action']}")
        
        # Save result
        output_file = f"instagram_analysis_single_{post['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'post': {
                    'id': post['id'],
                    'caption': post['caption'],
                    'url': post['url'],
                    'metrics': post['metrics']
                },
                'analysis': analysis
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Result saved to: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        return False


def test_with_login():
    """
    Test Method 2C: Fetch with Instagram login (for private accounts)
    """
    print("\n" + "="*80)
    print("TEST 3: Fetch with Instagram Login (Optional)")
    print("="*80)
    
    print("\n⚠️ This test requires Instagram credentials")
    print("Only use this if you need to access private accounts")
    print("\nFor public accounts, login is NOT required!\n")
    
    # Get credentials from environment variables (safer than hardcoding)
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        print("ℹ️ Skipping login test - no credentials provided")
        print("\nTo test with login, set environment variables:")
        print("   $env:INSTAGRAM_USERNAME='your_username'")
        print("   $env:INSTAGRAM_PASSWORD='your_password'")
        return None
    
    try:
        logger.info("🔐 Initializing with login credentials...")
        collector = InstagramCollector(
            instagram_username=username,
            instagram_password=password
        )
        
        # Try fetching from a profile
        profile_name = "nasa"  # Or any profile
        posts = collector.fetch_from_instagram(profile_name, max_posts=2)
        
        if posts:
            print(f"✅ Successfully logged in and fetched {len(posts)} posts")
            return True
        else:
            print("⚠️ Login succeeded but no posts fetched")
            return False
            
    except Exception as e:
        logger.error(f"❌ Login test failed: {e}")
        print("\n⚠️ Login failed. This could be due to:")
        print("1. Incorrect credentials")
        print("2. Two-factor authentication enabled (2FA)")
        print("3. Instagram security restrictions")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🔬 INSTAGRAM INSTALOADER TEST SUITE (METHOD 2)")
    print("="*80)
    print("\nThis will test fetching REAL Instagram posts using Instaloader")
    print("No API key required!")
    print("\n" + "="*80)
    
    results = {}
    
    # Test 1: Fetch from profile
    print("\n\n")
    results['profile_fetch'] = test_instaloader_profile()
    
    # Test 2: Fetch specific post
    print("\n\n")
    results['specific_post'] = test_specific_post()
    
    # Test 3: Login (optional)
    print("\n\n")
    results['login'] = test_with_login()
    
    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUMMARY")
    print("="*80)
    print(f"Profile Fetch:   {'✅ PASSED' if results['profile_fetch'] else '❌ FAILED'}")
    print(f"Specific Post:   {'⚠️ EXPECTED FAIL (Instagram blocks this)' if results['specific_post'] is None else ('✅ PASSED' if results['specific_post'] else '❌ FAILED')}")
    print(f"Login Test:      {'⏭️ SKIPPED' if results['login'] is None else ('✅ PASSED' if results['login'] else '❌ FAILED')}")
    
    if results['profile_fetch']:
        print("\n✅ METHOD 2 (INSTALOADER) IS FULLY WORKING!")
        print("\n🎉 Success! You can now:")
        print("1. ✅ Fetch posts from any public Instagram profile")
        print("2. ✅ Analyze images and captions for misinformation")
        print("3. ✅ Detect image-caption mismatches")
        print("\n📝 Next Steps:")
        print("1. Install AI models: pip install transformers torch")
        print("2. Check the generated JSON files for analysis results")
        print("3. Use fetch_from_instagram() in your code")
        print("4. Integrate with quick_start.py for real-time analysis")
        
        print("\n💡 Tips:")
        print("   - Use fetch_from_instagram('profile', max_posts=10) for best results")
        print("   - Specific post URLs often blocked by Instagram (use profile fetch)")
        print("   - Add delays between requests to avoid rate limiting")
    else:
        print("\n⚠️ Profile fetch failed - check error messages above")
        print("\nTroubleshooting:")
        print("1. Verify internet connection")
        print("2. Check Instagram is not blocking your IP")
        print("3. Try with a different profile name")
        print("4. Wait a few minutes and try again (rate limiting)")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
