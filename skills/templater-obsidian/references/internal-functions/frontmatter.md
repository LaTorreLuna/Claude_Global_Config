# tp.frontmatter Module - YAML Frontmatter Access

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/frontmatter-module.html

The frontmatter module exposes "all the frontmatter variables of a file as variables."

## Primary Function

### tp.frontmatter.<property_name>

Retrieves the value of a specific YAML frontmatter field from your file's metadata.

## Usage Patterns

### 1. Standard Notation (Simple Names)

For simple variable names without spaces or special characters:

```javascript
<% tp.frontmatter.alias %>
<% tp.frontmatter.status %>
<% tp.frontmatter.project %>
```

### 2. Bracket Notation (Spaces/Special Characters)

For variables with spaces or special characters:

```javascript
<% tp.frontmatter["variable name with spaces"] %>
<% tp.frontmatter["note type"] %>
<% tp.frontmatter["created-by"] %>
```

### 3. Array Manipulation

You can use JavaScript array methods on list-type frontmatter:

```javascript
// Join array items
<% tp.frontmatter.tags.join(", ") %>

// Map and transform
<% tp.frontmatter.categories.map(prop => `  - "${prop}"`).join("\n") %>

// Filter array
<% tp.frontmatter.tags.filter(tag => tag.startsWith("project")).join(", ") %>
```

## Practical Examples

### Example 1: Basic Access

Given frontmatter:
```yaml
---
alias: myfile
note type: seedling
status: active
---
```

Access with:
```javascript
Alias: <% tp.frontmatter.alias %>
// Output: myfile

Type: <% tp.frontmatter["note type"] %>
// Output: seedling

Status: <% tp.frontmatter.status %>
// Output: active
```

### Example 2: Array Processing

Given frontmatter:
```yaml
---
tags: [project, work, active]
categories:
  - Development
  - Planning
  - Review
---
```

Access with:
```javascript
// Simple array join
Tags: <% tp.frontmatter.tags.join(", ") %>
// Output: project, work, active

// Formatted list
Categories:
<% tp.frontmatter.categories.map(cat => `- ${cat}`).join("\n") %>
// Output:
// - Development
// - Planning
// - Review

// Conditional processing
<%* if (tp.frontmatter.tags.includes("active")) { %>
This is an active project!
<%* } %>
```

### Example 3: Dynamic Templates

Given frontmatter:
```yaml
---
project: Website Redesign
status: in-progress
assignee: John Doe
due_date: 2024-02-15
---
```

Template:
```javascript
# Project: <% tp.frontmatter.project %>

**Status:** <% tp.frontmatter.status %>
**Assigned to:** <% tp.frontmatter.assignee %>
**Due Date:** <% tp.frontmatter.due_date %>

<%* if (tp.frontmatter.status === "in-progress") { %>
## Current Tasks
- [ ] Task 1
- [ ] Task 2
<%* } else if (tp.frontmatter.status === "completed") { %>
## Project Complete ✓
<%* } %>
```

### Example 4: Conditional Content

```javascript
<%* const noteType = tp.frontmatter["note type"] %>
<%* if (noteType === "meeting") { %>
## Attendees
<% tp.frontmatter.attendees.map(a => `- ${a}`).join("\n") %>

## Action Items
<%* } else if (noteType === "project") { %>
## Project Overview
**Status:** <% tp.frontmatter.status %>
**Timeline:** <% tp.frontmatter.timeline %>
<%* } %>
```

### Example 5: Metadata Validation

```javascript
<%* if (!tp.frontmatter.created) { %>
⚠️ Warning: No creation date in frontmatter
<%* } %>

<%* if (!tp.frontmatter.tags || tp.frontmatter.tags.length === 0) { %>
⚠️ Warning: No tags assigned
<%* } %>

<%* if (tp.frontmatter.status === "archived") { %>
📦 This note has been archived
<%* } %>
```

## Common Use Cases

### 1. Generate Table of Contents from Categories
```javascript
## Table of Contents

<% tp.frontmatter.categories.map((cat, idx) => `${idx + 1}. [[${cat}]]`).join("\n") %>
```

### 2. Create Backlink Section
```javascript
## Related Notes

<%* if (tp.frontmatter.related) { %>
<% tp.frontmatter.related.map(link => `- [[${link}]]`).join("\n") %>
<%* } else { %>
No related notes yet.
<%* } %>
```

### 3. Status Badge
```javascript
<%*
const status = tp.frontmatter.status;
const badges = {
    "active": "🟢 Active",
    "in-progress": "🟡 In Progress",
    "completed": "✅ Completed",
    "archived": "📦 Archived"
};
%>
**Status:** <% badges[status] || status %>
```

### 4. Priority Indicator
```javascript
<%*
const priority = tp.frontmatter.priority;
const stars = "⭐".repeat(priority || 0);
%>
**Priority:** <% stars %> (<% priority %>/5)
```

## Best Practices

1. **Check for existence before using**:
   ```javascript
   <%* if (tp.frontmatter.property) { %>
   Property exists: <% tp.frontmatter.property %>
   <%* } %>
   ```

2. **Use bracket notation for safety**:
   ```javascript
   // Safer for properties that might not exist
   <% tp.frontmatter["optional-property"] || "default value" %>
   ```

3. **Validate array properties**:
   ```javascript
   <%* if (Array.isArray(tp.frontmatter.tags) && tp.frontmatter.tags.length > 0) { %>
   Tags: <% tp.frontmatter.tags.join(", ") %>
   <%* } %>
   ```

4. **Use default values**:
   ```javascript
   <% tp.frontmatter.status || "no status" %>
   <% tp.frontmatter.priority || 0 %>
   ```

## Limitations

- Frontmatter must exist in the file for properties to be accessible
- Properties are read-only within templates
- Changing frontmatter values in template doesn't update the actual frontmatter
- Complex nested objects may require careful navigation

## Additional Notes

This module is particularly useful for:
- Dynamically pulling metadata into templates without manual duplication
- Creating conditional template sections based on note type or status
- Generating formatted lists from array-based frontmatter
- Building note templates that adapt to metadata values
