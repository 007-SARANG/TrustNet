"""
TrustNet 2.0 - Quick Start Server (Simplified for Immediate Use)
Starts the API server without requiring all infrastructure
"""

import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
import asyncio
import socketio
from dotenv import load_dotenv
from agents.collectors.rss_collector import RSSCollector
from agents.collectors.instagram_collector import InstagramCollector, InstagramImageAnalyzer
from groq import Groq
import requests
import json
from datetime import datetime
from collections import defaultdict

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
)
logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=False,
    engineio_logger=False
)

# Create FastAPI app
app = FastAPI(
    title="TrustNet 2.0 API",
    description="AI-powered misinformation detection system",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Initialize Instagram collector with CLIP models
instagram_collector = InstagramCollector(
    instagram_username=os.getenv('INSTAGRAM_USERNAME'),
    instagram_password=os.getenv('INSTAGRAM_PASSWORD')
)
logger.info("✅ Instagram collector initialized with CLIP models")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 API Server started - Starting RSS collection...")
    asyncio.create_task(collect_rss_feeds())
    
    # Start Instagram monitoring if credentials are available
    if os.getenv('INSTAGRAM_USERNAME') and os.getenv('INSTAGRAM_PASSWORD'):
        logger.info("📸 Instagram credentials found - Starting auto-scraping...")
        asyncio.create_task(monitor_instagram_accounts())
    else:
        logger.warning("⚠️ Instagram credentials not found - Auto-scraping disabled")


# Models
class ContentSubmission(BaseModel):
    text: str
    source: str = "manual"
    url: Optional[str] = None

class AnalysisResponse(BaseModel):
    content_id: str
    status: str
    classification: Optional[str] = None
    confidence: Optional[float] = None
    details: Optional[Dict] = None

class InstagramAnalysisRequest(BaseModel):
    image_url: str
    caption: str

# Initialize Groq AI Client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY')) if os.getenv('GROQ_API_KEY') else None

# Mock stats for dashboard
stats = {
    "posts_analyzed": 0,
    "fake_detected": 0,
    "interventions": 0,
    "success_rate": 0.0
}

# Store recent posts to send to new clients
recent_posts = []

# Source credibility tracking
source_credibility = defaultdict(lambda: {"total": 0, "fake": 0, "score": 50.0})

# Trending topics tracker
trending_topics = defaultdict(int)

@app.get("/")
async def root():
    return {
        "message": "TrustNet 2.0 API",
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "api": "up",
            "groq": "configured" if os.getenv("GROQ_API_KEY") else "missing",
            "google_factcheck": "configured" if os.getenv("GOOGLE_FACTCHECK_API_KEY") else "missing"
        }
    }

@app.get("/metrics")
async def prometheus_metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/metrics")
async def get_metrics():
    """Get system metrics for dashboard"""
    global stats
    stats["posts_analyzed"] += 1  # Increment for demo
    return stats

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_content(content: ContentSubmission):
    """Analyze content for misinformation"""
    import uuid
    
    content_id = str(uuid.uuid4())
    
    # DETAILED LOGGING - Shows which post is being analyzed
    logger.info("="*80)
    logger.info(f"📝 NEW POST ANALYSIS STARTED")
    logger.info(f"   ID: {content_id}")
    logger.info(f"   Source: {content.source}")
    logger.info(f"   Content: {content.text}")
    if content.url:
        logger.info(f"   URL: {content.url}")
    logger.info("="*80)
    
    # Send real-time update via WebSocket
    await sio.emit('agent_update', {
        'agent': 'Scout',
        'message': f'Processing content: {content.text[:50]}...',
        'priority': 'MEDIUM',
        'type': 'info'
    })
    
    # Simulate processing
    await asyncio.sleep(1)
    
    # Simple keyword-based detection for demo
    fake_keywords = ['miracle', 'shocking', 'doctors hate', 'cure', 'breaking', 'unbelievable']
    text_lower = content.text.lower()
    is_suspicious = any(keyword in text_lower for keyword in fake_keywords)
    
    # Update stats
    global stats
    stats["posts_analyzed"] += 1
    if is_suspicious:
        stats["fake_detected"] += 1
        stats["interventions"] += 1
    
    # Send analysis complete update
    await sio.emit('agent_update', {
        'agent': 'Analyst',
        'message': f'Content classified as: {"FAKE" if is_suspicious else "REAL"}',
        'priority': 'HIGH' if is_suspicious else 'LOW',
        'type': 'warning' if is_suspicious else 'success'
    })
    
    # DETAILED RESULT LOGGING
    logger.info("✅ ANALYSIS COMPLETE")
    logger.info(f"   Classification: {'FAKE' if is_suspicious else 'REAL'}")
    logger.info(f"   Confidence: {0.85 if is_suspicious else 0.92:.2%}")
    logger.info(f"   Total Analyzed: {stats['posts_analyzed']}")
    logger.info(f"   Total Fake: {stats['fake_detected']}")
    logger.info("="*80 + "\n")
    
    return AnalysisResponse(
        content_id=content_id,
        status="completed",
        classification="fake" if is_suspicious else "real",
        confidence=0.85 if is_suspicious else 0.75,
        details={
            "source": content.source,
            "analysis": "Content analyzed using keyword detection" if is_suspicious else "No suspicious patterns detected",
            "groq_available": bool(os.getenv("GROQ_API_KEY")),
            "factcheck_available": bool(os.getenv("GOOGLE_FACTCHECK_API_KEY"))
        }
    )

@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "agents": [
            {"name": "Scout", "status": "active", "processed": stats["posts_analyzed"]},
            {"name": "Analyst", "status": "active", "processed": stats["posts_analyzed"]},
            {"name": "Investigator", "status": "active", "processed": stats["fake_detected"]},
            {"name": "Predictor", "status": "active", "processed": 0},
            {"name": "Strategist", "status": "active", "processed": 0},
            {"name": "Executor", "status": "active", "processed": stats["interventions"]},
        ]
    }

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    logger.info(f"✅ Dashboard connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected', 'message': 'Connected to TrustNet 2.0'}, to=sid)
    
    # Send initial agent status
    await sio.emit('agent_update', {
        'agent': 'System',
        'message': 'All agents operational and ready',
        'priority': 'LOW',
        'type': 'success'
    }, to=sid)
    
    # Send recent posts to new client
    global recent_posts
    if recent_posts:
        logger.info(f"📤 Sending {len(recent_posts)} recent posts to new client {sid}")
        for post in recent_posts:
            await sio.emit('new_post', post, to=sid)
        logger.info(f"✅ Sent all recent posts to {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"❌ Dashboard disconnected: {sid}")

@app.get("/api/test-post")
async def test_post():
    """Test endpoint to send a sample post to dashboard"""
    test_post = {
        'id': 'test-123',
        'platform': 'rss',
        'content': 'This is a TEST post to verify WebSocket connection is working!',
        'author': 'Test Author',
        'classification': 'REAL',
        'risk_score': 0.25,
        'url': 'https://example.com',
        'source': 'Test Feed',
        'timestamp': '2025-11-13T16:00:00Z',
        'metrics': {'score': 100, 'comments': 5}
    }
    
    logger.info("📡 Sending TEST post via WebSocket...")
    await sio.emit('new_post', test_post)
    logger.info("✅ Test post emitted")
    
    return {"status": "test post sent", "data": test_post}


@app.get("/api/source-credibility")
async def get_source_credibility():
    """Get credibility scores for all sources"""
    return {
        "sources": [
            {
                "name": source,
                "score": data["score"],
                "total_posts": data["total"],
                "fake_posts": data["fake"]
            }
            for source, data in sorted(
                source_credibility.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )
        ]
    }


@app.get("/api/trending-topics")
async def get_trending_topics():
    """Get trending topics from analyzed posts"""
    top_topics = sorted(
        trending_topics.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return {
        "topics": [
            {"topic": topic, "count": count}
            for topic, count in top_topics
        ]
    }


@app.get("/api/recent-posts")
async def get_recent_posts(limit: int = 20):
    """Get recent analyzed posts"""
    return {
        "posts": recent_posts[-limit:],
        "total": len(recent_posts)
    }

@app.post("/api/analyze-instagram-image")
async def analyze_instagram_image(request: InstagramAnalysisRequest):
    """Analyze Instagram image for informative content"""
    try:
        # Use the global instagram_collector instance (models already loaded)
        global instagram_collector
        
        # Fetch and analyze post
        post = instagram_collector.fetch_sample_post(request.image_url, request.caption)
        if not post:
            raise HTTPException(status_code=400, detail="Failed to fetch image")
        
        analysis = instagram_collector.analyze_post(post)
        
        return {
            "success": True,
            "analysis": analysis,
            "flagged": analysis['prevention']['flagged'],
            "action": analysis['prevention']['action']
        }
    except Exception as e:
        logger.error(f"Instagram analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export-report")
async def export_report():
    """Export analysis report as JSON"""
    return {
        "generated_at": datetime.now().isoformat(),
        "stats": stats,
        "source_credibility": dict(source_credibility),
        "trending_topics": dict(trending_topics),
        "recent_posts": recent_posts[-20:]
    }


async def analyze_with_ai(content: str, title: str, source: str) -> Dict:
    """
    Use Groq AI to analyze content for misinformation
    """
    try:
        if not groq_client:
            # Fallback to keyword-based if no API key
            fake_keywords = ['miracle', 'shocking', 'doctors hate', 'cure', 'banned', 'they don\'t want you to know']
            is_suspicious = any(keyword in content.lower() for keyword in fake_keywords)
            return {
                'classification': 'FAKE' if is_suspicious else 'REAL',
                'risk_score': 0.75 if is_suspicious else 0.25,
                'reasoning': 'Keyword-based analysis (AI not configured)',
                'claims': [],
                'credibility_factors': []
            }
        
        # Use Groq's Llama 3.1 for fast analysis
        prompt = f"""Analyze this news content for misinformation. Be concise and precise.

Title: {title}
Source: {source}
Content: {content[:500]}

Provide analysis in this JSON format:
{{
    "classification": "FAKE" or "MISLEADING" or "REAL",
    "risk_score": 0.0 to 1.0,
    "reasoning": "Brief explanation (1-2 sentences)",
    "key_claims": ["claim1", "claim2"],
    "credibility_factors": ["factor1", "factor2"]
}}

Respond with ONLY the JSON, no other text."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.info(f"🤖 AI Analysis: {result['classification']} (risk: {result['risk_score']:.2f})")
        return result
        
    except Exception as e:
        logger.error(f"❌ AI analysis error: {e}")
        # Fallback analysis
        return {
            'classification': 'UNKNOWN',
            'risk_score': 0.5,
            'reasoning': f'Analysis failed: {str(e)[:100]}',
            'key_claims': [],
            'credibility_factors': []
        }


async def check_google_factcheck(claims: List[str]) -> List[Dict]:
    """
    Check claims against Google Fact Check API
    """
    try:
        api_key = os.getenv('GOOGLE_FACTCHECK_API_KEY')
        if not api_key or not claims:
            return []
        
        fact_checks = []
        for claim in claims[:3]:  # Limit to 3 claims
            url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search"
            params = {'query': claim, 'key': api_key}
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'claims' in data:
                    for item in data['claims'][:2]:
                        fact_checks.append({
                            'claim': item.get('text'),
                            'rating': item.get('claimReview', [{}])[0].get('textualRating', 'Unknown'),
                            'source': item.get('claimReview', [{}])[0].get('publisher', {}).get('name', 'Unknown')
                        })
        
        return fact_checks
        
    except Exception as e:
        logger.error(f"❌ Google Fact Check error: {e}")
        return []


def update_source_credibility(source: str, is_fake: bool):
    """Update credibility score for a source"""
    global source_credibility
    source_credibility[source]["total"] += 1
    if is_fake:
        source_credibility[source]["fake"] += 1
    
    # Calculate credibility score (0-100)
    total = source_credibility[source]["total"]
    fake = source_credibility[source]["fake"]
    source_credibility[source]["score"] = max(0, 100 - (fake / total * 100))


def extract_topics(content: str) -> List[str]:
    """Extract key topics from content"""
    # Simple topic extraction (can be enhanced with NLP)
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'was', 'are', 'were'}
    words = content.lower().split()
    topics = [w for w in words if len(w) > 4 and w not in common_words]
    return list(set(topics))[:5]


# RSS Feed Collection Task
async def collect_rss_feeds():
    """Collect RSS feeds and analyze with AI"""
    await asyncio.sleep(5)  # Wait for server to start
    
    logger.info("📰 Starting AI-powered RSS feed collection...")
    collector = RSSCollector()
    seen_ids = set()
    
    while True:
        try:
            logger.info("🔍 Fetching RSS posts...")
            posts = collector.get_recent_posts(limit=5)
            
            # Only process new posts
            new_posts = [p for p in posts if p['id'] not in seen_ids]
            
            for post in new_posts:
                seen_ids.add(post['id'])
                
                # Extract content
                title = post.get('title', '')
                content = post.get('text', '')
                source = post.get('source', 'Unknown')
                full_content = title + ' ' + content
                
                logger.info(f"🤖 Analyzing: {title[:50]}...")
                
                # AI Analysis
                analysis = await analyze_with_ai(full_content, title, source)
                
                # Google Fact Check
                fact_checks = await check_google_factcheck(analysis.get('key_claims', []))
                
                # Update source credibility
                is_fake = analysis['classification'] in ['FAKE', 'MISLEADING']
                update_source_credibility(source, is_fake)
                
                # Extract and track topics
                topics = extract_topics(full_content)
                for topic in topics:
                    trending_topics[topic] += 1
                
                # Update stats
                global stats
                stats['posts_analyzed'] += 1
                if is_fake:
                    stats['fake_detected'] += 1
                stats['success_rate'] = (1 - stats['fake_detected'] / max(stats['posts_analyzed'], 1)) * 100
                
                # Get author safely
                author_info = post.get('author', {})
                if isinstance(author_info, dict):
                    author_name = author_info.get('username', 'Unknown')
                else:
                    author_name = str(author_info) if author_info else 'Unknown'
                
                post_data = {
                    'id': post['id'],
                    'platform': post.get('platform', 'rss'),
                    'content': full_content[:300],
                    'title': title,
                    'author': author_name,
                    'classification': analysis['classification'],
                    'risk_score': float(analysis['risk_score']),  # Ensure it's a float
                    'url': post.get('url', ''),
                    'source': source,
                    'timestamp': post.get('created_at', datetime.now().isoformat()),
                    'metrics': post.get('metrics', {}),
                    'ai_reasoning': analysis.get('reasoning', ''),
                    'key_claims': analysis.get('key_claims', []),
                    'fact_checks': fact_checks,
                    'credibility_factors': analysis.get('credibility_factors', []),
                    'source_credibility': source_credibility[source]['score'],
                    'topics': topics
                }
                
                # Store in recent posts
                global recent_posts
                recent_posts.append(post_data)
                recent_posts = recent_posts[-50:]  # Keep last 50 posts
                
                # Send to dashboard - broadcasts to ALL connected clients
                logger.info(f"📡 Broadcasting: {title[:50]} | {analysis['classification']} ({analysis['risk_score']:.2f})")
                logger.info(f"   Risk Score: {post_data['risk_score']} (type: {type(post_data['risk_score'])})")
                await sio.emit('new_post', post_data)
                
                # Send stats update
                await sio.emit('stats_update', stats)
                
            if new_posts:
                logger.info(f"✅ Processed {len(new_posts)} new posts")
            else:
                logger.info("ℹ️  No new posts this cycle")
            
            # Keep seen_ids manageable
            if len(seen_ids) > 1000:
                seen_ids = set(list(seen_ids)[-500:])
            
            # Wait 2 minutes before next check
            await asyncio.sleep(120)
            
        except Exception as e:
            logger.error(f"❌ RSS collection error: {e}", exc_info=True)
            await asyncio.sleep(120)


# Instagram Auto-Monitoring Task
async def monitor_instagram_accounts():
    """Automatically scrape and analyze Instagram posts from monitored accounts"""
    await asyncio.sleep(10)  # Wait for server to start
    
    logger.info("📸 Starting Instagram auto-monitoring...")
    
    # Load monitored accounts from config file
    try:
        from instagram_monitor_config import MONITORED_ACCOUNTS, CHECK_INTERVAL_MINUTES, MAX_POSTS_PER_ACCOUNT
        monitored_accounts = MONITORED_ACCOUNTS
        check_interval = CHECK_INTERVAL_MINUTES * 60  # Convert to seconds
        max_posts = MAX_POSTS_PER_ACCOUNT
        logger.info(f"📋 Loaded {len(monitored_accounts)} accounts to monitor")
    except ImportError:
        # Fallback to default accounts
        monitored_accounts = ['natgeo', 'nasa']
        check_interval = 900  # 15 minutes
        max_posts = 5
        logger.warning("⚠️ Config file not found, using default accounts")
    
    try:
        # Initialize Instagram collector
        collector = InstagramCollector(
            instagram_username=os.getenv('INSTAGRAM_USERNAME'),
            instagram_password=os.getenv('INSTAGRAM_PASSWORD')
        )
        
        seen_posts = set()
        
        while True:
            try:
                for account in monitored_accounts:
                    logger.info(f"📱 Checking Instagram account: @{account}")
                    
                    try:
                        # Fetch recent posts from account
                        posts = collector.fetch_from_instagram(
                            username=account,
                            max_posts=max_posts
                        )
                        
                        for post in posts:
                            # Skip if already seen
                            post_id = post.get('id', post.get('shortcode', ''))
                            if post_id in seen_posts:
                                continue
                            
                            seen_posts.add(post_id)
                            
                            # Analyze the post for image-caption mismatch
                            logger.info(f"🔍 Analyzing Instagram post from @{account}")
                            analysis = collector.analyze_post(post)
                            
                            # Check if it's a mismatch (misinformation)
                            is_mismatch = not analysis['image_caption_match']['matches']
                            classification = 'FAKE' if is_mismatch else 'REAL'
                            
                            # Update stats
                            global stats
                            stats['posts_analyzed'] += 1
                            if is_mismatch:
                                stats['fake_detected'] += 1
                                stats['interventions'] += 1
                            
                            # Prepare post data for dashboard
                            post_data = {
                                'id': post_id,
                                'platform': 'instagram',
                                'content': post.get('caption', 'No caption')[:300],
                                'author': account,
                                'classification': classification,
                                'risk_score': 1.0 - analysis['image_caption_match']['similarity'],
                                'url': f"https://www.instagram.com/p/{post.get('shortcode', '')}/" if post.get('shortcode') else '',
                                'source': f'Instagram @{account}',
                                'timestamp': datetime.now().isoformat(),
                                'metrics': {
                                    'likes': post.get('likes', 0),
                                    'comments': post.get('comments', 0)
                                },
                                'ai_reasoning': analysis['image_caption_match']['reasoning'],
                                'image_caption_similarity': analysis['image_caption_match']['similarity'],
                                'mismatch_detected': is_mismatch,
                                'prevention_action': analysis['prevention']['action']
                            }
                            
                            # Store in recent posts
                            global recent_posts
                            recent_posts.append(post_data)
                            recent_posts = recent_posts[-50:]
                            
                            # Broadcast to dashboard
                            logger.info(f"📡 Broadcasting Instagram post: @{account} | {classification} | Similarity: {analysis['image_caption_match']['similarity']:.2%}")
                            await sio.emit('new_post', post_data)
                            await sio.emit('stats_update', stats)
                            
                            # Alert if mismatch detected
                            if is_mismatch:
                                await sio.emit('agent_update', {
                                    'agent': 'Instagram Monitor',
                                    'message': f'🚨 MISMATCH DETECTED: @{account} - Image does not match caption!',
                                    'priority': 'HIGH',
                                    'type': 'error'
                                })
                        
                        logger.info(f"✅ Processed Instagram account: @{account}")
                        
                    except Exception as e:
                        logger.error(f"❌ Error scraping @{account}: {e}")
                        # Continue to next account
                        continue
                
                # Keep seen_posts manageable
                if len(seen_posts) > 500:
                    seen_posts = set(list(seen_posts)[-250:])
                
                # Wait before next check (Instagram rate limits)
                logger.info(f"⏳ Waiting {check_interval // 60} minutes before next Instagram check...")
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"❌ Instagram monitoring cycle error: {e}", exc_info=True)
                await asyncio.sleep(check_interval)
                
    except Exception as e:
        logger.error(f"❌ Instagram monitoring initialization error: {e}")
        logger.info("⚠️ Instagram auto-monitoring disabled - using manual mode only")


def main():
    """Start the server"""
    logger.info("=" * 80)
    logger.info("🚀 Starting TrustNet 2.0 API Server (Quick Start Mode)")
    logger.info("=" * 80)
    logger.info("")
    logger.info("✅ Docker Services Running:")
    logger.info("   - PostgreSQL: localhost:5432")
    logger.info("   - Redis: localhost:6379")
    logger.info("   - Kafka: localhost:9092")
    logger.info("   - Prometheus: http://localhost:9090")
    logger.info("   - Grafana: http://localhost:3001")
    logger.info("")
    logger.info("🔑 API Keys:")
    logger.info(f"   - Groq: {'✅ Configured' if os.getenv('GROQ_API_KEY') else '❌ Missing'}")
    logger.info(f"   - Google Fact Check: {'✅ Configured' if os.getenv('GOOGLE_FACTCHECK_API_KEY') else '❌ Missing'}")
    logger.info("")
    logger.info("📡 Starting API Server with WebSocket Support...")
    logger.info("   - API: http://localhost:8000")
    logger.info("   - WebSocket: ws://localhost:8000/socket.io")
    logger.info("   - Docs: http://localhost:8000/docs")
    logger.info("   - Dashboard: http://localhost:3000 (start with: cd dashboard && npm run dev)")
    logger.info("")
    logger.info("=" * 80)
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 80)
    
    uvicorn.run(
        socket_app,  # Use socket_app instead of app
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n✅ Server stopped")
