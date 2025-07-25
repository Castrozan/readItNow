#!/usr/bin/env python3
"""
ReadItNow - A beautiful terminal UI for browsing Obsidian ReadItLater notes

This is the main entrypoint for the ReadItNow application.
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        import textual
        import rich
        import yaml
        import frontmatter
        from importlib.metadata import version
        
        print("✅ All dependencies are available:")
        print(f"  - textual: {version('textual')}")
        print(f"  - rich: {version('rich')}")
        print(f"  - python-frontmatter: {version('python-frontmatter')}")
        print(f"  - PyYAML: {version('pyyaml')}")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Main application entrypoint."""
    print("🚀 ReadItNow - Terminal UI for Obsidian ReadItLater")
    print("=" * 50)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Some dependencies are missing. Please check your environment.")
        sys.exit(1)
    
    print("\n📍 Project Information:")
    print(f"  - Python version: {sys.version}")
    print(f"  - Running from: {Path(__file__).parent.absolute()}")
    
    print("\n🎯 Next Steps:")
    print("  1. The devenv environment is working correctly!")
    print("  2. All required dependencies are installed")
    print("  3. Ready to start building the terminal UI")
    
    print("\n💡 Available commands:")
    print("  - readitnow: Run this application")
    print("  - readitnow-dev: Run in development mode")
    
    print("\n🔧 Development Environment Status: ✅ Ready")

if __name__ == "__main__":
    main() 