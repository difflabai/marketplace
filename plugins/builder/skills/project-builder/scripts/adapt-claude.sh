#!/usr/bin/env bash
#
# adapt-claude.sh — Create symlinks from .project/ to Claude Code locations
#
# Maps the .project standard directory structure to where Claude Code
# expects its configuration files. Uses relative symlinks so the repo
# stays portable across machines.
#
# Usage:
#   ./project-standard/scripts/adapt-claude.sh [project-root]   # default: repo root
#   ./project-standard/scripts/adapt-claude.sh --clean [root]    # remove created symlinks
#
# Mappings (from Appendix B.1 of the .project spec):
#
#   {.project,.aiproject}/instructions/index.md    -> CLAUDE.md
#   {.project,.aiproject}/instructions/<topic>.md  -> .claude/rules/<topic>.md
#   {.project,.aiproject}/agents/<agent>.md        -> .claude/agents/<agent>.md
#   {.project,.aiproject}/skills/<name>/index.md   -> .claude/skills/<name>/SKILL.md
#
# Supported platforms: macOS, Linux, WSL, Windows (Git Bash / MSYS2)
#

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

CLEAN=false
if [[ "${1:-}" == "--clean" ]]; then
    CLEAN=true
    shift
fi

PROJECT_ROOT="$(cd "${1:-$SCRIPT_DIR/../..}" && pwd)"

# ---------------------------------------------------------------------------
# Discover .project or .aiproject (or scaffold)
# ---------------------------------------------------------------------------

if [[ -d "$PROJECT_ROOT/.project" && -f "$PROJECT_ROOT/.project/PROJECT.md" ]]; then
    DOT_PROJECT_DIR=".project"
elif [[ -d "$PROJECT_ROOT/.aiproject" && -f "$PROJECT_ROOT/.aiproject/PROJECT.md" ]]; then
    DOT_PROJECT_DIR=".aiproject"
elif ! $CLEAN; then
    DOT_PROJECT_DIR=".project"
    echo "No .project/ or .aiproject/ found. Creating .project/ scaffold..."
    mkdir -p "$PROJECT_ROOT/.project/instructions"
    cat > "$PROJECT_ROOT/.project/PROJECT.md" << 'MANIFEST'
---
spec: "1.0"
name: ""
description: ""
---

# Project

Add project overview and getting started instructions here.
MANIFEST
    cat > "$PROJECT_ROOT/.project/instructions/index.md" << 'INSTRUCTIONS'
---
name: base
description: Base project instructions, always loaded.
activation: always
---

# Instructions

Add project coding standards and conventions here.
INSTRUCTIONS
    echo "  CREATED: .project/PROJECT.md"
    echo "  CREATED: .project/instructions/index.md"
else
    echo "Error: no .project/ or .aiproject/ directory found at $PROJECT_ROOT" >&2
    exit 1
fi

DOT_PROJECT="$PROJECT_ROOT/$DOT_PROJECT_DIR"

# ---------------------------------------------------------------------------
# OS detection
# ---------------------------------------------------------------------------

OS="$(uname -s)"

symlink() {
    local target="$1" # relative path from link location to real file
    local link="$2"   # path where the symlink is created

    if $CLEAN; then
        if [[ -L "$link" ]]; then
            rm "$link"
            echo "  REMOVED: $link"
        fi
        return
    fi

    # Never overwrite a real (non-symlink) file
    if [[ -e "$link" && ! -L "$link" ]]; then
        echo "  SKIP: $link exists and is not a symlink" >&2
        return
    fi

    mkdir -p "$(dirname "$link")"

    case "$OS" in
        MINGW*|MSYS*|CYGWIN*)
            # Windows: try cmd mklink first, fall back to ln -s
            local win_target win_link
            win_target="$(cygpath -w "$PROJECT_ROOT/$target" 2>/dev/null || echo "$target")"
            win_link="$(cygpath -w "$link" 2>/dev/null || echo "$link")"
            rm -f "$link" 2>/dev/null || true
            if ! cmd //c mklink "$win_link" "$win_target" >/dev/null 2>&1; then
                if ! ln -sf "$target" "$link" 2>/dev/null; then
                    echo "  FAIL: $link (enable Developer Mode or run as admin)" >&2
                    return 1
                fi
            fi
            ;;
        *)
            ln -sf "$target" "$link"
            ;;
    esac

    echo "  LINK: $link -> $target"
}

# ---------------------------------------------------------------------------
# 1. instructions/index.md -> CLAUDE.md
# ---------------------------------------------------------------------------

INSTRUCTIONS_DIR="$DOT_PROJECT/instructions"
if [[ -f "$INSTRUCTIONS_DIR/index.md" ]] || $CLEAN; then
    symlink "$DOT_PROJECT_DIR/instructions/index.md" "$PROJECT_ROOT/CLAUDE.md"
fi

# ---------------------------------------------------------------------------
# 2. instructions/<topic>.md -> .claude/rules/<topic>.md
#    (skip index.md and local.md)
# ---------------------------------------------------------------------------

if $CLEAN; then
    for link in "$PROJECT_ROOT/.claude/rules"/*.md; do
        [[ -L "$link" ]] || continue
        symlink "" "$link"
    done
elif [[ -d "$INSTRUCTIONS_DIR" ]]; then
    for file in "$INSTRUCTIONS_DIR"/*.md; do
        [[ -f "$file" ]] || continue
        base="$(basename "$file")"
        [[ "$base" == "index.md" || "$base" == "local.md" ]] && continue
        symlink "../../$DOT_PROJECT_DIR/instructions/$base" "$PROJECT_ROOT/.claude/rules/$base"
    done
fi

# ---------------------------------------------------------------------------
# 3. agents/<agent>.md -> .claude/agents/<agent>.md
#    (skip index.md)
# ---------------------------------------------------------------------------

AGENTS_DIR="$DOT_PROJECT/agents"
if $CLEAN; then
    for link in "$PROJECT_ROOT/.claude/agents"/*.md; do
        [[ -L "$link" ]] || continue
        symlink "" "$link"
    done
elif [[ -d "$AGENTS_DIR" ]]; then
    for file in "$AGENTS_DIR"/*.md; do
        [[ -f "$file" ]] || continue
        base="$(basename "$file")"
        [[ "$base" == "index.md" ]] && continue
        symlink "../../$DOT_PROJECT_DIR/agents/$base" "$PROJECT_ROOT/.claude/agents/$base"
    done
fi

# ---------------------------------------------------------------------------
# 4. skills/<name>/index.md -> .claude/skills/<name>/SKILL.md
# ---------------------------------------------------------------------------

SKILLS_DIR="$DOT_PROJECT/skills"
if $CLEAN; then
    if [[ -d "$PROJECT_ROOT/.claude/skills" ]]; then
        for sdir in "$PROJECT_ROOT/.claude/skills"/*/; do
            [[ -d "$sdir" ]] || continue
            [[ -L "$sdir/SKILL.md" ]] || continue
            symlink "" "$sdir/SKILL.md"
        done
    fi
elif [[ -d "$SKILLS_DIR" ]]; then
    for skill_dir in "$SKILLS_DIR"/*/; do
        [[ -d "$skill_dir" ]] || continue
        [[ -f "$skill_dir/index.md" ]] || continue
        name="$(basename "$skill_dir")"
        symlink "../../../$DOT_PROJECT_DIR/skills/$name/index.md" "$PROJECT_ROOT/.claude/skills/$name/SKILL.md"
    done
fi

# ---------------------------------------------------------------------------
# Clean up empty directories on --clean
# ---------------------------------------------------------------------------

if $CLEAN; then
    # Remove skill subdirectories first (they nest deeper)
    if [[ -d "$PROJECT_ROOT/.claude/skills" ]]; then
        for sdir in "$PROJECT_ROOT/.claude/skills"/*/; do
            [[ -d "$sdir" ]] || continue
            if [[ -z "$(ls -A "$sdir" 2>/dev/null)" ]]; then
                rmdir "$sdir" 2>/dev/null || true
            fi
        done
    fi
    # Then remove top-level .claude subdirectories
    for dir in "$PROJECT_ROOT/.claude/rules" \
               "$PROJECT_ROOT/.claude/agents" \
               "$PROJECT_ROOT/.claude/skills"; do
        if [[ -d "$dir" ]] && [[ -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
            rmdir "$dir" 2>/dev/null || true
        fi
    done
    # Remove .claude/ itself if empty
    if [[ -d "$PROJECT_ROOT/.claude" ]] && [[ -z "$(ls -A "$PROJECT_ROOT/.claude" 2>/dev/null)" ]]; then
        rmdir "$PROJECT_ROOT/.claude" 2>/dev/null || true
    fi
    echo "Done. Symlinks removed."
else
    echo "Done. Claude Code symlinks created."
fi
