#!/usr/bin/env python3
"""
ReadItNow - A beautiful terminal UI for browsing Obsidian ReadItLater notes

This is the main entrypoint for the ReadItNow application.
"""

import sys
from config import load_or_create_config
from app import ReadItNowApp

def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        import textual
        import rich
        import yaml
        import frontmatter
        from importlib.metadata import version
        
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Main application entrypoint."""
    # Check dependencies
    if not check_dependencies():
        print("❌ Some dependencies are missing. Please check your environment.")
        sys.exit(1)
    
    # Load configuration
    config = load_or_create_config()
    
    # Launch the TUI application
    try:
        app = ReadItNowApp(config=config)
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running ReadItNow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 