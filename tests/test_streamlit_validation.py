#!/usr/bin/env python3
"""
Test script that simulates Streamlit file upload validation
"""

import sys
import os
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using absolute paths
sys.path.insert(0, 'src')
from config.settings import config
from utils.image_processing import ImageProcessor, ImageValidator

class MockStreamlitFile:
    """Mock Streamlit uploaded file object for testing."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.name = os.path.basename(file_path)
        self.size = os.path.getsize(file_path)
        
    def read(self):
        """Read file content."""
        with open(self.file_path, 'rb') as f:
            return f.read()

def test_streamlit_validation():
    """Test validation with mock Streamlit files."""
    print("🧪 Testing Streamlit File Validation")
    print("=" * 45)
    
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
        
        # Create mock Streamlit file
        mock_file = MockStreamlitFile(test_file)
        
        print(f"   Name: {mock_file.name}")
        print(f"   Size: {mock_file.size} bytes")
        
        # Test validation
        is_valid = image_validator.validate_uploaded_file(mock_file)
        print(f"   Valid: {'✅' if is_valid else '❌'}")
        
        if is_valid:
            # Test full processing
            try:
                file_content = mock_file.read()
                image = image_processor.load_image_from_bytes(file_content)
                image_processor.validate_image(image)
                print(f"   Processing: ✅ {image.size} {image.mode}")
            except Exception as e:
                print(f"   Processing: ❌ {str(e)}")
        else:
            # Debug why validation failed
            print(f"   Type validation: {'✅' if image_validator.validate_file_type(mock_file.name) else '❌'}")
            print(f"   Size validation: {'✅' if image_validator.validate_file_size(mock_file.size) else '❌'}")

if __name__ == "__main__":
    test_streamlit_validation() 