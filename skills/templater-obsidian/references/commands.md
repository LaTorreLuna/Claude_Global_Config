# Templater Commands

**Source:** https://silentvoid13.github.io/Templater/commands/overview.html

## Command Types

Templater defines two primary command formats:

### Interpolation Commands (`<%`)

**Syntax:** `<% expression %>`

**Behavior:** "It will output the result of the expression that's inside."

These tags process expressions and return their evaluated results to the document.

**Examples:**
```javascript
<% tp.date.now() %>                    // Outputs: 2024-01-15
<% tp.file.title %>                    // Outputs: My Note Title
<% tp.frontmatter.status %>            // Outputs: active
```

### Execution Commands (`<%*`)

**Syntax:** `<%* code %>`

**Behavior:** "It will execute the JavaScript code that's inside. It does not output anything by default."

These permit running JavaScript without producing direct output.

**Examples:**
```javascript
<%* const name = await tp.system.prompt("Enter name") %>
<%* await tp.file.create_new("template", "new-note") %>
<%* console.log("This won't appear in the note") %>
```

**To output from execution commands:**
```javascript
<%* tR += "This will be inserted" %>
```

Both command types close with the `%>` delimiter.

## Command Utilities

### Whitespace Control

Manages spacing around command tags.

**Syntax:**
- `<%-` - Trim whitespace before
- `-%>` - Trim whitespace after

**Examples:**
```javascript
// Without whitespace control
Line 1
<% tp.date.now() %>
Line 2

// With whitespace control
Line 1
<% tp.date.now() -%>
Line 2

// Trim both sides
Line 1
<%- tp.date.now() -%>
Line 2
```

### Dynamic Commands

Enables conditional or adaptive command execution.

**Purpose:** Run commands based on conditions or adapt template behavior dynamically.

**Example:**
```javascript
<%* if (tp.file.title.includes("Project")) { %>
This is a project note!
<%* } else { %>
This is a regular note!
<%* } %>
```

Both utilities function with all command types and are declared within opening tags.

## Available Modules

Internal modules accessible via the `tp` object:

- **tp.app** - Application interactions
- **tp.config** - Configuration access
- **tp.date** - Date operations
- **tp.file** - File operations
- **tp.frontmatter** - YAML frontmatter access
- **tp.hooks** - Lifecycle hooks
- **tp.obsidian** - Obsidian API integration
- **tp.system** - System commands and user interaction
- **tp.web** - Web operations

User functions can be created through script-based or system command approaches, extending Templater's base functionality beyond built-in commands.

## Best Practices

1. **Use interpolation for simple output**: `<% tp.date.now() %>`
2. **Use execution for logic and side effects**: `<%* await tp.file.rename("new-name") %>`
3. **Combine both**: Store results in execution, output later
   ```javascript
   <%* const title = await tp.system.prompt("Title") %>
   # <% title %>
   ```
4. **Use whitespace control**: Clean up template output with `-%>` and `<%-`
