# Claude Global Configuration

**Purpose**: Cross-platform Claude Code configuration synced via Git

**Need help finding documentation?** See **[DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)** - Complete navigation hub for all project docs

---

## What Gets Synced

### ✅ User Skills (24 global)
- Automatically available on all devices
- Located in `skills/` directory
- Individual symlinks in `~/.claude/skills/`

### ✅ Plugin Manifest (7 plugins)
- List of installed plugins
- Auto-installed on new devices via setup scripts
- Tracked in `plugins_manifest.json`

### ✅ Setup Scripts
- `tools/setup-device.sh` - Mac/Linux setup
- `tools/setup-windows.ps1` - Windows setup
- `tools/device-context.sh` - Device detection utility

## Structure

```
Claude_Global_Config/
├── skills/                    # 24 global user skills
├── commands/                  # Global slash commands
├── agents/                    # Global agent definitions
├── tools/                     # Setup and utility scripts
├── plugins_manifest.json      # Plugin installation list
├── README.md                  # This file
├── DOCUMENTATION_MAP.md       # Navigation hub for ALL docs
└── WINDOWS_SETUP.md          # Windows-specific guide
```

## Quick Setup

### Mac/Linux

```bash
# Clone repo
gh repo clone LaTorreLuna/Claude_Global_Config ~/Claude_Code/Claude_Global_Config

# Run setup (creates symlinks + installs plugins)
~/Claude_Code/Claude_Global_Config/tools/setup-device.sh

# Restart terminal
```

### Windows

```powershell
# Clone repo
gh repo clone LaTorreLuna/Claude_Global_Config "$env:USERPROFILE\Claude_Code\Claude_Global_Config"

# Run setup (creates junctions + installs plugins)
cd "$env:USERPROFILE\Claude_Code\Claude_Global_Config\tools"
.\setup-windows.ps1

# Restart Claude Code
```

## What You Get

After setup, you'll have:

- **24 user skills** (cross-platform, Git-synced)
- **7 plugins** (auto-installed from manifest):
  - document-skills (xlsx, docx, pptx, pdf)
  - example-skills (skill-creator, mcp-builder, etc.)
  - superpowers (brainstorming, write-plan, executing-plans, etc.)
  - elements-of-style
  - playwright-skill
  - project-planner-skill
  - claude-notifications-go

**Total: 70+ skills available** (24 user + 46+ from plugins)

## Skills in This Repo (24 total)

### Core Skills
- advanced-sql-skill
- article-extractor
- claudesidian
- csv-data-summarizer-claude-skill
- file-organizer
- meeting-insights-analyzer
- notebook-navigator
- word-diagram-formatter
- youtube-transcript

### Obsidian Skills (11 total)
- obsidian-core
- obsidian-databases
- obsidian-help-router
- obsidian-iconize
- obsidian-import
- obsidian-plugins
- obsidian-properties
- obsidian-publish
- obsidian-sync
- obsidian-teams
- obsidian-web-clipper

### Taxonomy Skills (3 total)
- tag-taxonomy-migration
- taxonomy-design-workflow
- taxonomy-validation

### Other
- templater-obsidian

## Updating Plugins

When you install new plugins on your main device:

```bash
# Copy updated plugin list to repo
cp ~/.claude/plugins/installed_plugins.json ~/Claude_Code/Claude_Global_Config/plugins_manifest.json

# Commit and push
cd ~/Claude_Code/Claude_Global_Config
git add plugins_manifest.json
git commit -m "Update plugin manifest"
git push
```

On other devices, just pull and run setup again:

```bash
cd ~/Claude_Code/Claude_Global_Config
git pull
./tools/setup-device.sh  # Mac/Linux
# Or: .\tools\setup-windows.ps1  # Windows
```

## Maintenance

### Adding New Skills

1. Add skill to `~/Claude_Code/Claude_Global_Config/skills/`
2. Commit and push to Git
3. Setup script will automatically symlink it on other devices

### Removing Skills

1. Remove from `~/Claude_Code/Claude_Global_Config/skills/`
2. Commit and push to Git
3. Manually remove symlink on other devices: `rm ~/.claude/skills/skill-name`

## Platform Support

| Feature | Mac | Windows |
|---------|-----|---------|
| User Skills (24) | ✅ | ✅ |
| Plugins (7) | ✅ | ✅ |
| FUSD Skills (4)* | ✅ | ❌ |

*FUSD skills are vault-specific and only available on Mac with Google Drive access

## Architecture

```
~/.claude/skills/ (flat directory with symlinks)
├── skill-1 → ~/Claude_Code/Claude_Global_Config/skills/skill-1/
├── skill-2 → ~/Claude_Code/Claude_Global_Config/skills/skill-2/
└── [22 more skills...]

~/.claude/plugins/ (managed by Claude Code)
├── installed_plugins.json (synced via Git as plugins_manifest.json)
├── cache/ (remote plugins)
└── marketplaces/ (local plugins)
```

## Documentation

**Complete project documentation map**: [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)

This comprehensive MOC includes:
- All setup guides (this file, Windows guide)
- Migration history and project decisions
- Technical research and architecture analysis
- Troubleshooting resources
- Maintenance workflows

**Quick links**:
- **Setting up new device?** → You're in the right place (see Quick Setup above)
- **Understanding the project?** → [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- **Windows setup?** → [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **Technical details?** → See DOCUMENTATION_MAP.md → Level 4: Technical Deep-Dive

## Support

For issues or questions:
- Check [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md) for all documentation
- Check [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for Windows-specific help
- Review setup scripts in `tools/` directory
- GitHub Issues: https://github.com/LaTorreLuna/Claude_Global_Config/issues
