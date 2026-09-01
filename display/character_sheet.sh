#!/usr/bin/env bash
# =============================================================
# XP Terminal RPG — Character Sheet Renderer
# Beautiful ASCII character display.
# =============================================================

CYAN='\033[0;96m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

# Read player data from Python engine
PLAYER_DATA=$(python3 -c "
import sys, json
sys.path.insert(0, '$HOME/.xp')
from engine.rpg import get_player, xp_for_next_level, xp_for_level
p = get_player()
if p:
    level = p['level']
    current_xp = p['xp'] - xp_for_level(level)
    needed = xp_for_next_level(level)
    p['xp_in_level'] = current_xp
    p['xp_needed'] = needed
    # Remove non-serializable
    for key in list(p.keys()):
        if not isinstance(p[key], (str, int, float, list, dict, bool, type(None))):
            del p[key]
    print(json.dumps(p))
" 2>/dev/null)

if [ -z "$PLAYER_DATA" ]; then
    echo -e "${RED}No character found. Run install.sh first.${NC}"
    exit 1
fi

# Parse JSON with Python
python3 -c "
import json, sys

p = json.loads('''$PLAYER_DATA''')

name = p.get('name', 'Coder')
level = p.get('level', 1)
cls = p.get('class', 'unchosen')
hp = p.get('hp', 100)
max_hp = p.get('max_hp', 100)
mp = p.get('mp', 50)
max_mp = p.get('max_mp', 50)
xp_cur = p.get('xp_in_level', 0)
xp_need = p.get('xp_needed', 100)
stats = p.get('stats', {})
equipped = p.get('equipped', [])

def bar(cur, mx, length=25):
    if mx <= 0: return '░' * length
    filled = min(length, int(length * cur / mx))
    return '█' * filled + '░' * (length - filled)

def xp_bar(cur, mx, length=25):
    if mx <= 0: return '░' * length
    filled = min(length, int(length * cur / mx))
    return '▓' * filled + '░' * (length - filled)

class_icons = {'warrior': '⚔️', 'mage': '🔮', 'rogue': '🗡️', 'healer': '💚'}
icon = class_icons.get(cls, '❓')

print()
print('┌─────────────────────────────────────────────────────┐')
print(f'│  {icon}  {name:<20s} Level {level:<3d}              │')
print(f'│  Class: {cls.title():<16s}                         │')
print('├─────────────────────────────────────────────────────┤')
print(f'│  ❤️  HP  [{bar(hp, max_hp)}]  {hp:>3d}/{max_hp:<3d}  │')
print(f'│  💎 MP  [{bar(mp, max_mp)}]  {mp:>3d}/{max_mp:<3d}  │')
print(f'│  ⭐ XP  [{xp_bar(xp_cur, xp_need)}]  {xp_cur}/{xp_need}  │')
print('├─────────────────────────────────────────────────────┤')
print('│  STATS                                              │')
for stat, val in stats.items():
    icons = {'STR': '💪', 'INT': '🧠', 'DEX': '⚡', 'WIS': '📖', 'CHA': '💬'}
    i = icons.get(stat, '•')
    val_bar = '▪' * min(val, 20)
    print(f'│  {i} {stat}: {val:>2d} {val_bar:<20s}          │')
print('├─────────────────────────────────────────────────────┤')
if equipped:
    print('│  EQUIPMENT                                          │')
    for item_id in equipped:
        print(f'│  • {item_id:<30s}            │')
    print('├─────────────────────────────────────────────────────┤')
print('└─────────────────────────────────────────────────────┘')
"
