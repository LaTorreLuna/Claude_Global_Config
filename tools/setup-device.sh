#!/bin/bash
# New Device Setup Script
# Version: 2.0 (Individual Symlinks)

set -e

echo "==================================="
echo "Claude Global Config Device Setup"
echo "Version: 2.0 (Individual Symlinks)"
echo "==================================="
echo ""

# 1. Clone Git repo if not exists
if [ ! -d ~/Claude_Global_Config ]; then
    echo "📥 Cloning Claude_Global_Config from GitHub..."
    gh repo clone LaTorreLuna/Claude_Global_Config ~/Claude_Global_Config
else
    echo "✅ Claude_Global_Config already exists"
    cd ~/Claude_Global_Config && git pull
fi

# 2. Create ~/.claude/skills/ directory
echo "📁 Creating ~/.claude/skills/ directory..."
mkdir -p ~/.claude/skills

# 3. Create symlinks for each global skill
echo "🔗 Creating individual symlinks for global skills..."
cd ~/.claude/skills/

# List of global skills (24 total)
GLOBAL_SKILLS=(
    "advanced-sql-skill"
    "article-extractor"
    "claudesidian"
    "csv-data-summarizer-claude-skill"
    "file-organizer"
    "meeting-insights-analyzer"
    "notebook-navigator"
    "word-diagram-formatter"
    "youtube-transcript"
    "obsidian-core"
    "obsidian-databases"
    "obsidian-help-router"
    "obsidian-iconize"
    "obsidian-import"
    "obsidian-plugins"
    "obsidian-properties"
    "obsidian-publish"
    "obsidian-sync"
    "obsidian-teams"
    "obsidian-web-clipper"
    "tag-taxonomy-migration"
    "taxonomy-design-workflow"
    "taxonomy-validation"
    "templater-obsidian"
)

for skill in "${GLOBAL_SKILLS[@]}"; do
    if [ ! -L "$skill" ]; then
        ln -s ~/Claude_Global_Config/skills/"$skill" "$skill"
        echo "  ✅ $skill"
    else
        echo "  ⏭️  $skill (already exists)"
    fi
done

echo ""
echo "📊 Global skills setup: $(ls -la | grep -c " -> $HOME/Claude_Global_Config") of 24"

# 4. Setup FUSD skills (Mac only - requires vault access)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "🔍 Detecting FUSD vault..."

    # Source device-context to get FUSD_VAULT
    source ~/Claude_Global_Config/tools/device-context.sh 2>/dev/null || true

    if [ -n "$FUSD_VAULT" ] && [ -d "$FUSD_VAULT" ]; then
        echo "✅ FUSD vault found: $FUSD_VAULT"
        echo "🔗 Creating symlinks for FUSD skills..."

        FUSD_SKILLS=(
            "fusd-document-taxonomy"
            "ghr-qualifications-configuration"
            "infor-isd-reports-skill"
            "lawson-lpl-generator-skill"
        )

        for skill in "${FUSD_SKILLS[@]}"; do
            if [ ! -L "$skill" ]; then
                ln -s "$FUSD_VAULT/_Claude_Config/skills/$skill" "$skill"
                echo "  ✅ $skill"
            else
                echo "  ⏭️  $skill (already exists)"
            fi
        done

        echo ""
        echo "📊 FUSD skills setup: $(ls -la | grep -c "_Claude_Config/skills") of 4"
    else
        echo "⚠️  FUSD vault not found (expected on Mac with Google Drive)"
        echo "  FUSD-specific skills will not be available on this device"
    fi
else
    echo ""
    echo "ℹ️  Windows detected - FUSD skills not available (Mac/Google Drive only)"
fi

# 5. Setup shell integration
echo ""
echo "🔧 Setting up shell integration..."
if ! grep -q "device-context.sh" ~/.zshrc 2>/dev/null && ! grep -q "device-context.sh" ~/.bashrc 2>/dev/null; then
    echo "# Claude Code device context" >> ~/.zshrc
    echo "source ~/Claude_Global_Config/tools/device-context.sh" >> ~/.zshrc
    echo "✅ Added to ~/.zshrc"
else
    echo "✅ Already configured in shell"
fi

# 6. Summary
echo ""
echo "==================================="
echo "✅ Setup Complete!"
echo "==================================="
echo ""
echo "Total skills: $(ls -1 ~/.claude/skills/ | wc -l)"
echo "  Global (Git): $(ls -la ~/.claude/skills/ | grep -c " -> $HOME/Claude_Global_Config")"
if [[ "$OSTYPE" == "darwin"* ]] && [ -n "$FUSD_VAULT" ]; then
    echo "  FUSD (Vault): $(ls -la ~/.claude/skills/ | grep -c "_Claude_Config/skills")"
fi
echo ""
echo "Next steps:"
echo "  1. Restart your terminal"
echo "  2. Test: ls ~/.claude/skills/"
echo "  3. Claude Code will auto-discover all skills"
