from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Static
from widgets.note_card import NoteCard

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