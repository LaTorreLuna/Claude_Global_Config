#!/bin/bash
# Device Context Detection Utility
# Version: 2.0 (Simplified for Individual Symlinks)
# Purpose: Provides device-independent paths

# ============================================
# Device Detection
# ============================================

# Detect current device
export DEVICE_NAME=$(scutil --get ComputerName 2>/dev/null || hostname)
export DEVICE_ID=$(system_profiler SPHardwareDataType | awk '/Serial Number/ {print $4}')

# ============================================
# Vault Location Detection
# ============================================

find_vault() {
    local vault_name="$1"

    # Strategy 1: Environment variable
    if [ -n "$FUSD_VAULT" ] && [ -d "$FUSD_VAULT" ]; then
        echo "$FUSD_VAULT"
        return 0
    fi

    # Strategy 2: Standard location
    if [ -d "$HOME/Documents/$vault_name" ]; then
        echo "$HOME/Documents/$vault_name"
        return 0
    fi

    # Strategy 3: Google Drive (any account, any device name)
    local gd_path=$(find "$HOME/Library/CloudStorage" -name "$vault_name" -type d 2>/dev/null | head -1)
    if [ -n "$gd_path" ]; then
        echo "$gd_path"
        return 0
    fi

    # Strategy 4: iCloud Drive
    if [ -d "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/$vault_name" ]; then
        echo "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/$vault_name"
        return 0
    fi

    return 1
}

# Export vault paths
export FUSD_VAULT=$(find_vault "FUSD Notes")
export OBSIDIAN_VAULT=$(find_vault "Obsidian Vault")

# ============================================
# Claude Config Paths
# ============================================

export CLAUDE_TOOLS="$HOME/.claude/tools"
export CLAUDE_SKILLS="$HOME/.claude/skills"
export CLAUDE_GLOBAL_CONFIG="$HOME/Claude_Code/Claude_Global_Config"

# ============================================
# Git Global Config Path
# ============================================

export CLAUDE_GLOBAL_GIT="$HOME/Claude_Code/Claude_Global_Config"

# ============================================
# Status Report
# ============================================

if [ "$1" = "--status" ]; then
    echo "Device Context Status:"
    echo "  Device: $DEVICE_NAME ($DEVICE_ID)"
    echo "  FUSD Vault: ${FUSD_VAULT:-NOT FOUND}"
    echo "  Claude Skills: $CLAUDE_SKILLS"
    echo "  Global Config (Git): $CLAUDE_GLOBAL_GIT"
    echo ""
    echo "Skill Counts:"
    echo "  Total skills: $(ls -1 $CLAUDE_SKILLS 2>/dev/null | wc -l)"
    echo "  Global skills (Git): $(ls -la $CLAUDE_SKILLS 2>/dev/null | grep -c " -> $HOME/Claude_Code/Claude_Global_Config")"
    echo "  FUSD skills (Vault): $(ls -la $CLAUDE_SKILLS 2>/dev/null | grep -c "_Claude_Config/skills")"
fi
