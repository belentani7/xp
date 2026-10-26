#!/usr/bin/env bash
# =============================================================
# XP Terminal RPG — Installer
# One command. Infinite adventure.
# =============================================================

set -euo pipefail

XP_PYTHON="${XP_PYTHON:-python3}"
if ! command -v "$XP_PYTHON" >/dev/null 2>&1; then
    echo "Python 3 is required to install XP." >&2
    exit 1
fi

XP_HOME="${XP_HOME:-$HOME/.xp}"
XP_SRC="$(cd "$(dirname "$0")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;96m'
MAGENTA='\033[0;95m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}"
cat << 'EOF'
 ╔═══════════════════════════════════════════════════╗
 ║                                                   ║
 ║   ██╗  ██╗██████╗     INSTALLING...              ║
 ║   ╚██╗██╔╝██╔══██╗                               ║
 ║    ╚███╔╝ ██████╔╝    Terminal Coding RPG         ║
 ║    ██╔██╗ ██╔═══╝                                 ║
 ║   ██╔╝ ██╗██║         v1.0.0                      ║
 ║   ╚═╝  ╚═╝╚═╝                                    ║
 ║                                                   ║
 ╚═══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# === 1. Create ~/.xp directory ===
echo -e "${GREEN}[1/6]${NC} Creating ${XP_HOME}..."
mkdir -p "$XP_HOME"

# === 2. Copy engine files ===
echo -e "${GREEN}[2/6]${NC} Installing RPG engine..."
mkdir -p "$XP_HOME/engine"
cp -f "$XP_SRC"/engine/*.py "$XP_HOME/engine/"
cp -f "$XP_SRC/xp" "$XP_HOME/xp"
chmod +x "$XP_HOME/xp"

# === 3. Copy database schema and initialize ===
echo -e "${GREEN}[3/6]${NC} Initializing character database..."
mkdir -p "$XP_HOME/database"
cp -f "$XP_SRC/database/schema.sql" "$XP_HOME/database/"

# Initialize database via Python
XP_HOME="$XP_HOME" XP_PLAYER_NAME="${USER:-Coder}" "$XP_PYTHON" - <<'PY'
import os
import sys
sys.path.insert(0, os.environ["XP_HOME"])
from engine.rpg import init_database, create_player, get_player

init_database()
if get_player() is None:
    name = os.environ.get("XP_PLAYER_NAME", "Coder")
    create_player(name)
    print(f"  Character created: {name}")
else:
    print("  Character already exists. Keeping your progress.")
PY

# === 4. Install git hooks ===
echo -e "${GREEN}[4/6]${NC} Setting up git hooks..."

# Copy hooks
mkdir -p "$XP_HOME/hooks"
cp -f "$XP_SRC/hooks/post-commit" "$XP_HOME/hooks/"
cp -f "$XP_SRC/hooks/post-merge" "$XP_HOME/hooks/"
chmod +x "$XP_HOME/hooks/post-commit"
chmod +x "$XP_HOME/hooks/post-merge"

# Never change global Git hooks without explicit opt-in: it can disable existing hooks.
if command -v git >/dev/null 2>&1; then
    if [ "${XP_INSTALL_GLOBAL_HOOKS:-0}" = "1" ]; then
        EXISTING_HOOKS="$(git config --global --get core.hooksPath 2>/dev/null || true)"
        if [ -z "$EXISTING_HOOKS" ]; then
            git config --global core.hooksPath "$XP_HOME/hooks"
            echo -e "  ${GREEN}Global XP hooks enabled.${NC}"
        elif [ "$EXISTING_HOOKS" = "$XP_HOME/hooks" ]; then
            echo -e "  ${GREEN}XP hooks are already configured.${NC}"
        else
            echo -e "  ${YELLOW}Existing global Git hooks preserved: $EXISTING_HOOKS${NC}"
            echo "  XP hooks were not activated."
        fi
    else
        echo "  Git hooks installed locally, not activated globally."
        echo "  Opt in: XP_INSTALL_GLOBAL_HOOKS=1 bash install.sh"
        echo "  Or install hooks in one selected repository."
    fi
else
    echo -e "  ${YELLOW}Git not found; hooks copied for later use.${NC}"
fi

# === 5. Copy display scripts and config ===
echo -e "${GREEN}[5/6]${NC} Installing display scripts and config..."
mkdir -p "$XP_HOME/display" "$XP_HOME/config" "$XP_HOME/ascii"
[ -d "$XP_SRC/display" ] && cp -f "$XP_SRC"/display/*.sh "$XP_HOME/display/" 2>/dev/null && chmod +x "$XP_HOME/display/"*.sh 2>/dev/null || true
[ -d "$XP_SRC/config" ] && cp -f "$XP_SRC/config/default.yaml" "$XP_HOME/config/" 2>/dev/null || true
[ -d "$XP_SRC/ascii" ] && cp -f "$XP_SRC"/ascii/*.txt "$XP_HOME/ascii/" 2>/dev/null || true

# === 6. Add to PATH ===
echo -e "${GREEN}[6/6]${NC} Adding xp to PATH..."

# Create symlink in /usr/local/bin or ~/.local/bin
if [ -n "${XP_BIN_DIR:-}" ]; then
    mkdir -p "$XP_BIN_DIR"
    ln -sf "$XP_HOME/xp" "$XP_BIN_DIR/xp"
    echo "  Linked to $XP_BIN_DIR/xp"
elif [ -d "$HOME/.local/bin" ]; then
    ln -sf "$XP_HOME/xp" "$HOME/.local/bin/xp" 2>/dev/null || true
    echo -e "  Linked to ~/.local/bin/xp"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    ln -sf "$XP_HOME/xp" "/usr/local/bin/xp" 2>/dev/null || true
    echo -e "  Linked to /usr/local/bin/xp"
else
    mkdir -p "$HOME/.local/bin"
    ln -sf "$XP_HOME/xp" "$HOME/.local/bin/xp" 2>/dev/null || true
    echo -e "  Linked to ~/.local/bin/xp"
    echo -e "  ${YELLOW}Add ~/.local/bin to your PATH if not already:${NC}"
    echo -e "  ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi

# === Done! ===
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✨ XP TERMINAL RPG INSTALLED! ✨${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""

# Print character sheet
XP_HOME="$XP_HOME" "$XP_PYTHON" "$XP_HOME/xp" status 2>/dev/null || echo -e "  Run ${CYAN}xp status${NC} to see your character!"

echo ""
echo -e "${BOLD}NEXT STEPS:${NC}"
echo -e "  1. Choose your class:  ${CYAN}xp class${NC}"
echo -e "  2. Equip your weapon:  ${CYAN}xp equip vim${NC}"
echo -e "  3. Start coding!       Every commit earns XP"
echo -e "  4. Check progress:     ${CYAN}xp status${NC}"
echo ""
echo -e "${MAGENTA}  The system remembers. The system grows.${NC}"
echo -e "${MAGENTA}  Do not reach level 99.${NC}"
echo ""
