---
name: templater-obsidian
description: Obsidian Templater plugin - template language syntax, internal functions (date, file, frontmatter, system, web), user functions, and dynamic note generation patterns
---

# Templater for Obsidian - Comprehensive Skill

Templater is a template language that lets you insert **variables** and **function results** into your notes, with JavaScript code execution capabilities for powerful automation.

## When to Use This Skill

Use this skill when:
- Creating dynamic Obsidian templates with dates, file metadata, or frontmatter
- Automating note creation with prompts, suggestions, or web data
- Building folder-based template systems
- Working with YAML frontmatter programmatically
- Creating templates that adapt based on user input
- Setting up Daily Notes or Zettelkasten workflows

## Quick Reference

### Core Syntax

```
<%  expression  %>     # Interpolation - outputs result
<%* code %>            # Execution - runs JavaScript, no output
<% tp.function() -%>   # Whitespace control (trim after)
```

### Most Common Patterns

```javascript
// Current date/time
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.now("YYYY-MM-DD HH:mm") %>
<% tp.date.tomorrow() %>
<% tp.date.yesterday() %>

// File metadata
<% tp.file.title %>
<% tp.file.creation_date("YYYY-MM-DD") %>
<% tp.file.last_modified_date("dddd Do MMMM YYYY") %>
<% tp.file.folder() %>
<% tp.file.path(true) %>  // vault-relative path

// Frontmatter access
<% tp.frontmatter.property_name %>
<% tp.frontmatter["property with spaces"] %>

// User interaction
<%* const name = await tp.system.prompt("Enter name") %>
<%* const file = await tp.system.suggester((f) => f.basename, app.vault.getMarkdownFiles()) %>

// File operations
<%* await tp.file.create_new("template-file", "new-note-name") %>
<%* await tp.file.rename("new-title") %>
<% tp.file.include("[[other-note]]") %>

// Cursor placement
<% tp.file.cursor(1) %>  // Jump here after template insertion

// Web data
<% await tp.web.daily_quote() %>
<% await tp.web.random_picture("200x200", "nature") %>
<% await tp.web.request("https://api.example.com/data", "field.subfield") %>
```

### Date Offsets

```javascript
// Numeric offsets (days)
<% tp.date.now("YYYY-MM-DD", -7) %>  // Last week
<% tp.date.now("YYYY-MM-DD", 30) %>  // 30 days from now

// ISO 8601 duration offsets
<% tp.date.now("YYYY-MM-DD", "P1Y") %>   // Next year
<% tp.date.now("YYYY-MM-DD", "P-1M") %>  // Last month
<% tp.date.now("YYYY-MM-DD", "P1W") %>   // Next week
```

### Template Examples

#### Daily Note Template
```markdown
---
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
tags: [daily-note]
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

<< [[<% tp.date.yesterday() %>]] | [[<% tp.date.tomorrow() %>]] >>

## Tasks
- [ ]

## Notes

<% tp.file.cursor(1) %>

---
<% await tp.web.daily_quote() %>
```

#### Meeting Note Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
type: meeting
attendees: []
---

# Meeting: <%* const title = await tp.system.prompt("Meeting title") %><% title %>

**Date:** <% tp.date.now("YYYY-MM-DD HH:mm") %>
**Attendees:** <%* const attendees = await tp.system.prompt("Attendees (comma-separated)") %><% attendees %>

## Agenda

<% tp.file.cursor(1) %>

## Action Items

- [ ]

## Notes

```

#### Project Template with Frontmatter
```markdown
---
project: <%* const project = await tp.system.prompt("Project name") %><% project %>
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [project]
---

# <% tp.file.title %>

**Created:** <% tp.date.now("YYYY-MM-DD") %>
**Status:** <% tp.frontmatter.status %>

## Overview

<% tp.file.cursor(1) %>

## Resources

```

### Function Quick Reference

#### tp.date.*
- `now(format, offset, reference, reference_format)` - Current date/time
- `tomorrow(format)` - Tomorrow's date
- `yesterday(format)` - Yesterday's date
- `weekday(format, weekday, reference, reference_format)` - Specific weekday

#### tp.file.*
- `title` - File title
- `content` - File content (read-only)
- `path(relative)` - File path
- `folder(absolute)` - Folder name
- `creation_date(format)` - Creation timestamp
- `last_modified_date(format)` - Last modified timestamp
- `tags` - Array of file tags
- `create_new(template, filename, open, folder)` - Create new file
- `rename(new_title)` - Rename file
- `move(new_path)` - Move file
- `include(link)` - Include another file's content
- `cursor(order)` - Set cursor position
- `selection()` - Get selected text

#### tp.frontmatter.*
- `tp.frontmatter.property_name` - Access any frontmatter property
- `tp.frontmatter["property with spaces"]` - Bracket notation for special characters

#### tp.system.*
- `clipboard()` - Get clipboard content
- `prompt(text, default, throw_on_cancel, multiline)` - User input modal
- `suggester(text_items, items, throw_on_cancel, placeholder)` - Selection modal
- `multi_suggester(...)` - Multi-selection modal

#### tp.web.*
- `daily_quote()` - Random daily quote
- `random_picture(size, query)` - Random Unsplash image
- `request(url, path)` - HTTP request with optional JSON path

#### tp.config.*
- `active_file` - File active when template launched
- `run_mode` - How Templater was triggered
- `target_file` - Destination file object
- `template_file` - Template file object

## Reference Files

Detailed documentation is available in `references/`:

### Core Documentation
- **introduction.md** - What is Templater, core concepts, examples
- **syntax.md** - Command syntax, argument passing, documentation conventions
- **settings.md** - Configuration options, folder templates, startup templates
- **commands.md** - Interpolation vs execution commands, whitespace control

### Internal Functions
- **internal-functions/date.md** - Date manipulation and formatting
- **internal-functions/file.md** - File operations and metadata
- **internal-functions/frontmatter.md** - YAML frontmatter access
- **internal-functions/system.md** - User prompts and system interaction
- **internal-functions/web.md** - Web requests and external data
- **internal-functions/config.md** - Template configuration access

### Advanced Topics
- **user-functions.md** - Creating custom JavaScript functions

## Common Workflows

### Setup Folder-Based Templates

1. **Settings > Template Folder Location**: Set your templates folder
2. **Settings > Folder Templates**: Map folders to templates
3. **Settings > Trigger on new file creation**: Enable automatic template application

### Create Interactive Template

```markdown
---
title: <%* const title = await tp.system.prompt("Note title") %><% title %>
type: <%* const types = ["meeting", "project", "reference", "task"]
const type = await tp.system.suggester(types, types) %><% type %>
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% title %>

Type: <% type %>

<% tp.file.cursor(1) %>
```

### Include Reusable Sections

Create a template file `templates/standard-footer.md`:
```markdown
---
*Created: <% tp.file.creation_date() %>*
*Modified: <% tp.file.last_modified_date() %>*
```

Then include it in other templates:
```markdown
# My Note Content

<% tp.file.include("[[templates/standard-footer]]") %>
```

### File Navigation and Creation

```javascript
// Select existing file and link to it
<%* const file = await tp.system.suggester(
    (f) => f.basename,
    app.vault.getMarkdownFiles()
)
-%>[[<% file.basename %>]]

// Create new note from template
<%* await tp.file.create_new(
    "templates/project-template",
    "New Project Name",
    true,  // open the new file
    "Projects"  // folder
) %>
```

## Important Notes

### Argument Syntax
- Function signatures in docs show types for clarity: `tp.date.now(format: string)`
- **Never include types in actual calls**: Use `<% tp.date.now("YYYY-MM-DD") %>`
- Optional arguments marked with `?`, defaults shown with `=`

### Async Functions
Many functions require `await` and execution commands (`<%* %>`):
- `tp.system.prompt()` - Always async
- `tp.system.suggester()` - Always async
- `tp.web.*` - All web functions are async
- `tp.file.create_new()`, `tp.file.rename()`, `tp.file.move()` - File operations are async

### Security Considerations
- System command functions have security implications
- Only enable "Trigger on new file creation" with trusted templates
- User functions unavailable on mobile (desktop only)

## Troubleshooting

**Template not executing?**
- Check for syntax errors (missing `%>`, unmatched quotes)
- Verify template folder is configured in settings
- Ensure file/folder template rules are set up correctly

**Async function not working?**
- Use execution command: `<%* %>` instead of `<% %>`
- Add `await` keyword before async functions
- Store results in variables: `<%* const result = await tp.system.prompt("...") %>`

**Frontmatter not accessible?**
- Ensure frontmatter exists in file
- Use bracket notation for properties with spaces
- Check property name spelling

## Additional Resources

- Official Docs: https://silentvoid13.github.io/Templater/
- Moment.js formats: https://momentjs.com/docs/#/displaying/format/
- Regex testing (for file regex templates): https://regex101.com/

## Notes

- This skill was manually curated from official Templater documentation
- Examples tested with Templater plugin version compatible with Obsidian 1.4+
- Date formatting uses moment.js syntax
- User functions are desktop-only features
