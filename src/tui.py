from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Label
from textual.widget import Widget
from textual.css.query import NoMatches
from rich.text import Text
from rich.markdown import Markdown
from rich.panel import Panel
from rich.console import Console
from pathlib import Path
import datetime

class NoteCard(Widget):
    """A card widget representing a single note from ReadItLater."""
    
    DEFAULT_CSS = """
    NoteCard {
        width: 1fr;
        height: 12;
        margin: 1;
        border: solid $primary;
        background: $surface;
    }
    
    NoteCard:hover {
        border: solid $accent;
        background: $primary-background;
    }
    
    NoteCard.read {
        opacity: 0.7;
        border: solid;
    }
    
    .thumbnail {
        width: 8;
        height: 4;
        background: $secondary;
        margin: 1 0 0 1;
    }
    
    .content {
        margin: 1;
        height: 1fr;
    }
    
    .title {
        text-style: bold;
        color: $text;
    }
    
    .excerpt {
        color: $text-muted;
        margin: 1 0;
    }
    
    .tags {
        color: $secondary;
        margin: 1 0 0 0;
    }
    """
    
    def __init__(self, note_data: dict, **kwargs):
        super().__init__(**kwargs)
        self.note_data = note_data
        self.is_read = "readitnow/read" in note_data.get("tags", [])
        
    def compose(self) -> ComposeResult:
        """Create the note card layout."""
        with Container():
            # Thumbnail placeholder
            yield Static("🖼️", classes="thumbnail")
            
            # Content area
            with Vertical(classes="content"):
                # Title
                title = self.note_data.get("title", "Untitled")
                if len(title) > 30:
                    title = title[:27] + "..."
                yield Label(title, classes="title")
                
                # Excerpt
                excerpt = self.note_data.get("excerpt", "No excerpt available")
                if len(excerpt) > 80:
                    excerpt = excerpt[:77] + "..."
                yield Label(excerpt, classes="excerpt")
                
                # Tags
                tags = self.note_data.get("tags", [])
                tag_text = " ".join([f"#{tag}" for tag in tags[:3]])  # Show max 3 tags
                if len(tags) > 3:
                    tag_text += " ..."
                if self.is_read:
                    tag_text = "✅ " + tag_text
                yield Label(tag_text, classes="tags")
    
    def on_mount(self) -> None:
        """Apply read styling if needed."""
        if self.is_read:
            self.add_class("read")

class NotesGrid(ScrollableContainer):
    """A scrollable container for notes in a 2-column grid."""
    
    DEFAULT_CSS = """
    NotesGrid {
        height: 1fr;
        scrollbar-gutter: stable;
    }
    
    .grid-row {
        height: auto;
        margin: 0;
    }
    """
    
    def __init__(self, notes: list[dict], **kwargs):
        super().__init__(**kwargs)
        self.notes = notes
    
    def compose(self) -> ComposeResult:
        """Create the 2-column grid of note cards."""
        # Group notes into pairs for 2-column layout
        for i in range(0, len(self.notes), 2):
            with Horizontal(classes="grid-row"):
                # Left column
                yield NoteCard(self.notes[i])
                
                # Right column (if exists)
                if i + 1 < len(self.notes):
                    yield NoteCard(self.notes[i + 1])
                else:
                    # Empty space for odd number of notes
                    yield Static()

class ReadItNowApp(App):
    """The main ReadItNow terminal application."""
    
    CSS = """
    Screen {
        background: $background;
    }
    
    .header {
        height: 3;
        background: $primary;
        color: $text;
        content-align: center middle;
        text-style: bold;
    }
    
    .main-content {
        height: 1fr;
    }
    
    .footer {
        height: 1;
        background: $secondary;
        color: $text;
        content-align: center middle;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]
    
    def __init__(self, vault_path: str, **kwargs):
        super().__init__(**kwargs)
        self.vault_path = vault_path
        self.mock_notes = self._create_mock_notes()
    
    def _create_mock_notes(self) -> list[dict]:
        """Create mock note data for demonstration."""
        return [
            {
                "title": "How to Build Better Software with Clean Architecture",
                "excerpt": "Clean architecture is a software design philosophy that separates the elements of a design into ring levels. The main rule is that code dependencies can only point inwards...",
                "tags": ["architecture", "software", "development"],
                "url": "https://example.com/clean-architecture",
                "file_path": "clean-architecture.md",
                "modified": datetime.datetime.now()
            },
            {
                "title": "The Rise of AI in Modern Development",
                "excerpt": "Artificial Intelligence is transforming how we write, test, and deploy software. From code completion to automated testing, AI tools are becoming essential...",
                "tags": ["ai", "development", "tools", "readitnow/read"],
                "url": "https://example.com/ai-development", 
                "file_path": "ai-development.md",
                "modified": datetime.datetime.now()
            },
            {
                "title": "Mastering Python Asyncio",
                "excerpt": "Asynchronous programming in Python can be challenging but extremely powerful. This guide covers the fundamentals of asyncio and how to write efficient async code...",
                "tags": ["python", "asyncio", "programming"],
                "url": "https://example.com/python-asyncio",
                "file_path": "python-asyncio.md", 
                "modified": datetime.datetime.now()
            },
            {
                "title": "Terminal UI Design Principles",
                "excerpt": "Creating beautiful and functional terminal user interfaces requires understanding both technical constraints and user experience principles. Here's what you need to know...",
                "tags": ["tui", "design", "terminal", "ux"],
                "url": "https://example.com/tui-design",
                "file_path": "tui-design.md",
                "modified": datetime.datetime.now()
            }
        ]
    
    def compose(self) -> ComposeResult:
        """Create the main application layout."""
        # Header
        yield Static("🚀 ReadItNow - Your ReadItLater Notes", classes="header")
        
        # Main content area with notes grid
        with Container(classes="main-content"):
            yield NotesGrid(self.mock_notes)
        
        # Footer with keybindings
        yield Static("Press 'q' to quit • ↑↓ Scroll • Enter Open", classes="footer")
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

def run_app(vault_path: str) -> None:
    """Run the ReadItNow TUI application."""
    app = ReadItNowApp(vault_path)
    app.run() 