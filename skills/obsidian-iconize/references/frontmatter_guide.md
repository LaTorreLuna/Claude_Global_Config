# Obsidian Iconize - Frontmatter Guide

**Comprehensive guide to using frontmatter properties for icon customization**

---

## Overview

Obsidian Iconize supports frontmatter properties to customize file icons. This method provides a programmatic way to assign icons to files without manual right-click operations.

## Setup Requirements

**CRITICAL:** You must enable the properties option in settings before frontmatter icons will work.

### Step 1: Enable Properties in Settings

1. Open Obsidian Iconize plugin settings
2. Locate the "Properties" option
3. Enable the toggle to allow Iconize to read frontmatter values
4. Save settings

Without this setting enabled, frontmatter `icon` properties will be ignored.

## Implementation

### Basic Syntax

Add an `icon` property to your file's YAML frontmatter:

```yaml
---
icon: IbBell
---
```

The icon identifier (e.g., `IbBell`) corresponds to icons from your installed icon packs.

### Icon Identifiers

Icon identifiers follow the naming convention from your installed icon packs:
- Icons from icon packs use their pack-specific naming (e.g., `IbBell`, `FiHome`, `RiUserLine`)
- Emoji can be used with their shortcodes (e.g., `:smile:`)
- Custom SVG icons use their filename without extension

### Finding Icon Names

To find available icon names:
1. Right-click any file/folder
2. Select "Change Icon"
3. Browse your installed icon packs
4. Hover over icons to see their identifier names

## Key Features

### Priority System

Frontmatter icon assignments have **highest priority** and override:
- Custom rules for default icons
- Icons set via right-click menu
- Any other icon assignment method

### File-Level Customization

Each file can have its own unique icon designation via frontmatter:

```yaml
---
icon: IbDocument
---
# Project Documentation
```

```yaml
---
icon: IbCode
---
# Code Examples
```

### Integration with Other Frontmatter

The `icon` property works seamlessly with other frontmatter properties:

```yaml
---
title: My Important Note
tags: [project, documentation]
icon: IbStar
cssclass: custom-note
---
```

## Advanced Usage

### Dynamic Icon Assignment

Combine with templating plugins (like Templater) for dynamic icon assignment:

```yaml
---
icon: <% tp.file.folder ? "IbFolder" : "IbFile" %>
---
```

### Conditional Icons

Use dataview or other plugins to programmatically set icons based on file properties or conditions.

## Display Behavior

### Where Frontmatter Icons Appear

Files with frontmatter icons will display the icon:
- In the file explorer (before filename)
- In tabs (if tab icons are enabled)
- Above the title (if title icons are enabled)
- In search results
- In backlinks and graph view

### Live Updates

Icon changes take effect immediately after:
- Saving the file with updated frontmatter
- Closing and reopening the file (in some cases)
- Reloading Obsidian (rarely needed)

## Troubleshooting

### Icon Not Appearing

If your frontmatter icon doesn't appear:

1. **Check properties setting:** Verify "Properties" is enabled in Iconize settings
2. **Verify icon identifier:** Ensure the icon name matches an installed icon pack
3. **Check syntax:** YAML frontmatter requires exact formatting (no extra spaces, proper dashes)
4. **Reload file:** Close and reopen the file to refresh
5. **Check icon pack:** Verify the icon pack containing your icon is installed

### Common Mistakes

**Incorrect:**
```yaml
---
icon : IbBell  # Extra space before colon
---
```

**Incorrect:**
```yaml
icon: IbBell  # Missing frontmatter delimiters
```

**Correct:**
```yaml
---
icon: IbBell
---
```

## Best Practices

### 1. Use Consistent Naming

Establish a convention for icon usage across your vault:
- Documentation files: `IbDocument`
- Code files: `IbCode`
- Meeting notes: `IbCalendar`

### 2. Template Integration

Create note templates with pre-defined icons:

```yaml
---
icon: IbNote
created: {{date}}
---
```

### 3. Backup Frontmatter

Before bulk changes, backup files or use version control to prevent accidental icon loss.

### 4. Icon Pack Management

Keep track of which icon packs you're using in frontmatter to avoid broken icons if packs are uninstalled.

## Comparison with Other Methods

| Method | Priority | Scope | Use Case |
|--------|----------|-------|----------|
| Frontmatter | Highest | Individual files | Specific file customization |
| Right-click menu | High | Individual files/folders | Quick manual assignment |
| Custom rules | Lowest | Vault-wide patterns | Default icons for unassigned items |

## Related Features

- **Custom Rules:** Set default icons for files without frontmatter
- **Icon in Tabs:** Display frontmatter icons in tab headers
- **Icon above Title:** Show frontmatter icons above note titles

## Examples

### Project Management

```yaml
---
icon: IbCheckCircle
status: complete
---
```

### Knowledge Base

```yaml
---
icon: IbBook
category: reference
---
```

### Daily Notes

```yaml
---
icon: IbCalendar
date: 2025-10-25
---
```

---

**Related Documentation:**
- Getting Started: `/references/getting_started.md`
- Files and Folders: `/references/files_and_folders.md`
- Custom Rules: `/references/files_and_folders.md#custom-rules`
