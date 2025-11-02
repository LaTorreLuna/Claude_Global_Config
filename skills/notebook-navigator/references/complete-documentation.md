# Notebook Navigator - Complete Documentation

**Source:** GitHub README (https://github.com/johansan/notebook-navigator)

---

## Overview

Notebook Navigator is an Obsidian plugin that replaces the default file explorer with a refined dual-pane interface featuring folder browsing, tag navigation, file previews, and extensive customization options.

**Website:** https://notebooknavigator.com

**License:** GPL-3.0

**Requirements:** Obsidian v1.8.0+

**Stats:**
- 1,000+ GitHub stars
- 23 forks
- 1,984 commits
- Actively maintained

---

## Installation

1. **Install Obsidian** from https://obsidian.md
2. **Enable community plugins** in Settings → Community plugins
3. **Install Notebook Navigator** via Browse → Search → Install
4. **Optional:** Install [Featured Image](https://github.com/johansan/obsidian-featured-image) plugin for automatic thumbnail generation
5. **Optional:** Install [Pixel Perfect Image](https://github.com/johansan/pixel-perfect-image) for advanced image operations

### Getting Started

If files aren't visible after enabling dual-pane layout, resize the navigation pane by dragging the divider between the left pane and editor.

---

## Key Features

### Interface
- **Dual-pane layout** on desktop with optional single-pane mode
- **Mobile optimized** for Android, iOS, and iPadOS
- **Customizable startup view** (navigation or notes list)
- **Multi-language support** including RTL language support
- **Resizable panes** for flexible workspace organization

### Navigation
- **Shortcuts section** for pinned items
- **Recent notes** tracking (configurable 1-10 entries)
- **Hierarchical folder tree** with expand/collapse controls
- **Hierarchical tag tree** supporting nested tag relationships
- **Auto-reveal active file** when opened from other sources
- **Auto-expand on drag** for intuitive file moving
- **Breadcrumb navigation** for quick parent access
- **Full keyboard navigation** with arrow keys and customizable hotkeys
- **Multi-selection** via Cmd/Ctrl+Click and Shift+Click
- **Root folder reordering** via drag-and-drop

### Organization
- **Pin notes** to keep important items at folder/tag tops
- **Folder notes** turning folders into clickable links
- **Custom colors and backgrounds** with opacity support
- **Custom icons** (Lucide, emoji, 8 icon packs)
- **Per-folder sort customization**
- **Per-folder appearance settings**
- **Hidden tags** via prefix or wildcard matching
- **Untagged notes** section for organization

### File Display
- **Note previews** (1-5 lines configurable)
- **Feature images** from frontmatter or embedded images
- **Date grouping** (Today, Yesterday, This Week)
- **Frontmatter support** for metadata reading
- **Note metadata** display (dates, tags)
- **Slim mode** for compact display
- **Clickable tags** in file list

### Productivity
- **Quick actions** (hover buttons for common tasks)
- **Quick search** with instant filtering
- **Omnisearch integration** for full-text search
- **Drag & drop** for file operations
- **Tag operations** via context menu and commands
- **File operations** (create, rename, delete, duplicate, move)
- **Filtering** with patterns and frontmatter properties
- **Search commands** via command palette

### Advanced Features
- **Style Settings integration** with 80+ CSS variables
- **Light/dark mode support** with separate theming
- **Public API** for JavaScript/TypeScript developers
- **Metadata control** via API
- **Event subscriptions** for plugin integration

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate up/down in current pane |
| ← | Collapse folder or go to parent (nav); switch to navigation pane (list) |
| → | Expand folder or switch to list pane (nav); switch to editor (list) |
| Tab | Switch between panes; switch from search to list pane |
| Shift+Tab | Switch to navigation pane from list or search |
| Enter | Exit search field to list pane |
| Escape | Close search field |
| PageUp/Down | Scroll in panes |
| Home/End | Jump to first/last item |
| Delete/Backspace | Delete selected item |
| Cmd/Ctrl+A | Select all notes in folder |
| Cmd/Ctrl+Click | Toggle note selection |
| Shift+Click | Select range of notes |
| Shift+Home/End | Select to first/last item |
| Shift+↑/↓ | Extend selection |

**Note:** All shortcuts are customizable via `.obsidian/plugins/notebook-navigator/data.json` including VIM-style support.

---

## Navigation Pane Toolbar

1. **Shortcuts** - Jump to pinned items section
2. **Collapse/Expand all** - Manage folder/tag visibility
3. **Show hidden** - Toggle excluded folders and hidden tags
4. **Reorder root folders** - Customize vault folder ordering
5. **New folder** - Create folder in selected location

---

## List Pane Toolbar

1. **Search** - Filter files by name, tag, or full-text (with Omnisearch)
2. **Show descendants** - Toggle display of subfolder/subtag notes
3. **Sort** - Change ordering (date modified, date created, title)
4. **Appearance** - Customize display (preview rows, titles, slim mode)
5. **New note** - Create note in selected folder

---

## Drag & Drop Operations

- Drag files between folders to move them
- Drag files to tags to add tags
- Drag files to "Untagged" to remove all tags
- Drag files to shortcuts to pin them
- Drag shortcuts to reorder
- Drag root folders when in reorder mode

---

## Commands Reference

### View & Navigation
- `notebook-navigator:open` - Open plugin (bind to Cmd/Ctrl+Shift+E for keyboard focus)
- `notebook-navigator:open-homepage` - Load homepage file
- `notebook-navigator:reveal-file` - Show current file in navigator
- `notebook-navigator:navigate-to-folder` - Jump to folder via search
- `notebook-navigator:navigate-to-tag` - Jump to tag via search
- `notebook-navigator:add-shortcut` - Pin current item
- `notebook-navigator:search` - Focus search field (bind to Cmd/Ctrl+Shift+F)

### Layout & Display
- `notebook-navigator:toggle-dual-pane` - Switch layout mode
- `notebook-navigator:toggle-descendants` - Toggle subfolder/subtag notes
- `notebook-navigator:toggle-hidden` - Show/hide excluded items
- `notebook-navigator:toggle-tag-sort` - Switch tag sort method
- `notebook-navigator:collapse-expand` - Collapse/expand all items

### File Operations
- `notebook-navigator:new-note` - Create note in selected folder
- `notebook-navigator:move-files` - Move selected files
- `notebook-navigator:convert-to-folder-note` - Convert file to folder note
- `notebook-navigator:pin-all-folder-notes` - Pin all folder notes
- `notebook-navigator:delete-files` - Delete selected files

### Tag Operations
- `notebook-navigator:add-tag` - Add tag to selected files
- `notebook-navigator:remove-tag` - Remove tag from files
- `notebook-navigator:remove-all-tags` - Clear all tags

### Maintenance
- `notebook-navigator:rebuild-cache` - Rebuild local cache

---

## Settings Overview

### General Filtering
- **Show file types:** Documents, supported, or all files
- **Hide folders:** Pattern matching (e.g., `assets*`, `*/temp`)
- **Hide notes:** Frontmatter property filtering

### General Behavior
- **Auto-reveal active note** when opened from other sources
- **Ignore events from right sidebar** option

### General View
- **Default startup view:** Navigation pane or notes list
- **Homepage:** Optional auto-opening file
- **Show icons:** Display alongside items
- **Date/Time format:** Customizable formatting

### Desktop Appearance
- **Dual pane layout:** Enable side-by-side view
- **Orientation:** Horizontal or vertical split
- **Dual pane background:** Separate, primary, or secondary
- **Show tooltips** with optional file paths

### Navigation Pane
- **Auto-select first note** when switching folders
- **Auto-expand folders and tags** on selection
- **Collapse items:** Affects folders, tags, or both
- **Keep selected item expanded** when collapsing others
- **Navigation banner:** Display optional image
- **Show shortcuts** section
- **Show recent notes** (1-10 count configurable)
- **Show note count** with optional separate counts
- **Tree indentation:** Adjust nesting width
- **Item height:** Customize with optional text scaling

### Folders & Tags
- **Show root folder** as vault name
- **Inherit folder colors** to child folders
- **Enable folder notes** with:
  - Default type (Markdown, Canvas, Base)
  - Custom note name
  - Frontmatter properties
  - Hide from list option
  - Auto-pin option
- **Show tags** section with:
  - Sort order (A-Z, Z-A, frequency)
  - Tags folder display
  - Untagged notes section
  - Hidden tags list

### List Pane
- **List pane title** position (header, list, hidden)
- **Sort notes by:** Date edited/created, title (ascending/descending)
- **Multi-select modifier:** Cmd/Ctrl or Option/Alt click
- **Show notes from descendants** toggle
- **Group notes:** None, by date, or by folder
- **Optimize note height** for visual refinement
- **Show quick actions** with reveal, pin, and new tab options

### Notes Display
- **Read metadata from frontmatter** for names, timestamps, icons, colors
- **Icon field:** Frontmatter property name
- **Color field:** Frontmatter property name
- **Save to frontmatter** option
- **Show feature images** with sizing options
- **Show note preview** (0-5 lines)
- **Show note tags** in list
- **Show modification date**

### Search
- **Quick search type:** File name, tags, or full-text
- **Search persistence** across sessions

---

## Architecture Highlights

### Performance
- **React + TanStack Virtual** for virtualized rendering handling 100,000+ notes
- **IndexedDB + RAM Cache** dual-layer caching with synchronous metadata access
- **Batch Processing Engine** with parallel processing and cancellation
- **Unified Cleanup System** validates metadata in single startup pass

### Code Quality
- **Obsidian ESLint Plugin** full compliance
- **Zero-tolerance build process** aborting on errors/warnings
- **No explicit-any** across 35,000+ TypeScript lines
- **TypeScript, ESLint, Knip (dead code), Prettier** validation

---

## Documentation

- **[API Reference](https://github.com/johansan/notebook-navigator/blob/main/docs/api-reference.md)** - JavaScript/TypeScript public API
- **[Theming Guide](https://github.com/johansan/notebook-navigator/blob/main/docs/theming-guide.md)** - CSS and custom properties
- **[Startup Process](https://github.com/johansan/notebook-navigator/blob/main/docs/startup-process.md)** - Initialization sequence with diagrams
- **[Storage Architecture](https://github.com/johansan/notebook-navigator/blob/main/docs/storage-architecture.md)** - Data containers and flow
- **[Rendering Architecture](https://github.com/johansan/notebook-navigator/blob/main/docs/rendering-architecture.md)** - React components and virtual scrolling
- **[Scroll Orchestration](https://github.com/johansan/notebook-navigator/blob/main/docs/scroll-orchestration.md)** - Dynamic scroll management
- **[Service Architecture](https://github.com/johansan/notebook-navigator/blob/main/docs/service-architecture.md)** - Business logic layer

---

## Additional Resources

- **[Website](https://notebooknavigator.com)** with multi-language docs
- **[Discord Community](https://discord.gg/6eeSUvzEJr)** for support and discussion
- **[GitHub Repository](https://github.com/johansan/notebook-navigator)** for issues and contributions

---

## Support

Consider [sponsoring on GitHub](https://github.com/sponsors/johansan) or [buying a coffee](https://www.buymeacoffee.com/johansan) to support development.
