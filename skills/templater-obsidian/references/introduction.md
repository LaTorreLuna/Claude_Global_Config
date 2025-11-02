# Templater Introduction

**Source:** https://silentvoid13.github.io/Templater/introduction.html

## What is Templater?

Templater is a template language that lets you insert **variables** and **functions results** into your notes. It will also let you execute JavaScript code manipulating those variables and functions.

With Templater, you will be able to create powerful templates to automate manual tasks.

## Quick Example

### Input Template:
```markdown
---
creation date: <% tp.file.creation_date() %>
modification date: <% tp.file.last_modified_date("dddd Do MMMM YYYY HH:mm:ss") %>
---

<< [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>]] >>

# <% tp.file.title %>

<% tp.web.daily_quote() %>
```

### Output Result:
```markdown
---
creation date: 2021-01-07 17:20
modification date: Thursday 7th January 2021 17:20:43
---

<< [[2021-04-08]] | [[2021-04-10]] >>

# Test Test

> Do the best you can until you know better. Then when you know better, do better.
> — Maya Angelou
```

## Main Documentation Sections

The Templater documentation covers:

1. **Installation** - Setting up the plugin
2. **Terminology** - Core concepts and vocabulary
3. **Syntax** - Command syntax and structure
4. **Settings** - Configuration options
5. **FAQs** - Common questions

### Internal Function Modules

Templater provides nine core internal function modules:

1. **tp.app** - Application interactions
2. **tp.config** - Configuration access
3. **tp.date** - Date manipulation
4. **tp.file** - File operations
5. **tp.frontmatter** - YAML frontmatter access
6. **tp.hooks** - Lifecycle hooks
7. **tp.obsidian** - Obsidian API access
8. **tp.system** - System interactions and user prompts
9. **tp.web** - Web requests and external data

### User Functions

Create custom JavaScript functions to extend Templater's capabilities.

### Commands

Two command types enable different behaviors:
- **Interpolation** (`<% %>`) - Output expression results
- **Execution** (`<%* %>`) - Run JavaScript without output
