# Templater for Obsidian - Claude Skill

Comprehensive documentation for the Templater plugin, manually curated from official sources.

## Installation

1. Copy this `templater-obsidian-manual/` directory to your Claude skills location
2. Or use the skill directly in Claude Code sessions

## What's Included

### SKILL.md
Main skill file with:
- Quick reference for all Templater functions
- Common usage patterns
- Template examples (Daily Notes, Meeting Notes, Project Templates)
- Best practices and troubleshooting

### Reference Documentation

#### Core Documentation
- `references/introduction.md` - Overview and core concepts
- `references/syntax.md` - Command syntax and argument passing
- `references/settings.md` - Configuration and setup
- `references/commands.md` - Interpolation vs execution commands

#### Internal Functions
- `references/internal-functions/date.md` - Date manipulation (tp.date.*)
- `references/internal-functions/file.md` - File operations (tp.file.*)
- `references/internal-functions/frontmatter.md` - YAML frontmatter access (tp.frontmatter.*)
- `references/internal-functions/system.md` - User prompts and interaction (tp.system.*)
- `references/internal-functions/web.md` - Web requests and external data (tp.web.*)
- `references/internal-functions/config.md` - Template configuration (tp.config.*)

#### Advanced Topics
- `references/user-functions.md` - Creating custom JavaScript functions

## Quick Start

### Basic Template Syntax

```javascript
<%  expression  %>     # Interpolation - outputs result
<%* code %>            # Execution - runs JavaScript, no output
```

### Most Common Functions

```javascript
// Dates
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.tomorrow() %>

// File metadata
<% tp.file.title %>
<% tp.file.creation_date() %>

// Frontmatter
<% tp.frontmatter.property_name %>

// User input
<%* const name = await tp.system.prompt("Enter name") %>

// File operations
<%* await tp.file.create_new("template", "filename") %>
```

## Documentation Source

Manually curated from: https://silentvoid13.github.io/Templater/

Last updated: October 2024

## File Structure

```
templater-obsidian-manual/
├── SKILL.md                           # Main skill file
├── README.md                          # This file
├── references/                        # Detailed documentation
│   ├── introduction.md
│   ├── syntax.md
│   ├── settings.md
│   ├── commands.md
│   ├── user-functions.md
│   └── internal-functions/
│       ├── date.md
│       ├── file.md
│       ├── frontmatter.md
│       ├── system.md
│       ├── web.md
│       └── config.md
├── scripts/                           # (Empty - for future utilities)
└── assets/                            # (Empty - for future templates)
```

## Usage in Claude Code

When working with Obsidian Templater templates, Claude will automatically reference this skill to provide:

- Correct syntax for Templater functions
- Examples of common patterns
- Troubleshooting guidance
- Best practices for template design

## Features

✅ Complete function reference for all tp.* modules
✅ Extensive examples for each function
✅ Common workflow patterns
✅ Date formatting guide
✅ Interactive template examples
✅ Error handling patterns
✅ Security considerations
✅ Performance tips
✅ Mobile limitations documented

## Notes

- This skill covers Templater functionality for desktop Obsidian
- User functions are desktop-only (not available on mobile)
- All examples tested with Templater plugin compatible with Obsidian 1.4+
- Date formatting uses moment.js syntax

## Contributing

To update this skill:
1. Review official Templater documentation for changes
2. Update relevant reference files
3. Add new examples to SKILL.md
4. Test examples in actual Templater templates

## License

Documentation content curated from official Templater documentation at https://silentvoid13.github.io/Templater/

Skill organization and curation by Claude Code skill builder.
