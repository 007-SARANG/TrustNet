# 🚀 TrustNet 2.0 - Quick Start Guide: Real-Time Post Monitoring

## 📋 What You Need

To see **REAL social media posts** being analyzed, you need API keys from social media platforms.

---

## ⚡ FASTEST Way to Get Started (5 minutes)

### Option 1: Twitter/X API (Recommended - Easiest)

**Step 1:** Go to https://developer.twitter.com/en/portal/dashboard

**Step 2:** Sign in with your Twitter/X account

**Step 3:** Click "Create Project" or "Create App"

**Step 4:** Copy these 3 keys:
- API Key (Consumer Key)
- API Secret (Consumer Secret)  
- Bearer Token

**Step 5:** Add to your `.env` file:
```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Step 6:** Run the monitor:
```cmd
python real_time_monitor.py
```

**Done!** You'll see REAL tweets being collected and analyzed!

---

### Option 2: Reddit API (Also Easy & FREE)

**Step 1:** Go to https://www.reddit.com/prefs/apps

**Step 2:** Click "Create App" or "Create Another App"

**Step 3:** Fill in:
- Name: TrustNet
- Type: Select "script"
- Redirect URI: http://localhost:8000

**Step 4:** Copy:
- Client ID (under app name)
- Client Secret

**Step 5:** Add to your `.env` file:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

**Step 6:** Run the monitor:
```cmd
python real_time_monitor.py
```

**Done!** You'll see REAL Reddit posts being collected and analyzed!

---

## 🎯 How to See Posts

### Method 1: Terminal Output
When you run `python real_time_monitor.py`, you'll see:

```
================================================================================
📝 ANALYZING TWITTER POST
   ID: 1234567890
   Author: @someuser
   Content: Breaking news about...
================================================================================

✅ ANALYSIS COMPLETE
   Classification: FAKE
   Risk Score: 75%
   Red Flags: 3
================================================================================
```

### Method 2: Dashboard (Visual)
1. Start backend: `python quick_start.py`
2. Start dashboard: `cd dashboard && npm run dev`
3. Open browser: `http://localhost:3000/live`
4. **See live posts appear in real-time!** 📡

---

## 🔧 Installation

### Install Required Packages

**For Twitter:**
```cmd
pip install tweepy
```

**For Reddit:**
```cmd
pip install praw
```

---

## 📖 Full Setup (All Platforms)

### 1. Twitter/X API ✅
```env
TWITTER_API_KEY=xxxxx
TWITTER_API_SECRET=xxxxx
TWITTER_BEARER_TOKEN=xxxxx
```
Get from: https://developer.twitter.com/en/portal/dashboard

### 2. Reddit API ✅
```env
REDDIT_CLIENT_ID=xxxxx
REDDIT_CLIENT_SECRET=xxxxx
```
Get from: https://www.reddit.com/prefs/apps

### 3. News API (Optional)
```env
NEWS_API_KEY=xxxxx
```
Get from: https://newsapi.org/register

### 4. YouTube API (Optional)
```env
YOUTUBE_API_KEY=xxxxx
```
Get from: https://console.cloud.google.com/apis/library/youtube.googleapis.com

---

## 🎬 Usage

### Standalone Monitoring (No Dashboard)
```cmd
python real_time_monitor.py
```
This will print posts to terminal as they're collected.

### With Dashboard (Visual Interface)
**Terminal 1:**
```cmd
python quick_start.py
```

**Terminal 2:**
```cmd
cd dashboard
npm run dev
```

**Browser:**
Open `http://localhost:3000/live` to see live posts!

---

## 💡 What You'll See

### Twitter Posts
```
🐦 NEW TWEET COLLECTED
   ID: 1234567890
   Author: @example
   Text: Breaking news: Scientists discover...
   Likes: 523 | RTs: 142 | Replies: 89
   
✅ ANALYSIS COMPLETE
   Classification: REAL
   Risk Score: 15%
   Red Flags: 0
```

### Reddit Posts
```
🤖 NEW REDDIT POST COLLECTED
   ID: abc123
   Subreddit: r/worldnews
   Author: u/example
   Title: New study shows...
   Score: 1234 | Comments: 456 | Ratio: 89%
   
✅ ANALYSIS COMPLETE
   Classification: REAL
   Risk Score: 20%
   Red Flags: 0
```

---

## 🆘 Troubleshooting

### "No APIs configured"
- You need to add API keys to `.env` file
- At minimum, add Twitter OR Reddit
- See REQUIRED_APIS.md for detailed setup

### "401 Unauthorized"
- Check your API keys are correct
- Make sure keys are in `.env` file
- Restart the server after adding keys

### "Rate limit exceeded"
- Twitter Free: 500K tweets/month
- Wait a few minutes and try again
- Consider upgrading to Twitter Elevated ($100/month)

---

## 📊 Cost Summary

| Platform | Cost | Rate Limit | Setup Time |
|----------|------|------------|------------|
| Twitter Basic | **FREE** | 500K/month | 5 min |
| Reddit | **FREE** | 86K/day | 5 min |
| News API | **FREE** | 100/day | 2 min |
| YouTube | **FREE** | 10K/day | 5 min |

**Total Starting Cost: $0** ✅

---

## 🎯 Next Steps

1. ✅ Get Twitter API keys (5 minutes)
2. ✅ Add to `.env` file
3. ✅ Run `pip install tweepy`
4. ✅ Run `python real_time_monitor.py`
5. ✅ Watch REAL posts being analyzed!

**Need help?** Check `REQUIRED_APIS.md` for detailed instructions!
