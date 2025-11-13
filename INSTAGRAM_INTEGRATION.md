# Instagram Image Analysis Integration

## Overview

This module adds **offline Instagram image detection and comparison** to TrustNet, using local AI models to classify informative content and detect misinformation.

## Features

### 1. **Offline Image Classification**
- Uses CLIP (Contrastive Language-Image Pre-training) to classify images
- Determines if content is:
  - ✅ Informative (educational, news, data)
  - ⚠️ Entertainment (casual, personal)
  - 🚫 Advertisement (promotional, sponsored)
  - ❌ Misinformation (fake news, misleading)

### 2. **Image-Caption Similarity Analysis**
- Compares generated images with original content
- Detects image-caption mismatches
- Uses CLIP embeddings for semantic similarity

### 3. **Prevention Algorithm**
- Flags non-informative content based on business rules
- Actions: `allow`, `flag`, `review`, `block`
- Configurable thresholds and rules

### 4. **Offline AI Models**
- **CLIP** (openai/clip-vit-base-patch32): Image-text understanding
- **Stable Diffusion** (optional): Image generation from captions
- All models cached locally for offline use

## Installation

### Basic Setup (CLIP only - ~350MB)
```bash
pip install transformers torch torchvision pillow requests
```

### Full Setup (with Stable Diffusion - ~4GB)
```bash
pip install transformers torch torchvision diffusers accelerate pillow requests
```

### Quick Install (from requirements.txt)
```bash
pip install -r requirements.txt
```

## Usage

### 1. Standalone Test
```bash
python test_instagram.py
```

### 2. API Integration
The Instagram analyzer is integrated into the main API:

```bash
# Start the server
python quick_start.py

# Test the endpoint
curl -X POST "http://localhost:8000/api/analyze-instagram-image" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "caption": "Climate data shows rising temperatures"
  }'
```

### 3. Python Integration
```python
from agents.collectors.instagram_collector import InstagramCollector

# Initialize
collector = InstagramCollector()

# Fetch post (simulated or from API)
post = collector.fetch_sample_post(
    image_path="path/to/image.jpg",
    caption="Your caption here"
)

# Analyze
analysis = collector.analyze_post(post)

# Check results
if analysis['prevention']['flagged']:
    print(f"⚠️ Flagged: {analysis['prevention']['reason']}")
    print(f"Action: {analysis['prevention']['action']}")
```

## Architecture

### Components

```
InstagramImageAnalyzer
├── _load_models()          # Load CLIP + Stable Diffusion
├── classify_informative()  # Classify content type
├── compare_images()        # Image similarity analysis
└── generate_image()        # Generate from caption (optional)

InstagramCollector
├── fetch_sample_post()     # Get Instagram post
├── analyze_post()          # Full analysis pipeline
├── _apply_prevention_rules() # Business logic
├── get_sample_posts()      # Test data
└── save_analysis_log()     # Export results
```

### Analysis Pipeline

```
1. Fetch Instagram Post
   ↓
2. Load Image + Caption
   ↓
3. CLIP Classification
   ├── Informative Score
   ├── Entertainment Score
   ├── Advertisement Score
   └── Misinformation Score
   ↓
4. (Optional) Generate Reference Image
   ↓
5. (Optional) Compare Images (CLIP embeddings)
   ↓
6. Apply Prevention Rules
   ├── Check misinformation threshold
   ├── Check informative value
   ├── Check advertisement score
   └── Check image-caption match
   ↓
7. Return Analysis + Flag Decision
```

## Prevention Rules

### Current Rules

| Rule | Condition | Action |
|------|-----------|--------|
| High Misinformation | Misinfo score > 0.5 | `block` |
| Low Informative | Informative score < 0.3 | `review` |
| Advertisement | Ad score > 0.6 | `flag` |
| Image Mismatch | Similarity < 0.3 | `review` |

### Customizing Rules

Edit `_apply_prevention_rules()` in `instagram_collector.py`:

```python
def _apply_prevention_rules(self, classification: Dict, comparison: Optional[Dict]) -> Dict:
    # Your custom logic here
    if classification.get('scores', {}).get('misinformation', 0) > YOUR_THRESHOLD:
        return {'flagged': True, 'action': 'block', 'reason': 'Your reason'}
    # ...
```

## Model Details

### CLIP (openai/clip-vit-base-patch32)
- **Size**: ~350 MB
- **Purpose**: Image-text understanding
- **Offline**: ✅ Cached locally
- **Speed**: Fast (~0.1s per image)

### Stable Diffusion (runwayml/stable-diffusion-v1-5)
- **Size**: ~4 GB
- **Purpose**: Image generation (optional)
- **Offline**: ✅ Cached locally
- **Speed**: Slower (~5s per image)

### Download Location
Models are cached in `./models/` directory by default.

## API Endpoints

### POST `/api/analyze-instagram-image`
Analyze an Instagram image for informative content.

**Request:**
```json
{
  "image_url": "https://example.com/image.jpg",
  "caption": "Caption text here"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "post_id": "abc123...",
    "classification": {
      "is_informative": true,
      "confidence": 0.75,
      "reasoning": "Educational/informative content",
      "scores": {
        "informative": 0.75,
        "entertainment": 0.15,
        "advertisement": 0.05,
        "misinformation": 0.05
      }
    },
    "prevention": {
      "flagged": false,
      "reason": "",
      "action": "allow",
      "confidence": 0.75
    }
  },
  "flagged": false,
  "action": "allow"
}
```

## Performance

### With GPU (CUDA)
- Classification: ~0.05s per image
- Comparison: ~0.1s per pair
- Generation: ~3-5s per image

### CPU Only
- Classification: ~0.2s per image
- Comparison: ~0.3s per pair
- Generation: ~15-30s per image

## Testing

### Run Test Suite
```bash
python test_instagram.py
```

### Expected Output
```
🔬 TRUSTNET INSTAGRAM IMAGE ANALYSIS TEST
════════════════════════════════════════════════════════════════════════════════

📸 TEST CASE 1: Informative Climate Post
────────────────────────────────────────────────────────────────────────────────
📊 CLASSIFICATION:
   Informative: ✅ YES
   Confidence: 75.00%
   Reasoning: Educational/informative content

🚨 PREVENTION:
   Flagged: 🟢 NO
   Action: ALLOW

...
```

## Troubleshooting

### Models not loading?
```bash
# Install dependencies
pip install transformers torch torchvision

# Verify installation
python -c "import transformers; print('✅ Transformers installed')"
python -c "import torch; print('✅ PyTorch installed')"
```

### Out of memory?
- Use CPU instead of GPU
- Reduce batch size
- Use smaller CLIP model variant

### Slow performance?
- Enable GPU/CUDA if available
- Use smaller CLIP model
- Skip Stable Diffusion generation

## Integration with TrustNet Dashboard

The Instagram analysis integrates seamlessly with the existing TrustNet dashboard:

1. Posts are collected via `InstagramCollector`
2. Analyzed using CLIP models
3. Flagged posts are broadcast via WebSocket
4. Displayed in the Live Feed with risk scores
5. Source credibility tracking includes Instagram data

## Future Enhancements

- [ ] Real Instagram API integration
- [ ] Video content analysis
- [ ] Multi-language support
- [ ] Custom model fine-tuning
- [ ] Batch processing
- [ ] Advanced image forensics
- [ ] Deepfake detection

## License

Part of TrustNet 2.0 - AI-Powered Misinformation Detection System

## Support

For issues or questions about the Instagram integration, refer to the main TrustNet documentation or create an issue in the repository.
