# tp.config Module - Configuration Access

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/config-module.html

The `tp.config` module provides access to Templater's running configuration. This module is "mostly useful when writing scripts requiring some context information."

## Available Properties

### tp.config.active_file

**Description:** The active file (if existing) when launching Templater

**Use Case:** Determine what file was open before template execution

**Example:**
```javascript
<%* if (tp.config.active_file) { %>
Previous file: [[<% tp.config.active_file.basename %>]]
<%* } %>
```

### tp.config.run_mode

**Description:** The `RunMode`, representing the way Templater was launched

**Values:**
- `Create new from template` - Template used to create new file
- `Append to active file` - Template appended to current file
- Other execution modes

**Use Case:** Adjust template behavior based on how it was triggered

**Example:**
```javascript
<%* if (tp.config.run_mode === "Create new from template") { %>
# <% tp.file.title %>

Created: <% tp.date.now() %>
<%* } else { %>
---
Section added: <% tp.date.now() %>
<%* } %>
```

### tp.config.target_file

**Description:** The `TFile` object representing the target file where the template will be inserted

**Use Case:** Access destination file's metadata and properties

**Example:**
```javascript
Target file: <% tp.config.target_file.basename %>
Target path: <% tp.config.target_file.path %>
Target created: <% tp.date.now("YYYY-MM-DD", 0, tp.config.target_file.stat.ctime) %>
```

### tp.config.template_file

**Description:** The `TFile` object representing the template file

**Use Case:** Reference information about the source template

**Example:**
```javascript
Template: <% tp.config.template_file.basename %>
Template location: <% tp.config.template_file.path %>
```

## Common Use Cases

### Conditional Template Logic

```javascript
<%*
// Different behavior based on how template was triggered
const mode = tp.config.run_mode;
%>

<%* if (mode === "Create new from template") { %>
---
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
template: <% tp.config.template_file.basename %>
---

# <% tp.file.title %>

<% tp.file.cursor(1) %>

<%* } else { %>
## Section Added: <% tp.date.now("YYYY-MM-DD HH:mm") %>

<% tp.file.cursor(1) %>

<%* } %>
```

### Template Metadata Tracking

```javascript
---
created_from: <% tp.config.template_file.path %>
applied_to: <% tp.config.target_file.path %>
execution_date: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>
---
```

### Context-Aware Templates

```javascript
<%*
// Check if template is being applied to a specific folder
const targetPath = tp.config.target_file.path;
const isProjectNote = targetPath.includes("Projects/");
const isMeetingNote = targetPath.includes("Meetings/");
%>

<%* if (isProjectNote) { %>
## Project Details
**Status:**
**Timeline:**
<%* } else if (isMeetingNote) { %>
## Meeting Details
**Date:** <% tp.date.now("YYYY-MM-DD") %>
**Attendees:**
<%* } %>
```

### Active File Reference

```javascript
<%*
// Link back to the file that was active when template was triggered
if (tp.config.active_file && tp.config.active_file.path !== tp.config.target_file.path) {
%>
**Previous context:** [[<% tp.config.active_file.basename %>]]
<%* } %>
```

### Template Version Tracking

```javascript
---
template_version: 2.1
template_file: <% tp.config.template_file.basename %>
applied_date: <% tp.date.now("YYYY-MM-DD") %>
---

<%*
// Store template metadata for version tracking
const templateMeta = {
    name: tp.config.template_file.basename,
    path: tp.config.template_file.path,
    applied: tp.date.now("YYYY-MM-DD HH:mm:ss")
};
%>
```

## TFile Object Properties

Both `target_file` and `template_file` are TFile objects with these properties:

- `basename` - File name without extension
- `extension` - File extension
- `name` - Full file name with extension
- `path` - Full vault path
- `stat.ctime` - Creation timestamp
- `stat.mtime` - Modification timestamp
- `stat.size` - File size in bytes

**Example:**
```javascript
# File Information

**Name:** <% tp.config.target_file.name %>
**Basename:** <% tp.config.target_file.basename %>
**Extension:** <% tp.config.target_file.extension %>
**Path:** <% tp.config.target_file.path %>
**Size:** <% tp.config.target_file.stat.size %> bytes
**Created:** <% new Date(tp.config.target_file.stat.ctime).toISOString() %>
**Modified:** <% new Date(tp.config.target_file.stat.mtime).toISOString() %>
```

## Advanced Examples

### Folder-Specific Template Behavior

```javascript
<%*
const folder = tp.config.target_file.parent.path;
const folderName = tp.config.target_file.parent.name;
%>

# <% tp.file.title %>

**Location:** <% folderName %>

<%* if (folder === "Projects") { %>
**Project Type:**
**Status:**
**Timeline:**

## Objectives
<% tp.file.cursor(1) %>

## Resources

## Notes

<%* } else if (folder === "Daily Notes") { %>
**Date:** <% tp.date.now("YYYY-MM-DD") %>

## Tasks
- [ ]

## Notes
<% tp.file.cursor(1) %>

<%* } else { %>
<% tp.file.cursor(1) %>
<%* } %>
```

### Template Audit Trail

```javascript
---
template_audit:
  template: <% tp.config.template_file.basename %>
  template_path: <% tp.config.template_file.path %>
  target: <% tp.config.target_file.basename %>
  target_path: <% tp.config.target_file.path %>
  run_mode: <% tp.config.run_mode %>
  execution_time: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>
<%* if (tp.config.active_file) { %>
  previous_file: <% tp.config.active_file.basename %>
<%* } %>
---
```

## Best Practices

1. **Check for existence**:
   ```javascript
   <%* if (tp.config.active_file) { %>
   Active file exists: <% tp.config.active_file.basename %>
   <%* } %>
   ```

2. **Use for context-aware templates**:
   - Adapt template content based on destination folder
   - Track template usage and application
   - Create different outputs for different run modes

3. **Combine with other modules**:
   ```javascript
   <%*
   const isNewFile = tp.config.run_mode === "Create new from template";
   const folder = tp.config.target_file.parent.name;
   const fileType = tp.frontmatter["note type"];
   %>
   ```

4. **Document template metadata**:
   - Track which template was used
   - Record when and how template was applied
   - Enable template version management

## Limitations

- `active_file` may be null if no file was active
- `run_mode` values are string-based, check exact strings
- TFile objects provide read-only access
- Configuration is snapshot at execution time

## Notes

- This module is primarily for advanced template scripting
- Most basic templates won't need config module
- Useful for template debugging and troubleshooting
- Enables template behavior based on execution context
