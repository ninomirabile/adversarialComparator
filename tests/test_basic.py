#!/usr/bin/env python3
"""
Basic test script for Adversarial Comparator - Phase 1
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from config.settings import config
        print("✓ Config imported successfully")
        
        from models.model_factory import ModelFactory
        print("✓ ModelFactory imported successfully")
        
        from attacks.attack_factory import AttackFactory
        print("✓ AttackFactory imported successfully")
        
        from utils.image_processing import ImageProcessor, ImageValidator
        print("✓ Image utilities imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from config.settings import config
        
        print(f"✓ Phase: {config.phase} - {config.phase_name}")
        print(f"✓ Model: {config.model.model_type}")
        print(f"✓ Device: {config.model.device}")
        print(f"✓ Available attacks: {config.attack.available_attacks}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_model_factory():
    """Test model factory."""
    print("\nTesting model factory...")
    
    try:
        from config.settings import config
        from models.model_factory import ModelFactory
        
        factory = ModelFactory(config.model)
        available_models = factory.list_available_models()
        print(f"✓ Available models: {available_models}")
        
        # Test model creation (this will download the model)
        print("Loading ResNet18 model (this may take a moment)...")
        model = factory.get_model('resnet18')
        model_info = model.get_model_info()
        print(f"✓ Model loaded: {model_info['model_type']}")
        print(f"✓ Parameters: {model_info['total_parameters']:,}")
        
        return True
    except Exception as e:
        print(f"✗ Model factory test failed: {e}")
        return False

def test_attack_factory():
    """Test attack factory."""
    print("\nTesting attack factory...")
    
    try:
        from config.settings import config
        from attacks.attack_factory import AttackFactory
        
        factory = AttackFactory(config.attack)
        available_attacks = factory.list_available_attacks()
        print(f"✓ Available attacks: {available_attacks}")
        
        # Test attack creation
        attack = factory.get_attack('fgsm', epsilon=0.1)
        attack_info = attack.get_attack_info()
        print(f"✓ Attack created: {attack_info['attack_type']}")
        print(f"✓ Epsilon: {attack_info['epsilon']}")
        
        return True
    except Exception as e:
        print(f"✗ Attack factory test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Adversarial Comparator - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_model_factory,
        test_attack_factory
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("  streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 