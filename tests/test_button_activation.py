#!/usr/bin/env python3
"""
Test script to verify button activation after image upload
"""

import sys
import os

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

def test_button_activation_logic():
    """Test the logic that determines button activation."""
    print("🧪 Testing Button Activation Logic")
    print("=" * 40)
    
    # Initialize components
    image_processor = ImageProcessor(config.ui)
    image_validator = ImageValidator(config.ui)
    
    # Test with STOP sign image
    test_file = "tests/STOP_sign.jpg"
    
    if not os.path.exists(test_file):
        print(f"❌ Test image not found: {test_file}")
        return
    
    # Create mock Streamlit file
    mock_file = MockStreamlitFile(test_file)
    
    print(f"📁 Testing file: {mock_file.name}")
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
            
            # Test button activation logic
            print("\n🔘 Button Activation Logic Test:")
            
            # Simulate session state
            current_image = image
            model_loaded = False
            
            # Test conditions
            print(f"   current_image is None: {'❌' if current_image is not None else '✅'}")
            print(f"   model_loaded: {'✅' if model_loaded else '❌'}")
            
            # Button should be enabled if image is loaded
            button_enabled = current_image is not None
            print(f"   Button enabled: {'✅' if button_enabled else '❌'}")
            
            # Status message logic
            if current_image is None:
                status = "📁 Upload an image to start"
            elif not model_loaded:
                status = "🤖 Loading model..."
            else:
                status = "✅ Ready to generate attack"
            
            print(f"   Status message: {status}")
            
            print("\n✅ Button activation logic test completed!")
            
        except Exception as e:
            print(f"   Processing: ❌ {str(e)}")
    else:
        print("   ❌ File validation failed")

if __name__ == "__main__":
    test_button_activation_logic() 