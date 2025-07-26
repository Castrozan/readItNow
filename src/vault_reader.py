import os
from pathlib import Path
from typing import List, Dict, Optional
from note_parser import NoteParser
import re

class VaultReader:
    """Manage reading and organizing notes from the Obsidian vault."""
    
    def __init__(self, config: dict):
        self.config = config
        self.vault_path = Path(config['vault_path'])
        self.max_notes = config.get('max_notes', 20)
        self.parser = NoteParser(config)
        
        # Validate vault path
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault path does not exist: {self.vault_path}")
        if not self.vault_path.is_dir():
            raise NotADirectoryError(f"Vault path is not a directory: {self.vault_path}")
    
    def get_recent_notes(self) -> List[dict]:
        """Get the most recent notes from the vault, sorted by modification time."""
        try:
            # Find all markdown files
            md_files = list(self.vault_path.glob("*.md"))
            
            # Filter out hidden files
            md_files = [f for f in md_files if not f.name.startswith('.')]
            
            # Sort by modification time (newest first)
            md_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Limit to max_notes
            md_files = md_files[:self.max_notes]
            
            # Parse each file
            notes = []
            for file_path in md_files:
                try:
                    note_data = self.parser.parse_file(file_path)
                    notes.append(note_data)
                except Exception as e:
                    # Log error but continue with other files
                    print(f"Warning: Could not parse {file_path}: {e}")
                    continue
            
            return notes
            
        except Exception as e:
            print(f"Error reading vault: {e}")
            return []
    
    def get_note_by_path(self, file_path: str) -> Optional[dict]:
        """Get a specific note by its file path."""
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            return self.parser.parse_file(path)
        except Exception as e:
            print(f"Error reading note {file_path}: {e}")
            return None
    
    def mark_as_read(self, file_path: str) -> bool:
        """Mark a note as read by adding [[readitnow/read]] tag."""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # Read current content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already marked as read
            if re.search(r'\[\[readitnow/read\]\]', content, re.IGNORECASE):
                return True  # Already marked as read
            
            # Add read tag at the end
            if content.strip():
                content += "\n\n[[readitnow/read]]"
            else:
                content = "[[readitnow/read]]"
            
            # Write back to file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error marking note as read {file_path}: {e}")
            return False
    
    def mark_as_unread(self, file_path: str) -> bool:
        """Mark a note as unread by removing [[readitnow/read]] tag."""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # Read current content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove read tag (case-insensitive)
            content = re.sub(r'\s*\[\[readitnow/read\]\]\s*', '', content, flags=re.IGNORECASE)
            
            # Clean up extra whitespace
            content = re.sub(r'\n\s*\n\s*$', '\n', content)
            content = content.strip()
            
            # Write back to file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error marking note as unread {file_path}: {e}")
            return False
    
    def toggle_read_status(self, file_path: str) -> bool:
        """Toggle the read status of a note."""
        try:
            # First check current status
            note_data = self.get_note_by_path(file_path)
            if not note_data:
                return False
            
            if note_data['is_read']:
                return self.mark_as_unread(file_path)
            else:
                return self.mark_as_read(file_path)
                
        except Exception as e:
            print(f"Error toggling read status {file_path}: {e}")
            return False
    
    def get_vault_stats(self) -> dict:
        """Get statistics about the vault."""
        try:
            md_files = list(self.vault_path.glob("*.md"))
            md_files = [f for f in md_files if not f.name.startswith('.')]
            
            total_notes = len(md_files)
            
            # Count read notes (this is expensive, so only do it if needed)
            read_notes = 0
            for file_path in md_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if re.search(r'\[\[readitnow/read\]\]', content, re.IGNORECASE):
                        read_notes += 1
                except Exception:
                    continue
            
            return {
                'total_notes': total_notes,
                'read_notes': read_notes,
                'unread_notes': total_notes - read_notes,
                'vault_path': str(self.vault_path),
                'showing_notes': min(total_notes, self.max_notes)
            }
            
        except Exception as e:
            print(f"Error getting vault stats: {e}")
            return {
                'total_notes': 0,
                'read_notes': 0,
                'unread_notes': 0,
                'vault_path': str(self.vault_path),
                'showing_notes': 0
            } 