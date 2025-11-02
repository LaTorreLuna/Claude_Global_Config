# Claude Global Configuration

**Purpose**: Cross-platform Claude Code configuration synced via Git

## Structure

- `skills/` - Global skills (work on all devices/projects)
- `commands/` - Global slash commands
- `agents/` - Global agent definitions
- `tools/` - Global scripts and utilities

## Sync Strategy

- **Git** - Cross-platform (Mac + Windows)
- **Auto-sync** - Pull on shell startup, push after changes
- **Devices** - Available on all machines

## Skills in This Repo

Global skills (22 total):
- pdf-smart-handler
- advanced-sql-skill
- file-organizer
- article-extractor
- csv-data-summarizer-claude-skill
- youtube-transcript
- claudesidian
- obsidian-* (10 Obsidian skills)
- taxonomy-* (3 taxonomy skills)
- templater-obsidian
- notebook-navigator
