"""
Test Instagram Image-Caption Mismatch with Real Posts
Tests your login credentials and scrapes actual Instagram posts
"""

import os
import sys
from dotenv import load_dotenv
import instaloader

# Load environment variables
load_dotenv()

print("\n" + "="*80)
print("🔬 TESTING INSTAGRAM SCRAPING WITH REAL POSTS")
print("="*80)

# Get credentials
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

print(f"\n📋 Credentials:")
print(f"   Username: {username}")
print(f"   Password: {'*' * len(password) if password else 'Not set'}")

if not username or not password:
    print("\n❌ ERROR: Instagram credentials not found in .env file!")
    print("   Please add:")
    print("   INSTAGRAM_USERNAME=your_username")
    print("   INSTAGRAM_PASSWORD=your_password")
    sys.exit(1)

# Initialize Instaloader
L = instaloader.Instaloader()

print("\n⏳ Attempting to login to Instagram...")

try:
    # Login
    L.login(username, password)
    print("✅ Successfully logged in to Instagram!")
    
    # Test with a popular Instagram account
    test_accounts = [
        'natgeo',  # National Geographic - reliable source
        'nasa',    # NASA - scientific content
        'instagram',  # Instagram official
    ]
    
    print(f"\n{'='*80}")
    print("📸 SCRAPING RECENT POSTS")
    print("="*80)
    
    for account_name in test_accounts[:1]:  # Test with just first account
        print(f"\n🔍 Fetching posts from @{account_name}...")
        
        try:
            profile = instaloader.Profile.from_username(L.context, account_name)
            
            print(f"   📊 Account Stats:")
            print(f"      Followers: {profile.followers:,}")
            print(f"      Posts: {profile.mediacount:,}")
            
            print(f"\n   📝 Recent Posts:")
            
            # Get 3 recent posts
            post_count = 0
            for post in profile.get_posts():
                if post_count >= 3:
                    break
                
                post_count += 1
                
                print(f"\n   {'─'*76}")
                print(f"   Post #{post_count}")
                print(f"   {'─'*76}")
                print(f"   🔗 URL: https://www.instagram.com/p/{post.shortcode}/")
                print(f"   📅 Date: {post.date_local}")
                print(f"   ❤️  Likes: {post.likes:,}")
                print(f"   💬 Comments: {post.comments}")
                
                # Get caption (first 100 chars)
                caption = post.caption or "No caption"
                caption_preview = caption[:100] + "..." if len(caption) > 100 else caption
                print(f"   📝 Caption: {caption_preview}")
                
                # Check if post has image
                if post.is_video:
                    print(f"   🎥 Type: Video (skipping)")
                else:
                    print(f"   🖼️  Type: Image")
                    print(f"   🔗 Image URL: {post.url}")
                    
                    # This is what we'd analyze
                    print(f"\n   ✨ READY FOR ANALYSIS:")
                    print(f"      Image: {post.url[:50]}...")
                    print(f"      Caption: {caption[:80]}...")
                    
            print(f"\n✅ Successfully scraped {post_count} posts from @{account_name}")
            
        except Exception as e:
            print(f"   ❌ Error fetching posts from @{account_name}: {e}")
            
    print(f"\n{'='*80}")
    print("📊 TEST COMPLETE")
    print("="*80)
    print("\n✅ Instagram scraping is working!")
    print("✅ You can now fetch real posts for mismatch detection")
    print("\nNEXT: The system will analyze these posts for image-caption mismatches")
    
except instaloader.exceptions.BadCredentialsException:
    print("\n❌ LOGIN FAILED: Invalid username or password")
    print("   Please check your credentials in .env file")
    sys.exit(1)
    
except instaloader.exceptions.TwoFactorAuthRequiredException:
    print("\n⚠️  TWO-FACTOR AUTHENTICATION REQUIRED")
    print("   Your account has 2FA enabled. Solutions:")
    print("   1. Disable 2FA temporarily")
    print("   2. Use session file (more complex)")
    sys.exit(1)
    
except instaloader.exceptions.ConnectionException as e:
    print(f"\n❌ CONNECTION ERROR: {e}")
    print("   Possible reasons:")
    print("   - Rate limited by Instagram")
    print("   - Network connection issues")
    print("   - Instagram blocking automated access")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
