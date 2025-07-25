# ReadItNow Project Specification

## 1. Project Name & Branding

* **Chosen Name**: **ReadItNow**
* **Alternative Names Considered:**

  * KittyLater
  * VaultView
  * ObsiPeek
  * Laternal
  * TwoColumnTome
  * InkLater
  * ReadCursor
  * NoteGrid

## 2. Purpose & Vision

Build a **beautiful**, **two‑column**, **infinite‑scroll** terminal UI in **Kitty** that surfaces the newest items from your Obsidian ReadItLater folder, making it irresistible to "read it now".

## 3. Key Features

1. **Entry Listing**

   * Show the latest *N* Markdown notes from `vault/plugins/readitlater`, sorted by modification time.
   * Render as a two‑column grid, with as many rows as fit the terminal.

2. **Note Card**

   * **Thumbnail** preview (YouTube/X/twitter/imgur links) or placeholder.
   * **Title** (from front‑matter `title` or filename).
   * **Excerpt**: first paragraph of the Markdown body, rendered via Rich Markdown.
   * **Tags**: show user tags plus a special badge when marked read.
   * **Read State**: visually differentiate cards tagged `readitnow/read` (e.g. dimmed or ✔ badge).

3. **Infinite Scroll**

   * Automatically load the next batch of notes when scrolling to the end.

4. **Interactions & Keybindings**

   * **Arrow Keys** (↑↓←→): move focus among cards
   * **PageUp/PageDown**: scroll the grid view
   * **Enter**: open the note’s `url` in the default browser
   * **Shift+Enter**: open the `.md` note file in the configured editor
   * **m**: toggle read/unread state (adds/removes `readitnow/read` tag)
   * **q**: quit the app

## 4. Persistence & Configuration

### a) Configuration File (YAML)

* **Path:** `~/.config/readitnow/config.yaml`
* **Schema:**

  ```yaml
  vault_path: "/home/you/vault/plugins/readitlater"
  columns: 2
  batch_size: 20
  theme: "tokyonight"
  editor: "nvim"
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

### b) Read/Unread State via Front‑Matter Tag

* **Tag:** `readitnow/read`
* **Mechanism:** On toggle, insert or remove this tag in the note’s front‑matter `tags:` list.
* **Advantages:** No external database, fully version‑controlled and portable with your notes.

## 5. Front‑Matter Editing (Definition)

“Front‑matter” is the YAML block at the top of each Markdown note holding metadata:

```yaml
---
title: "My Cool Article"
date: "2025-07-25"
tags:
  - readitlater
---
Body of the note...
```

**Editing steps:**

1. **Read** the YAML block.
2. **Parse** into a data structure.
3. **Modify** (toggle `readitnow/read` in `tags`).
4. **Serialize** back to YAML and **rewrite** the file, preserving the Markdown body.

## 6. Architecture & Module Layout

```
readitnow/
├── README.md
├── pyproject.toml         # Python project settings & dependencies
├── ~/.config/readitnow/config.yaml  # User’s config (not in repo)
└── readitnow/
    ├── __init__.py
    ├── app.py            # Textual App subclass & startup logic
    ├── config.py         # XDG‑style YAML config loader
    ├── fm_utils.py       # Front‑matter read & toggle functions
    ├── models.py         # Note model: metadata, read‑flag, thumbnail URL
    ├── widgets/
    │   ├── note_card.py  # NoteCard widget (thumbnail, title, excerpt, badge)
    │   └── grid_view.py  # GridView container + infinite scroll logic
    └── commands.py       # Helpers: open_link, open_file
```

## 7. UI Flow

1. **Startup**

   * Load `config.yaml` → get vault path, columns, batch size, editor, theme.
   * Scan `vault/plugins/readitlater` for `.md` files → build sorted `Note` list.

2. **Compose**

   * Mount a `ScrollView` containing a `GridView` (2 columns).
   * Load the first batch of `NoteCard` widgets.

3. **Interaction**

   * Arrow keys to change focus.
   * PgUp/PgDn to scroll.
   * Enter → open URL in browser.
   * Shift+Enter → open file in editor.
   * m → toggle `readitnow/read` tag and update card style.
   * q → quit.

4. **Infinite Scroll**

   * On reaching bottom, load next batch of notes and mount additional cards.

## 8. Tech Stack

* **Language:** Python 3.10+
* **Framework:** Textual (with Rich for rendering)
* **Dependencies:**

  * `textual`
  * `rich`
  * `pyyaml` (or `ruamel.yaml`)
  * `python-frontmatter`

## 9. Alternative TUI Frameworks Considered

* **Python:** Textual, Urwid, Prompt Toolkit
* **Go:** Bubble Tea + Lip Gloss, tview
* **Node.js:** Blessed / blessed‑contrib, Ink (React in terminal)
* **Rust:** ratatui (tui‑rs), cursive

## 10. Next Steps (Outline)

1. **Stub Modules**: config loader, front‑matter utils, models, widgets, commands.
2. **Skeleton App**: App subclass mounting placeholder grid, responding to keybindings.
3. **Iterate**: fill in NoteCard rendering, infinite scroll, front‑matter toggling.
4. **Polish**: theming, caching thumbnails, error handling, packaging.

---

This spec captures our entire design discussion—definitions, responsibilities, file layout, UI behavior, persistence strategy, and naming. When you’re ready to dive into implementation, we have a clear roadmap!
