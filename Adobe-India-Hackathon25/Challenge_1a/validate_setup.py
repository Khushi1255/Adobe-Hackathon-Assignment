#!/usr/bin/env python3
"""
Validation script for Challenge 1a setup
Checks that all components are properly configured
"""

import os
import sys
import importlib
from pathlib import Path

def check_imports():
    """Check that all required modules can be imported"""
    print("=== Checking Module Imports ===")
    
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_path)
    
    modules_to_check = [
        'pdfstructure.source',
        'pdfstructure.hierarchy.parser',
        'pdfstructure.model.document',
        'heading_detector',
        'title_extractor', 
        'output_generator'
    ]
    
    failed_imports = []
    
    for module in modules_to_check:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def check_files():
    """Check that all required files exist"""
    print("\n=== Checking Required Files ===")
    
    required_files = [
        'process_pdfs.py',
        'requirements.txt',
        'Dockerfile',
        'README.md',
        'src/heading_detector.py',
        'src/title_extractor.py',
        'src/output_generator.py',
        'sample_dataset/schema/output_schema.json'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_pdfstructure():
    """Check that pdfstructure is properly set up"""
    print("\n=== Checking pdfstructure Setup ===")
    
    pdfstructure_path = 'src/pdfstructure'
    if not os.path.exists(pdfstructure_path):
        print(f"❌ pdfstructure directory not found: {pdfstructure_path}")
        return False
    
    # Check for key pdfstructure files
    key_files = [
        'source.py',
        'hierarchy/parser.py',
        'model/document.py',
        'analysis/styledistribution.py'
    ]
    
    missing_files = []
    for file_path in key_files:
        full_path = os.path.join(pdfstructure_path, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_dockerfile():
    """Check Dockerfile configuration"""
    print("\n=== Checking Dockerfile ===")
    
    dockerfile_path = 'Dockerfile'
    if not os.path.exists(dockerfile_path):
        print(f"❌ Dockerfile not found")
        return False
    
    with open(dockerfile_path, 'r') as f:
        content = f.read()
    
    checks = [
        ('FROM --platform=linux/amd64', 'AMD64 platform specified'),
        ('python:3.10', 'Python 3.10 base image'),
        ('COPY requirements.txt', 'Requirements file copied'),
        ('RUN pip install', 'Dependencies installed'),
        ('COPY src/', 'Source code copied'),
        ('COPY process_pdfs.py', 'Main script copied'),
        ('CMD ["python", "process_pdfs.py"]', 'Correct entry point')
    ]
    
    all_good = True
    for check, description in checks:
        if check in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_good = False
    
    return all_good

def check_requirements():
    """Check requirements.txt"""
    print("\n=== Checking requirements.txt ===")
    
    requirements_path = 'requirements.txt'
    if not os.path.exists(requirements_path):
        print(f"❌ requirements.txt not found")
        return False
    
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    required_packages = ['pdfminer.six', 'numpy']
    
    all_good = True
    for package in required_packages:
        if package in content:
            print(f"✅ {package}")
        else:
            print(f"❌ {package}")
            all_good = False
    
    return all_good

def main():
    """Run all validation checks"""
    print("Challenge 1a Setup Validation")
    print("=" * 40)
    
    checks = [
        check_imports,
        check_files,
        check_pdfstructure,
        check_dockerfile,
        check_requirements
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
    
    print(f"\n=== Validation Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All validation checks passed! Setup is complete.")
        print("\nNext steps:")
        print("1. Build Docker image: docker build --platform linux/amd64 -t challenge1a-pdf-extractor .")
        print("2. Test with sample data: python test_implementation.py")
        print("3. Run with Docker: docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output:/app/output --network none challenge1a-pdf-extractor")
        return True
    else:
        print("❌ Some validation checks failed. Please review the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 