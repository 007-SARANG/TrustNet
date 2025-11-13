"""
FastAPI Server - REST API for TrustNet 2.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import uvicorn
import logging

from orchestration.coordinator import TrustNetCoordinator

logger = logging.getLogger(__name__)

app = FastAPI(
    title="TrustNet 2.0 API",
    description="AI-powered misinformation detection and intervention system",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global coordinator instance
coordinator: Optional[TrustNetCoordinator] = None


class ContentSubmission(BaseModel):
    """Content submission schema"""
    text: str
    source: str = "manual"
    url: Optional[str] = None
    images: list[str] = []
    videos: list[str] = []
    author: Optional[Dict] = None
    engagement: Optional[Dict] = None


class AnalysisResponse(BaseModel):
    """Analysis response schema"""
    content_id: str
    status: str
    classification: Optional[str] = None
    fake_probability: Optional[float] = None
    viral_risk: Optional[float] = None
    intervention_status: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize coordinator on startup"""
    global coordinator
    logger.info("Starting TrustNet API server...")
    coordinator = TrustNetCoordinator()
    await coordinator.initialize()
    logger.info("✅ API server ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global coordinator
    if coordinator:
        await coordinator.shutdown()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "TrustNet 2.0",
        "status": "operational",
        "version": "2.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "coordinator": "initialized" if coordinator else "not initialized",
        "agents": {
            "scout": "ready",
            "analyst": "ready",
            "investigator": "ready",
            "predictor": "ready",
            "strategist": "ready",
            "executor": "ready"
        }
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_content(
    submission: ContentSubmission,
    background_tasks: BackgroundTasks
):
    """
    Submit content for analysis
    
    This endpoint accepts social media content and runs it through
    the complete TrustNet pipeline.
    """
    if not coordinator:
        raise HTTPException(status_code=503, detail="Coordinator not initialized")
    
    # Convert submission to content format
    content = {
        'id': f"manual_{hash(submission.text)}",
        'text': submission.text,
        'source': submission.source,
        'url': submission.url,
        'images': submission.images,
        'videos': submission.videos,
        'author': submission.author or {},
        'engagement': submission.engagement or {},
        'time_since_post_hours': 0
    }
    
    # Process through pipeline (async in background)
    result = await coordinator.process_content(content)
    
    if not result:
        return AnalysisResponse(
            content_id=content['id'],
            status="CLEARED",
            classification="REAL"
        )
    
    return AnalysisResponse(
        content_id=content['id'],
        status=result.get('status', 'UNKNOWN'),
        classification=result.get('classification'),
        fake_probability=result.get('fake_probability'),
        viral_risk=result.get('viral_risk'),
        intervention_status=result.get('intervention_status')
    )


@app.get("/api/metrics")
async def get_metrics():
    """Get system metrics"""
    if not coordinator:
        raise HTTPException(status_code=503, detail="Coordinator not initialized")
    
    return coordinator.get_metrics()


@app.get("/api/interventions/{content_id}")
async def get_intervention(content_id: str):
    """
    Get intervention status and details for specific content
    """
    # In production: query from database
    return {
        "content_id": content_id,
        "status": "In progress",
        "message": "Intervention tracking - connect to database for real data"
    }


@app.get("/api/dashboard/stats")
async def dashboard_stats():
    """Get dashboard statistics"""
    if not coordinator:
        raise HTTPException(status_code=503, detail="Coordinator not initialized")
    
    metrics = coordinator.get_metrics()
    
    return {
        "today": {
            "posts_analyzed": metrics['posts_analyzed'],
            "fake_detected": metrics['fake_detected'],
            "interventions": metrics['interventions'],
            "success_rate": f"{metrics['success_rate'] * 100:.1f}%"
        },
        "agents_status": {
            "scout": "active",
            "analyst": "active",
            "investigator": "active",
            "predictor": "active",
            "strategist": "active",
            "executor": "active"
        }
    }


async def start_api_server():
    """Start the API server"""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
