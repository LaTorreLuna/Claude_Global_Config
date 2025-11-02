# Templater Settings and Configuration

**Source:** https://silentvoid13.github.io/Templater/settings.html

## General Settings

### Template Folder Location
Files in this folder will be available as templates. Configure this to point to your templates directory.

### Syntax Highlighting
- **Desktop version**: Adds syntax highlighting for Templater commands in edit mode
- **Mobile version**: Enables highlighting on mobile (use cautiously as it may affect live preview)

### Automatic Cursor Jump
Automatically triggers `tp.file.cursor` after inserting a template. Can also be manually triggered via hotkey.

### Trigger on New File Creation
Templater listens for new file events and replaces commands matching configured rules.

**Compatible with:**
- Daily Notes plugin
- Calendar plugin
- Review plugin
- Note Refactor plugin

**Requirements:**
- Setup of Folder Templates or File Regex Templates
- **Warning**: Only use with trusted content sources

## Advanced Template Rules

### Folder Templates
Automatically applies templates to specified folders and subfolders.

**Behavior:**
- Uses deepest matching rule
- Order is irrelevant
- Requires "Trigger Template on new file creation" enabled

**Example:**
- Folder: `Projects/` → Template: `templates/project-template.md`
- Folder: `Projects/Active/` → Template: `templates/active-project-template.md`

When creating a file in `Projects/Active/`, the second template is used (deepest match).

### File Regex Templates
Tests new file paths against regex patterns.

**Behavior:**
- "Rules are tested top-to-bottom, and the first match will be used"
- Mutually exclusive with Folder Templates
- Recommends Regex101 tool for verification

**Example:**
```
Regex: ^Daily Notes/\d{4}-\d{2}-\d{2}\.md$
Template: templates/daily-note.md
```

## Additional Features

### Template Hotkeys
Bind templates to keyboard shortcuts for quick access.

**Setup:**
1. Settings > Template Hotkeys
2. Assign template to hotkey
3. Press hotkey to insert template

### Startup Templates
Templates that will get executed once when Templater starts.

**Characteristics:**
- Produces no output
- Useful for setting up hooks
- Runs automatically on Obsidian startup

### User Functions
JavaScript files loaded as CommonJS modules.

**Types:**
1. **Script User Functions** - JavaScript-based custom functions
2. **System Command Functions** - Execute system commands (security warnings apply)

**Security Note:** System command functions can execute arbitrary commands on your system. Only use trusted scripts.
