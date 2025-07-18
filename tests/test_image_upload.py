#!/usr/bin/env python3
"""
Test script for image upload and validation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using absolute paths
sys.path.insert(0, 'src')
from config.settings import config
from utils.image_processing import ImageProcessor, ImageValidator
from PIL import Image

def test_image_validation():
    """Test image validation with test files."""
    print("🧪 Testing Image Validation")
    print("=" * 40)
    
    # Initialize components
    image_processor = ImageProcessor(config.ui)
    image_validator = ImageValidator(config.ui)
    
    # Test files
    test_files = [
        "tests/photo-1572670014853-1d3a3f22b40f.jpeg",
        "tests/STOP_sign.jpg"
    ]
    
    for test_file in test_files:
        print(f"\n📁 Testing file: {test_file}")
        
        if not os.path.exists(test_file):
            print(f"❌ File not found: {test_file}")
            continue
        
        # Get file info
        file_size = os.path.getsize(test_file)
        file_name = os.path.basename(test_file)
        
        print(f"   Size: {file_size} bytes")
        print(f"   Name: {file_name}")
        
        # Test file type validation
        is_valid_type = image_validator.validate_file_type(file_name)
        print(f"   Valid type: {'✅' if is_valid_type else '❌'}")
        
        # Test file size validation
        is_valid_size = image_validator.validate_file_size(file_size)
        print(f"   Valid size: {'✅' if is_valid_size else '❌'}")
        
        # Test image loading
        try:
            image = image_processor.load_image(test_file)
            print(f"   Image loaded: ✅")
            print(f"   Image size: {image.size}")
            print(f"   Image mode: {image.mode}")
            
            # Test image validation
            image_processor.validate_image(image)
            print(f"   Image validation: ✅")
            
        except Exception as e:
            print(f"   Image loading/validation: ❌ {str(e)}")

if __name__ == "__main__":
    test_image_validation() 