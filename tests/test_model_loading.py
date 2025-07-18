#!/usr/bin/env python3
"""
Test script for model loading and adversarial attack generation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using absolute paths
sys.path.insert(0, 'src')
from config.settings import config
from models.model_factory import ModelFactory
from attacks.attack_factory import AttackFactory
from utils.image_processing import ImageProcessor, ImageValidator

def test_model_and_attack():
    """Test model loading and attack generation."""
    print("🧪 Testing Model Loading and Attack Generation")
    print("=" * 50)
    
    try:
        # Initialize components
        print("1. Initializing components...")
        model_factory = ModelFactory(config.model)
        attack_factory = AttackFactory(config.attack)
        image_processor = ImageProcessor(config.ui)
        image_validator = ImageValidator(config.ui)
        print("   ✅ Components initialized")
        
        # Test model loading
        print("2. Loading model...")
        model = model_factory.get_model()
        print(f"   ✅ Model loaded: {type(model).__name__}")
        
        # Test with STOP sign image
        print("3. Testing with STOP sign image...")
        test_image_path = "tests/STOP_sign.jpg"
        
        if not os.path.exists(test_image_path):
            print(f"   ❌ Test image not found: {test_image_path}")
            return
        
        # Load and process image
        image = image_processor.load_image(test_image_path)
        image_processor.validate_image(image)
        print(f"   ✅ Image loaded: {image.size} {image.mode}")
        
        # Get original predictions
        print("4. Getting original predictions...")
        image_tensor = model.preprocess(image)
        original_predictions = model.get_predictions(image_tensor)
        print(f"   ✅ Original prediction: {original_predictions[0]['class_name']} ({original_predictions[0]['confidence']:.3f})")
        
        # Generate adversarial attack
        print("5. Generating adversarial attack...")
        attack = attack_factory.get_attack("fgsm", epsilon=0.1)
        adversarial_tensor = attack(image_tensor, model.model)
        
        # Convert back to image
        adversarial_image = image_processor.tensor_to_pil(adversarial_tensor)
        print(f"   ✅ Adversarial image generated: {adversarial_image.size}")
        
        # Get adversarial predictions
        adversarial_predictions = model.get_predictions(adversarial_tensor)
        print(f"   ✅ Adversarial prediction: {adversarial_predictions[0]['class_name']} ({adversarial_predictions[0]['confidence']:.3f})")
        
        # Check if attack was successful
        original_class = original_predictions[0]['class_id']
        adversarial_class = adversarial_predictions[0]['class_id']
        
        if original_class != adversarial_class:
            print("   🎯 Attack successful! Prediction changed.")
        else:
            print("   🛡️ Attack unsuccessful. Prediction unchanged.")
        
        # Show confidence comparison
        original_conf = original_predictions[0]['confidence']
        adversarial_conf = adversarial_predictions[0]['confidence']
        confidence_drop = original_conf - adversarial_conf
        
        print(f"   📊 Confidence drop: {confidence_drop:.3f}")
        
        print("\n🎉 All tests passed! The application should work correctly.")
        print("\n📝 Next steps:")
        print("   1. Open http://localhost:8501 in your browser")
        print("   2. Upload tests/STOP_sign.jpg")
        print("   3. Click 'Generate Attack'")
        print("   4. Compare the results")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_and_attack() 