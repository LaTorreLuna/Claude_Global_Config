#!/bin/bash
# Bidirectional Skills Sync Tool
# Automatically syncs skills between local device and Git repo

set -e

REPO_PATH="$HOME/Claude_Code/Claude_Global_Config"
SKILLS_DIR="$HOME/.claude/skills"
REPO_SKILLS="$REPO_PATH/skills"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================"
echo "Claude Skills Bidirectional Sync Tool"
echo "========================================"
echo ""

# ============================================
# STEP 1: Check for remote updates (pull)
# ============================================

echo "🔍 Checking for new skills from other devices..."
cd "$REPO_PATH"

# Fetch latest from remote
git fetch origin main >/dev/null 2>&1

# Check if remote has changes
BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")

if [ "$BEHIND" -gt 0 ]; then
    echo -e "${YELLOW}📥 Remote has $BEHIND new commit(s)${NC}"
    echo ""

    # Show what skills are new/changed
    NEW_SKILLS=$(git diff HEAD origin/main --name-only | grep "^skills/" | cut -d'/' -f2 | sort -u)

    if [ -n "$NEW_SKILLS" ]; then
        echo "New/updated skills available:"
        echo "$NEW_SKILLS" | sed 's/^/  - /'
        echo ""

        read -p "Pull these changes and create symlinks? [Y/n] " -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            git pull origin main

            # Create symlinks for new skills
            cd "$SKILLS_DIR"
            for skill in $NEW_SKILLS; do
                if [ ! -e "$skill" ] && [ -d "$REPO_SKILLS/$skill" ]; then
                    ln -s "$REPO_SKILLS/$skill" "$skill"
                    echo -e "${GREEN}✅ Symlinked: $skill${NC}"
                fi
            done

            echo ""
            echo -e "${GREEN}✅ Pulled and synced new skills${NC}"
        else
            echo "⏭️  Skipped pull"
        fi
    else
        echo "ℹ️  Changes don't include skill updates"
        read -p "Pull anyway? [y/N] " -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git pull origin main
        fi
    fi
    echo ""
else
    echo "✅ Already up to date with remote"
    echo ""
fi

# ============================================
# STEP 2: Detect local skills (push)
# ============================================

echo "🔍 Scanning for local skills not in Git repo..."
cd "$SKILLS_DIR"

# Find all directories that are NOT symlinks (real local directories)
LOCAL_SKILLS=()
while IFS= read -r item; do
    if [ -d "$item" ] && [ ! -L "$item" ]; then
        # Also exclude if already exists in repo
        if [ ! -d "$REPO_SKILLS/$item" ]; then
            LOCAL_SKILLS+=("$item")
        fi
    fi
done < <(ls -1)

if [ ${#LOCAL_SKILLS[@]} -eq 0 ]; then
    echo "✅ No new local skills found"
    echo ""
    echo "All skills are either:"
    echo "  - Symlinked to Git repo (global)"
    echo "  - Symlinked to vault (FUSD-specific)"
    echo "  - Already in Git repo"
    echo ""
    exit 0
fi

echo -e "${YELLOW}📋 Found ${#LOCAL_SKILLS[@]} local skill(s) not in Git:${NC}"
for skill in "${LOCAL_SKILLS[@]}"; do
    echo "  - $skill"
done
echo ""

# ============================================
# STEP 3: Classify each local skill
# ============================================

SKILLS_TO_SYNC=()

for skill in "${LOCAL_SKILLS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}📦 Skill: $skill${NC}"
    echo ""

    # Show skill info if SKILL.md exists
    if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
        echo "Description:"
        head -20 "$SKILLS_DIR/$skill/SKILL.md" | grep -E "^(name:|description:)" || echo "  (no description found)"
        echo ""
    fi

    echo "Classify this skill:"
    echo "  [G] Global - Add to Git repo and sync to all devices"
    echo "  [P] Project - Keep local only (project-specific)"
    echo "  [F] FUSD - Move to FUSD vault (Mac/work-specific)"
    echo "  [S] Skip - Don't process this skill now"
    echo ""

    read -p "Choice [G/p/f/s]: " -r
    echo ""

    case "${REPLY,,}" in
        g|"")
            echo -e "${GREEN}✅ Will add to Git repo${NC}"
            SKILLS_TO_SYNC+=("$skill")
            ;;
        p)
            echo "⏭️  Keeping as project-specific (no action)"
            ;;
        f)
            echo -e "${YELLOW}⚠️  FUSD vault migration not yet implemented${NC}"
            echo "   Manually move to: ~/Documents/FUSD Notes/_Claude_Config/skills/"
            ;;
        s)
            echo "⏭️  Skipped"
            ;;
        *)
            echo -e "${RED}Invalid choice, skipping${NC}"
            ;;
    esac
    echo ""
done

# ============================================
# STEP 4: Sync selected skills to Git
# ============================================

if [ ${#SKILLS_TO_SYNC[@]} -eq 0 ]; then
    echo "No skills selected for sync"
    exit 0
fi

echo "========================================"
echo "📤 Syncing ${#SKILLS_TO_SYNC[@]} skill(s) to Git"
echo "========================================"
echo ""

for skill in "${SKILLS_TO_SYNC[@]}"; do
    echo "Processing: $skill"

    # 1. Copy to Git repo
    echo "  📁 Copying to Git repo..."
    cp -r "$SKILLS_DIR/$skill" "$REPO_SKILLS/"

    # 2. Replace local with symlink
    echo "  🔗 Replacing with symlink..."
    rm -rf "$SKILLS_DIR/$skill"
    ln -s "$REPO_SKILLS/$skill" "$SKILLS_DIR/$skill"

    echo -e "  ${GREEN}✅ Converted to symlink${NC}"
    echo ""
done

# ============================================
# STEP 5: Commit and push to Git
# ============================================

cd "$REPO_PATH"

# Stage new skills
for skill in "${SKILLS_TO_SYNC[@]}"; do
    git add "skills/$skill"
done

# Create commit message
if [ ${#SKILLS_TO_SYNC[@]} -eq 1 ]; then
    COMMIT_MSG="Add global skill: ${SKILLS_TO_SYNC[0]}"
else
    COMMIT_MSG="Add ${#SKILLS_TO_SYNC[@]} global skills

Skills added:
$(printf '  - %s\n' "${SKILLS_TO_SYNC[@]}")"
fi

COMMIT_MSG="$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit
echo "📝 Creating commit..."
git commit -m "$COMMIT_MSG"

# Push
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "========================================"
echo -e "${GREEN}✅ Sync Complete!${NC}"
echo "========================================"
echo ""
echo "Skills synced to Git:"
for skill in "${SKILLS_TO_SYNC[@]}"; do
    echo "  ✅ $skill"
done
echo ""
echo "These skills will now be available on all devices."
echo "On other devices, run:"
echo "  cd ~/Claude_Code/Claude_Global_Config"
echo "  git pull"
echo "  ./tools/setup-device.sh"
