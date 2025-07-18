#!/usr/bin/env python3
"""
Simple test script for Adversarial Comparator - Phase 1
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_basic_functionality():
    """Test basic functionality without relative imports."""
    print("🧪 Testing Adversarial Comparator - Phase 1")
    print("=" * 50)
    
    try:
        # Test imports
        print("Testing imports...")
        
        # Import config
        from config.settings import config
        print("✓ Config loaded successfully")
        print(f"  - Phase: {config.phase} - {config.phase_name}")
        print(f"  - Model: {config.model.model_type}")
        print(f"  - Device: {config.model.device}")
        
        # Import factories
        from models.model_factory import ModelFactory
        from attacks.attack_factory import AttackFactory
        print("✓ Factories imported successfully")
        
        # Test model factory
        print("\nTesting model factory...")
        model_factory = ModelFactory(config.model)
        available_models = model_factory.list_available_models()
        print(f"✓ Available models: {available_models}")
        
        # Test attack factory
        print("\nTesting attack factory...")
        attack_factory = AttackFactory(config.attack)
        available_attacks = attack_factory.list_available_attacks()
        print(f"✓ Available attacks: {available_attacks}")
        
        # Test attack creation
        attack = attack_factory.get_attack('fgsm', epsilon=0.1)
        print(f"✓ FGSM attack created with epsilon={attack.epsilon}")
        
        print("\n" + "=" * 50)
        print("🎉 All basic tests passed!")
        print("\nThe application should be ready to run.")
        print("To start the Streamlit app:")
        print("  streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1) 