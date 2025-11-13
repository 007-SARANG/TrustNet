# 🔐 Instagram Login Guide for TrustNet

## ⚠️ Important: Do You Need to Login?

### **PUBLIC POSTS = NO LOGIN NEEDED!** ✅
- Instaloader can fetch **public Instagram posts WITHOUT any login**
- No credentials required
- No API keys needed
- Just works out of the box!

### **PRIVATE POSTS = LOGIN REQUIRED** 🔒
- Only needed if you want to access:
  - Private accounts
  - Posts from accounts that blocked anonymous viewing
  - Higher rate limits

---

## 📋 Three Ways to Provide Instagram Credentials

### **Method 1: Environment Variables (.env file)** ⭐ **RECOMMENDED**

#### Why this method?
- ✅ Most secure (credentials not in code)
- ✅ Easy to manage
- ✅ Git-ignored by default
- ✅ Used by production apps

#### How to use:

1. **Open your `.env` file** in the TrustNet directory

2. **Add your credentials** (uncomment and fill in):
```env
# Instagram Login (Optional - only for private accounts)
# For PUBLIC posts, NO login needed!
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```

3. **Example**:
```env
INSTAGRAM_USERNAME=john_doe
INSTAGRAM_PASSWORD=MySecurePassword123!
```

4. **Save the file** - TrustNet will automatically load these credentials!

#### Usage in code:
```python
from agents.collectors.instagram_collector import InstagramCollector

# Automatically loads from .env
collector = InstagramCollector(
    instagram_username=os.getenv('INSTAGRAM_USERNAME'),
    instagram_password=os.getenv('INSTAGRAM_PASSWORD')
)

# Now you can fetch posts
posts = collector.fetch_from_instagram('some_private_account', max_posts=5)
```

---

### **Method 2: Command Line (For Testing)** 🧪

#### PowerShell:
```powershell
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_password"
python test_instagram_instaloader.py
```

#### CMD:
```cmd
set INSTAGRAM_USERNAME=your_username
set INSTAGRAM_PASSWORD=your_password
python test_instagram_instaloader.py
```

#### Linux/Mac:
```bash
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"
python test_instagram_instaloader.py
```

**Note**: These credentials last only for the current terminal session

---

### **Method 3: Direct in Code (NOT RECOMMENDED)** ⚠️

```python
from agents.collectors.instagram_collector import InstagramCollector

# DON'T do this in production!
collector = InstagramCollector(
    instagram_username="your_username",
    instagram_password="your_password"
)
```

**Why not recommended?**
- ❌ Credentials visible in code
- ❌ Risk of committing to git
- ❌ Hard to manage across environments
- ❌ Security risk

---

## 🧪 Testing Instagram Login

### Test with public posts (NO LOGIN):
```bash
python test_instagram_instaloader.py
```
This will fetch public posts from @nasa - no credentials needed!

### Test with login:
```powershell
# Set credentials in PowerShell
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_password"

# Run test
python test_instagram_instaloader.py
```

---

## 🚀 Quick Start Examples

### Example 1: Fetch Public Posts (No Login)
```python
from agents.collectors.instagram_collector import InstagramCollector

# No credentials needed for public posts!
collector = InstagramCollector()

# Fetch from any public profile
posts = collector.fetch_from_instagram('nasa', max_posts=10)

for post in posts:
    print(f"Caption: {post['caption'][:50]}...")
    print(f"Likes: {post['metrics']['likes']}")
```

### Example 2: Fetch Specific Post (No Login)
```python
collector = InstagramCollector()

# Fetch any public Instagram post by URL
post = collector.fetch_specific_post(
    'https://www.instagram.com/p/ABC123xyz/'
)

if post:
    analysis = collector.analyze_post(post)
    print(f"Flagged: {analysis['prevention']['flagged']}")
```

### Example 3: With Login (For Private Accounts)
```python
import os
from agents.collectors.instagram_collector import InstagramCollector

# Load credentials from .env
collector = InstagramCollector(
    instagram_username=os.getenv('INSTAGRAM_USERNAME'),
    instagram_password=os.getenv('INSTAGRAM_PASSWORD')
)

# Now you can access private accounts (if you follow them)
posts = collector.fetch_from_instagram('private_account', max_posts=5)
```

---

## 🔧 Current Integration Status

### ✅ Already Integrated:
1. **quick_start.py** - Backend server
   - Automatically loads credentials from `.env`
   - Uses them when available
   - Falls back to no-login mode if not provided

2. **instagram_collector.py** - Core module
   - Supports optional login
   - Works without login for public posts
   - Handles authentication errors gracefully

3. **test_instagram_instaloader.py** - Test suite
   - Tests both logged-in and anonymous modes
   - Validates credential loading from environment

### 🎯 How to Use Right Now:

**Option A: For Public Posts Only (Easiest)**
```bash
# Just run it - no setup needed!
python test_instagram_instaloader.py
```

**Option B: For Private Accounts**
```bash
# 1. Edit .env file, add:
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# 2. Run tests
python test_instagram_instaloader.py
```

---

## 🛡️ Security Best Practices

### DO ✅
- Store credentials in `.env` file
- Add `.env` to `.gitignore` (already done)
- Use environment variables in production
- Keep credentials secret
- Use strong, unique passwords

### DON'T ❌
- Hardcode credentials in code
- Commit credentials to git
- Share your `.env` file
- Use your main Instagram password (use app-specific password)
- Store credentials in public places

---

## ⚠️ Instagram 2FA (Two-Factor Authentication)

If you have 2FA enabled on Instagram:

1. **Option 1**: Disable 2FA temporarily for testing
2. **Option 2**: Generate an app-specific password (if Instagram offers it)
3. **Option 3**: Use Instaloader's session file approach:

```python
import instaloader

loader = instaloader.Instaloader()
loader.load_session_from_file('your_username')  # Loads saved session
```

**To save a session**:
```bash
# Login once interactively
instaloader --login your_username

# This saves the session file, then you can use it in code
```

---

## 📊 Rate Limits & Best Practices

### Without Login:
- ~200 requests per hour per IP
- Instagram may block if you make too many requests
- Good for: occasional checks, testing

### With Login:
- Higher rate limits (~500-1000 requests/hour)
- More stable access
- Good for: regular monitoring, production use

### Best Practices:
```python
import time

collector = InstagramCollector()

# Add delays between requests
for profile in ['nasa', 'natgeo', 'bbc']:
    posts = collector.fetch_from_instagram(profile, max_posts=5)
    time.sleep(5)  # 5 second delay between profiles
```

---

## 🔍 Troubleshooting

### "Login failed" error:
1. Check username and password are correct
2. Verify no typos in `.env` file
3. Check if 2FA is enabled (see section above)
4. Try waiting a few minutes (rate limiting)

### "403 Forbidden" error:
- Instagram is blocking requests
- Solution: Wait 10-15 minutes, then try again
- Use login credentials for better access
- Add delays between requests

### "No posts fetched":
- Check if profile is public
- Verify profile name is correct (no @ symbol)
- Check internet connection
- Try with a different profile

---

## 📞 Support

For issues:
1. Check this guide first
2. Review error messages in terminal
3. Try the test script: `python test_instagram_instaloader.py`
4. Check Instaloader docs: https://instaloader.github.io/

---

## 🎯 Summary

**For 99% of use cases, YOU DON'T NEED TO LOGIN!**

Just run:
```bash
python test_instagram_instaloader.py
```

It will fetch real posts from NASA's public Instagram without any credentials!

Only login if you need:
- Private account access
- Higher rate limits
- More stable long-term access

**To add credentials**: Just edit `.env` file and uncomment these lines:
```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

That's it! 🚀
