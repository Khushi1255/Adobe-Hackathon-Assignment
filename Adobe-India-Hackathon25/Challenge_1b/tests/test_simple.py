#!/usr/bin/env python3
"""
Simple test script for Challenge 1b core functionality
"""

import os
import sys
import json
from pathlib import Path

def test_basic_imports():
    """Test basic module imports"""
    print("=== Testing Basic Imports ===")
    
    try:
        import numpy
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import faiss
        print("✅ faiss-cpu")
    except ImportError as e:
        print(f"❌ faiss-cpu: {e}")
        return False
    
    try:
        import torch
        print("✅ torch")
        if torch.cuda.is_available():
            print("⚠️  CUDA available but using CPU mode")
        else:
            print("✅ CUDA not available - CPU-only mode")
    except ImportError as e:
        print(f"❌ torch: {e}")
        return False
    
    try:
        import transformers
        print("✅ transformers")
    except ImportError as e:
        print(f"❌ transformers: {e}")
        return False
    
    try:
        import langchain
        print("✅ langchain")
    except ImportError as e:
        print(f"❌ langchain: {e}")
        return False
    
    return True

def test_config():
    """Test configuration setup"""
    print("\n=== Testing Configuration ===")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from src.utils.config import Config
        
        config = Config()
        
        # Check device settings
        device_rerank = config['model']['device_rerank']
        device_embedding = config['model']['device_embedding']
        
        if device_rerank == 'cpu':
            print("✅ Reranker device: CPU")
        else:
            print(f"❌ Reranker device: {device_rerank}")
            return False
        
        if device_embedding == 'cpu':
            print("✅ Embedding device: CPU")
        else:
            print(f"❌ Embedding device: {device_embedding}")
            return False
        
        print("✅ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_sample_data():
    """Test sample data availability"""
    print("\n=== Testing Sample Data ===")
    
    try:
        # Check if sample data exists
        collections = ["Collection 1", "Collection 2", "Collection 3"]
        
        for collection in collections:
            collection_path = Path(collection)
            if collection_path.exists():
                print(f"✅ {collection}/")
                
                # Check for input/output files
                input_file = collection_path / "challenge1b_input.json"
                output_file = collection_path / "challenge1b_output.json"
                
                if input_file.exists():
                    print(f"  ✅ {collection}/challenge1b_input.json")
                else:
                    print(f"  ❌ {collection}/challenge1b_input.json")
                
                if output_file.exists():
                    print(f"  ✅ {collection}/challenge1b_output.json")
                else:
                    print(f"  ❌ {collection}/challenge1b_output.json")
            else:
                print(f"❌ {collection}/")
        
        # Test loading a sample input
        input_file = Path("Collection 1/challenge1b_input.json")
        if input_file.exists():
            with open(input_file, 'r') as f:
                data = json.load(f)
            
            # Check required fields
            required_fields = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
            for field in required_fields:
                if field in data:
                    print(f"✅ {field}")
                else:
                    print(f"❌ Missing field: {field}")
                    return False
            
            print("✅ Sample data validation passed")
            return True
        else:
            print("❌ Sample input file not found")
            return False
            
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def test_docker_ready():
    """Test if Docker setup is ready"""
    print("\n=== Testing Docker Setup ===")
    
    required_files = [
        "Dockerfile",
        "requirements.txt",
        "process_challenge1b.py",
        "README.md"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    
    print("✅ Docker setup ready")
    return True

def main():
    """Main test function"""
    print("Challenge 1b Simple Test")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_config,
        test_sample_data,
        test_docker_ready
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Challenge 1b is ready for testing.")
        print("\nNext steps:")
        print("1. Build Docker: docker build --platform linux/amd64 -t challenge1b-rag-system .")
        print("2. Test with sample data")
        print("3. Run with Docker: docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output:/app/output --network none challenge1b-rag-system")
    else:
        print("❌ Some tests failed. Please check the setup.")
    
    return passed == total

if __name__ == "__main__":
    main() 