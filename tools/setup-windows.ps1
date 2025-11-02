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
