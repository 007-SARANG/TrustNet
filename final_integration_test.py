"""
Final Test: Instagram Mismatch Detection - Complete Integration Test
Shows the entire system working end-to-end
"""

import requests
import json

print("\n" + "="*80)
print("🎯 FINAL INTEGRATION TEST - INSTAGRAM MISMATCH DETECTION")
print("="*80)

# Test cases
test_cases = [
    {
        "name": "YOUR USE CASE: Cat Image + BMW Caption",
        "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400",
        "caption": "New BMW M5 2024 unveiled! Amazing luxury sports car with 600HP engine",
        "expected": "BLOCK"
    },
    {
        "name": "Space Image + Space Caption (Match)",
        "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400",
        "caption": "Beautiful starry night sky with Milky Way galaxy visible",
        "expected": "ALLOW"
    },
    {
        "name": "Beach Image + Bitcoin Caption (Mismatch)",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400",
        "caption": "BREAKING: Bitcoin crashes to zero! All cryptocurrency investors lost everything!",
        "expected": "BLOCK"
    }
]

print("\n📡 Testing Backend API Endpoint...")
print("   URL: http://localhost:8000/api/analyze-instagram-image")

success_count = 0
fail_count = 0

for i, test in enumerate(test_cases, 1):
    print(f"\n{'─'*80}")
    print(f"Test {i}/3: {test['name']}")
    print(f"{'─'*80}")
    print(f"📝 Caption: {test['caption'][:60]}...")
    print(f"🖼️  Image: {test['image_url'][:50]}...")
    print(f"🎯 Expected: {test['expected']}")
    
    try:
        # Call the backend API
        response = requests.post(
            "http://localhost:8000/api/analyze-instagram-image",
            json={
                "image_url": test['image_url'],
                "caption": test['caption']
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis = data['analysis']
            
            similarity = analysis['image_caption_match']['similarity'] * 100
            matches = analysis['image_caption_match']['matches']
            action = analysis['prevention']['action'].upper()
            
            print(f"\n📊 RESULTS:")
            print(f"   Similarity: {similarity:.2f}%")
            print(f"   Matches: {'YES' if matches else 'NO'}")
            print(f"   Action: {action}")
            print(f"   Reasoning: {analysis['image_caption_match']['reasoning']}")
            
            # Check if result matches expectation
            if action == test['expected']:
                print(f"\n✅ TEST PASSED - Action matches expectation ({test['expected']})")
                success_count += 1
                
                # Highlight the BMW use case
                if "BMW" in test['caption']:
                    print("\n" + "🌟"*40)
                    print("   ⭐⭐⭐ YOUR EXACT USE CASE - WORKING! ⭐⭐⭐")
                    print("   Cat photo + BMW caption = BLOCKED ✅")
                    print("   Similarity: {:.2f}% (Critical mismatch!)".format(similarity))
                    print("🌟"*40)
            else:
                print(f"\n⚠️ TEST FAILED - Expected {test['expected']}, got {action}")
                fail_count += 1
                
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            fail_count += 1
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR: Cannot reach backend")
        print("   Make sure quick_start.py is running!")
        fail_count += 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        fail_count += 1

# Summary
print(f"\n{'='*80}")
print("📊 TEST SUMMARY")
print(f"{'='*80}")
print(f"✅ Passed: {success_count}/3")
print(f"❌ Failed: {fail_count}/3")

if success_count == 3:
    print("\n🎉 ALL TESTS PASSED!")
    print("   ✅ Backend API working")
    print("   ✅ CLIP model operational")
    print("   ✅ Image-caption mismatch detection accurate")
    print("   ✅ Your use case (Cat + BMW) correctly BLOCKED")
    print("\n🚀 SYSTEM FULLY OPERATIONAL!")
elif success_count > 0:
    print(f"\n⚠️ PARTIAL SUCCESS: {success_count}/3 tests passed")
else:
    print("\n❌ ALL TESTS FAILED")
    print("   Check if backend is running: python quick_start.py")

print(f"\n{'='*80}")
print("🎯 NEXT: Open Dashboard")
print("   URL: http://localhost:3002")
print("   Navigate to: Live Posts Feed → Instagram Detector")
print("   Click: Load Mismatch Example (Cat + BMW)")
print("   See: Your exact use case working in the UI!")
print(f"{'='*80}\n")
