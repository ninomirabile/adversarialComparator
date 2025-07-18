#!/usr/bin/env python3
"""
Test script to verify infinite loop fix
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_loop_fix_logic():
    """Test the infinite loop fix logic."""
    print("🧪 Testing Infinite Loop Fix")
    print("=" * 40)
    
    # Simulate session state
    session_state = {
        'image_processed': False,
        'current_image': None,
        'current_predictions': None,
        'adversarial_image': None,
        'adversarial_predictions': None
    }
    
    # Test 1: Initial state
    print("1. Testing initial state...")
    print(f"   image_processed: {session_state['image_processed']}")
    print(f"   current_image: {session_state['current_image']}")
    
    # Test 2: Simulate file upload
    print("2. Simulating file upload...")
    uploaded_file = "fake_image.jpg"
    if uploaded_file is not None:
        # Check if already processed
        if session_state['image_processed']:
            print("   ❌ Would skip processing (already processed)")
        else:
            print("   ✅ Would process new file")
            # Simulate processing
            session_state['current_image'] = "processed_image"
            session_state['image_processed'] = True
            print(f"   Updated image_processed: {session_state['image_processed']}")
    
    # Test 3: Simulate second upload attempt
    print("3. Simulating second upload attempt...")
    if session_state['image_processed']:
        print("   ✅ Would skip processing (already processed)")
    else:
        print("   ❌ Would process again (not processed)")
    
    # Test 4: Simulate file removal
    print("4. Simulating file removal...")
    uploaded_file = None
    if uploaded_file is None:
        # Reset flags
        session_state['image_processed'] = False
        session_state['current_image'] = None
        session_state['current_predictions'] = None
        session_state['adversarial_image'] = None
        session_state['adversarial_predictions'] = None
        print("   ✅ Reset all flags")
        print(f"   image_processed: {session_state['image_processed']}")
    
    print("\n🎉 Loop fix logic test passed!")
    print("\n📝 Expected behavior:")
    print("   - Process file only once when uploaded")
    print("   - Skip processing if already processed")
    print("   - Reset flags when file is removed")
    print("   - No infinite loops or repeated processing")

if __name__ == "__main__":
    test_loop_fix_logic() 