from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static
from widgets.notes_grid import NotesGrid
import datetime

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