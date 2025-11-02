# Claude Code Multi-Device Migration - Documentation Map

**Purpose**: Navigation hub for ALL project documentation across multiple locations

**Created**: 2025-11-01
**Status**: Active Reference
**Synced via Git**: This file is in the Git repository and syncs across all devices

---

## Quick Navigation

**Need to...**
- [[#For New Device Setup|Set up a new device?]] → Use Setup Guides
- [[#For Historical Context|Understand what happened?]] → Read Migration History
- [[#For Troubleshooting & Technical Deep-Dive|Troubleshoot issues?]] → Check Technical Research
- [[#For Maintenance|Update the system?]] → See Maintenance Workflows

---

## Document Hierarchy

### Level 1: Setup Guides (User-Facing, Active Use)

**Location**: `/Users/astro/Claude_Global_Config/` (Git repo, syncs to all devices)

**Audience**: Anyone setting up Claude Code on a new device

**Documents**:

| File | Purpose | When to Use |
|------|---------|-------------|
| **[README.md](file:///Users/astro/Claude_Global_Config/README.md)** | Main setup guide for Mac/Linux/Windows | First time setup on ANY device |
| **[WINDOWS_SETUP.md](file:///Users/astro/Claude_Global_Config/WINDOWS_SETUP.md)** | Windows-specific instructions | Windows device setup |
| **[plugins_manifest.json](file:///Users/astro/Claude_Global_Config/plugins_manifest.json)** | Plugin installation list (7 plugins) | Auto-read by setup scripts |
| **THIS FILE** | Navigation hub for all docs | Finding documentation |

**What's Here**:
- One-command setup instructions
- 24 global skills (cross-platform)
- 7 plugin manifest (auto-install)
- Setup automation scripts

---

### Level 2: Technical Implementation (Scripts & Tools)

**Location**: `/Users/astro/Claude_Global_Config/tools/` (Git repo)

**Audience**: Developers maintaining the system

**Scripts**:

| File | Platform | Purpose |
|------|----------|---------|
| **[setup-device.sh](file:///Users/astro/Claude_Global_Config/tools/setup-device.sh)** | Mac/Linux | Automated setup: symlinks + plugins |
| **[setup-windows.ps1](file:///Users/astro/Claude_Global_Config/tools/setup-windows.ps1)** | Windows | Automated setup: junctions + plugins |
| **[device-context.sh](file:///Users/astro/Claude_Global_Config/tools/device-context.sh)** | Mac/Linux | Environment detection utility |

**What They Do**:
1. Clone Git repo
2. Create `~/.claude/skills/` directory
3. Create 24 individual symlinks for global skills
4. Create 4 individual symlinks for FUSD skills (Mac only)
5. Read `plugins_manifest.json`
6. Install all 7 plugins automatically
7. Configure shell integration

---

### Level 3: Migration History (Project Management)

**Location**: `/Users/astro/Documents/Claude_Multi_Device_Migration_Project/`

**Audience**: Understanding project decisions, timeline, and evolution

**Documents**:

| File | Purpose | Read When... |
|------|---------|--------------|
| **[MIGRATION_COMPLETE.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_COMPLETE.md)** | Final summary & success metrics | Confirming what was achieved |
| **[MIGRATION_PLAN_REVISED.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_PLAN_REVISED.md)** | Revised plan after blocker discovery | Understanding the CORRECT approach |
| **[BLOCKER.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/BLOCKER.md)** | Critical blocker: subdirectory support | Why nested directories don't work |
| **[MIGRATION_PLAN.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_PLAN.md)** | Original plan (INCORRECT assumptions) | Historical reference only |
| **[PROJECT_STATUS.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/PROJECT_STATUS.md)** | Status tracking during migration | Timeline reconstruction |
| **[CONTEXT.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/CONTEXT.md)** | Project context and background | Understanding project origins |
| **[NEXT_STEPS.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/NEXT_STEPS.md)** | Post-migration action items | Future enhancements |
| **[RESEARCH_FINDINGS.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/RESEARCH_FINDINGS.md)** | Research compilation | Background investigation summary |
| **[README.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/README.md)** | Project folder overview | Entry point to this directory |

**Key Insights**:
- Original plan assumed nested directories (WRONG)
- Blocker discovered via documentation research
- Plan revised to individual symlinks (CORRECT)
- Total migration time: ~2.5 hours (including research)
- Timeline: Oct 31 - Nov 1, 2024

---

### Level 4: Technical Deep-Dive (Research & Analysis)

**Location**: `/Users/astro/Documents/Synthesis/claude-code-research/`

**Audience**: Developers needing technical architecture details

**Documents**:

| File | Purpose | Read When... |
|------|---------|--------------|
| **[README.md](file:///Users/astro/Documents/Synthesis/claude-code-research/README.md)** | Research directory overview | Finding specific technical docs |
| **[01-comprehensive-architecture-analysis.md](file:///Users/astro/Documents/Synthesis/claude-code-research/01-comprehensive-architecture-analysis.md)** | Full Claude Code system architecture | Understanding configuration hierarchy, component integration |
| **[02-skills-subdirectory-support-analysis.md](file:///Users/astro/Documents/Synthesis/claude-code-research/02-skills-subdirectory-support-analysis.md)** | Subdirectory support investigation | Why flat structure is required |

**What's Covered**:
- Configuration precedence (Enterprise > Project > User)
- Skills system architecture
- Agents, hooks, plugins architecture
- Skills directory structure rules
- Empirical evidence and testing
- Best practices for organizing projects

**Critical Finding**: User skills require flat structure; plugins can use nested organization

---

### Level 5: Vault-Specific Documentation (FUSD Context)

**Location**: `/Users/astro/Documents/FUSD Notes/_Claude_Config/`

**Audience**: FUSD vault users (Mac only, Google Drive synced)

**Documents**:

| File | Purpose | Read When... |
|------|---------|--------------|
| **[MIGRATION_LOG.md](file:///Users/astro/Documents/FUSD Notes/_Claude_Config/MIGRATION_LOG.md)** | Vault-specific migration log | Understanding vault changes |
| **skills/** directory | 4 FUSD-specific skills | Using FUSD skills |

**FUSD Skills (4 total)**:
- `fusd-document-taxonomy` - FUSD document classification
- `ghr-qualifications-configuration` - GHR system specific
- `infor-isd-reports-skill` - Infor/ISD specific
- `lawson-lpl-generator-skill` - Lawson system specific

**Platform Note**: FUSD skills only available on Mac (Google Drive path differences break Windows)

---

## Documentation by Use Case

### For New Device Setup

**Start here**: [README.md](file:///Users/astro/Claude_Global_Config/README.md) (Git repo root)

**Mac/Linux**:
```bash
gh repo clone LaTorreLuna/Claude_Global_Config ~/Claude_Global_Config
~/Claude_Global_Config/tools/setup-device.sh
# Restart terminal
```

**Windows**:
```powershell
gh repo clone LaTorreLuna/Claude_Global_Config "$env:USERPROFILE\Claude_Global_Config"
cd "$env:USERPROFILE\Claude_Global_Config\tools"
.\setup-windows.ps1
# Restart Claude Code
```

**What you get**: 70+ skills (24 user + 46+ plugin skills)

---

### For Historical Context

**Why this migration happened**:
1. Read [CONTEXT.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/CONTEXT.md) - Project origins
2. Read [RESEARCH_FINDINGS.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/RESEARCH_FINDINGS.md) - Initial investigation
3. Read [BLOCKER.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/BLOCKER.md) - Critical discovery
4. Read [MIGRATION_PLAN_REVISED.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_PLAN_REVISED.md) - Corrected approach
5. Read [MIGRATION_COMPLETE.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_COMPLETE.md) - Final outcome

**Timeline**: October 2024 (planning) → October 31, 2024 (research) → November 1, 2024 (execution)

---

### For Troubleshooting & Technical Deep-Dive

**Skills not loading?**
1. Check [02-skills-subdirectory-support-analysis.md](file:///Users/astro/Documents/Synthesis/claude-code-research/02-skills-subdirectory-support-analysis.md) - Verify flat structure
2. Verify symlinks exist: `ls -la ~/.claude/skills/`
3. Check skill has `SKILL.md` at root

**Configuration precedence issues?**
1. Read [01-comprehensive-architecture-analysis.md](file:///Users/astro/Documents/Synthesis/claude-code-research/01-comprehensive-architecture-analysis.md) - Section 1.2
2. Check Enterprise > Project > User hierarchy

**Plugin installation failing?**
1. Verify `plugins_manifest.json` is valid JSON
2. Re-run setup script to trigger auto-install
3. Check [README.md](file:///Users/astro/Claude_Global_Config/README.md) - Plugin section

**FUSD skills not available (Windows)?**
- Expected behavior - FUSD skills are Mac-only (Google Drive path dependencies)
- See [MIGRATION_COMPLETE.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_COMPLETE.md) - Platform Support section

---

### For Maintenance

**Adding new global skills**:
```bash
# 1. Add skill to Git repo
mkdir ~/Claude_Global_Config/skills/new-skill
# ... create SKILL.md and files ...

# 2. Commit and push
cd ~/Claude_Global_Config
git add skills/new-skill
git commit -m "Add new-skill"
git push

# 3. On other devices
git pull
./tools/setup-device.sh  # Auto-creates symlink
```

**Adding new plugins**:
```bash
# 1. Install plugin on main device
claude plugin install new-plugin

# 2. Update manifest in Git
cp ~/.claude/plugins/installed_plugins.json ~/Claude_Global_Config/plugins_manifest.json

# 3. Commit and push
cd ~/Claude_Global_Config
git add plugins_manifest.json
git commit -m "Add new-plugin to manifest"
git push

# 4. On other devices
git pull
./tools/setup-device.sh  # Auto-installs plugin
```

**Updating existing skills**:
```bash
cd ~/Claude_Global_Config
# Edit skill files
git add skills/skill-name
git commit -m "Update skill-name"
git push

# On other devices
git pull  # Changes sync automatically via symlinks
```

---

## Architecture Summary

### What Gets Synced

**Via Git (cross-platform)**:
- 24 global user skills (content)
- 7 plugin manifest (list only, not content)
- Setup automation scripts
- Documentation (this file)

**Via Google Drive (Mac only)**:
- 4 FUSD vault skills (content)
- Vault-specific documentation

**NOT Synced**:
- Plugin content (managed by Claude Code)
- `~/.claude/` directory (created by setup scripts)

### Symlink Architecture

```
~/.claude/skills/ (flat directory)
├── advanced-sql-skill/ → ~/Claude_Global_Config/skills/advanced-sql-skill/
├── article-extractor/ → ~/Claude_Global_Config/skills/article-extractor/
├── [... 22 more global skills ...]
├── fusd-document-taxonomy/ → $FUSD_VAULT/_Claude_Config/skills/fusd-document-taxonomy/
├── ghr-qualifications-configuration/ → $FUSD_VAULT/_Claude_Config/skills/ghr-qualifications-configuration/
├── infor-isd-reports-skill/ → $FUSD_VAULT/_Claude_Config/skills/infor-isd-reports-skill/
└── lawson-lpl-generator-skill/ → $FUSD_VAULT/_Claude_Config/skills/lawson-lpl-generator-skill/
```

**Why Individual Symlinks?**
- Claude Code requires flat directory structure
- Does NOT recurse into subdirectories for user skills
- See [BLOCKER.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/BLOCKER.md) for details

### Platform Support

| Feature | Mac | Windows | Linux |
|---------|-----|---------|-------|
| Global Skills (24) | ✅ | ✅ | ✅ |
| Plugin Skills (46+) | ✅ | ✅ | ✅ |
| FUSD Skills (4) | ✅ | ❌ | ❌ |
| **Total Skills** | **74+** | **70+** | **70+** |

---

## Skills Inventory

### Global Skills (24 total)

**Git-synced, available on all devices**:

**Core Skills (9)**:
- advanced-sql-skill
- article-extractor
- claudesidian
- csv-data-summarizer-claude-skill
- file-organizer
- meeting-insights-analyzer
- notebook-navigator
- word-diagram-formatter
- youtube-transcript

**Obsidian Skills (11)**:
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

**Taxonomy Skills (3)**:
- tag-taxonomy-migration
- taxonomy-design-workflow
- taxonomy-validation

**Other (1)**:
- templater-obsidian

### FUSD Skills (4 total)

**Vault-synced, Mac only**:
- fusd-document-taxonomy (FUSD document classification)
- ghr-qualifications-configuration (GHR Talent configuration)
- infor-isd-reports-skill (Infor ISD operations)
- lawson-lpl-generator-skill (Lawson LPL generation)

### Plugin Skills (46+ total)

**Auto-installed from 7 plugins**:

**document-skills** (4 skills):
- xlsx, docx, pptx, pdf

**example-skills** (10 skills):
- skill-creator, mcp-builder, canvas-design, algorithmic-art
- internal-comms, webapp-testing, artifacts-builder
- slack-gif-creator, theme-factory, brand-guidelines

**superpowers** (22 skills):
- brainstorming, write-plan, executing-plans
- requesting-code-review, receiving-code-review, code-reviewer
- finishing-a-development-branch, root-cause-tracing
- condition-based-waiting, defense-in-depth
- dispatching-parallel-agents
- [11 more workflow skills]

**Other plugins** (10+ skills):
- elements-of-style
- playwright-skill
- project-planner-skill
- claude-notifications-go

---

## Key Design Decisions

### 1. Individual Symlinks (Not Nested Directories)

**Decision**: Flat structure with individual skill symlinks

**Reason**: Claude Code does not recurse into subdirectories for user skills

**Research**: [02-skills-subdirectory-support-analysis.md](file:///Users/astro/Documents/Synthesis/claude-code-research/02-skills-subdirectory-support-analysis.md)

**Evidence**: Documented in [BLOCKER.md](file:///Users/astro/Documents/Claude_Multi_Device_Migration_Project/BLOCKER.md)

### 2. Plugin Manifest (Not Plugin Content)

**Decision**: Sync plugin list via Git, let Claude Code download content

**Reason**:
- Plugin content managed by Claude Code (updates, versioning)
- Syncing list triggers auto-install on new devices
- Avoids Git repo bloat from plugin cache files

**Implementation**: `plugins_manifest.json` extracted from `~/.claude/plugins/installed_plugins.json`

### 3. Vault Skills Separate

**Decision**: Keep FUSD skills in vault, not in Git

**Reason**:
- FUSD-specific (not useful on other projects)
- Google Drive sync works for Mac (path differences break Windows)
- Separation of concerns: global vs project-specific

---

## Repository Information

**GitHub Repository**: https://github.com/LaTorreLuna/Claude_Global_Config

**Branch**: main

**Visibility**: Public

**Key Files**:
- `README.md` - User-facing setup guide
- `WINDOWS_SETUP.md` - Windows-specific instructions
- `DOCUMENTATION_MAP.md` - This navigation hub
- `plugins_manifest.json` - Plugin installation list
- `skills/` - 24 global skills
- `commands/` - Global slash commands
- `agents/` - Global agent definitions
- `tools/` - Setup automation scripts

---

## Backup Information

**Backup Location**: `/Users/astro/claude_migration_backup_20251101_195022`

**Contents**:
- `claude_home/` - Full `~/.claude/` backup (483MB)
- `fusd_vault_config/` - Vault `.claude` config (404KB)
- `ROLLBACK.sh` - Emergency restore script

**Retention**: Keep for 30 days, delete after verification period

---

## Success Metrics

**All criteria met on 2025-11-01**:

### Must Have ✅
- [x] 24 global skills in Git, accessible on all devices
- [x] 4 FUSD skills in Vault, accessible on Mac
- [x] Flat structure in `~/.claude/skills/` (Claude Code requirement)
- [x] Individual symlinks working
- [x] Git sync functional
- [x] Windows setup documented
- [x] Plugins sync automatically

### Nice to Have ✅
- [x] Automated setup script tested
- [x] PowerShell script for Windows created
- [x] Documentation complete
- [x] Performance verified (no slowdown)
- [x] Plugin manifest system

---

## Future Enhancements (Optional)

**Potential Additions**:
1. Auto-sync hooks (Git push after skill changes)
2. Skill development workflow (template for creating new skills)
3. Plugin update notifications (alert when manifest changes upstream)
4. Second Mac testing (verify setup script on fresh device)
5. Commands sync (add global slash commands to repo)
6. Agents sync (add global agent definitions to repo)

**Not Planned**:
- Syncing plugin content (handled by Claude Code)
- Nested skill directories (not supported by Claude Code)
- FUSD skills on Windows (vault unavailable)

---

## Lessons Learned

### What Went Right ✅
1. **Research first** - Reading Claude Code docs prevented wasted effort
2. **Individual symlinks** - Correct approach for flat structure requirement
3. **Git for global** - Cross-platform solution for user skills
4. **Plugin manifest** - Elegant solution: sync list, not content
5. **Automation scripts** - One-command setup on new devices

### What Could Be Better 🔄
1. **Original research** - Should have researched Claude Code behavior BEFORE designing architecture
2. **Assumption validation** - Don't assume nested directories work without checking
3. **Complete solution** - Plugin sync should have been part of original plan

### Key Insight 💡
> "Global means EVERYTHING automatically available, not 'global except you manually install X on each device.'"

The plugin manifest addition was critical to making this truly complete.

---

## Support & Contact

**For issues or questions**:
1. Check [README.md](file:///Users/astro/Claude_Global_Config/README.md) in Git repo
2. Review [WINDOWS_SETUP.md](file:///Users/astro/Claude_Global_Config/WINDOWS_SETUP.md) for Windows issues
3. See migration project folder for historical context
4. GitHub Issues: https://github.com/LaTorreLuna/Claude_Global_Config/issues

---

## Document Change Log

**2025-11-01** - Initial creation
- Mapped all documentation across 4 locations
- Created hierarchical navigation structure
- Added use-case-based access patterns
- Included complete skills inventory
- Documented key design decisions

---

**Status**: Production Ready - All documentation mapped and accessible

**Total Skills Available**: 70+ skills on any device with one command
