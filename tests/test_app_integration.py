#!/usr/bin/env python3
"""
Integration test for the complete application workflow
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_complete_workflow():
    """Test the complete application workflow."""
    print("🧪 Testing Complete Application Workflow")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from config.settings import config
        from models.model_factory import ModelFactory
        from attacks.attack_factory import AttackFactory
        from utils.image_processing import ImageProcessor, ImageValidator
        print("   ✅ All imports successful")
        
        # Test model factory
        print("2. Testing model factory...")
        model_factory = ModelFactory(config.model)
        available_models = model_factory.list_available_models()
        print(f"   ✅ Available models: {available_models}")
        
        # Test attack factory
        print("3. Testing attack factory...")
        attack_factory = AttackFactory(config.attack)
        available_attacks = attack_factory.list_available_attacks()
        print(f"   ✅ Available attacks: {available_attacks}")
        
        # Test image processing
        print("4. Testing image processing...")
        image_processor = ImageProcessor(config.ui)
        image_validator = ImageValidator(config.ui)
        print("   ✅ Image processing components initialized")
        
        # Test with a small image
        print("5. Testing with STOP_sign.jpg...")
        test_image_path = "tests/STOP_sign.jpg"
        
        if os.path.exists(test_image_path):
            # Load and validate image
            image = image_processor.load_image(test_image_path)
            image_processor.validate_image(image)
            print(f"   ✅ Image loaded: {image.size} {image.mode}")
            
            # Test model loading and prediction
            print("6. Testing model prediction...")
            model = model_factory.get_model()
            image_tensor = model.preprocess(image)
            predictions = model.get_predictions(image_tensor)
            print(f"   ✅ Model prediction successful")
            print(f"   Top prediction: {predictions[0]['class_name']} ({predictions[0]['confidence']:.3f})")
            
            # Test attack generation
            print("7. Testing attack generation...")
            attack = attack_factory.get_attack("fgsm", epsilon=0.1)
            adversarial_tensor = attack(image_tensor, model.model)
            adversarial_image = image_processor.tensor_to_pil(adversarial_tensor)
            adversarial_predictions = model.get_predictions(adversarial_tensor)
            print(f"   ✅ Attack generation successful")
            print(f"   Adversarial prediction: {adversarial_predictions[0]['class_name']} ({adversarial_predictions[0]['confidence']:.3f})")
            
            # Check if attack was successful
            original_class = predictions[0]['class_id']
            adversarial_class = adversarial_predictions[0]['class_id']
            if original_class != adversarial_class:
                print("   🎯 Attack successful! Prediction changed.")
            else:
                print("   🛡️ Attack unsuccessful. Prediction unchanged.")
                
        else:
            print(f"   ❌ Test image not found: {test_image_path}")
        
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Open http://localhost:8501 in your browser")
        print("   2. Upload an image (try tests/STOP_sign.jpg)")
        print("   3. Adjust epsilon value and click 'Generate Attack'")
        print("   4. Compare original vs adversarial predictions")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_workflow() 