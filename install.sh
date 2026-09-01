#!/usr/bin/env bash
# =============================================================
# XP Terminal RPG — Installer
# One command. Infinite adventure.
# =============================================================

set -e

XP_HOME="$HOME/.xp"
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
python3 -c "
import sys
sys.path.insert(0, '$XP_HOME')
from engine.rpg import init_database, create_player
init_database()
# Create player if not exists
from engine.rpg import get_player
if get_player() is None:
    name = '${USER:-Coder}'
    create_player(name)
    print(f'  Character created: {name}')
else:
    print('  Character already exists. Keeping your progress.')
" 2>/dev/null || {
    echo -e "${YELLOW}  Warning: Could not initialize database. Check Python 3 is installed.${NC}"
}

# === 4. Install git hooks ===
echo -e "${GREEN}[4/6]${NC} Setting up git hooks..."

# Copy hooks
mkdir -p "$XP_HOME/hooks"
cp -f "$XP_SRC/hooks/post-commit" "$XP_HOME/hooks/"
cp -f "$XP_SRC/hooks/post-merge" "$XP_HOME/hooks/"
chmod +x "$XP_HOME/hooks/post-commit"
chmod +x "$XP_HOME/hooks/post-merge"

# Set up global git hooks directory
if command -v git &> /dev/null; then
    EXISTING_HOOKS=$(git config --global core.hooksPath 2>/dev/null || echo "")
    if [ -z "$EXISTING_HOOKS" ]; then
        git config --global core.hooksPath "$XP_HOME/hooks"
        echo -e "  ${GREEN}Global git hooks installed at ${XP_HOME}/hooks${NC}"
    else
        echo -e "  ${YELLOW}Git hooks path already set to: ${EXISTING_HOOKS}${NC}"
        echo -e "  ${YELLOW}Copy hooks manually:${NC}"
        echo -e "  cp ${XP_HOME}/hooks/post-commit ${EXISTING_HOOKS}/"
        echo -e "  cp ${XP_HOME}/hooks/post-merge ${EXISTING_HOOKS}/"
    fi
else
    echo -e "  ${YELLOW}Warning: git not found. Hooks will be set up when git is available.${NC}"
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
if [ -d "$HOME/.local/bin" ]; then
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
python3 "$XP_HOME/xp" status 2>/dev/null || echo -e "  Run ${CYAN}xp status${NC} to see your character!"

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
