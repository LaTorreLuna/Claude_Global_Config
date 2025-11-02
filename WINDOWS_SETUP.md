# Windows Setup Guide

## Prerequisites

- Git for Windows installed
- GitHub CLI (gh) installed
- Claude Code installed

## Setup Steps

### 1. Clone Git Repo

```powershell
gh repo clone LaTorreLuna/Claude_Global_Config "$env:USERPROFILE\Claude_Global_Config"
```

### 2. Create Skills Directory

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
```

### 3. Create Individual Symlinks for Global Skills

```powershell
# Navigate to skills directory
cd "$env:USERPROFILE\.claude\skills"

# Create junction (Windows symlink) for each global skill (24 total)

cmd /c mklink /J advanced-sql-skill "$env:USERPROFILE\Claude_Global_Config\skills\advanced-sql-skill"
cmd /c mklink /J article-extractor "$env:USERPROFILE\Claude_Global_Config\skills\article-extractor"
cmd /c mklink /J claudesidian "$env:USERPROFILE\Claude_Global_Config\skills\claudesidian"
cmd /c mklink /J csv-data-summarizer-claude-skill "$env:USERPROFILE\Claude_Global_Config\skills\csv-data-summarizer-claude-skill"
cmd /c mklink /J file-organizer "$env:USERPROFILE\Claude_Global_Config\skills\file-organizer"
cmd /c mklink /J meeting-insights-analyzer "$env:USERPROFILE\Claude_Global_Config\skills\meeting-insights-analyzer"
cmd /c mklink /J notebook-navigator "$env:USERPROFILE\Claude_Global_Config\skills\notebook-navigator"
cmd /c mklink /J word-diagram-formatter "$env:USERPROFILE\Claude_Global_Config\skills\word-diagram-formatter"
cmd /c mklink /J youtube-transcript "$env:USERPROFILE\Claude_Global_Config\skills\youtube-transcript"

# Obsidian skills (10 total)
cmd /c mklink /J obsidian-core "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-core"
cmd /c mklink /J obsidian-databases "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-databases"
cmd /c mklink /J obsidian-help-router "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-help-router"
cmd /c mklink /J obsidian-iconize "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-iconize"
cmd /c mklink /J obsidian-import "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-import"
cmd /c mklink /J obsidian-plugins "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-plugins"
cmd /c mklink /J obsidian-properties "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-properties"
cmd /c mklink /J obsidian-publish "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-publish"
cmd /c mklink /J obsidian-sync "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-sync"
cmd /c mklink /J obsidian-teams "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-teams"
cmd /c mklink /J obsidian-web-clipper "$env:USERPROFILE\Claude_Global_Config\skills\obsidian-web-clipper"

# Taxonomy skills (3 total)
cmd /c mklink /J tag-taxonomy-migration "$env:USERPROFILE\Claude_Global_Config\skills\tag-taxonomy-migration"
cmd /c mklink /J taxonomy-design-workflow "$env:USERPROFILE\Claude_Global_Config\skills\taxonomy-design-workflow"
cmd /c mklink /J taxonomy-validation "$env:USERPROFILE\Claude_Global_Config\skills\taxonomy-validation"

# Templater
cmd /c mklink /J templater-obsidian "$env:USERPROFILE\Claude_Global_Config\skills\templater-obsidian"
```

### 4. Verify

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\skills"
# Should show 24 junctions pointing to Claude_Global_Config
```

### 5. Count Skills

```powershell
(Get-ChildItem "$env:USERPROFILE\.claude\skills" | Measure-Object).Count
# Should show: 24
```

## What Works on Windows

✅ **Global skills (24)** - Git-synced, cross-platform
❌ **FUSD skills (4)** - Mac/Google Drive only (not available on Windows)

## Automated Setup Script (PowerShell)

For easier setup, create `setup-windows.ps1`:

```powershell
# Windows Setup Script for Claude Global Config
# Version: 2.0 (Individual Symlinks)

Write-Host "====================================="
Write-Host "Claude Global Config - Windows Setup"
Write-Host "Version: 2.0 (Individual Symlinks)"
Write-Host "====================================="
Write-Host ""

# 1. Clone Git repo if not exists
if (!(Test-Path "$env:USERPROFILE\Claude_Global_Config")) {
    Write-Host "📥 Cloning Claude_Global_Config from GitHub..."
    gh repo clone LaTorreLuna/Claude_Global_Config "$env:USERPROFILE\Claude_Global_Config"
} else {
    Write-Host "✅ Claude_Global_Config already exists"
    cd "$env:USERPROFILE\Claude_Global_Config"
    git pull
}

# 2. Create skills directory
Write-Host "📁 Creating skills directory..."
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null

# 3. Create junctions for each global skill
Write-Host "🔗 Creating junctions for global skills..."
cd "$env:USERPROFILE\.claude\skills"

$globalSkills = @(
    "advanced-sql-skill",
    "article-extractor",
    "claudesidian",
    "csv-data-summarizer-claude-skill",
    "file-organizer",
    "meeting-insights-analyzer",
    "notebook-navigator",
    "word-diagram-formatter",
    "youtube-transcript",
    "obsidian-core",
    "obsidian-databases",
    "obsidian-help-router",
    "obsidian-iconize",
    "obsidian-import",
    "obsidian-plugins",
    "obsidian-properties",
    "obsidian-publish",
    "obsidian-sync",
    "obsidian-teams",
    "obsidian-web-clipper",
    "tag-taxonomy-migration",
    "taxonomy-design-workflow",
    "taxonomy-validation",
    "templater-obsidian"
)

foreach ($skill in $globalSkills) {
    if (!(Test-Path $skill)) {
        cmd /c mklink /J $skill "$env:USERPROFILE\Claude_Global_Config\skills\$skill" | Out-Null
        Write-Host "  ✅ $skill"
    } else {
        Write-Host "  ⏭️  $skill (already exists)"
    }
}

# 4. Summary
Write-Host ""
Write-Host "====================================="
Write-Host "✅ Setup Complete!"
Write-Host "====================================="
Write-Host ""
Write-Host "Total skills: $((Get-ChildItem "$env:USERPROFILE\.claude\skills" | Measure-Object).Count)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Restart Claude Code"
Write-Host "  2. Test: dir `$env:USERPROFILE\.claude\skills"
Write-Host "  3. Claude Code will auto-discover all 24 global skills"
```

Save this as `setup-windows.ps1` in the Git repo's `tools/` directory, then run:

```powershell
cd $env:USERPROFILE\Claude_Global_Config\tools
.\setup-windows.ps1
```

## Troubleshooting

### Junctions vs Symlinks

Windows has two types of links:
- **Symlinks** (require admin privileges)
- **Junctions** (no admin required, recommended)

This guide uses junctions (`mklink /J`) which work without admin privileges.

### Permission Denied

If you get permission errors, run PowerShell as Administrator for the initial setup.

### Git Line Endings

Ensure Git is configured for cross-platform line endings:

```powershell
git config --global core.autocrlf true
```

## Limitations

- **FUSD skills unavailable**: The 4 FUSD-specific skills are Mac-only (Google Drive vault sync)
- **Mac/Windows differences**: Some scripts might need path adjustments for cross-platform compatibility

## Support

For issues or questions, see the main repository README or create an issue on GitHub.
