---
name: claudesidian
description: Use when working with Claudesidian - an Obsidian vault starter kit integrated with Claude Code for AI-powered note-taking and knowledge management. Trigger for setup, PARA organization, MCP configuration, or vault workflows.
---

# Claudesidian Skill

Comprehensive assistance with Claudesidian - a pre-configured Obsidian vault that transforms Claude Code into an AI-powered second brain. This skill provides expert guidance on setup, configuration, workflows, and troubleshooting.

## When to Use This Skill

This skill should be triggered when users mention or need help with:

**Setup & Installation:**
- Setting up a new Claudesidian vault
- Running `/init-bootstrap` command
- Installing dependencies (pnpm, npm)
- Configuring Git integration
- Setting up MCP servers (Gemini Vision, Firecrawl)

**Organization & Structure:**
- Working with PARA method (Projects, Areas, Resources, Archives)
- Organizing vault folders and files
- Understanding folder structure (00_Inbox through 06_Metadata)
- Creating or managing templates
- Setting up daily notes or weekly reviews

**Claude Code Integration:**
- Using Claudesidian slash commands
- Configuring `.claude/` directory
- Working with custom commands
- Understanding thinking mode vs writing mode
- Troubleshooting Claude Code connections

**MCP & Advanced Features:**
- Configuring Gemini Vision for image/video analysis
- Setting up Firecrawl for web research
- Understanding MCP server integration
- Working with API keys (GEMINI_API_KEY, FIRECRAWL_API_KEY)
- Troubleshooting MCP connections

**Upgrading & Maintenance:**
- Running `/upgrade` command
- Understanding version control
- Managing backups
- Handling Git conflicts
- Updating to new features

## What is Claudesidian?

Claudesidian is an **Obsidian vault starter kit** that combines:

- **Obsidian** - A powerful markdown-based note-taking app
- **Claude Code** - Anthropic's CLI tool for AI assistance
- **PARA Method** - A proven organization system for knowledge management
- **Git Integration** - Version control for your notes
- **MCP Servers** - Advanced integrations (optional)

**Core Philosophy:** Use AI as a thinking partner, not just a writing assistant. Claudesidian enables collaborative intelligence where you and Claude work together to build knowledge, explore ideas, and develop insights.

## Quick Reference

### Essential Commands

**Setup & Initialization:**
```bash
# Clone the repository (pick your own folder name)
git clone https://github.com/heyitsnoah/claudesidian.git my-vault
cd my-vault

# Start Claude Code
claude

# Run interactive setup wizard
/init-bootstrap
```

**Vault Management:**
```bash
# Install global launcher (access vault from anywhere)
/install-claudesidian-command

# Later, from any directory:
claudesidian  # Launches your vault
```

**Daily Workflow:**
```bash
# In Claude Code, use these slash commands:
/thinking-partner   # Explore ideas collaboratively
/inbox-processor    # Organize captured notes
/research-assistant # Deep dive into topics
/daily-review       # End of day reflection
/weekly-synthesis   # Find patterns in your week
```

**Maintenance:**
```bash
# Check for updates
# (Claudesidian checks automatically on startup)

# Preview available updates
/upgrade check

# Run interactive upgrade
/upgrade

# Force upgrade (skip confirmations for safe updates)
/upgrade force
```

### PARA Folder Structure

```
00_Inbox/           # Temporary capture (process regularly)
01_Projects/        # Active work with deadlines
02_Areas/           # Ongoing responsibilities
03_Resources/       # Reference materials
04_Archive/         # Completed/inactive items
05_Attachments/     # Images, PDFs, files
06_Metadata/        # Vault configuration
  ├── Reference/    # Documentation
  └── Templates/    # Note templates
.scripts/           # Helper automation scripts
```

### Web Research with Firecrawl

**Save full web content to your vault:**
```bash
# Single article
npm run firecrawl:scrape -- "https://example.com/article" "03_Resources/Articles"

# Batch save multiple URLs
npm run firecrawl:batch -- urls.txt "03_Resources/Research"

# Custom output directory
.scripts/firecrawl-batch.sh -o "01_Projects/MyProject/Research" urls.txt
```

**Why Firecrawl matters:** Scripts save FULL article text as markdown files in your vault. Claude can then search thousands of saved articles without context limits. Perfect for research projects and building a knowledge archive.

### Image/Video Analysis with Gemini Vision

**Process visual content directly:**
```bash
# Gemini Vision MCP enables:
- Direct image analysis (no need to describe screenshots)
- PDF text extraction (full document text without copy-paste)
- Video analysis (both local files and YouTube URLs)
- Bulk processing (analyze multiple images at once)
- Auto-generate filenames from image content
```

**Example workflow:**
```
# Take screenshot of error → Save to 05_Attachments/
# Tell Claude: "Analyze the latest screenshot and explain the error"
# Claude reads the image directly via Gemini Vision MCP
```

### Helper Scripts

**Run with npm/pnpm:**
```bash
# Attachment management
npm run attachments:list         # Show unprocessed files
npm run attachments:organized    # Count organized files
npm run attachments:sizes        # Find large files
npm run attachments:orphans      # Find unreferenced files

# Vault statistics
npm run vault:stats              # Display vault metrics

# Transcript extraction
npm run transcript-extract -- "https://youtube.com/watch?v=..." "00_Inbox/Clippings/"
```

### Custom Commands & Configuration

**Create a new command:**
```bash
# In Claude Code
/create-command

# Or manually create:
# .claude/commands/my-command.md
```

**Example custom command structure:**
```markdown
<!-- .claude/commands/project-starter.md -->
You are helping start a new project in the PARA system.

Steps:
1. Ask for project name and goal
2. Create folder in 01_Projects/[name]/
3. Create project README with template
4. Set up initial notes structure
5. Link to relevant resources
```

## Key Concepts

### Thinking Mode vs Writing Mode

**Thinking Mode (Research & Exploration):**
- Claude asks questions to understand your goals
- Searches existing notes for relevant content
- Helps make connections between ideas
- Maintains exploration log
- **Example:** "I'm exploring ideas about [topic], not ready to write yet"

**Writing Mode (Content Creation):**
- Generates drafts based on research
- Helps structure and edit content
- Creates final deliverables
- **Example:** "Create a blog post about [topic] based on my notes"

**Best Practice:** Always start in thinking mode. Let Claude help you explore before jumping to writing.

### The PARA Method

**Projects** - Time-bound work with specific goals
```
Examples:
- "Q4 2025 Marketing Strategy"
- "Website Redesign"
- "Learn Spanish"

Location: 01_Projects/
Move to Archive when complete
```

**Areas** - Ongoing responsibilities without end dates
```
Examples:
- "Health & Fitness"
- "Personal Finance"
- "Team Management"

Location: 02_Areas/
Continuous maintenance
```

**Resources** - Topics of ongoing interest
```
Examples:
- "AI Research"
- "Writing Techniques"
- "Python Development"

Location: 03_Resources/
Reference material
```

**Archives** - Completed or inactive items
```
What goes here:
- Finished projects with outputs
- Old notes no longer relevant
- Superseded resources

Location: 04_Archive/
Organized by completion date
```

### Git-Based Knowledge Management

**Why Git for notes:**
- Track evolution of ideas over time
- Safely experiment with organization changes
- Sync across devices
- Collaborate with others
- Roll back changes if needed

**Basic workflow:**
```bash
# After each session
git add .
git commit -m "Session: [what you worked on]"

# Sync with remote
git pull
git push

# Recommended: Commit after major insights
```

### Token Maximalism

**Principle:** More context = better results

**Implementation:**
- Save chat transcripts to vault
- Capture partial thoughts and fragments
- Don't delete "messy" notes
- Link related notes extensively
- Let Claude search your entire vault

**Why:** Claude Code can handle large contexts. Your "messy" notes often contain valuable connections.

### MCP Server Architecture

**What are MCP servers:**
Model Context Protocol servers extend Claude's capabilities with specialized tools.

**Claudesidian's optional MCPs:**

1. **Gemini Vision** - Visual content processing
   - Setup: `export GEMINI_API_KEY="your-key"`
   - Use: Automatic when referencing images/PDFs
   - Location: `.claude/mcp-servers/gemini-vision/`

2. **Firecrawl** - Web content scraping
   - Setup: `export FIRECRAWL_API_KEY="fc-your-key"`
   - Use: Via helper scripts
   - Location: `.scripts/firecrawl-*.sh`

**Configuration:** `.mcp.json` in vault root

## Reference Files

This skill includes comprehensive documentation extracted from the official repository:

### readme.md (Primary Reference - ~1,080 lines)
**Contains:**
- Complete setup guide (git clone vs ZIP download)
- Folder structure explanation
- PARA method overview
- All slash commands documentation
- Upgrade system guide
- Gemini Vision setup instructions
- Firecrawl setup instructions
- Helper scripts reference
- Git integration guide
- Mobile access setup
- Philosophy and best practices
- Troubleshooting common issues

**When to use:**
- First-time setup
- Understanding core concepts
- Finding specific commands
- Troubleshooting issues

**Key sections:**
- Quick Start (lines 10-50)
- Folder Structure (lines 60-90)
- Commands reference (lines 100-150)
- Setup guides (lines 200-300)

### changelog.md (Version History - ~520 lines)
**Contains:**
- Complete version history from 0.1.0 to 0.13.1
- Feature additions by version
- Bug fixes and improvements
- Breaking changes
- Migration notes

**When to use:**
- Understanding what changed between versions
- Checking if a feature exists
- Finding when a bug was fixed
- Upgrade planning

**Recent versions:**
- v0.13.1 (2025-10-13): Path fixes, backup improvements
- v0.13.0 (2025-01-17): iCloud import, launcher command
- v0.12.0 (2025-01-17): Download attachment, pull request commands

### contributing.md (Developer Guide - ~100 lines)
**Contains:**
- Development setup instructions
- Commit message conventions
- Semantic versioning guide
- Pull request process
- Changelog update guidelines
- Release process for maintainers
- Code style guidelines

**When to use:**
- Contributing to Claudesidian
- Understanding version numbering
- Creating pull requests
- Following coding standards

**Key conventions:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `refactor:` - Code improvements

## Working with This Skill

### For Beginners (First Time Users)

**Start here:**
1. Read **Quick Start** section above
2. Clone repository to local machine
3. Run `/init-bootstrap` in Claude Code
4. Answer setup questions honestly
5. Open vault in Obsidian (optional but recommended)
6. Try `/thinking-partner` command

**Common beginner questions:**
- "What's the PARA method?" → See **Key Concepts** section
- "How do I use slash commands?" → Type `/` in Claude Code
- "Do I need Obsidian?" → No, but highly recommended
- "What are MCP servers?" → Optional advanced features

**First session suggestion:**
```
Tell Claude:
"I'm new to Claudesidian. Help me understand how to
organize my first project using the PARA method."
```

### For Setup & Configuration

**Initial setup checklist:**
- [ ] Clone repository with custom folder name
- [ ] Run `/init-bootstrap` wizard
- [ ] Import existing Obsidian vault (if applicable)
- [ ] Set up Git repository
- [ ] Configure Gemini Vision (optional)
- [ ] Configure Firecrawl (optional)
- [ ] Install global launcher command
- [ ] Test slash commands

**Reconfiguration:**
- Re-run `/init-bootstrap` to change settings
- Edit `CLAUDE.md` directly for manual changes
- Update `.mcp.json` for MCP server configuration

**Troubleshooting setup:**
- Check `reference/readme.md` Troubleshooting section
- Verify `.claude/` directory exists
- Ensure dependencies installed (`pnpm install`)
- Check API keys set in environment

### For Daily Usage

**Morning routine:**
```bash
# Launch vault
claudesidian  # (if global command installed)
# or: cd my-vault && claude

# Review inbox
/inbox-processor

# Start daily note
/daily-review
```

**During work:**
```bash
# Capture quick thoughts to 00_Inbox/
# Use /thinking-partner for exploration
# Create project notes in 01_Projects/
# Link to resources in 03_Resources/
```

**Evening routine:**
```bash
# Reflect on day
/daily-review

# Commit changes
git add .
git commit -m "Session: [summary]"
git push
```

**Weekly review:**
```bash
# Find patterns in your week
/weekly-synthesis

# Move completed projects to 04_Archive/
# Clean up 00_Inbox/
# Plan next week's projects
```

### For Advanced Users

**Custom workflow automation:**
- Create custom slash commands in `.claude/commands/`
- Write helper scripts in `.scripts/`
- Build templates in `06_Metadata/Templates/`
- Extend MCP server capabilities

**Git worktree for parallel work:**
```bash
# Create worktrees for different contexts
git worktree add ../vault-work work-context
git worktree add ../vault-personal personal-context

# Run separate Claude sessions
cd ../vault-work && claude  # Terminal 1
cd ../vault-personal && claude  # Terminal 2
```

**Batch operations:**
```bash
# Batch file organization
python3 .scripts/batch_organizer.py

# Batch link updates
node .scripts/update-attachment-links.js

# Batch tagging
python3 .scripts/auto_tagger.js
```

**Advanced MCP integration:**
- Study `.claude/mcp-servers/` structure
- Review MCP documentation
- Build custom MCP servers
- Integrate third-party tools

## Common Use Cases

### Research Project Workflow

**Scenario:** Researching AI safety for a paper

**Workflow:**
```bash
# 1. Create project
mkdir -p "01_Projects/AI_Safety_Paper/"

# 2. Web research with Firecrawl
# Create urls.txt with research articles
npm run firecrawl:batch -- urls.txt "01_Projects/AI_Safety_Paper/Sources/"

# 3. Thinking mode exploration
/thinking-partner
# Tell Claude: "I'm researching AI safety. Search my vault for
# related notes and help me identify key themes."

# 4. Synthesis
/research-assistant
# Tell Claude: "Synthesize findings from AI_Safety_Paper/Sources/
# and create an outline."

# 5. Writing
# "Based on our research, create a first draft of the introduction."

# 6. Archive when complete
mv "01_Projects/AI_Safety_Paper/" "04_Archive/2025-01-15_AI_Safety_Paper/"
```

### Learning New Framework

**Scenario:** Learning React for project

**Workflow:**
```bash
# 1. Create area (ongoing learning)
mkdir -p "02_Areas/Learning_React/"

# 2. Capture resources
# Save tutorials, docs, examples to 02_Areas/Learning_React/Resources/

# 3. Practice projects
# Create projects in 01_Projects/ that use React

# 4. Link learning notes
# Link 02_Areas/Learning_React/ ← → 01_Projects/React_App/

# 5. Daily practice
/thinking-partner
# "Review my React progress and suggest next learning goals."
```

### Team Knowledge Base

**Scenario:** Building team documentation

**Workflow:**
```bash
# 1. Vault as team repository
git remote add origin team-repo-url

# 2. Structure for team
03_Resources/Team_Docs/
  ├── Onboarding/
  ├── Processes/
  ├── Technical_Specs/
  └── Meeting_Notes/

# 3. Collaborative editing
# Multiple team members clone vault
# Use Git branches for major changes
# Regular pulls/pushes to sync

# 4. AI assistance
/research-assistant
# "Analyze our team docs and identify knowledge gaps."
```

## Upgrade & Maintenance

### Understanding the Upgrade System

**Automatic update checks:**
- Claudesidian checks for updates on session start
- Displays notification if new version available
- Safe to ignore until you're ready

**Upgrade workflow:**
```bash
# 1. Check what's new
/upgrade check

# 2. See file-by-file changes
/upgrade  # Interactive mode shows diffs

# 3. Apply updates selectively
# Review each change before accepting
# Skip customized files

# 4. Force safe updates
/upgrade force  # Auto-accepts safe system files
```

**What gets updated:**
- System files (commands, agents, scripts)
- Core documentation
- Dependencies

**What's protected:**
- Your notes (00_Inbox, 01_Projects, 02_Areas, 03_Resources)
- Custom commands you created
- CLAUDE.md customizations
- Local configuration

**Safety features:**
- Complete backup before changes (`.backup/upgrade-[timestamp]/`)
- File-by-file review
- Rollback capability
- Progress tracking (`.upgrade-checklist.md`)

### Backup Strategy

**Automatic backups:**
- `/upgrade` creates timestamped backups
- Location: `.backup/upgrade-YYYY-MM-DD-HHMM/`

**Manual backups:**
```bash
# Full vault backup
cp -r my-vault/ my-vault-backup-$(date +%Y%m%d)/

# Git-based backup
git tag backup-$(date +%Y%m%d)
git push --tags
```

**Cloud backup (recommended):**
```bash
# 1. Create private GitHub repo
# 2. Add as remote
git remote add origin github.com/you/vault.git

# 3. Push regularly
git push origin main

# Result: Full vault history in cloud
```

## Troubleshooting

### Common Issues

**Issue: Claude Code can't find commands**
```bash
# Solution: Verify .claude/ directory exists
ls .claude/commands/

# Recreate if missing
/init-bootstrap
```

**Issue: MCP servers not working**
```bash
# Solution: Check API keys
echo $GEMINI_API_KEY
echo $FIRECRAWL_API_KEY

# Verify .mcp.json exists
cat .mcp.json

# Restart Claude Code
```

**Issue: Git conflicts after upgrade**
```bash
# Solution: Accept their changes for system files
git checkout --theirs .claude/commands/
git checkout --theirs .scripts/

# Keep your changes for content
git checkout --ours 01_Projects/
git checkout --ours 02_Areas/

git commit
```

**Issue: Vault feels disorganized**
```bash
# Solution: Regular maintenance
/inbox-processor  # Process captures
/weekly-synthesis  # Find patterns

# Move completed projects to archive
mv 01_Projects/Done_Project/ 04_Archive/
```

**Issue: Can't access vault from other computer**
```bash
# Solution: Git sync
# On computer A:
git push

# On computer B:
git pull

# For mobile: Use SSH + Termius
```

For more troubleshooting, see `reference/readme.md` sections:
- "Troubleshooting" (line ~970)
- "Common Issues" throughout

## Best Practices

### From Real Usage

1. **Start in thinking mode**
   - Don't jump to writing immediately
   - Let Claude help you explore first
   - Use `/thinking-partner` liberally

2. **Be a token maximalist**
   - More context = better results
   - Save everything to vault
   - Link notes extensively
   - Let Claude search your full vault

3. **Process inbox regularly**
   - Review 00_Inbox/ at least weekly
   - Move items to proper PARA locations
   - Delete outdated captures

4. **Trust but verify**
   - Always read AI-generated content
   - Claude makes mistakes
   - You're the final authority

5. **Break your flow without fear**
   - AI helps you resume easily
   - Take breaks mid-thought
   - Sessions can span days

6. **Commit frequently**
   - After major insights
   - End of each session
   - Before experiments

7. **Use templates**
   - Create templates in `06_Metadata/Templates/`
   - Standardize project structures
   - Reduce friction for new notes

8. **Link liberally**
   - Use `[[note-name]]` syntax
   - Create maps of content (MOCs)
   - Build knowledge graphs

## Navigation Tips

**Finding information in this skill:**

- **Setup questions** → Quick Reference → Essential Commands
- **Concept questions** → Key Concepts section
- **Workflow questions** → Working with This Skill section
- **Problem solving** → Troubleshooting section
- **Detailed info** → Reference Files (readme.md)
- **Version info** → Reference Files (changelog.md)
- **Contributing** → Reference Files (contributing.md)

**Finding information in reference files:**

- **readme.md** - Comprehensive guide, searchable by topic
- **changelog.md** - Version-based, reverse chronological
- **contributing.md** - Process-focused, development workflow

**Using Claude with this skill:**

```
Good prompts:
- "How do I set up Gemini Vision in Claudesidian?"
- "Explain the PARA method with examples"
- "Walk me through the upgrade process"
- "Help me organize a research project"

Less effective:
- "Tell me about Claudesidian" (too broad)
- "What can this do?" (read Quick Reference first)
```

## Integration with Other Tools

**Obsidian plugins (recommended):**
- Templater - Enhanced templates
- Dataview - Query your notes
- Calendar - Daily notes management
- Excalidraw - Diagrams in notes
- Graph View - Visualize connections

**Git GUI clients (optional):**
- GitKraken - Visual Git interface
- Sourcetree - Free Git GUI
- GitHub Desktop - Simple interface

**Mobile access:**
- Obsidian mobile app + iCloud/Google Drive sync
- SSH via Termius for remote vault access
- Working Copy app for Git on iOS

**API integrations:**
- Zapier → Firecrawl → Inbox automation
- IFTTT → Capture thoughts to Inbox
- Shortcuts (iOS/Mac) → Quick capture

## Philosophy & Principles

### Core Beliefs

**AI amplifies thinking, not just writing:**
Claudesidian treats Claude Code as a thinking partner. The goal is insight, not just information.

**Local files = full control:**
Everything lives in markdown files on your computer. No vendor lock-in, no data hostage.

**Structure enables creativity:**
PARA method provides scaffolding. Within that structure, explore freely.

**Iteration beats perfection:**
Start messy, refine over time. Your vault grows with you.

**The goal is insight:**
Accumulating notes is not the goal. Developing understanding is.

### Design Principles

**Appropriate complexity:**
Claudesidian provides structure without over-engineering. Choose simplicity when multiple solutions exist.

**Progressive disclosure:**
Basic features work immediately. Advanced features available when needed.

**Safe experimentation:**
Git enables risk-free exploration. Try things, roll back if needed.

**Community contribution:**
Best practices emerge from use, not theory. Share what works.

## Resources

**Official links:**
- Repository: https://github.com/heyitsnoah/claudesidian
- Issues: https://github.com/heyitsnoah/claudesidian/issues
- Discussions: https://github.com/heyitsnoah/claudesidian/discussions

**External resources:**
- [Obsidian Documentation](https://help.obsidian.md)
- [PARA Method Guide](https://fortelabs.com/blog/para/)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io)

**Inspiration:**
- [How to Use Claude Code as a Second Brain](https://every.to/podcast/how-to-use-claude-code-as-a-thinking-partner) - Noah Brier interview with Dan Shipper
- Built by [Alephic](https://alephic.com) - AI-first strategy and software partner

## Getting Help

**First steps:**
1. Check this skill's Troubleshooting section
2. Review `reference/readme.md` Troubleshooting
3. Search `reference/changelog.md` for related changes

**Still stuck:**
1. Open issue: https://github.com/heyitsnoah/claudesidian/issues
2. Include:
   - What you're trying to do
   - What happens instead
   - Error messages (if any)
   - Claudesidian version (check changelog)
   - Operating system

**Contributing:**
See `reference/contributing.md` for guidelines on:
- Submitting bug reports
- Suggesting features
- Contributing code
- Improving documentation

---

**Remember:** The bicycle feels wobbly at first, then you forget it was ever hard. Claudesidian works the same way. Start simple, explore gradually, build your second brain over time.
