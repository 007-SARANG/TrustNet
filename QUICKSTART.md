# TrustNet 2.0 - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clone and Setup

```bash
git clone https://github.com/yourusername/trustnet-2.0.git
cd trustnet-2.0

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys (at minimum):
# - OPENAI_API_KEY (for GPT-4 analysis)
# - TWITTER_API_KEY (optional, for live streaming)
```

### Step 3: Start Infrastructure

```bash
# Start Docker services (PostgreSQL, Redis, Kafka)
docker-compose up -d

# Wait for services to be ready (~30 seconds)
```

### Step 4: Run Demo

```bash
# Test the system with sample data
python scripts/demo.py
```

You should see:
- 3 test cases processed
- Complete pipeline execution
- Final metrics display

### Step 5: Start API Server

```bash
# Start the main application
python main.py
```

The system will start:
- API Server: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📡 Test the API

### Using curl:

```bash
# Submit content for analysis
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Breaking: Vaccine causes infertility!",
    "source": "twitter"
  }'

# Get metrics
curl "http://localhost:8000/api/metrics"
```

### Using Python:

```python
import requests

response = requests.post('http://localhost:8000/api/analyze', json={
    'text': 'Breaking news: Vaccine causes infertility!',
    'source': 'twitter'
})

print(response.json())
```

## 🎯 Next Steps

1. **Configure Real Data Sources**: Add Twitter/Reddit API keys in `.env`
2. **Customize Agents**: Modify thresholds in `config/config.py`
3. **Train Models**: Fine-tune RoBERTa on your dataset
4. **Deploy Dashboard**: See `dashboard/README.md`

## 🔧 Troubleshooting

**Issue**: Docker services won't start
```bash
# Check if ports are available
docker ps
# Stop conflicting services
docker-compose down
```

**Issue**: Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Redis connection failed
```bash
# Check Redis is running
docker-compose ps
# Restart if needed
docker-compose restart redis
```

## 📚 Learn More

- [Full Documentation](docs/ARCHITECTURE.md)
- [API Reference](http://localhost:8000/docs)
- [Contributing Guide](CONTRIBUTING.md)

## 💬 Get Help

- Open an issue on GitHub
- Join our Discord community
- Email: support@trustnet-ai.com

Happy detecting! 🛡️
