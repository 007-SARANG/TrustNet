# ✅ TrustNet 2.0 - Real-Time Post Monitoring Setup Complete!

## 📋 What I Built For You

### 1. **Social Media Collectors** ✅
- `agents/collectors/twitter_collector.py` - Collects tweets in real-time
- `agents/collectors/reddit_collector.py` - Collects Reddit posts in real-time

### 2. **Real-Time Monitor** ✅
- `real_time_monitor.py` - Orchestrates collection from multiple platforms
- Shows detailed logs of each post being analyzed
- Sends posts to dashboard via WebSocket

### 3. **Live Posts Dashboard Page** ✅
- `dashboard/src/pages/LivePostsFeed.jsx` - Beautiful UI showing real posts
- Platform badges (Twitter, Reddit, YouTube)
- Risk scores and classifications
- Click to open original post

### 4. **Documentation** ✅
- `REQUIRED_APIS.md` - Detailed API setup guide
- `QUICK_START_REAL_POSTS.md` - 5-minute quick start

---

## 🎯 What You Need to Do Now

### Step 1: Get API Keys (Choose One or Both)

#### Option A: Twitter/X API (Recommended)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a project
3. Copy: API Key, API Secret, Bearer Token
4. Add to `.env`:
```env
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
```

#### Option B: Reddit API (Easiest)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Copy: Client ID, Client Secret
4. Add to `.env`:
```env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```

### Step 2: Install Dependencies
```cmd
pip install tweepy praw
```

### Step 3: Run Real-Time Monitor
```cmd
python real_time_monitor.py
```

You'll see REAL posts being collected and analyzed!

### Step 4: View in Dashboard
1. Start backend: `python quick_start.py`
2. Start dashboard: `cd dashboard && npm run dev`
3. Open: `http://localhost:3000/live`
4. See live posts! 📡

---

## 🔍 How to See Posts Being Analyzed

### ✅ Terminal Output (Already Working!)
When backend is running, you'll see:
```
================================================================================
📝 ANALYZING TWITTER POST
   ID: 1234567890
   Author: @example
   Content: Breaking news: Scientists discover miracle cure...
================================================================================

✅ ANALYSIS COMPLETE
   Classification: FAKE
   Risk Score: 85%
   Red Flags: 3
================================================================================
```

### ✅ Dashboard (Once APIs Configured)
Navigate to `http://localhost:3000/live` to see:
- Real-time posts from Twitter, Reddit, etc.
- Platform badges
- Risk scores
- Classification (FAKE/REAL)
- Engagement metrics (likes, shares, comments)
- Click to view original post

---

## 📊 APIs You Need

### Currently Configured ✅
- ✅ Groq API (LLM for analysis) - FREE
- ✅ Google Fact Check API - FREE

### Need to Add (For Real Posts) 🔴
- 🔴 Twitter API - Get from https://developer.twitter.com
- 🔴 Reddit API - Get from https://www.reddit.com/prefs/apps

### Optional (Later) ⚪
- ⚪ News API - https://newsapi.org
- ⚪ YouTube API - https://console.cloud.google.com

---

## 💰 Cost

| API | Cost | Rate Limit |
|-----|------|------------|
| Twitter Basic | **FREE** | 500K tweets/month |
| Reddit | **FREE** | Unlimited |
| News API | **FREE** | 100/day |
| YouTube | **FREE** | 10K/day |

**Total: $0/month** ✅

---

## 🎬 Quick Demo (Without APIs)

Run the test script to see how it works:
```cmd
test_posts.bat
```

This sends test posts through the system so you can see the analysis flow.

---

## 📚 Documentation

- **REQUIRED_APIS.md** - Full API setup guide
- **QUICK_START_REAL_POSTS.md** - 5-minute quick start
- **GOOGLE_API_SETUP.md** - Google API setup
- **README.md** - Full project documentation

---

## 🆘 Troubleshooting

### "No APIs configured"
→ Add Twitter or Reddit API keys to `.env`

### "404 Not Found"
→ Fixed! Prometheus /metrics endpoint added

### "Can't see posts in dashboard"
→ Need to configure Twitter/Reddit APIs first

### "Rate limit exceeded"
→ Twitter Free: 500K/month, wait a few minutes

---

## 🚀 Next Steps

1. **Get Twitter API keys** (takes 5 minutes)
   - Go to https://developer.twitter.com/en/portal/dashboard
   - Create project, copy keys

2. **Add to `.env` file**
   ```env
   TWITTER_API_KEY=xxxxx
   TWITTER_API_SECRET=xxxxx
   TWITTER_BEARER_TOKEN=xxxxx
   ```

3. **Install packages**
   ```cmd
   pip install tweepy
   ```

4. **Run monitor**
   ```cmd
   python real_time_monitor.py
   ```

5. **See REAL tweets being analyzed!** ✅

---

## 📞 What to Do Next

**Tell me:**
- Which platform do you want to start with? (Twitter or Reddit)
- Do you have API keys already?
- Do you want to see the dashboard working with real posts?

I'll guide you through the setup!
