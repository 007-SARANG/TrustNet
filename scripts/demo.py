"""
Demo Script - Test TrustNet 2.0 with sample misinformation
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.coordinator import TrustNetCoordinator
from utils.logger import setup_logging

# Setup logging
logger = setup_logging()


# Sample test cases
TEST_CASES = [
    {
        'id': 'test_001',
        'text': 'BREAKING: New vaccine causes infertility in 90% of women! Share before this is deleted!',
        'source': 'twitter',
        'images': [],
        'videos': [],
        'author': {
            'id': 'user_123',
            'followers': 5000,
            'verified': False,
            'account_age_days': 45
        },
        'engagement': {
            'likes': 2500,
            'retweets': 1200,
            'comments': 450
        },
        'time_since_post_hours': 2,
        'description': 'Clear health misinformation with urgency markers'
    },
    {
        'id': 'test_002',
        'text': 'Study shows coffee reduces risk of heart disease by 15%',
        'source': 'twitter',
        'url': 'https://reuters.com/health/study-coffee',
        'author': {
            'id': 'reuters',
            'followers': 1000000,
            'verified': True,
            'account_age_days': 3650
        },
        'engagement': {
            'likes': 500,
            'retweets': 200,
            'comments': 50
        },
        'time_since_post_hours': 5,
        'description': 'Legitimate news from credible source'
    },
    {
        'id': 'test_003',
        'text': '5G towers are causing COVID-19 symptoms! Government cover-up exposed!',
        'source': 'twitter',
        'author': {
            'id': 'conspiracy_news',
            'followers': 15000,
            'verified': False,
            'account_age_days': 120
        },
        'engagement': {
            'likes': 8000,
            'retweets': 4500,
            'comments': 1200
        },
        'time_since_post_hours': 6,
        'description': 'Conspiracy theory with high engagement'
    }
]


async def run_demo():
    """Run demo with test cases"""
    
    print("\n" + "="*80)
    print("🚀 TrustNet 2.0 - DEMO MODE")
    print("="*80)
    print("\nThis demo will process 3 sample posts through the complete pipeline:")
    print("  1. Clear health misinformation (high urgency)")
    print("  2. Legitimate news (credible source)")
    print("  3. Conspiracy theory (viral potential)")
    print("\n" + "="*80 + "\n")
    
    # Initialize coordinator
    logger.info("Initializing TrustNet Coordinator...")
    coordinator = TrustNetCoordinator()
    await coordinator.initialize()
    
    # Process each test case
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}/3: {test_case['description']}")
        print(f"{'='*80}")
        print(f"Text: {test_case['text'][:100]}...")
        print(f"Source: {test_case['source']}")
        print(f"Engagement: {test_case['engagement']}")
        print(f"{'='*80}\n")
        
        # Process through pipeline
        result = await coordinator.process_content(test_case)
        
        # Display results
        print(f"\n{'─'*80}")
        print("📊 RESULTS:")
        print(f"{'─'*80}")
        
        if result:
            if result.get('status') == 'REAL':
                print("✅ Classification: REAL/BENIGN")
                print("   Action: Monitoring only")
            elif result.get('status') == 'LOW_RISK':
                print("⚠️  Classification: FAKE but LOW RISK")
                print("   Action: Monitoring only")
            elif result.get('status') == 'SUCCESS':
                print("🚨 Classification: FAKE - HIGH RISK")
                print(f"   Intervention: {result.get('intervention_status', 'Executed')}")
                monitoring = result.get('monitoring', {})
                print(f"   Predicted Reduction: {monitoring.get('predicted_reduction', 'N/A')}")
                print(f"   Actual Reduction: {monitoring.get('actual_reduction', 'N/A')}")
                print(f"   Success: {'✅ YES' if monitoring.get('success') else '❌ NO'}")
        else:
            print("✅ Content cleared by Scout Agent")
            print("   Action: No further processing needed")
        
        print(f"{'─'*80}\n")
        
        # Pause between test cases
        if i < len(TEST_CASES):
            await asyncio.sleep(1)
    
    # Final metrics
    print(f"\n{'='*80}")
    print("📈 FINAL METRICS")
    print(f"{'='*80}")
    metrics = coordinator.get_metrics()
    print(f"Posts Analyzed:   {metrics['posts_analyzed']}")
    print(f"Fake Detected:    {metrics['fake_detected']}")
    print(f"Interventions:    {metrics['interventions']}")
    print(f"Success Rate:     {metrics['success_rate']*100:.1f}%")
    print(f"{'='*80}\n")
    
    # Cleanup
    await coordinator.shutdown()
    
    print("\n✅ Demo complete!\n")
    print("Next steps:")
    print("  1. Start the API server: python main.py")
    print("  2. Open dashboard: http://localhost:3000")
    print("  3. View API docs: http://localhost:8000/docs")
    print("  4. Configure real social media API keys in .env")
    print("")


if __name__ == "__main__":
    asyncio.run(run_demo())
