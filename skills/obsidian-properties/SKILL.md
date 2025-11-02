---
name: obsidian-properties
description: Use when working with Obsidian properties, frontmatter, YAML metadata, or aliases. Covers property types, syntax, configuration, and the Properties plugin.
---

# Obsidian Properties Skill

This skill provides guidance on Obsidian's properties system, frontmatter/YAML metadata, and aliases.

## When to Use This Skill

Use this skill when:
- Adding or editing YAML frontmatter in notes
- Working with properties (text, number, date, list, etc.)
- Configuring the Properties plugin
- Using aliases for note navigation
- Managing note metadata
- Setting up property templates
- Understanding property syntax

## Coverage

This skill covers **3 documentation pages**:

1. **Core Properties** (`/properties`) - Frontmatter, property types, syntax
2. **Properties Plugin** (`/plugins/properties`) - Plugin features and configuration
3. **Aliases** (`/aliases`) - Alias syntax, use cases, and property integration

## Documentation URLs

For current documentation, refer to:
- Properties: https://help.obsidian.md/properties
- Properties Plugin: https://help.obsidian.md/plugins/properties
- Aliases: https://help.obsidian.md/aliases

## Related Skills

- **obsidian-plugins** - For other Obsidian core plugins
- **obsidian-help** (router) - For general Obsidian documentation

## Usage Examples

**Adding properties to a note:**
```yaml
---
title: My Note
tags: [project, important]
date: 2025-10-26
status: in-progress
aliases: [My Note Alias, Alternative Name]
---
```

**Property types:**
- Text: `title: My Note`
- Number: `rating: 5`
- Date: `date: 2025-10-26`
- List: `tags: [tag1, tag2]`
- Boolean: `published: true`

**Aliases:**
```yaml
---
aliases: [Short Name, Alternative Title]
---
```

## References

See `references/properties.md` for complete URL mappings.
