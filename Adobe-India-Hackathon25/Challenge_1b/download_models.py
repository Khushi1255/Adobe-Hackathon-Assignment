#!/usr/bin/env python3
"""
Script to pre-download models for offline operation
"""

import os
import sys
from pathlib import Path

def download_models():
    """Download required models for offline operation"""
    print("=== Downloading Models for Offline Operation ===")
    
    try:
        # Import required libraries
        from sentence_transformers import SentenceTransformer
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # Create cache directory
        cache_dir = Path("./model_cache")
        cache_dir.mkdir(exist_ok=True)
        
        # Set environment variables for caching
        os.environ['TRANSFORMERS_CACHE'] = str(cache_dir / "transformers")
        os.environ['HF_HOME'] = str(cache_dir / "huggingface")
        
        print("📥 Downloading embedding model: sentence-transformers/all-MiniLM-L6-v2")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✅ Embedding model downloaded")
        
        print("📥 Downloading rerank model: cross-encoder/ms-marco-MiniLM-L-6-v2")
        tokenizer = AutoTokenizer.from_pretrained('cross-encoder/ms-marco-MiniLM-L-6-v2')
        model = AutoModelForSequenceClassification.from_pretrained('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("✅ Rerank model downloaded")
        
        print(f"✅ All models downloaded to: {cache_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading models: {e}")
        return False

if __name__ == "__main__":
    success = download_models()
    if success:
        print("🎉 Model download completed successfully!")
    else:
        print("❌ Model download failed!")
        sys.exit(1) 