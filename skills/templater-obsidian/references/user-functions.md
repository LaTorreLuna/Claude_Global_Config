# User Functions in Templater

**Source:** https://silentvoid13.github.io/Templater/user-functions/overview.html

## Overview

Templater allows you to define custom functions to extend its capabilities beyond the built-in internal functions. User functions enable you to create reusable, project-specific template logic.

## Invocation Syntax

User functions are called using the pattern:

```javascript
<% tp.user.<user_function_name>() %>
```

**Example:**
```javascript
<% tp.user.echo() %>
<% tp.user.getCurrentProject() %>
<% tp.user.formatDate(tp.date.now()) %>
```

## Types of User Functions

Templater provides two approaches for creating user functions:

### 1. Script User Functions

JavaScript-based custom functions that run within Templater's context.

**Characteristics:**
- Written in JavaScript
- Can use Templater's internal functions
- Access to Obsidian's API
- Loaded as CommonJS modules

### 2. System Command User Functions

Functions that execute system commands and return their output.

**Characteristics:**
- Execute shell commands
- Return command output
- **Security warnings apply** - only use trusted commands
- Can interact with system utilities

## Key Limitations

**Mobile Compatibility:**
> "Currently user functions are unavailable on Obsidian for mobile"

User functions are restricted to desktop environments only.

## Configuration

User functions must be configured in Templater settings:

1. **Settings > Templater > User Script Functions**
   - Specify folder containing JavaScript files
   - Each `.js` file becomes a user function

2. **Settings > Templater > System Command User Functions**
   - Define system commands and their invocation names

## Example Use Cases

### Script User Functions

```javascript
// In user_scripts/getCurrentProject.js
module.exports = async function(tp) {
    // Access Templater functions
    const currentFile = tp.file.title;

    // Custom logic
    if (currentFile.includes("Project")) {
        return "Active Project";
    }
    return "General Note";
};
```

**Usage in template:**
```javascript
**Project Type:** <% tp.user.getCurrentProject() %>
```

### System Command Functions

**Example command definition:**
```
Name: git_branch
Command: git rev-parse --abbrev-ref HEAD
```

**Usage in template:**
```javascript
**Current Branch:** <% tp.user.git_branch() %>
```

## Best Practices

1. **Organize user scripts in dedicated folder**:
   ```
   vault/
   ├── templates/
   └── scripts/
       └── templater/
           ├── formatters.js
           ├── helpers.js
           └── integrations.js
   ```

2. **Use CommonJS module format**:
   ```javascript
   module.exports = async function(tp) {
       // Function logic
       return result;
   };
   ```

3. **Accept tp parameter** for access to Templater functions:
   ```javascript
   module.exports = async function(tp) {
       const date = tp.date.now();
       const title = tp.file.title;
       // Use Templater's internal functions
   };
   ```

4. **Handle errors gracefully**:
   ```javascript
   module.exports = async function(tp) {
       try {
           // Function logic
           return result;
       } catch (error) {
           return "Error: " + error.message;
       }
   };
   ```

5. **Document your user functions**:
   - Add comments explaining purpose and parameters
   - Include usage examples
   - Document return values

## Security Considerations

**System Command Functions:**
- Can execute arbitrary system commands
- Only use trusted, verified commands
- Avoid user-provided input in system commands
- Consider security implications before enabling

**Script Functions:**
- Have access to Obsidian API
- Can read/write files in vault
- Can access system via Node.js modules
- Review third-party scripts carefully

## Advanced Topics

For detailed implementation guides, refer to:
- **Script User Functions (Section 3.1)** - Detailed JavaScript implementation
- **System Command User Functions (Section 3.2)** - System integration patterns

## Limitations Summary

- **Desktop only** - Not available on mobile
- **Requires configuration** - Must be set up in settings
- **Security considerations** - Especially for system commands
- **Performance** - Complex functions may slow template insertion
- **Debugging** - Errors may not always be clear

## Quick Reference

### Calling User Functions

```javascript
// No parameters
<% tp.user.myFunction() %>

// With parameters
<% tp.user.formatDate(tp.date.now(), "long") %>

// Async functions
<%* const result = await tp.user.asyncFunction() %>
<% result %>
```

### Creating Script Functions

```javascript
// File: scripts/templater/myFunction.js
module.exports = async function(tp) {
    // Access Templater internals
    const date = tp.date.now();
    const file = tp.file.title;

    // Custom logic
    const result = `${file} - ${date}`;

    // Return value
    return result;
};
```

### Common Patterns

```javascript
// Return formatted text
module.exports = function(tp) {
    return `**Created:** ${tp.date.now()}`;
};

// Access frontmatter
module.exports = function(tp) {
    const status = tp.frontmatter.status || "unknown";
    return `Status: ${status}`;
};

// Conditional logic
module.exports = function(tp) {
    const folder = tp.file.folder();
    if (folder === "Projects") {
        return "## Project Template";
    }
    return "## General Template";
};

// External API calls
module.exports = async function(tp) {
    const data = await fetch('https://api.example.com/data');
    const json = await data.json();
    return json.value;
};
```

## Tips

1. **Test functions in isolation** before using in templates
2. **Use async/await** for operations that may take time
3. **Return strings** for easy template insertion
4. **Keep functions focused** - one function, one purpose
5. **Reuse Templater's functions** instead of reimplementing

## Resources

- Obsidian API documentation
- Node.js documentation for system interactions
- JavaScript async/await patterns
- CommonJS module format

## Example Library Structure

```
vault/
└── scripts/
    └── templater/
        ├── README.md
        ├── dates/
        │   ├── formatDate.js
        │   └── workdayCalculator.js
        ├── files/
        │   ├── findRelated.js
        │   └── generateTitle.js
        └── utilities/
            ├── capitalize.js
            └── slugify.js
```

This organization makes user functions easier to maintain and discover.
