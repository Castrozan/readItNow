#!/usr/bin/env python3
"""
ReadItNow - A beautiful terminal UI for browsing Obsidian ReadItLater notes

This is the main entrypoint for the ReadItNow application.
"""

import sys
from pathlib import Path
from config import load_or_create_config

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
    print("🚀 ReadItNow - Terminal UI for Obsidian ReadItLater")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Some dependencies are missing. Please check your environment.")
        sys.exit(1)
    
    config = load_or_create_config()
    vault_path = config.get('vault_path')
    
    print("\n✅ Configuration loaded successfully!")
    print(f"  - Vault Path: {vault_path}")

    # Further implementation will go here...

if __name__ == "__main__":
    main() 