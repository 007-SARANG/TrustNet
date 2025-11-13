"""
TrustNet 2.0 - Main Entry Point
Orchestrates all agents and starts the complete real-time system
"""

import asyncio
import logging
import sys
from dotenv import load_dotenv
from pathlib import Path

from utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()


async def main():
    """Main entry point for TrustNet 2.0 - Real-Time Production System"""
    
    logger.info("=" * 80)
    logger.info("🚀 Starting TrustNet 2.0: Real-Time Misinformation Detection System")
    logger.info("=" * 80)
    
    try:
        # Import here to avoid circular imports and check dependencies
        from orchestration.coordinator import TrustNetCoordinator
        from api.server import start_api_server
        from data_pipeline.ingestion import start_data_ingestion
        
        # Initialize coordinator
        logger.info("📋 Initializing TrustNet Coordinator...")
        coordinator = TrustNetCoordinator()
        await coordinator.initialize()
        logger.info("✅ Coordinator initialized")
        
        # Start data ingestion pipeline (Twitter, Reddit, etc.)
        logger.info("📡 Starting real-time data ingestion pipeline...")
        ingestion_task = asyncio.create_task(start_data_ingestion())
        logger.info("✅ Data ingestion started")
        
        # Start API server
        logger.info("🌐 Starting FastAPI server...")
        api_task = asyncio.create_task(start_api_server())
        logger.info("✅ API server started")
        
        # Start agent orchestration
        logger.info("🤖 Starting 6-agent orchestration system...")
        orchestration_task = asyncio.create_task(coordinator.run())
        logger.info("✅ Agent orchestration started")
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("✨ TrustNet 2.0 is now LIVE and processing real-time data!")
        logger.info("=" * 80)
        logger.info("📊 Dashboard:    http://localhost:3000")
        logger.info("📚 API Docs:     http://localhost:8000/docs")
        logger.info("📈 Metrics:      http://localhost:8000/api/metrics")
        logger.info("🔍 Prometheus:   http://localhost:9090")
        logger.info("📉 Grafana:      http://localhost:3001")
        logger.info("🧪 MLflow:       http://localhost:5000")
        logger.info("=" * 80)
        logger.info("")
        logger.info("👁️  Monitoring:")
        logger.info("   - Scout Agent: Content monitoring (10K posts/min)")
        logger.info("   - Analyst Agent: Multi-modal classification")
        logger.info("   - Investigator: Fact-checking & evidence")
        logger.info("   - Predictor: Viral spread forecasting")
        logger.info("   - Strategist: Intervention planning")
        logger.info("   - Executor: Real-time interventions")
        logger.info("")
        logger.info("Press Ctrl+C to stop the system")
        logger.info("=" * 80)
        
        # Wait for all tasks
        await asyncio.gather(
            ingestion_task,
            api_task,
            orchestration_task,
            return_exceptions=True
        )
        
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 80)
        logger.info("⚠️  Shutting down TrustNet 2.0...")
        logger.info("=" * 80)
        
        # Graceful shutdown
        if 'coordinator' in locals():
            logger.info("🛑 Stopping agents...")
            await coordinator.shutdown()
        
        logger.info("✅ All services stopped")
        logger.info("✅ Shutdown complete. Goodbye!")
        logger.info("=" * 80)
        
    except ImportError as e:
        logger.error("=" * 80)
        logger.error("❌ DEPENDENCY ERROR")
        logger.error("=" * 80)
        logger.error(f"Missing dependency: {e}")
        logger.error("")
        logger.error("Please ensure:")
        logger.error("1. All Python packages are installed: pip install -r requirements.txt")
        logger.error("2. Infrastructure services are running: docker-compose up -d")
        logger.error("3. Environment variables are set in .env file")
        logger.error("")
        logger.error("See PRODUCTION_SETUP.md for detailed instructions")
        logger.error("=" * 80)
        sys.exit(1)
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error("❌ FATAL ERROR")
        logger.error("=" * 80)
        logger.error(f"Error: {e}", exc_info=True)
        logger.error("")
        logger.error("Troubleshooting:")
        logger.error("1. Check if Redis is running: docker ps | grep redis")
        logger.error("2. Check if PostgreSQL is running: docker ps | grep postgres")
        logger.error("3. Check if Kafka is running: docker ps | grep kafka")
        logger.error("4. Review logs: docker-compose logs")
        logger.error("")
        logger.error("See PRODUCTION_SETUP.md for help")
        logger.error("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
