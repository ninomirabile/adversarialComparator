#!/usr/bin/env python3
"""
Launcher script for Adversarial Comparator
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application."""
    print("🎯 Adversarial Comparator - Phase 1")
    print("=" * 40)
    print("Launching Streamlit application...")
    print("The app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("=" * 40)
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 