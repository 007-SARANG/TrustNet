"""
Demo: Image-Caption Mismatch Detection for Instagram Posts
Shows how TrustNet detects misinformation by comparing images and captions
"""

import logging
import os
from PIL import Image, ImageDraw, ImageFont
import io
from agents.collectors.instagram_collector import InstagramCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_demo_image(text, color='lightblue', size=(600, 600)):
    """Create a simple demo image with text"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a decent font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    text_width = draw.textlength(text, font=font) if hasattr(draw, 'textlength') else 200
    text_position = ((size[0] - text_width) // 2, size[1] // 2 - 20)
    
    draw.text(text_position, text, fill='black', font=font)
    return img


def demo_matching_posts():
    """Demo 1: Posts where image and caption MATCH (informative)"""
    print("\n" + "="*80)
    print("DEMO 1: MATCHING IMAGE & CAPTION ✅")
    print("="*80)
    
    examples = [
        {
            'image_text': 'SPACE NEBULA',
            'caption': 'Amazing nebula captured by Hubble telescope showing stellar nursery',
            'color': 'darkblue',
            'expected': 'PASS - Informative content'
        },
        {
            'image_text': 'COVID VACCINE',
            'caption': 'New COVID vaccine data from CDC shows 95% efficacy rate',
            'color': 'lightgreen',
            'expected': 'PASS - Informative health news'
        },
        {
            'image_text': 'CLIMATE DATA',
            'caption': 'Global temperature data from NASA shows 1.2°C warming since 1880',
            'color': 'orange',
            'expected': 'PASS - Informative science'
        }
    ]
    
    collector = InstagramCollector(
        instagram_username=os.getenv('INSTAGRAM_USERNAME'),
        instagram_password=os.getenv('INSTAGRAM_PASSWORD')
    )
    
    for idx, example in enumerate(examples, 1):
        print(f"\n{'─'*80}")
        print(f"Example {idx}:")
        print(f"  🖼️  Image shows: {example['image_text']}")
        print(f"  📝 Caption says: {example['caption']}")
        print(f"  ✅ Expected: {example['expected']}")
        
        # Create demo image
        img = create_demo_image(example['image_text'], example['color'])
        
        # Create post
        post = {
            'id': f'demo_{idx}',
            'platform': 'instagram',
            'image': img,
            'image_path': f'demo_{idx}.png',
            'caption': example['caption'],
            'author': {'username': 'demo_user'},
            'created_at': '2025-11-13',
            'metrics': {'likes': 1000, 'comments': 50, 'shares': 10}
        }
        
        # Analyze
        analysis = collector.analyze_post(post)
        
        print(f"\n  📊 ANALYSIS RESULT:")
        print(f"     Image-Caption Similarity: {analysis['image_caption_match']['similarity']:.2f}")
        print(f"     Matches: {analysis['image_caption_match']['matches']}")
        print(f"     Category: {analysis['classification']['category']}")
        print(f"     Flagged: {analysis['prevention']['flagged']}")
        print(f"     Action: {analysis['prevention']['action']}")


def demo_mismatch_posts():
    """Demo 2: Posts where image and caption MISMATCH (misinformation!)"""
    print("\n\n" + "="*80)
    print("DEMO 2: MISMATCHING IMAGE & CAPTION 🚨")
    print("="*80)
    
    examples = [
        {
            'image_text': 'CAT PHOTO',
            'caption': 'New BMW M5 2024 unveiled! Amazing luxury sports car with 600HP engine',
            'color': 'pink',
            'expected': 'BLOCK - Clear mismatch (cat ≠ car)'
        },
        {
            'image_text': 'RANDOM PILLS',
            'caption': 'iPhone 15 Pro Max now available! Latest Apple smartphone with A17 chip',
            'color': 'yellow',
            'expected': 'BLOCK - Clear mismatch (pills ≠ phone)'
        },
        {
            'image_text': 'BEACH SUNSET',
            'caption': 'BREAKING: Bitcoin crashes to zero! All cryptocurrency investors lost everything!',
            'color': 'coral',
            'expected': 'REVIEW - Mismatch + misleading claim'
        }
    ]
    
    collector = InstagramCollector(
        instagram_username=os.getenv('INSTAGRAM_USERNAME'),
        instagram_password=os.getenv('INSTAGRAM_PASSWORD')
    )
    
    for idx, example in enumerate(examples, 1):
        print(f"\n{'─'*80}")
        print(f"Example {idx}:")
        print(f"  🖼️  Image shows: {example['image_text']}")
        print(f"  📝 Caption says: {example['caption']}")
        print(f"  🚨 Expected: {example['expected']}")
        
        # Create demo image
        img = create_demo_image(example['image_text'], example['color'])
        
        # Create post
        post = {
            'id': f'mismatch_{idx}',
            'platform': 'instagram',
            'image': img,
            'image_path': f'mismatch_{idx}.png',
            'caption': example['caption'],
            'author': {'username': 'suspicious_user'},
            'created_at': '2025-11-13',
            'metrics': {'likes': 50000, 'comments': 2000, 'shares': 5000}
        }
        
        # Analyze
        analysis = collector.analyze_post(post)
        
        print(f"\n  📊 ANALYSIS RESULT:")
        print(f"     Image-Caption Similarity: {analysis['image_caption_match']['similarity']:.2f}")
        print(f"     Matches: {analysis['image_caption_match']['matches']}")
        print(f"     Reasoning: {analysis['image_caption_match']['reasoning']}")
        print(f"     Flagged: {'🚨 YES' if analysis['prevention']['flagged'] else 'NO'}")
        print(f"     Action: {analysis['prevention']['action']}")
        print(f"     Rules Triggered: {', '.join(analysis['prevention']['rules_triggered'])}")


def main():
    print("\n" + "="*80)
    print("🔬 TRUSTNET IMAGE-CAPTION MISMATCH DETECTION DEMO")
    print("="*80)
    print("\nThis demonstrates how TrustNet detects misinformation by:")
    print("1. Analyzing image content using AI (CLIP model)")
    print("2. Comparing it with caption text")
    print("3. Flagging mismatches as potential misinformation")
    print("\n⚠️  Note: Full functionality requires CLIP models (transformers + torch)")
    print("   Install with: pip install transformers torch")
    print("="*80)
    
    # Check if models are available
    try:
        import torch
        import transformers
        print("\n✅ AI Models Available - Full analysis enabled")
    except ImportError:
        print("\n⚠️  AI Models Not Installed - Using fallback mode")
        print("   For full image-caption matching, install:")
        print("   pip install transformers torch")
    
    # Run demos
    demo_matching_posts()
    demo_mismatch_posts()
    
    # Summary
    print("\n\n" + "="*80)
    print("📋 SUMMARY: HOW IT WORKS")
    print("="*80)
    print("""
TrustNet's Image-Caption Mismatch Detection:

1️⃣  POST COLLECTION
   - Scrapes Instagram posts using Instaloader
   - Extracts image + caption + metadata
   - Works with your login credentials from .env file

2️⃣  AI ANALYSIS (CLIP Model)
   - Encodes image content into embeddings
   - Encodes caption text into embeddings
   - Calculates semantic similarity (0.0 - 1.0)

3️⃣  MISMATCH DETECTION
   - High similarity (>0.65): ✅ Image matches caption
   - Medium similarity (0.30-0.65): ⚠️  Partial match
   - Low similarity (<0.30): 🚨 MISMATCH - potential misinformation!

4️⃣  PREVENTION RULES
   - Rule 0: Image-caption mismatch → BLOCK/REVIEW
   - Rule 1: High misinformation score → BLOCK
   - Rule 2: Low informative value → REVIEW
   - Rule 3: Advertisement content → FLAG

REAL-WORLD EXAMPLES:
✅ MATCH: Image of space + caption about space = Informative
🚨 MISMATCH: Image of cat + caption about BMW car = Misinformation!
🚨 MISMATCH: Image of pills + caption about iPhone = Misinformation!

YOUR CREDENTIALS ARE SET:
- Username: """ + (os.getenv('INSTAGRAM_USERNAME') or 'Not set') + """
- Ready to scrape: """ + ('✅ Yes' if os.getenv('INSTAGRAM_USERNAME') else '❌ No (add to .env)') + """
    """)
    print("="*80)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Install AI models: pip install transformers torch")
    print("2. Run: python test_instagram_instaloader.py")
    print("3. Check real Instagram posts for mismatches!")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
