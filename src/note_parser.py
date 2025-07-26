import re
from pathlib import Path
from typing import List, Dict
import datetime

class NoteParser:
    """Parse Obsidian-format notes with robust error handling."""
    
    def __init__(self, config: dict):
        self.config = config
        self.excerpt_lines = config.get('excerpt_lines', 5)
        self.skip_empty_lines = True
        self.strip_markdown = True
        self.safe_mode = True
    
    def parse_file(self, file_path: Path) -> dict:
        """Parse a note file with robust error handling."""
        note_data = {
            "title": "Untitled",
            "excerpt": "No content available", 
            "tags": [],
            "url": "",
            "file_path": str(file_path),
            "modified": datetime.datetime.now(),
            "thumbnail_url": "",
            "is_read": False
        }
        
        try:
            # Extract title from filename
            note_data["title"] = self.extract_title(file_path)
            
            # Read and parse file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            note_data["tags"] = self.extract_tags(content)
            note_data["excerpt"] = self.extract_excerpt(content, self.excerpt_lines)
            note_data["url"] = self.extract_url(content)
            note_data["thumbnail_url"] = self.extract_thumbnail(content, note_data["url"])
            note_data["is_read"] = self.is_read(content)
            
        except Exception as e:
            if not self.safe_mode:
                raise
            # In safe mode, log error but continue with defaults
            print(f"Warning: Error parsing {file_path}: {e}")
        
        return note_data
    
    def extract_title(self, file_path: Path) -> str:
        """Extract title from filename, removing .md extension."""
        try:
            return file_path.stem
        except Exception:
            return "Untitled"
    
    def extract_tags(self, content: str) -> List[str]:
        """Extract tags from [[tag-here]] wiki-link format."""
        try:
            # Pattern to match [[tag]] but exclude URLs
            pattern = r'\[\[([^\]]+)\]\]'
            matches = re.findall(pattern, content)
            
            # Filter out URLs and clean tags
            tags = []
            for match in matches:
                # Skip if it looks like a URL
                if '://' in match or match.startswith('http'):
                    continue
                # Clean and add tag
                clean_tag = match.strip()
                if clean_tag:
                    tags.append(clean_tag)
            
            return tags
        except Exception:
            return []
    
    def extract_excerpt(self, content: str, lines: int) -> str:
        """Extract first N lines of content for preview."""
        try:
            content_lines = content.split('\n')
            excerpt_lines = []
            lines_collected = 0
            
            for line in content_lines:
                # Skip empty lines if configured
                if self.skip_empty_lines and not line.strip():
                    continue
                
                # Skip wiki-link only lines
                if re.match(r'^\s*\[\[.*\]\]\s*$', line):
                    continue
                
                # Process line
                processed_line = line.strip()
                
                # Strip basic markdown if configured
                if self.strip_markdown:
                    # Remove markdown headers
                    processed_line = re.sub(r'^#+\s*', '', processed_line)
                    # Remove markdown links but keep text: [text](url) -> text
                    processed_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', processed_line)
                    # Remove markdown emphasis
                    processed_line = re.sub(r'\*\*(.*?)\*\*', r'\1', processed_line)
                    processed_line = re.sub(r'\*(.*?)\*', r'\1', processed_line)
                
                if processed_line:
                    excerpt_lines.append(processed_line)
                    lines_collected += 1
                    
                    if lines_collected >= lines:
                        break
            
            return ' '.join(excerpt_lines) if excerpt_lines else "No content available"
            
        except Exception:
            return "No content available"
    
    def extract_url(self, content: str) -> str:
        """Extract URL from markdown links or iframe."""
        try:
            # Look for markdown links: [Title](URL)
            markdown_link = re.search(r'\[([^\]]+)\]\(([^)]+)\)', content)
            if markdown_link:
                url = markdown_link.group(2)
                # Skip pic.twitter.com and other image URLs for main URL
                if not ('pic.twitter.com' in url or 't.co' in url):
                    return url
            
            # Look for iframe src
            iframe_match = re.search(r'<iframe[^>]+src=[\'"]+([^\'\"]+)[\'"]+', content)
            if iframe_match:
                return iframe_match.group(1)
            
            # Look for plain URLs (as fallback)
            url_match = re.search(r'https?://[^\s\)]+', content)
            if url_match:
                url = url_match.group(0)
                # Clean up URL (remove trailing punctuation)
                url = re.sub(r'[\.,%]+$', '', url)
                return url
                
            return ""
        except Exception:
            return ""
    
    def extract_thumbnail(self, content: str, url: str) -> str:
        """Extract thumbnail URL from Twitter/YouTube content."""
        try:
            # Twitter image: look for pic.twitter.com
            twitter_pic = re.search(r'pic\.twitter\.com/([a-zA-Z0-9]+)', content)
            if twitter_pic:
                # Note: This is a simplified approach. Real implementation might
                # need to resolve t.co links or use Twitter API
                return f"https://pbs.twimg.com/media/{twitter_pic.group(1)}.jpg"
            
            # YouTube thumbnail: extract video ID from URL
            if url and 'youtube.com' in url:
                # Pattern: youtube.com/watch?v=VIDEO_ID
                video_match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
                if video_match:
                    video_id = video_match.group(1)
                    return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            
            # YouTube embed: extract from iframe
            youtube_embed = re.search(r'youtube(?:-nocookie)?\.com/embed/([a-zA-Z0-9_-]+)', content)
            if youtube_embed:
                video_id = youtube_embed.group(1)
                return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            
            return ""
        except Exception:
            return ""
    
    def is_read(self, content: str) -> bool:
        """Check if note is marked as read."""
        try:
            # Look for [[readitnow/read]] tag (case-insensitive)
            return bool(re.search(r'\[\[readitnow/read\]\]', content, re.IGNORECASE))
        except Exception:
            return False 