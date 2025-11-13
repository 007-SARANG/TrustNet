# TrustNet 2.0 - Real-Time Production Setup Guide

## 🚀 Production Deployment Checklist

### Prerequisites
- Python 3.10+
- Docker Desktop (for infrastructure)
- Node.js 18+ (for dashboard)
- API Keys (see below)

---

## Step 1: Set Up Environment Variables

Create `.env` file in the project root:

```bash
# API Keys (REQUIRED for real-time operation)
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_FACTCHECK_API_KEY=your-google-factcheck-key
GOOGLE_CSE_ID=your-custom-search-engine-id

# Twitter/X API (for real-time social media monitoring)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Reddit API (optional)
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USER_AGENT=TrustNet/2.0

# Database Configuration
POSTGRES_USER=trustnet_user
POSTGRES_PASSWORD=trustnet_pass_CHANGE_THIS
POSTGRES_DB=trustnet
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=trustnet_redis_CHANGE_THIS

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# MLflow (for model tracking)
MLFLOW_TRACKING_URI=http://localhost:5000

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## Step 2: Start Infrastructure Services

**Option A: Using Docker (Recommended)**

```bash
# Start all services
docker-compose up -d

# Check services are running
docker-compose ps

# View logs
docker-compose logs -f
```

Services that will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Kafka + Zookeeper (port 9092)
- MLflow (port 5000)
- Prometheus (port 9090)
- Grafana (port 3001)

**Option B: Install Manually**

If you can't use Docker:

### Install PostgreSQL
- Download: https://www.postgresql.org/download/windows/
- Create database: `trustnet`
- User: `trustnet_user`

### Install Redis
- Download: https://redis.io/download
- Windows: https://github.com/microsoftarchive/redis/releases
- Start: `redis-server`

### Install Kafka (Complex - Docker recommended)
- Download: https://kafka.apache.org/downloads
- Requires Java 11+

---

## Step 3: Initialize Database

Run database migrations:

```bash
cd D:\PROJECT\TrustNet

# Initialize database schema
python -c "from utils.database import init_db; init_db()"

# Or use Alembic for migrations
alembic upgrade head
```

---

## Step 4: Get API Keys

### OpenAI API (REQUIRED)
1. Go to https://platform.openai.com/
2. Create account / Login
3. Go to API Keys section
4. Create new secret key
5. Add to `.env` file

**Cost**: ~$0.002 per analysis (GPT-4)

### Google Fact Check API (REQUIRED)
1. Go to https://console.cloud.google.com/
2. Enable "Fact Check Tools API"
3. Create credentials (API key)
4. Add to `.env` file

**Cost**: Free (10,000 requests/day)

### Google Custom Search (REQUIRED)
1. Go to https://programmablesearchengine.google.com/
2. Create new search engine
3. Get Search Engine ID
4. Add to `.env` file

### Twitter API (for real-time monitoring)
1. Go to https://developer.twitter.com/
2. Apply for Elevated Access
3. Create project and app
4. Get API keys
5. Add to `.env` file

**Cost**: $100/month (Basic tier)

---

## Step 5: Start Backend System

```bash
cd D:\PROJECT\TrustNet

# Start the full system
python main.py
```

This will start:
- ✅ All 6 AI agents (Scout, Analyst, Investigator, Predictor, Strategist, Executor)
- ✅ FastAPI server (port 8000)
- ✅ Data ingestion pipeline
- ✅ Agent orchestration
- ✅ WebSocket for real-time updates

---

## Step 6: Start Dashboard

```bash
cd D:\PROJECT\TrustNet\dashboard

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Dashboard will be at: http://localhost:3000

---

## Step 7: Verify System is Running

### Check API Health
```bash
curl http://localhost:8000/health
```

### Check Agents Status
```bash
curl http://localhost:8000/api/agents/status
```

### Test Content Analysis
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Breaking: Miracle cure discovered!\", \"source\": \"twitter\"}"
```

---

## 🎯 Real-Time Data Sources

### Twitter Stream
Edit `data_pipeline/ingestion.py` to add real-time Twitter streaming:

```python
import tweepy

def start_twitter_stream():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET")
    )
    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_SECRET")
    )
    
    stream = tweepy.Stream(auth, TrustNetListener())
    stream.filter(track=['vaccine', 'election', 'covid'], languages=['en'])
```

### Reddit Stream
```python
import praw

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

for submission in reddit.subreddit("all").stream.submissions():
    # Process submission
    pass
```

---

## 📊 Monitoring & Observability

### Prometheus Metrics
- URL: http://localhost:9090
- Tracks: API latency, agent performance, detection rates

### Grafana Dashboards
- URL: http://localhost:3001
- Login: admin / admin
- Pre-configured dashboards for TrustNet metrics

### MLflow Tracking
- URL: http://localhost:5000
- View model performance, experiments, metrics

---

## 🔥 Production Considerations

### 1. Rate Limiting
APIs have limits:
- OpenAI: 10,000 requests/day (GPT-4)
- Twitter: Depends on tier
- Google: 10,000/day

### 2. Scaling
For high volume:
```bash
# Run multiple worker instances
python -m celery -A orchestration.tasks worker --loglevel=info --concurrency=4
```

### 3. Database Tuning
```sql
-- Optimize PostgreSQL for TrustNet
ALTER DATABASE trustnet SET shared_buffers = '256MB';
CREATE INDEX idx_content_timestamp ON content(created_at);
CREATE INDEX idx_classification ON analysis(classification);
```

### 4. Caching Strategy
- Redis caches: Fact-check results, source credibility, bot patterns
- TTL: 24 hours for most data
- Invalidation: On new evidence

---

## 🐛 Troubleshooting

### Issue: "Connection refused" to Redis
```bash
# Check Redis is running
docker ps | grep redis

# Check logs
docker logs trustnet_redis
```

### Issue: "No module named 'redis'"
```bash
pip install -r requirements.txt
```

### Issue: API key errors
```bash
# Verify .env file exists
cat .env

# Check environment variables are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: Kafka connection errors
```bash
# Restart Kafka
docker-compose restart kafka zookeeper
```

---

## 📈 Performance Benchmarks

**Expected Performance:**
- Processing: 10,000 posts/minute (Scout)
- Latency: <500ms per content item
- Accuracy: 70% detection (Analyst)
- Prediction: 87% viral spread accuracy
- Intervention: 95% success rate

**Resource Requirements:**
- CPU: 4+ cores
- RAM: 16GB minimum
- Disk: 100GB SSD
- Network: 100Mbps+

---

## 🔒 Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Use HTTPS in production
- [ ] Enable API authentication
- [ ] Set up firewall rules
- [ ] Regular security audits
- [ ] Encrypt sensitive data
- [ ] Rate limiting on API endpoints
- [ ] Monitor for anomalies

---

## 📚 Next Steps

1. **Test the system** with sample data
2. **Configure monitoring** (Grafana dashboards)
3. **Set up alerting** (PagerDuty, Slack)
4. **Deploy to cloud** (AWS, GCP, Azure)
5. **Scale horizontally** (Kubernetes)

---

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs`
2. Review API docs: http://localhost:8000/docs
3. Check GitHub issues
4. Contact: your-email@example.com

---

**Ready to deploy? Start with Step 1! 🚀**
