from textual.containers import Container, Vertical
from textual.widgets import Static, Label
from textual.widget import Widget
from textual.app import ComposeResult

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
        self.is_read = note_data.get("is_read", False)
        
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
                yield Label(title, classes="title", markup=False)
                
                # Excerpt
                excerpt = self.note_data.get("excerpt", "No excerpt available")
                if len(excerpt) > 80:
                    excerpt = excerpt[:77] + "..."
                yield Label(excerpt, classes="excerpt", markup=False)
                
                # Tags
                tags = self.note_data.get("tags", [])
                tag_text = " ".join([f"#{tag}" for tag in tags[:3]])  # Show max 3 tags
                if len(tags) > 3:
                    tag_text += " ..."
                if self.is_read:
                    tag_text = "✅ " + tag_text
                yield Label(tag_text, classes="tags", markup=False)
    
    def on_mount(self) -> None:
        """Apply read styling if needed."""
        if self.is_read:
            self.add_class("read") 