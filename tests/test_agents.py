"""
Test Script - Unit tests for agents
"""

import pytest
import asyncio
from agents.scout import ScoutAgent
from agents.analyst import AnalystAgent


@pytest.mark.asyncio
async def test_scout_agent():
    """Test Scout Agent content filtering"""
    
    config = {'priority_threshold': 0.7}
    scout = ScoutAgent(config)
    
    # Test case 1: Suspicious content
    suspicious_content = {
        'id': 'test_001',
        'text': 'URGENT! Vaccine causes infertility! Share now!',
        'engagement': {'likes': 1000, 'retweets': 500},
        'time_since_post_hours': 1,
        'author': {'followers': 5000}
    }
    
    result = await scout.process_content(suspicious_content)
    assert result is not None
    assert result['priority_score'] >= 0.7
    assert result['priority_level'] in ['HIGH', 'MEDIUM']
    
    # Test case 2: Benign content
    benign_content = {
        'id': 'test_002',
        'text': 'Having coffee this morning',
        'engagement': {'likes': 5, 'retweets': 1},
        'time_since_post_hours': 24,
        'author': {'followers': 100}
    }
    
    result = await scout.process_content(benign_content)
    # Should not be flagged or have low priority
    assert result is None or result['priority_score'] < 0.7


@pytest.mark.asyncio
async def test_analyst_agent():
    """Test Analyst Agent classification"""
    
    config = {'fake_threshold': 0.7}
    analyst = AnalystAgent(config)
    
    # Test flagged content
    flagged_content = {
        'content_id': 'test_001',
        'text': 'Breaking: Vaccine causes serious side effects!',
        'images': [],
        'videos': []
    }
    
    result = await analyst.analyze_content(flagged_content)
    assert 'fake_probability' in result
    assert 'classification' in result
    assert result['classification'] in ['FAKE', 'REAL']


def test_imports():
    """Test that all agents can be imported"""
    from agents.scout import ScoutAgent
    from agents.analyst import AnalystAgent
    from agents.investigator import InvestigatorAgent
    from agents.predictor import PredictorAgent
    from agents.strategist import StrategistAgent
    from agents.executor import ExecutorAgent
    from orchestration.coordinator import TrustNetCoordinator
    
    assert ScoutAgent is not None
    assert AnalystAgent is not None
    assert InvestigatorAgent is not None
    assert PredictorAgent is not None
    assert StrategistAgent is not None
    assert ExecutorAgent is not None
    assert TrustNetCoordinator is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
