# 🚀 TrustNet 2.0 - Quick Start Checklist

## ✅ What You Have Completed

- [x] Got Google Fact Check API Key
- [x] Got Groq API Key (Better than OpenAI!)
- [x] Configured `.env` file
- [x] Installed Python dependencies

---

## 📋 What You Need to Do Next

### Option 1: Run WITHOUT Docker (Simplified Mode)
**Perfect for testing and development**

```bash
# 1. Start the backend (simplified mode)
python main.py

# 2. Start the dashboard (new terminal)
cd dashboard
npm install
npm run dev

# 3. Open browser
http://localhost:3000
```

**This will run in demo mode without real-time streaming**

---

### Option 2: Run WITH Docker (Full Production Mode)
**For real-time social media monitoring**

#### Step 1: Install Docker Desktop
- Download: https://www.docker.com/products/docker-desktop
- Install and restart computer
- Open Docker Desktop

#### Step 2: Start Infrastructure
```bash
# Start all services (PostgreSQL, Redis, Kafka, etc.)
docker-compose up -d

# Wait 30 seconds for services to start

# Check services are running
docker-compose ps
```

#### Step 3: Start TrustNet
```bash
# Start the backend
python main.py

# Start the dashboard (new terminal)
cd dashboard
npm install
npm run dev

# Open browser
http://localhost:3000
```

---

## 🎯 Recommended: Start with Option 1 (Without Docker)

**Why?**
- ✅ Faster to get started
- ✅ No Docker installation needed
- ✅ Works perfectly for testing
- ✅ Can add Docker later for production

**What will work:**
- ✅ Dashboard UI
- ✅ Manual content analysis
- ✅ All 6 AI agents
- ✅ Groq AI analysis
- ✅ Google Fact-checking
- ✅ Network visualization

**What won't work (yet):**
- ⏳ Real-time Twitter/Reddit streaming (need Docker + API keys)
- ⏳ Persistent database storage (uses in-memory)
- ⏳ Kafka message queue (not needed for testing)

---

## 🚀 Quick Start Commands

### Terminal 1: Start Backend
```bash
cd D:\PROJECT\TrustNet
python main.py
```

### Terminal 2: Start Dashboard
```bash
cd D:\PROJECT\TrustNet\dashboard
npm install
npm run dev
```

### Browser
```
http://localhost:3000
```

---

## 🧪 Test the System

Once both are running, try analyzing content:

1. Go to http://localhost:3000
2. Click on "Activity Feed" or "Dashboard"
3. Submit test content through the API:

```bash
curl -X POST http://localhost:8000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"BREAKING: Scientists discover miracle cure that doctors don't want you to know!\", \"source\": \"test\"}"
```

You should see:
- ✅ Fake content detection
- ✅ Fact-check results
- ✅ AI analysis from Groq
- ✅ Real-time updates in dashboard

---

## ❓ Which Option Do You Want?

**Choose one:**

1. **START NOW (Simplified)** → Run `python main.py`
2. **INSTALL DOCKER FIRST** → I'll guide you through Docker setup

Let me know and I'll help you! 🎉
