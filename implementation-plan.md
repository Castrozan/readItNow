# ReadItNow Project Specification

## 1. Project Name & Branding

* **Chosen Name**: **ReadItNow**

## 2. Purpose & Vision

Build a **beautiful**, **two‑column**, **infinite‑scroll** terminal UI that surfaces the newest items from your Obsidian ReadItLater folder, making it irresistible to "read it now".

## 3. Key Features

1. **Entry Listing**

   * Show the latest *N* Markdown notes from `vault/ReadItLater Inbox`, sorted by modification time.
   * Render as a two‑column grid, with as many rows as fit the terminal.

2. **Note Card**

   * **Thumbnail** preview (Twitter/YouTube links) or placeholder.
   * **Title** (from filename without .md extension).
   * **Excerpt**: first N lines of the Markdown body (configurable, default: 5).
   * **Tags**: extracted from `[[tag-here]]` wiki-link format.
   * **Read State**: visually differentiate cards tagged `[[readitnow/read]]` (e.g. dimmed or ✔ badge).

3. **Infinite Scroll**

   * Automatically load the next batch of notes when scrolling to the end.

4. **Interactions & Keybindings**

   * **Arrow Keys** (↑↓←→): move focus among cards and scroll
   * **PageUp/PageDown**: scroll the grid view
   * **Enter**: open the note's `url` in the default browser
   * **Shift+Enter**: open the `.md` note file in the default editor
   * **r**: toggle read/unread state (adds/removes `[[readitnow/read]]` tag)
   * **q**: quit the app

## 4. Persistence & Configuration

### a) Configuration File (YAML)

* **Path:** `~/.config/readitnow/config.yaml`
* **Schema:**

  ```yaml
  vault_path: "/home/you/vault/ReadItLater Inbox"
  max_notes: 20
  excerpt_lines: 5
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
  thumbnail_cache: "~/.cache/readitnow/thumbnails"
  ```

> **Note:** Only this YAML is persisted externally. All other state lives in your vault.

### b) Read/Unread State via Wiki-Link Tags

* **Tag:** `[[readitnow/read]]`
* **Mechanism:** On toggle, append or remove this tag from the note content.
* **Advantages:** No external database, fully version‑controlled and portable with your notes.

## 5. Note Parsing (Obsidian Format)

ReadItNow adapts to your existing Obsidian note format without requiring YAML front-matter:

### Sample Note Structure:
```markdown
[[ReadItLater]] [[Tweet]]

# [Aadit Sheth](https://twitter.com/aaditsh/status/1909332848152105301)

> This guy literally turned WhatsApp into an AI assistant using Claude and ElevenLabs[pic.twitter.com/f77uIBIQkj](https://t.co/f77uIBIQkj)
> 
> — Aadit Sheth (@aaditsh) [April 7, 2025](https://twitter.com/aaditsh/status/1909332848152105301?ref_src=twsrc%5Etfw)
```

### Parsing Strategy:

1. **Title Extraction**: Use filename (without .md extension)
2. **Tags Extraction**: Extract from `[[tag-here]]` wiki-links using regex `\[\[([^\]]+)\]\]`
3. **Content Extraction**: First N lines (configurable, default: 5), skip empty lines
4. **URL Extraction**: Extract from `[Title](URL)` markdown links or `<iframe src="...">`
5. **Thumbnail Detection**:
   - **Twitter**: Search for `pic.twitter.com/` or `t.co/` image links
   - **YouTube**: Extract video ID and construct thumbnail URL `https://img.youtube.com/vi/VIDEO_ID/mqdefault.jpg`
6. **Read Status**: Search for `[[readitnow/read]]` tag in content

### Error Handling:

All parsing uses defensive programming with sensible defaults:
- Title: `"Untitled"` if filename invalid
- Excerpt: `"No content available"` if content empty
- Tags: `[]` (empty list) if no tags found
- URL: `""` (empty string) if no URL found
- Thumbnail: `""` (empty string, show placeholder) if no image found
- Read status: `False` (unread) by default

## 6. UI Flow

1. **Startup**

   * Load `config.yaml` → get vault path and settings.
   * Scan vault directory for `.md` files → build sorted `Note` list.

2. **Compose**

   * Mount a `ScrollView` containing a `GridView` (2 columns).
   * Load the first batch of `NoteCard` widgets.

3. **Interaction**

   * Arrow keys to change focus and scroll.
   * PgUp/PgDn to scroll.
   * Enter → open URL in browser.
   * Shift+Enter → open file in default editor.
   * r → toggle `[[readitnow/read]]` tag and update card style.
   * q → quit.

4. **Infinite Scroll**

   * On reaching bottom, load next batch of notes and mount additional cards.

## 7. Tech Stack

* **Language:** Python 3.10+
* **Framework:** Textual (with Rich for rendering)
* **Dependencies:**
  * `textual`
  * `rich`
  * `pyyaml` (or `ruamel.yaml`)
