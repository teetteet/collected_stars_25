"""
BulletML Pattern Generator - Main Entry Point
Launch the application
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import create_gui


def main():
    """Main entry point for the application"""
    print("=" * 60)
    print("BulletML Pattern Generator")
    print("=" * 60)
    print("\nKeyboard Shortcuts:")
    print("  Ctrl+S - Save pattern")
    print("  Ctrl+O - Load pattern")
    print("  Ctrl+R - Reset to defaults")
    print("  Ctrl+U - Update preview")
    print("  Ctrl+1 - Load Spiral preset")
    print("  Ctrl+2 - Load Circle preset")
    print("  Ctrl+3 - Load Wave preset")
    print("  Ctrl+4 - Load Flower preset")
    print("\nStarting GUI...")
    print("=" * 60)
    
    # Create and run the GUI
    gui = create_gui()
    gui.run()


if __name__ == "__main__":
    main()
