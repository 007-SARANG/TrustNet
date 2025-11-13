# Required APIs for TrustNet 2.0 Real-Time Monitoring

## ✅ Already Configured
1. **Groq API** (LLM for analysis) - ✅ FREE
2. **Google Fact Check API** - ✅ FREE (10K requests/day)

## 🔴 CRITICAL - Need for Real-Time Post Monitoring

### 1. Twitter/X API (Top Priority)
**Purpose:** Monitor tweets in real-time, track hashtags, detect viral misinformation

**Options:**
- **Twitter API v2 - Basic** (FREE but limited)
  - 500K tweets/month read limit
  - Sign up: https://developer.twitter.com/en/portal/dashboard
  - Good for: Testing, small-scale monitoring
  
- **Twitter API v2 - Elevated** ($100/month)
  - Better rate limits
  - Real-time streaming
  - Sign up: Same portal, request elevation
  - Good for: Production use

- **Twitter API v2 - Enterprise** ($$$)
  - Full firehose access
  - Unlimited streaming
  - Contact Twitter for pricing

**What you get:**
```python
# Real-time tweets matching keywords
tweets = client.search_recent_tweets(
    query="vaccine OR covid -is:retweet",
    max_results=100,
    tweet_fields=['created_at', 'author_id', 'public_metrics']
)
```

### 2. Reddit API (High Priority)
**Purpose:** Monitor subreddits for misinformation, track discussions

**Cost:** FREE (with rate limits)
**Sign up:** https://www.reddit.com/prefs/apps
**Rate Limit:** 60 requests/minute

**What you get:**
```python
# Get posts from subreddits
posts = reddit.subreddit('news').hot(limit=100)
```

### 3. YouTube Data API (Medium Priority)
**Purpose:** Analyze video titles, descriptions, comments for misinformation

**Cost:** FREE (10,000 quota units/day = ~100 video analyses)
**Sign up:** https://console.cloud.google.com/apis/library/youtube.googleapis.com
**Already have Google Cloud account:** ✅ Can enable immediately

**What you get:**
```python
# Search trending videos
videos = youtube.search().list(
    part='snippet',
    q='breaking news',
    type='video',
    maxResults=50
)
```

### 4. Facebook/Instagram Graph API (Optional)
**Purpose:** Monitor public posts, pages, groups

**Cost:** FREE (requires app review)
**Sign up:** https://developers.facebook.com/
**Limitation:** Can only access content from pages/users who authorize your app

**Note:** Very restricted due to privacy policies. Not recommended for general monitoring.

### 5. News API (High Priority)
**Purpose:** Monitor news articles, verify sources

**Cost:** 
- Developer: FREE (100 requests/day)
- Business: $449/month (unlimited)

**Sign up:** https://newsapi.org/register
**Good for:** Cross-referencing claims with legitimate news sources

### 6. CrowdTangle API (Facebook-owned, for researchers)
**Purpose:** Track social media trends, viral content

**Cost:** FREE (for researchers, journalists, academics)
**Sign up:** https://www.crowdtangle.com/request
**Requirements:** Academic/research affiliation

### 7. RSS Feeds (FREE Alternative)
**Purpose:** Monitor news sites, blogs without API

**Cost:** FREE
**Implementation:** Built-in to Python
**Good for:** News monitoring without API costs

## 📊 Recommended Setup Priority

### Phase 1: Immediate (FREE APIs)
1. ✅ Twitter API Basic (FREE) - Get this FIRST
2. ✅ Reddit API (FREE)
3. ✅ News API Developer (FREE)
4. ✅ YouTube API (FREE)
5. ✅ RSS Feeds (FREE)

### Phase 2: Scale Up (Paid when needed)
1. Twitter API Elevated ($100/month) - When you need more volume
2. News API Business ($449/month) - For production
3. Webhooks for real-time notifications

## 🎯 How to Get Started (Next 30 minutes)

### Step 1: Twitter API (Most Important)
```
1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Sign in with your Twitter account
3. Create a new project
4. Get your API keys:
   - API Key (Consumer Key)
   - API Secret Key (Consumer Secret)
   - Bearer Token
```

### Step 2: Reddit API
```
1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script"
4. Get your credentials:
   - Client ID
   - Client Secret
```

### Step 3: News API
```
1. Go to: https://newsapi.org/register
2. Sign up for free account
3. Copy your API key
```

### Step 4: YouTube API
```
1. Go to: https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create API credentials
4. Copy your API key
```

## 💰 Cost Breakdown (Starting)

| API | Cost | Requests/Day | Good For |
|-----|------|--------------|----------|
| Twitter Basic | FREE | ~1,500 tweets | Testing |
| Reddit | FREE | ~86,400 requests | Production |
| News API | FREE | 100 articles | Testing |
| YouTube | FREE | ~100 videos | Testing |
| Groq (LLM) | FREE | 30 req/min | Production ✅ |
| Google Fact Check | FREE | 10,000 | Production ✅ |

**Total Starting Cost: $0/month** ✅

## 💰 Cost Breakdown (Production Scale)

| API | Cost | Requests/Day | Good For |
|-----|------|--------------|----------|
| Twitter Elevated | $100/mo | ~50,000 tweets | Production |
| Reddit | FREE | ~86,400 requests | Production |
| News API Business | $449/mo | Unlimited | Production |
| YouTube | FREE | ~100 videos | Production |
| Groq (LLM) | FREE | 30 req/min | Production ✅ |
| Google Fact Check | FREE | 10,000 | Production ✅ |

**Total Production Cost: ~$549/month**

## 🔧 What I'll Build Next

Once you get the API keys, I'll create:

1. **Social Media Collectors** (agents/collectors/)
   - `twitter_collector.py` - Stream tweets in real-time
   - `reddit_collector.py` - Monitor subreddits
   - `news_collector.py` - Fetch latest news articles
   - `youtube_collector.py` - Analyze trending videos

2. **Real-Time Dashboard Updates**
   - Live feed showing actual posts
   - Platform badges (Twitter, Reddit, YouTube)
   - Click to see full post
   - Real-time metrics

3. **Trending Topics Detection**
   - Identify viral misinformation
   - Track hashtags
   - Alert on suspicious patterns

## 📝 Next Steps

**Tell me which APIs you want to start with:**
- Option A: Start with FREE APIs (Twitter Basic, Reddit, News API)
- Option B: Go straight to paid Twitter Elevated for better access
- Option C: Start with just one platform (which one?)

**I'll wait for your API keys and then build the collectors!**
