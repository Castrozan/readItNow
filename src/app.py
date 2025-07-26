from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static
from widgets.notes_grid import NotesGrid
from vault_reader import VaultReader
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
        ("up", "scroll_up", "Scroll Up"),
        ("down", "scroll_down", "Scroll Down"),
    ]
    
    def __init__(self, config: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or {}
        # TODO: check if vault_path and display error to user
        self.vault_path = self.config.get('vault_path', '')
        
        try:
            # Initialize vault reader
            self.vault_reader = VaultReader(self.config)
            self.notes = self.vault_reader.get_recent_notes()
            self.vault_stats = self.vault_reader.get_vault_stats()
        except Exception as e:
            print(f"Error initializing vault reader: {e}")
            self.vault_reader = None
            self.notes = []
            self.vault_stats = {'total_notes': 0, 'showing_notes': 0}

    def compose(self) -> ComposeResult:
        """Create the main application layout."""
        # Header
        yield Static("🚀 ReadItNow - Your ReadItLater Notes", classes="header")
        
        # Main content area with notes grid
        with Container(classes="main-content"):
            yield NotesGrid(self.notes)
        
        # Footer with keybindings
        yield Static("Press 'q' to quit • ↑↓ Scroll • Enter Open", classes="footer")
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_scroll_up(self) -> None:
        """Scroll up the notes grid."""
        self.query_one(NotesGrid).scroll_up()

    def action_scroll_down(self) -> None:
        """Scroll down the notes grid."""
        self.query_one(NotesGrid).scroll_down() 