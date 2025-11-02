# tp.file Module - File Operations

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/file-module.html

## Properties

### tp.file.content

Returns the string contents of the file when Templater executes.

**Note:** "Manipulating this string will _not_ update the current file"

**Example:**
```javascript
<% tp.file.content %>
```

### tp.file.title

Retrieves the file's title (without extension).

**Example:**
```javascript
<% tp.file.title %>
// Output: My Note Title
```

### tp.file.tags

Returns an array of string tags from the file.

**Example:**
```javascript
<% tp.file.tags %>
// Output: ["project", "active", "work"]

// Iterate over tags
<%* tp.file.tags.forEach(tag => { %>
- #<% tag %>
<%* }) %>
```

## Path Functions

### tp.file.path()

**Signature:** `tp.file.path(relative: boolean = false)`

Gets the file's absolute system path.

**Parameters:**
- `relative`: When `true`, returns vault-relative path only

**Examples:**
```javascript
<% tp.file.path() %>
// Output: /Users/name/vault/Projects/My Note.md

<% tp.file.path(true) %>
// Output: Projects/My Note.md
```

### tp.file.folder()

**Signature:** `tp.file.folder(absolute: boolean = false)`

Returns the folder name containing the file.

**Parameters:**
- `absolute`: When `true`, provides vault-absolute path; `false` gives only basename

**Examples:**
```javascript
<% tp.file.folder() %>
// Output: Projects

<% tp.file.folder(true) %>
// Output: Work/Active/Projects
```

## Date Functions

### tp.file.creation_date()

**Signature:** `tp.file.creation_date(format: string = "YYYY-MM-DD HH:mm")`

Retrieves creation date with customizable formatting.

**Examples:**
```javascript
<% tp.file.creation_date() %>
// Output: 2024-01-15 14:30

<% tp.file.creation_date("YYYY-MM-DD") %>
// Output: 2024-01-15

<% tp.file.creation_date("dddd, MMMM Do YYYY") %>
// Output: Monday, January 15th 2024
```

### tp.file.last_modified_date()

**Signature:** `tp.file.last_modified_date(format: string = "YYYY-MM-DD HH:mm")`

Gets last modification date with format options.

**Examples:**
```javascript
<% tp.file.last_modified_date() %>
// Output: 2024-01-15 16:45

<% tp.file.last_modified_date("YYYY-MM-DD HH:mm:ss") %>
// Output: 2024-01-15 16:45:30
```

## Selection Function

### tp.file.selection()

Retrieves currently selected text in the active file.

**Example:**
```javascript
<%* const selected = tp.file.selection() %>
You selected: <% selected %>
```

## File Operations

### tp.file.create_new()

**Signature:** `tp.file.create_new(template: TFile | string, filename?: string, open_new: boolean = false, folder?: TFolder | string)`

Creates new file using template or content string.

**Parameters:**
- `template`: Template file object or content string
- `filename`: Name for new file (optional)
- `open_new`: Whether to open the new file (default: false)
- `folder`: Destination folder (optional)

**Examples:**
```javascript
// Create from template
<%* await tp.file.create_new("templates/project", "New Project") %>

// Create and open
<%* await tp.file.create_new("templates/project", "New Project", true) %>

// Create in specific folder
<%* await tp.file.create_new("templates/project", "New Project", false, "Projects/Active") %>

// Create from content string
<%* await tp.file.create_new("# New Note\n\nContent here", "Quick Note") %>
```

### tp.file.rename()

**Signature:** `tp.file.rename(new_title: string)`

Renames file while preserving extension.

**Example:**
```javascript
<%* await tp.file.rename("New Note Title") %>
```

**Note:** Must use execution command (`<%* %>`) with `await`

### tp.file.move()

**Signature:** `tp.file.move(new_path: string, file_to_move?: TFile)`

Moves file to new vault location (path excludes extension).

**Examples:**
```javascript
// Move current file
<%* await tp.file.move("Archive/Old Notes/" + tp.file.title) %>

// Move specific file
<%*
const fileToMove = tp.file.find_tfile("Some File");
await tp.file.move("Projects/" + fileToMove.basename, fileToMove);
%>
```

### tp.file.exists()

**Signature:** `tp.file.exists(filepath: string)`

Checks if file exists at specified path.

**Example:**
```javascript
<%* if (tp.file.exists("templates/daily.md")) { %>
Template exists!
<%* } %>
```

### tp.file.find_tfile()

**Signature:** `tp.file.find_tfile(filename: string)`

Searches for file and returns TFile instance.

**Example:**
```javascript
<%*
const template = tp.file.find_tfile("my-template");
await tp.file.create_new(template, "New Note");
%>
```

### tp.file.include()

**Signature:** `tp.file.include(include_link: string | TFile)`

Includes file content with template resolution.

**Features:**
- Supports sections: `[[File#Section]]`
- Supports blocks: `[[File#^block]]`
- Templates in included files are resolved

**Examples:**
```javascript
// Include entire file
<% tp.file.include("[[templates/footer]]") %>

// Include specific section
<% tp.file.include("[[templates/shared#Contact Info]]") %>

// Include block
<% tp.file.include("[[templates/shared#^contact-block]]") %>
```

## Cursor Functions

### tp.file.cursor()

**Signature:** `tp.file.cursor(order?: number)`

Sets cursor position after template insertion.

**Features:**
- Multi-cursor support via same order numbers
- Automatically triggered if "Automatic Cursor Jump" is enabled
- Can be manually triggered via hotkey

**Examples:**
```javascript
// Single cursor
# Title

<% tp.file.cursor(1) %>

// Multiple cursors (same order)
Name: <% tp.file.cursor(1) %>
Email: <% tp.file.cursor(1) %>

// Ordered cursors
First: <% tp.file.cursor(1) %>
Second: <% tp.file.cursor(2) %>
Third: <% tp.file.cursor(3) %>
```

### tp.file.cursor_append()

**Signature:** `tp.file.cursor_append(content: string)`

Appends content after active cursor position.

**Example:**
```javascript
<%* await tp.file.cursor_append("\n\n---\nFooter content") %>
```

## Common Workflows

### Create Daily Note
```javascript
<%*
const today = tp.date.now("YYYY-MM-DD");
const dailyPath = "Daily Notes/" + today;

if (!tp.file.exists(dailyPath + ".md")) {
    await tp.file.create_new("templates/daily", today, true, "Daily Notes");
}
%>
```

### Archive Old Note
```javascript
<%*
const archivePath = "Archive/" + tp.file.folder() + "/" + tp.file.title;
await tp.file.move(archivePath);
%>
```

### Include Dynamic Section
```javascript
# Project: <% tp.file.title %>

## Standard Sections
<% tp.file.include("[[templates/project-sections]]") %>

## Project-Specific Content
<% tp.file.cursor(1) %>
```
