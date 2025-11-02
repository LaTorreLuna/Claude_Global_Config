---
name: notebook-navigator
description: Use when working with Notebook Navigator Obsidian plugin - a modern file explorer replacement with dual-pane interface, tag browsing, file previews, keyboard navigation, and extensive customization. Covers installation, features, API, theming, and configuration.
---

# Notebook Navigator Skill

Comprehensive guidance for the Notebook Navigator Obsidian plugin - a refined dual-pane file explorer replacement featuring folder browsing, tag navigation, file previews, and extensive customization options.

## When to Use This Skill

This skill should be triggered when:
- Installing or configuring Notebook Navigator in Obsidian
- Using dual-pane layout, folder tree, or tag browsing features
- Working with keyboard navigation and shortcuts
- Customizing appearance, colors, icons, or behavior
- Implementing folder notes or pinned notes
- Using the public API for plugin development
- Troubleshooting issues or optimizing performance
- Creating custom themes or CSS modifications

## Key Features Overview

### Interface
- **Dual-pane layout** (navigation + list panes) on desktop
- **Single-pane mode** for mobile (Android, iOS, iPadOS)
- **Customizable startup view** (navigation or notes list)
- **Multi-language support** including RTL languages
- **Resizable panes** for flexible workspace

### Navigation
- **Shortcuts section** for pinned items
- **Recent notes tracking** (1-10 configurable)
- **Hierarchical folder & tag trees**
- **Auto-reveal active file** when opened elsewhere
- **Breadcrumb navigation** for quick parent access
- **Full keyboard navigation** with customizable hotkeys
- **Multi-selection** (Cmd/Ctrl+Click, Shift+Click)
- **Root folder reordering** via drag-and-drop

### Organization
- **Pin notes** to keep important items at top
- **Folder notes** turning folders into clickable links
- **Custom colors & backgrounds** with opacity
- **Custom icons** (Lucide, emoji, 8 icon packs)
- **Per-folder sort & appearance** customization
- **Hidden tags** via prefix/wildcard matching
- **Untagged notes section**

### File Display
- **Note previews** (1-5 lines configurable)
- **Feature images** from frontmatter or embedded images
- **Date grouping** (Today, Yesterday, This Week)
- **Frontmatter support** for metadata
- **Note metadata display** (dates, tags)
- **Slim mode** for compact display
- **Clickable tags** in file list

### Productivity
- **Quick actions** hover buttons
- **Quick search** with instant filtering
- **Omnisearch integration** for full-text search
- **Drag & drop** file operations
- **Tag operations** via context menu and commands
- **Filtering** with patterns and frontmatter properties

## Quick Reference

### Essential Keyboard Shortcuts

```
↑/↓             Navigate up/down in current pane
←               Collapse folder or go to parent (nav pane)
→               Expand folder or switch to list pane
Tab             Switch between panes
Enter           Exit search field to list pane
Escape          Close search field
Cmd/Ctrl+A      Select all notes in folder
Cmd/Ctrl+Click  Toggle note selection
Shift+Click     Select range of notes
Delete          Delete selected item
```

### Key Commands

```bash
# Open plugin
notebook-navigator:open

# Search (bind to Cmd/Ctrl+Shift+F)
notebook-navigator:search

# Reveal active file
notebook-navigator:reveal-file

# Toggle dual-pane layout
notebook-navigator:toggle-dual-pane

# Create note in selected folder
notebook-navigator:new-note

# Add tag to selected files
notebook-navigator:add-tag

# Pin current item
notebook-navigator:add-shortcut
```

### Drag & Drop Operations

```
Drag files → folders        Move files
Drag files → tags          Add tags
Drag files → "Untagged"    Remove all tags
Drag files → shortcuts     Pin them
Drag shortcuts             Reorder
Drag root folders          Reorder (in reorder mode)
```

## Installation

See `references/installation.md` for complete setup instructions including:
- Obsidian installation and community plugin setup
- Notebook Navigator installation from community plugins
- Optional companion plugins (Featured Image, Pixel Perfect Image)
- Getting started troubleshooting

## Configuration

See `references/settings.md` for comprehensive settings documentation covering:
- General filtering (file types, hidden folders, excluded notes)
- General behavior (auto-reveal, ignore sidebar events)
- Desktop appearance (dual-pane, orientation, backgrounds)
- Navigation pane (shortcuts, recent notes, banners, indentation)
- Folders & tags (folder notes, tag sorting, hidden tags)
- List pane (sorting, grouping, multi-select, quick actions)
- Notes display (metadata, images, previews, colors)
- Search (quick search type, persistence)

## API Development

See `references/api.md` for public API documentation including:
- JavaScript/TypeScript API reference
- Event subscriptions for plugin integration
- Metadata control methods
- Plugin integration patterns

## Theming & Customization

See `references/theming.md` for theming guide including:
- 80+ CSS variables via Style Settings integration
- Light/dark mode separate theming
- Custom colors, backgrounds, and icons
- Per-folder appearance customization

## Architecture

See `references/architecture.md` for technical details:
- Performance (React + TanStack Virtual, IndexedDB caching)
- Storage architecture and data flow
- Rendering architecture with virtualization
- Service architecture and business logic

## Reference Files

### references/installation.md
Complete installation and setup instructions

### references/features.md
Comprehensive feature list with examples

### references/keyboard-shortcuts.md
All keyboard shortcuts and customization

### references/commands.md
Complete command reference with descriptions

### references/settings.md
Detailed settings configuration guide

### references/api.md
Public API documentation for developers

### references/theming.md
CSS theming and customization guide

### references/architecture.md
Technical architecture documentation

## Common Tasks

### Setting Up Dual-Pane Layout
1. Enable Notebook Navigator in Community Plugins
2. Settings → Notebook Navigator → Desktop Appearance → Enable "Dual pane layout"
3. Resize navigation pane by dragging divider if files not visible

### Creating Folder Notes
1. Settings → Notebook Navigator → Folders & Tags → Enable "Folder notes"
2. Choose default type (Markdown, Canvas, Base)
3. Set custom note name if desired
4. Optional: Enable "Hide folder note from list"
5. Optional: Enable "Automatically pin folder notes"

### Customizing Keyboard Shortcuts
Edit `.obsidian/plugins/notebook-navigator/data.json` to customize shortcuts including VIM-style support.

### Using the API
```typescript
// Get plugin instance
const plugin = app.plugins.getPlugin('notebook-navigator');

// Access metadata
const metadata = plugin.api.getMetadata(file);

// Subscribe to events
plugin.api.on('file-selected', (file) => {
  console.log('Selected:', file.path);
});
```

## Resources

- **Website:** https://notebooknavigator.com (multi-language docs)
- **GitHub:** https://github.com/johansan/notebook-navigator
- **Discord:** https://discord.gg/6eeSUvzEJr
- **API Docs:** https://github.com/johansan/notebook-navigator/blob/main/docs/api-reference.md

## Support

- **Issues:** https://github.com/johansan/notebook-navigator/issues
- **Sponsor:** https://github.com/sponsors/johansan
- **Buy a Coffee:** https://www.buymeacoffee.com/johansan

## Requirements

- **Obsidian:** v1.8.0+
- **License:** GPL-3.0
- **Stats:** 1,000+ GitHub stars, actively maintained

## Notes

- Optimized for 100,000+ notes with virtualized rendering
- Zero-tolerance build process (no errors/warnings)
- 35,000+ lines of TypeScript with no explicit-any
- Full ESLint compliance with Obsidian plugin standards
