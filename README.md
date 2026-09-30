# TrustNet 2.0: Agentic AI Misinformation Detection & Intervention System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

TrustNet is a research and hackathon prototype for exploring a multi-agent misinformation analysis workflow. The repository describes a six-agent architecture, but it does not provide reproducible end-to-end benchmarks or evidence for production-scale automated interventions. Treat the architecture and integrations as a prototype until the implementation and evaluation are independently verified.

## 🏆 Key Features

- **Multimodal Analysis**: Text, image, and video deepfake detection
- **Proactive Prevention**: Includes a proposed viral-spread prediction component; no validated accuracy is reported
- **Processing**: No end-to-end latency benchmark is published
- **Continuous Learning**: RL-based agents that improve over time
- **Prototype Scope**: API and dashboard components are present; deployment readiness is not established

## 🤖 The Six Agents

### 1. Scout Agent - The Sentinel
Designed to monitor incoming posts, detect anomalies, filter spam, and flag suspicious content; throughput has not been benchmarked.

### 2. Analyst Agent - The Detective
Multi-modal classification using RoBERTa, CNN deepfake detection, CLIP cross-modal verification, and GPT-4 analysis.

### 3. Investigator Agent - The Fact-Checker
Searches fact-check databases, reverse image search, domain credibility checks, and evidence compilation.

### 4. Predictor Agent - The Oracle
GNN-based viral spread forecasting, bot detection, network analysis, and risk assessment.

### 5. Strategist Agent - The Tactician
RL-based (PPO) intervention planning, multi-action optimization, cost-benefit analysis.

### 6. Executor Agent - The Operator
Automated intervention execution, platform reporting, fact-check deployment, and outcome monitoring.

## 🏗️ Architecture

```
Data Sources → Kafka → Redis → Scout → Analyst → Investigator
                                           ↓
                                      Predictor → Strategist → Executor
                                                                    ↓
                                                              Dashboard
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Node.js 18+ (for dashboard)
- API Keys: Twitter, OpenAI GPT-4, Google Fact Check

### Installation

```bash
# Clone repository
git clone https://github.com/007-SARANG/TrustNet.git
cd trustnet-2.0

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start infrastructure (Kafka, Redis, PostgreSQL)
docker-compose up -d

# Initialize database
python scripts/init_db.py

# Start the system
python main.py
```

### Running the Dashboard

```bash
cd dashboard
npm install
npm start
# Open http://localhost:3000
```

## 📁 Project Structure

```
trustnet-2.0/
├── agents/                  # AI Agent implementations
│   ├── scout/              # Agent 1: Content monitoring
│   ├── analyst/            # Agent 2: Classification
│   ├── investigator/       # Agent 3: Fact-checking
│   ├── predictor/          # Agent 4: Viral forecasting
│   ├── strategist/         # Agent 5: Intervention planning
│   └── executor/           # Agent 6: Action execution
├── orchestration/          # LangGraph coordination
├── data_pipeline/          # Kafka/Redis ingestion
├── models/                 # ML models (RoBERTa, GNN, etc.)
├── dashboard/              # React frontend
├── api/                    # FastAPI backend
├── config/                 # Configuration files
├── tests/                  # Unit & integration tests
├── scripts/                # Utility scripts
└── docker/                 # Docker configurations
```

## 🔧 Configuration

Edit `config/config.yaml`:

```yaml
data_sources:
  twitter:
    enabled: true
    rate_limit: 5000
  reddit:
    enabled: true
    
agents:
  scout:
    priority_threshold: 0.7
  analyst:
    fake_threshold: 0.7
    
orchestration:
  max_concurrent_agents: 10
```

## 📊 Evaluation Status

The repository does not include reproducible end-to-end evidence for the previously listed accuracy, intervention, latency, or throughput figures. Those figures are withdrawn and should not be used to assess the system. Model-level metrics should be reported only alongside the dataset, split methodology, evaluation script, and measured results.

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific agent tests
pytest tests/agents/test_analyst.py

# Run integration tests
pytest tests/integration/
```

## 📚 API Documentation

Once running, visit:
- API Docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:3000`

### Example API Usage

```python
import requests

# Submit content for analysis
response = requests.post('http://localhost:8000/api/analyze', json={
    'text': 'Breaking: Vaccine causes infertility!',
    'source': 'twitter',
    'url': 'https://twitter.com/...'
})

# Get intervention status
response = requests.get('http://localhost:8000/api/interventions/tweet_123456')
```

## 🎓 How It Works

1. **Data Collection**: Streams from Twitter/Reddit/Telegram → Kafka queue
2. **Scout Agent**: Filters and flags suspicious content (priority scoring)
3. **Analyst Agent**: Multi-modal classification (text + image + video)
4. **Investigator Agent**: Searches fact-check databases, finds evidence
5. **Predictor Agent**: Builds network graph, forecasts viral spread
6. **Strategist Agent**: RL agent selects optimal intervention strategy
7. **Executor Agent**: Executes actions (bot throttling, fact-checks)
8. **Learning Loop**: Feeds outcomes back to improve all agents

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FakeNewsNet dataset for training data
- Twitter API for social media access
- OpenAI GPT-4 for advanced text analysis
- Hugging Face Transformers for RoBERTa models

## 📧 Contact

- **Team**: TrustNet AI
- **Email**: contact@trustnet-ai.com
- **Demo**: [https://demo.trustnet-ai.com](https://demo.trustnet-ai.com)

## 🏅 Hackathon Submission

This is a hackathon/research prototype. The repository’s architectural description is aspirational in places; component completeness, end-to-end tests, production readiness, and real-world intervention outcomes have not been established.

**Built with ❤️ by the TrustNet Team**
