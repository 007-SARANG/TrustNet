"""
Test Instagram Image Analysis Integration
Demonstrates offline image detection and comparison
"""

import logging
from agents.collectors.instagram_collector import InstagramCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_instagram_analysis():
    """Test Instagram image analysis with sample data"""
    
    print("\n" + "="*80)
    print("🔬 TRUSTNET INSTAGRAM IMAGE ANALYSIS TEST")
    print("="*80 + "\n")
    
    # Initialize collector
    collector = InstagramCollector()
    
    # Test cases
    test_cases = [
        {
            'name': 'Informative Climate Post',
            'image_url': 'https://via.placeholder.com/600x600.png?text=Climate+Science+2025',
            'caption': 'New climate research published in Nature shows accelerating ice melt. Key findings: 1) Arctic temperatures up 3°C 2) Sea level projections revised upward.'
        },
        {
            'name': 'Entertainment Selfie',
            'image_url': 'https://via.placeholder.com/600x600.png?text=Selfie+Photo',
            'caption': 'Amazing day at the beach! Feeling blessed 🌊☀️ #beachvibes #happy #summer'
        },
        {
            'name': 'Suspicious Health Claim',
            'image_url': 'https://via.placeholder.com/600x600.png?text=Miracle+Cure',
            'caption': 'SHOCKING discovery! This ONE simple trick cures diabetes that doctors DON\'T want you to know! Click link in bio to buy now!'
        },
        {
            'name': 'News Update',
            'image_url': 'https://via.placeholder.com/600x600.png?text=Breaking+News',
            'caption': 'BREAKING: Election results announced. Official count shows 52% voter turnout across all districts. Full analysis on our website.'
        }
    ]
    
    analyses = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'─'*80}")
        print(f"📸 TEST CASE {i}: {test_case['name']}")
        print(f"{'─'*80}")
        print(f"Caption: {test_case['caption'][:80]}...")
        print()
        
        try:
            # Fetch post
            post = collector.fetch_sample_post(
                test_case['image_url'],
                test_case['caption']
            )
            
            if not post:
                print("❌ Failed to fetch post")
                continue
            
            # Analyze
            analysis = collector.analyze_post(post)
            analyses.append(analysis)
            
            # Display results
            classification = analysis['classification']
            prevention = analysis['prevention']
            
            print(f"📊 CLASSIFICATION:")
            print(f"   Informative: {'✅ YES' if classification['is_informative'] else '❌ NO'}")
            print(f"   Confidence: {classification['confidence']:.2%}")
            print(f"   Reasoning: {classification['reasoning']}")
            
            if 'scores' in classification:
                print(f"\n   Detailed Scores:")
                for category, score in classification['scores'].items():
                    print(f"      {category.capitalize()}: {score:.2%}")
            
            print(f"\n🚨 PREVENTION:")
            print(f"   Flagged: {'🔴 YES' if prevention['flagged'] else '🟢 NO'}")
            print(f"   Action: {prevention['action'].upper()}")
            print(f"   Reason: {prevention['reason'] or 'N/A'}")
            
            if analysis.get('comparison'):
                comp = analysis['comparison']
                print(f"\n🔍 IMAGE COMPARISON:")
                print(f"   Similarity: {comp['similarity']:.2%}")
                print(f"   Match Level: {comp['match'].upper()}")
                print(f"   Analysis: {comp['reasoning']}")
            
        except Exception as e:
            print(f"❌ Error analyzing post: {e}")
            logger.error(f"Test case {i} error", exc_info=True)
    
    # Summary
    print(f"\n{'═'*80}")
    print("📈 SUMMARY")
    print(f"{'═'*80}")
    print(f"Total posts analyzed: {len(analyses)}")
    print(f"Posts flagged: {len(collector.flagged_posts)}")
    
    if collector.flagged_posts:
        print(f"\n🚨 Flagged Posts:")
        for flagged in collector.flagged_posts:
            print(f"   - {flagged['prevention']['reason']} (action: {flagged['prevention']['action']})")
    
    # Save log
    collector.save_analysis_log(analyses, "./test_instagram_analysis.json")
    print(f"\n✅ Analysis log saved to: test_instagram_analysis.json")
    
    print(f"\n{'═'*80}\n")


if __name__ == "__main__":
    print("\n🚀 Starting TrustNet Instagram Integration Test...")
    print("⚠️  Note: Full functionality requires CLIP model (~350MB download)")
    print("    The system will work with fallback logic if models unavailable.\n")
    
    test_instagram_analysis()
