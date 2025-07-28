#!/usr/bin/env python3
"""
Test script for Challenge 1a implementation
Validates the solution with sample data
"""

import os
import sys
import json
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from process_pdfs import PDFProcessor


def test_single_pdf():
    """Test processing a single PDF file"""
    print("=== Testing Single PDF Processing ===")
    
    # Test with sample PDF
    sample_pdf = "sample_dataset/pdfs/file02.pdf"
    if not os.path.exists(sample_pdf):
        print(f"Sample PDF not found: {sample_pdf}")
        return False
    
    processor = PDFProcessor()
    
    try:
        start_time = time.time()
        result = processor.process_pdf(sample_pdf)
        processing_time = time.time() - start_time
        
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Title: {result['title']}")
        print(f"Number of headings: {len(result['outline'])}")
        
        # Validate output
        if processor.output_generator.validate_output(result):
            print("✅ Output validation passed")
        else:
            print("❌ Output validation failed")
            return False
        
        # Check performance
        if processing_time <= 10:
            print("✅ Performance constraint met")
        else:
            print(f"❌ Performance constraint failed: {processing_time:.2f}s > 10s")
            return False
        
        # Print first few headings
        print("\nFirst 5 headings:")
        for i, heading in enumerate(result['outline'][:5]):
            print(f"  {i+1}. {heading['level']}: {heading['text']} (page {heading['page']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def test_output_schema():
    """Test output schema compliance"""
    print("\n=== Testing Output Schema ===")
    
    # Load expected schema
    schema_file = "sample_dataset/schema/output_schema.json"
    if not os.path.exists(schema_file):
        print(f"Schema file not found: {schema_file}")
        return False
    
    with open(schema_file, 'r') as f:
        schema = json.load(f)
    
    print("✅ Schema file loaded")
    
    # Test with sample PDF
    sample_pdf = "sample_dataset/pdfs/file02.pdf"
    if not os.path.exists(sample_pdf):
        print(f"Sample PDF not found: {sample_pdf}")
        return False
    
    processor = PDFProcessor()
    
    try:
        result = processor.process_pdf(sample_pdf)
        
        # Basic schema validation
        if 'title' not in result:
            print("❌ Missing 'title' field")
            return False
        
        if 'outline' not in result:
            print("❌ Missing 'outline' field")
            return False
        
        if not isinstance(result['title'], str):
            print("❌ 'title' is not a string")
            return False
        
        if not isinstance(result['outline'], list):
            print("❌ 'outline' is not a list")
            return False
        
        # Validate each heading
        for i, heading in enumerate(result['outline']):
            if not isinstance(heading, dict):
                print(f"❌ Heading {i} is not a dictionary")
                return False
            
            required_fields = ['level', 'text', 'page']
            for field in required_fields:
                if field not in heading:
                    print(f"❌ Heading {i} missing '{field}' field")
                    return False
            
            if heading['level'] not in ['H1', 'H2', 'H3']:
                print(f"❌ Heading {i} has invalid level: {heading['level']}")
                return False
            
            if not isinstance(heading['text'], str):
                print(f"❌ Heading {i} 'text' is not a string")
                return False
            
            if not isinstance(heading['page'], int):
                print(f"❌ Heading {i} 'page' is not an integer")
                return False
        
        print("✅ Schema validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Error during schema testing: {e}")
        return False


def test_performance():
    """Test performance with larger PDF"""
    print("\n=== Testing Performance ===")
    
    # Test with largest sample PDF
    sample_pdf = "sample_dataset/pdfs/file05.pdf"
    if not os.path.exists(sample_pdf):
        print(f"Sample PDF not found: {sample_pdf}")
        return False
    
    processor = PDFProcessor()
    
    try:
        start_time = time.time()
        result = processor.process_pdf(sample_pdf)
        processing_time = time.time() - start_time
        
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Title: {result['title']}")
        print(f"Number of headings: {len(result['outline'])}")
        
        if processing_time <= 10:
            print("✅ Performance constraint met")
            return True
        else:
            print(f"❌ Performance constraint failed: {processing_time:.2f}s > 10s")
            return False
        
    except Exception as e:
        print(f"❌ Error during performance testing: {e}")
        return False


def main():
    """Run all tests"""
    print("Challenge 1a Implementation Test Suite")
    print("=" * 50)
    
    tests = [
        test_single_pdf,
        test_output_schema,
        test_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Implementation is ready.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 