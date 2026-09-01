#!/usr/bin/env bash
# =============================================================
# XP Terminal RPG — Level Up Animation
# Celebrate when you level up!
# =============================================================

LEVEL=${1:-2}

CYAN='\033[0;96m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;95m'
BOLD='\033[1m'
NC='\033[0m'

# Sound effect (optional)
play_sound() {
    if command -v aplay &> /dev/null; then
        # Linux: beep
        echo -ne '\007' 2>/dev/null
    elif command -v afplay &> /dev/null; then
        # macOS: system sound
        afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &
    fi
}

# Animation frames
echo ""
echo -e "${YELLOW}"
sleep 0.1

echo "  ╔══════════════════════════════════════════════╗"
sleep 0.1
echo "  ║                                              ║"
sleep 0.1
echo -e "  ║    ${MAGENTA}✦${YELLOW}                              ${MAGENTA}✦${YELLOW}       ║"
sleep 0.1
echo -e "  ║          ${MAGENTA}★${YELLOW}                    ${MAGENTA}★${YELLOW}             ║"
sleep 0.2
echo -e "  ║               ${GREEN}╔════════════╗${YELLOW}               ║"
sleep 0.2
echo -e "  ║    ${MAGENTA}✦${YELLOW}        ${GREEN}║  ${BOLD}${YELLOW}LEVEL UP!${GREEN}  ║${YELLOW}      ${MAGENTA}✦${YELLOW}       ║"
sleep 0.3
echo -e "  ║               ${GREEN}║  ${BOLD}${YELLOW}Level ${LEVEL}${GREEN}   ║${YELLOW}               ║"
sleep 0.2
echo -e "  ║          ${MAGENTA}★${YELLOW}    ${GREEN}╚════════════╝${YELLOW}    ${MAGENTA}★${YELLOW}             ║"
sleep 0.1
echo -e "  ║    ${MAGENTA}✦${YELLOW}                              ${MAGENTA}✦${YELLOW}       ║"
sleep 0.1
echo "  ║                                              ║"
sleep 0.1
echo "  ╚══════════════════════════════════════════════╝"

echo -e "${NC}"

# Play sound
play_sound

# Stat increases
echo -e "  ${GREEN}${BOLD}Stat Increases:${NC}"
echo -e "  ${GREEN}  +2 Primary Stat${NC}"
echo -e "  ${GREEN}  +1 Secondary Stat${NC}"
echo -e "  ${GREEN}  +10 Max HP${NC}"
echo -e "  ${GREEN}  +5 Max MP${NC}"
echo ""

# Class-specific message
CLASS=$(python3 -c "
import sys
sys.path.insert(0, '$HOME/.xp')
from engine.rpg import get_player
p = get_player()
if p and p.get('class'):
    print(p['class'])
" 2>/dev/null)

case "$CLASS" in
    warrior)
        echo -e "  ${YELLOW}⚔️  The Warrior grows stronger. Bugs tremble.${NC}"
        ;;
    mage)
        echo -e "  ${MAGENTA}🔮 The Mage's knowledge deepens. New patterns emerge.${NC}"
        ;;
    rogue)
        echo -e "  ${GREEN}🗡️  The Rogue sharpens their speed. Nothing is safe.${NC}"
        ;;
    healer)
        echo -e "  ${CYAN}💚 The Healer's wisdom expands. The team benefits.${NC}"
        ;;
    *)
        echo -e "  ${DIM}Choose a class with 'xp class' to unlock unique abilities.${NC}"
        ;;
esac

echo ""
echo -e "  ${DIM}The system remembers your growth.${NC}"
echo ""
