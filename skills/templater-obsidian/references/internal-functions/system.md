# tp.system Module - System Interaction and User Prompts

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/system-module.html

The `tp.system` module provides functions for user interaction and system access.

## Functions

### tp.system.clipboard()

Retrieves current clipboard content without arguments. Simple synchronous operation for pasting stored data into templates.

**Example:**
```javascript
<% tp.system.clipboard() %>

// Use in sentence
You copied: <% tp.system.clipboard() %>
```

### tp.system.prompt()

**Signature:** `tp.system.prompt(prompt_text?: string, default_value?: string, throw_on_cancel: boolean = false, multiline: boolean = false)`

Spawns an input modal for user input.

**Parameters:**
- `prompt_text`: Label above the input field
- `default_value`: Pre-filled content
- `throw_on_cancel`: Error handling flag (default: false, returns null on cancel)
- `multiline`: Enables textarea mode (default: false)

**Examples:**
```javascript
// Basic prompt
<%* const name = await tp.system.prompt("Enter your name") %>
Hello, <% name %>!

// With default value
<%* const title = await tp.system.prompt("Note title", tp.file.title) %>

// Multiline prompt
<%* const description = await tp.system.prompt("Project description", "", false, true) %>

// Store and reuse
<%* const projectName = await tp.system.prompt("Project name") %>
# Project: <% projectName %>

Project: <% projectName %>
Created: <% tp.date.now() %>
```

**Note:** This is an **async function** - must use `await` and execution command (`<%* %>`)

### tp.system.suggester()

**Signature:** `tp.system.suggester(text_items: string[] | ((item: T) => string), items: T[], throw_on_cancel: boolean = false, placeholder: string = "", limit?: number)`

Creates a selection modal for single-item picking.

**Parameters:**
- `text_items`: Display strings or mapping function
- `items`: Actual values to return
- `throw_on_cancel`: Error control (default: false)
- `placeholder`: Input hint text
- `limit`: Performance optimization for large datasets

**Examples:**
```javascript
// Simple list selection
<%*
const colors = ["Red", "Green", "Blue"];
const selected = await tp.system.suggester(colors, colors);
%>
You selected: <% selected %>

// With different display and values
<%*
const display = ["Option A", "Option B", "Option C"];
const values = ["value-a", "value-b", "value-c"];
const choice = await tp.system.suggester(display, values);
%>
Choice: <% choice %>

// Select from vault files
<%*
const file = await tp.system.suggester(
    (item) => item.basename,
    app.vault.getMarkdownFiles()
);
%>
[[<% file.basename %>]]

// With placeholder
<%*
const status = await tp.system.suggester(
    ["Active", "In Progress", "Completed", "Archived"],
    ["active", "in-progress", "completed", "archived"],
    false,
    "Select project status"
);
%>

// Select from frontmatter tags
<%*
const allFiles = app.vault.getMarkdownFiles();
const allTags = new Set();
allFiles.forEach(file => {
    const cache = app.metadataCache.getFileCache(file);
    if (cache?.frontmatter?.tags) {
        cache.frontmatter.tags.forEach(tag => allTags.add(tag));
    }
});
const tag = await tp.system.suggester(
    Array.from(allTags),
    Array.from(allTags),
    false,
    "Select a tag"
);
%>
Tag: #<% tag %>
```

**Note:** This is an **async function** - must use `await` and execution command (`<%* %>`)

### tp.system.multi_suggester()

**Signature:** Similar to `suggester()` but allows selecting multiple items, returning an array of chosen values.

**Examples:**
```javascript
// Select multiple tags
<%*
const availableTags = ["project", "work", "personal", "urgent", "review"];
const selectedTags = await tp.system.multi_suggester(availableTags, availableTags);
%>
Selected tags: <% selectedTags.join(", ") %>

// Select multiple files
<%*
const files = await tp.system.multi_suggester(
    (item) => item.basename,
    app.vault.getMarkdownFiles()
);
%>
## Related Files
<% files.map(f => `- [[${f.basename}]]`).join("\n") %>
```

**Note:** This is an **async function** - must use `await` and execution command (`<%* %>`)

## Common Workflows

### Interactive Note Creation

```javascript
---
title: <%* const title = await tp.system.prompt("Note title") %><% title %>
type: <%* const type = await tp.system.suggester(
    ["Meeting", "Project", "Reference", "Task"],
    ["meeting", "project", "reference", "task"]
) %><% type %>
created: <% tp.date.now("YYYY-MM-DD") %>
---

# <% title %>

<%* if (type === "meeting") { %>
**Attendees:** <%* const attendees = await tp.system.prompt("Attendees (comma-separated)") %><% attendees %>
**Date:** <% tp.date.now("YYYY-MM-DD HH:mm") %>

## Agenda
<% tp.file.cursor(1) %>

## Notes

## Action Items
- [ ]

<%* } else if (type === "project") { %>
**Status:** <%* const status = await tp.system.suggester(
    ["Active", "Planning", "On Hold", "Completed"],
    ["active", "planning", "on-hold", "completed"]
) %><% status %>

## Overview
<% tp.file.cursor(1) %>

## Tasks
- [ ]

<%* } else if (type === "task") { %>
**Priority:** <%* const priority = await tp.system.suggester(
    ["High", "Medium", "Low"],
    ["high", "medium", "low"]
) %><% priority %>
**Due Date:** <%* const dueDate = await tp.system.prompt("Due date (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD", 7)) %><% dueDate %>

## Details
<% tp.file.cursor(1) %>

<%* } else { %>
<% tp.file.cursor(1) %>
<%* } %>
```

### Link to Related Notes

```javascript
## Related Notes
<%*
const relatedFiles = await tp.system.multi_suggester(
    (f) => f.basename,
    app.vault.getMarkdownFiles(),
    false,
    "Select related notes"
);
%>
<% relatedFiles.map(f => `- [[${f.basename}]]`).join("\n") %>
```

### Paste and Format Clipboard

```javascript
<%*
const content = tp.system.clipboard();
const shouldFormat = await tp.system.suggester(
    ["Yes, format it", "No, paste as-is"],
    [true, false],
    false,
    "Format clipboard content?"
);
%>
<%* if (shouldFormat) { %>
```
<% content %>
```
<%* } else { %>
<% content %>
<%* } %>
```

### Conditional Sections Based on Input

```javascript
<%*
const includeFooter = await tp.system.suggester(
    ["Include footer", "Skip footer"],
    [true, false]
);

const includeTOC = await tp.system.suggester(
    ["Include TOC", "Skip TOC"],
    [true, false]
);
%>

# <% tp.file.title %>

<%* if (includeTOC) { %>
## Table of Contents
- [[#Section 1]]
- [[#Section 2]]
<%* } %>

## Content
<% tp.file.cursor(1) %>

<%* if (includeFooter) { %>
---
*Created: <% tp.date.now("YYYY-MM-DD") %>*
<%* } %>
```

## Best Practices

1. **Always use `await` with prompts**:
   ```javascript
   // CORRECT
   <%* const name = await tp.system.prompt("Name") %>

   // INCORRECT - will not work
   <% const name = tp.system.prompt("Name") %>
   ```

2. **Store results in variables**:
   ```javascript
   // CORRECT - store then use
   <%* const choice = await tp.system.suggester(options, values) %>
   Selected: <% choice %>

   // INCORRECT - can't await in interpolation
   <% await tp.system.suggester(options, values) %>
   ```

3. **Provide default values**:
   ```javascript
   <%* const date = await tp.system.prompt(
       "Due date",
       tp.date.now("YYYY-MM-DD", 7)  // defaults to next week
   ) %>
   ```

4. **Use placeholders for clarity**:
   ```javascript
   <%* const status = await tp.system.suggester(
       statusOptions,
       statusValues,
       false,
       "Select project status"  // clear placeholder
   ) %>
   ```

5. **Handle cancellation**:
   ```javascript
   <%* const name = await tp.system.prompt("Name") %>
   <%* if (name) { %>
   Hello, <% name %>!
   <%* } else { %>
   No name provided.
   <%* } %>
   ```

## Error Handling

Both prompt functions return `null` on cancellation by default unless `throw_on_cancel` is enabled.

```javascript
// With error handling
<%*
const input = await tp.system.prompt("Required input", "", true);
// Will throw error if cancelled

try {
    const result = await tp.system.prompt("Input", "", true);
} catch (e) {
    // User cancelled
}
%>
```

## Performance Notes

- `suggester()` and `multi_suggester()` support a `limit` parameter for large datasets
- Consider filtering large arrays before passing to suggester
- For very large file lists, consider pre-filtering by folder or tag
