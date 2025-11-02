#!/bin/bash
# Quick Navigation Script
# Use: ./QUICK_NAV.sh [number]

case "$1" in
    1)
        echo "Opening: New Device Setup (README.md)"
        open ~/Claude_Global_Config/README.md || cat ~/Claude_Global_Config/README.md
        ;;
    2)
        echo "Opening: What Happened? (MIGRATION_COMPLETE.md)"
        open ~/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_COMPLETE.md || cat ~/Documents/Claude_Multi_Device_Migration_Project/MIGRATION_COMPLETE.md
        ;;
    3)
        echo "Opening: Why Flat Structure? (Research)"
        open ~/Documents/Synthesis/claude-code-research/02-skills-subdirectory-support-analysis.md || cat ~/Documents/Synthesis/claude-code-research/02-skills-subdirectory-support-analysis.md
        ;;
    4)
        echo "Opening: Windows Setup"
        open ~/Claude_Global_Config/WINDOWS_SETUP.md || cat ~/Claude_Global_Config/WINDOWS_SETUP.md
        ;;
    5)
        echo "Opening: Full Documentation Map"
        open ~/Claude_Global_Config/DOCUMENTATION_MAP.md || cat ~/Claude_Global_Config/DOCUMENTATION_MAP.md
        ;;
    *)
        echo "Quick Navigation Menu:"
        echo ""
        echo "1. New Device Setup (README.md)"
        echo "2. What Happened? (MIGRATION_COMPLETE.md) ← You want this"
        echo "3. Why Flat Structure? (Technical Research)"
        echo "4. Windows Setup Guide"
        echo "5. Full Documentation Map"
        echo ""
        echo "Usage: ./QUICK_NAV.sh [number]"
        echo "Example: ./QUICK_NAV.sh 2"
        ;;
esac
