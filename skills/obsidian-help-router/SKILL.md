---
name: obsidian-help
description: Use when answering questions about Obsidian features, plugins, or workflows. Routes to specialized sub-skills for efficient token usage via progressive disclosure.
---

# Obsidian Help Documentation Router

This router skill provides intelligent routing to **9 specialized Obsidian documentation skills**, enabling progressive disclosure and token-efficient access to 162 pages of documentation.

## How It Works

Instead of loading all 162 pages at once, this router analyzes your query and directs you to the most relevant sub-skill, loading only 3-66 pages as needed.

## Available Skills

### 1. **obsidian-properties** (3 pages)
**Use for:** Properties, frontmatter, YAML metadata, aliases
**Keywords:** `properties`, `frontmatter`, `yaml`, `metadata`, `aliases`

### 2. **obsidian-plugins** (26 pages)
**Use for:** Core plugins (bookmarks, canvas, search, templates, etc.)
**Keywords:** `plugin`, `bookmarks`, `canvas`, `search`, `templates`, `tags view`, `backlinks`

### 3. **obsidian-sync** (16 pages)
**Use for:** Obsidian Sync setup, conflicts, version history
**Keywords:** `sync`, `synchronization`, `conflict`, `version history`, `remote vault`

### 4. **obsidian-publish** (16 pages)
**Use for:** Publishing vaults to the web
**Keywords:** `publish`, `publishing`, `website`, `public vault`, `embed`

### 5. **obsidian-import** (13 pages)
**Use for:** Importing from other apps (Notion, Evernote, etc.)
**Keywords:** `import`, `migration`, `notion`, `evernote`, `bear`, `roam`

### 6. **obsidian-databases** (10 pages)
**Use for:** Canvas, databases, visual workflows
**Keywords:** `canvas`, `database`, `visual`, `whiteboard`, `nodes`

### 7. **obsidian-web-clipper** (8 pages)
**Use for:** Web clipping and browser integration
**Keywords:** `web clipper`, `browser`, `clip`, `capture`, `highlight`

### 8. **obsidian-teams** (4 pages)
**Use for:** Team collaboration features
**Keywords:** `teams`, `collaboration`, `shared vault`, `enterprise`

### 9. **obsidian-core** (66 pages)
**Use for:** General features (hotkeys, syntax, workspace, themes, mobile)
**Keywords:** `hotkey`, `syntax`, `workspace`, `theme`, `mobile`, `settings`

## Routing Logic

**Query Analysis:**
1. Extract keywords from user query
2. Match to skill coverage areas
3. Route to most specific skill
4. Default to `obsidian-core` for general queries

**Examples:**

| Query | Routes to | Why |
|-------|-----------|-----|
| "How do I add YAML frontmatter?" | obsidian-properties | Frontmatter = properties |
| "Configure bookmarks plugin" | obsidian-plugins | Specific plugin |
| "Sync conflict resolution" | obsidian-sync | Sync-specific |
| "Publish vault to web" | obsidian-publish | Publishing |
| "Import from Notion" | obsidian-import | Import/migration |
| "Create canvas workflow" | obsidian-databases | Canvas feature |
| "Clip webpage to vault" | obsidian-web-clipper | Web clipping |
| "Share vault with team" | obsidian-teams | Team collaboration |
| "Change hotkey bindings" | obsidian-core | General settings |

## Usage Instructions

**When user asks about Obsidian:**

1. **Analyze the query** - Identify main topic
2. **Route to skill** - Use most specific skill
3. **Invoke skill** - Load only what's needed
4. **Respond** - Answer using sub-skill knowledge

**Progressive Disclosure Benefits:**
- Load 3-66 pages instead of all 162
- Reduce token consumption by 50-95%
- Faster responses with focused content
- Better context utilization

## Token Efficiency Comparison

| Approach | Pages Loaded | Token Savings |
|----------|-------------|---------------|
| Monolithic skill | 162 | 0% (baseline) |
| Router + Properties | 3 | 98% |
| Router + Web Clipper | 8 | 95% |
| Router + Plugins | 26 | 84% |
| Router + Core | 66 | 59% |

## Implementation Pattern

```
User Query: "How do I add aliases to my notes?"

1. Router analyzes: "aliases" → obsidian-properties
2. Invoke obsidian-properties skill (3 pages)
3. Find alias documentation
4. Respond with guidance

Tokens saved: ~95% vs loading all 162 pages
```

## Fallback Strategy

If query doesn't clearly match a skill:
1. Default to **obsidian-core** (most comprehensive)
2. Suggest related skills if topic becomes clear
3. Allow user to manually select skill

## Direct Skill Access

Users can directly invoke sub-skills if they know what they need:

- `@obsidian-properties` - Properties/frontmatter
- `@obsidian-plugins` - Core plugins
- `@obsidian-sync` - Sync features
- `@obsidian-publish` - Publishing
- `@obsidian-import` - Import tools
- `@obsidian-databases` - Canvas/databases
- `@obsidian-web-clipper` - Web clipping
- `@obsidian-teams` - Team features
- `@obsidian-core` - General features

## Maintenance

All 9 sub-skills are in:
```
/Users/astro/Documents/FUSD Notes/output/obsidian-{skill-name}/
```

Each contains:
- `SKILL.md` - Skill definition
- `references/` - URL mappings and documentation

## Documentation Source

All documentation URLs reference: `https://help.obsidian.md/`

**Note:** Content extraction was limited due to JavaScript rendering, but URL mappings provide navigation to current documentation.
