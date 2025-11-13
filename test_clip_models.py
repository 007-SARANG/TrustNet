"""Test if CLIP models can be loaded"""

try:
    import torch
    from transformers import CLIPProcessor, CLIPModel
    print("✅ PyTorch and Transformers imported successfully")
    print(f"   PyTorch: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    
    print("\n📦 Loading CLIP model...")
    clip_model = CLIPModel.from_pretrained(
        "openai/clip-vit-base-patch32",
        cache_dir="./models"
    )
    print("✅ CLIP model loaded!")
    
    print("\n📦 Loading CLIP processor...")
    clip_processor = CLIPProcessor.from_pretrained(
        "openai/clip-vit-base-patch32",
        cache_dir="./models"
    )
    print("✅ CLIP processor loaded!")
    
    print("\n✅ All models loaded successfully!")
    print(f"   Model type: {type(clip_model)}")
    print(f"   Processor type: {type(clip_processor)}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
