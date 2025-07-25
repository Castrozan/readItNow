# ReadItNow

A beautiful, two-column, infinite-scroll terminal UI that surfaces the newest items from your Obsidian ReadItLater folder, making it irresistible to "read it now".

## 🚀 Features

- **📚 Entry Listing**: Display latest Markdown notes from your ReadItLater folder in a two-column grid
- **🎨 Note Cards**: Rich previews with thumbnails, titles, excerpts, and tags
- **♾️ Infinite Scroll**: Automatically load more content as you scroll
- **⌨️ Keyboard Navigation**: Intuitive arrow key and shortcut controls
- **📱 Smart Interactions**: Open links in browser, edit files, toggle read status
- **🏷️ Tag Management**: Seamless read/unread state tracking via front-matter tags

## 🛠️ Installation

to be done

## ⚙️ Configuration

Create your configuration file at `~/.config/readitnow/config.yaml`:

```yaml
# Path to your Obsidian vault's ReadItLater folder
vault_path: "/home/you/vault/plugins/readitlater"

# Custom keybindings (optional)
keybindings:
  open_link: "enter"
  open_file: "shift+enter"
  up: "up"
  down: "down"
  left: "left"
  right: "right"
  page_up: "pageup"
  page_down: "pagedown"
  quit: "q"

# Thumbnail cache location
thumbnail_cache: "~/.cache/readitnow/thumbnails"
```

## 🎮 Usage

### Starting the App

to be done

### Keyboard Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Navigate between cards |
| **Page Up/Down** | Scroll the grid view |
| **Enter** | Open note's URL in browser |
| **Shift+Enter** | Open note file in default editor |
| **r** | Toggle read/unread state |
| **q** | Quit the application |

### Note Card Features

Each note card displays:
- **Thumbnail**: Preview for YouTube/X/Twitter/Imgur links or placeholder
- **Title**: From front-matter `title` or filename
- **Excerpt**: First paragraph rendered with Rich Markdown
- **Tags**: User tags with special read status badge
- **Read State**: Visual indicator for `readitnow/read` tagged notes

## 🔧 Technical Details

### Front-Matter Integration

ReadItNow uses YAML front-matter to track read status:

```yaml
---
title: "My Cool Article"
date: "2025-07-25"
tags:
  - readitlater
  - readitnow/read  # Added when marked as read
---
Body of the note...
```

### State Management

- **No external database**: All state lives in your Obsidian vault
- **Version controlled**: Changes are tracked with your notes
- **Portable**: Works across different machines

## 🤝 Contributing

to be done

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Textual](https://textual.textualize.io/) for the terminal UI
- Inspired by the need for better ReadItLater workflow management
- Thanks to the Obsidian community for the ReadItLater plugin
