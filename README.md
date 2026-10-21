# ⚔️ XP — Terminal Coding RPG

**Turn every coding session into an adventure.**

Every git commit earns XP. Every bug fix defeats an enemy. Every PR merged wins a boss fight.
Level up your character, unlock achievements, build streaks, and discover hidden lore.

```
 ╔═══════════════════════════════════════════════╗
 ║   ██╗  ██╗██████╗                            ║
 ║   ╚██╗██╔╝██╔══██╗   Terminal Coding RPG     ║
 ║    ╚███╔╝ ██████╔╝                           ║
 ║    ██╔██╗ ██╔═══╝    Every commit matters    ║
 ║   ██╔╝ ██╗██║                                ║
 ║   ╚═╝  ╚═╝╚═╝       v1.0.0                   ║
 ╚═══════════════════════════════════════════════╝
```

## 🎮 How It Works

| Action | XP | Description |
|--------|-----|-------------|
| `git commit` | +10 XP | Base XP for any commit |
| Bug fix | +50 XP | Commit messages with "fix", "bug", "patch" |
| Refactor | +75 XP | Commit messages with "refactor", "clean" |
| New feature | +40 XP | Commit messages with "feat", "add", "new" |
| Hotfix | +60 XP | Emergency fixes earn bonus XP |
| PR merged | +100 XP | Boss fight victory! |
| Code review | +20 XP | Reviewing others' code |
| Documentation | +30 XP | Writing docs |
| Tests | +25 XP | Test commits |
| Deploy | +50 XP | Shipping to production |

**Time bonuses:** Code at night (2-5am) for 1.5x XP. Early bird (5-7am) gets 1.2x. The system rewards dedication.

**Class bonuses:** Each character class gets multipliers for their specialty actions.

## 🚀 Install

### One-liner

```bash
git clone https://github.com/belentani7/xp.git && cd xp && bash install.sh
```

### Manual

```bash
git clone https://github.com/belentani7/xp.git
cd xp
chmod +x install.sh
./install.sh
```

The installer:
1. Copies the RPG engine to `~/.xp/`
2. Creates your SQLite character database
3. Initializes you as a Level 1 character
4. Sets up global git hooks (auto-awards XP on every commit)
5. Adds `xp` to your PATH

### Git Hooks (per-repo)

If you prefer per-repo hooks instead of global:

```bash
cp ~/.xp/hooks/post-commit .git/hooks/
cp ~/.xp/hooks/post-merge .git/hooks/
chmod +x .git/hooks/post-commit .git/hooks/post-merge
```

## Git hooks: instalación segura

La instalación predeterminada **no cambia** `core.hooksPath` global de Git y, por tanto, no desactiva los hooks existentes de otros proyectos. Para activar expresamente los hooks de XP en tu cuenta:

```bash
XP_INSTALL_GLOBAL_HOOKS=1 bash install.sh
```

Si ya existe una ruta global de hooks, el instalador la respeta y no la sobreescribe. Como alternativa, usa los hooks únicamente en un repositorio determinado. Revisa su comportamiento antes de instalarlos y mantén una copia de hooks propios.

## 📋 Commands

```
xp status          Show character sheet (level, XP, HP, stats)
xp quest           Show current quests
xp achievements    List unlocked achievements (50+)
xp items           Browse equipment shop
xp equip [item]    Equip a weapon/armor/accessory
xp class [name]    Choose class (warrior/mage/rogue/healer)
xp log [N]         Show last N XP entries
xp streak          Show coding streak
xp leaderboard     Show leaderboard
xp combat [bug]    Fight a bug (manual combat!)
xp lore            Show unlocked hidden lore
xp help            Show help
```

## 🎭 Character Classes

| Class | Title | Specialty | Bonus XP |
|-------|-------|-----------|----------|
| ⚔️ **Warrior** | The Relentless Debugger | Refactoring & debugging | Refactor ×1.5, Bugfix ×1.3 |
| 🔮 **Mage** | The Architect | New features & architecture | Feature ×1.5, Architecture ×1.4 |
| 🗡️ **Rogue** | The Speed Demon | Speed & hotfixes | Hotfix ×1.5, Speed ×1.4 |
| 💚 **Healer** | The Code Medic | Reviews & documentation | Review ×1.5, Docs ×1.5 |

Choose with: `xp class warrior`

## 🛡️ Equipment

**Weapons:** Vim (dagger), Neovim (sword), VS Code (staff), Emacs (tome), Cursor (enchanted blade), JetBrains (warhammer), Nano (hatchet)

**Armor:** Dev Hoodie (+5 focus), Noise-Canceling Headphones (+3 concentration), Bottomless Coffee (+2 energy), Energy Drink of Haste (+5 DEX, -2 WIS), Standing Desk (+3 STR, +3 WIS)

**Accessories:** Mechanical Keyboard (+5 DEX), Dual Monitors (+3 awareness), Rubber Duck of Clarity (+4 WIS), Laptop Stickers (+5 CHA), Arch Linux (btw) (+4 INT, -2 CHA)

Equip with: `xp equip neovim`

## 🏆 Achievements (50+)

**Coding:** First Blood, Centurion (100 commits), Bug Slayer (50 fixes), Refactor Master, Test Driven

**Git:** Branch Out, Merge Master, Conflict Resolver, Clean History, Tag Master

**Collaboration:** Ship It!, Fleet Admiral (10 PRs), Review Eagle, Open Source Hero

**Streaks:** Three Day Rule, Weekend Warrior (7 days), Monthly Grind (30 days), Century Club (100 days), Year of Code (365 days!)

**Time:** Night Owl (2-5am commits), Early Bird, Witching Hour, Friday Deploy 🔥

**Mastery:** Apprentice (Lv.10), Journeyman (Lv.25), Master Coder (Lv.50), Grandmaster (Lv.75), The System (Lv.99)

**Special:** Identity Crisis, Gear Up, Walk of Shame (first revert), 10K Club, Lore Seeker, Lore Master

## 🔥 Streaks

Code every day to build your streak. The system tracks consecutive days with commits.

```
$ xp streak

  🔥 CODING STREAK
  Current: 12 days 🔥🔥🔥🔥🔥🔥🔥
  Best:    23 days
```

## ⚔️ Combat

Fight bugs manually when you need extra XP:

```
$ xp combat NullPointerException

  ⚔️  COMBAT: NullPointerException
  Severity: CRITICAL

  Turn 1: You deal 18 damage! CRITICAL! (Bug HP: 282)
  Turn 2: You deal 12 damage! (Bug HP: 270)
  ...
  🏆 VICTORY! +200 XP
```

## 📜 Hidden Lore

The XP system was "discovered" in an abandoned game studio's source code. As you level up, you unlock fragments of Studio 7's story. Each message is stranger than the last.

> Level 5: "Day 1: The engine compiles. Something watches from the build logs."
>
> Level 50: "We understand now. The code writes the coder. Keep leveling."
>
> Level 99: ???

## 🏅 GitHub Badge

Show your XP level on your GitHub profile:

```markdown
![XP Level](https://img.shields.io/badge/XP-Lv.42%20%7C%2018,500%20XP-9333ea?style=for-the-badge&logo=github)
```

Or use the auto-updating badge via GitHub Actions (see `.github/workflows/update-badge.yml`).

## 📁 Project Structure

```
xp/
├── xp                      # Main CLI entry point
├── install.sh              # One-command installer
├── engine/
│   ├── rpg.py              # Core RPG engine (XP, levels, stats)
│   ├── classes.py          # Character classes
│   ├── items.py            # Equipment system
│   ├── achievements.py     # 50+ achievements
│   └── quests.py           # Quest system
├── hooks/
│   ├── post-commit         # Git hook: awards XP per commit
│   └── post-merge          # Git hook: boss fight XP
├── database/
│   └── schema.sql          # SQLite schema
├── display/
│   ├── character_sheet.sh  # ASCII character renderer
│   └── level_up.sh         # Level up animation
├── config/
│   └── default.yaml        # Default configuration
├── web/
│   └── badge.svg           # GitHub profile badge
├── ascii/
│   ├── character.txt       # ASCII character art
│   └── items.txt           # ASCII equipment art
└── .github/
    └── workflows/
        └── update-badge.yml  # Auto-update badge
```

## 🔧 Requirements

- **Python 3.7+** (stdlib only, no pip installs)
- **Git** (for hooks and commit tracking)
- **SQLite 3** (included with Python)
- **Bash** (for installer and hooks)
- Works on **Linux**, **macOS**, and **WSL**

## 🧪 Testing with Real Git

```bash
# Install xp
./install.sh

# Create a test repo
mkdir test-project && cd test-project
git init

# Copy hooks (if not using global)
cp ~/.xp/hooks/post-commit .git/hooks/
cp ~/.xp/hooks/post-merge .git/hooks/

# Make commits and watch XP flow
echo "hello" > main.py
git add . && git commit -m "feat: initial commit"
# → 🚀 New Feature! +40 XP

echo "fix" >> main.py
git add . && git commit -m "fix: resolve startup crash"
# → 🐛 Bug Fixed! +50 XP

xp status
# → Level 1, 90 XP, 90% to level 2
```

## 🎯 Philosophy

XP is designed to be **addictive like Duolingo but for coding**. The core loop:

1. **Commit code** → earn XP → see progress bar fill
2. **Level up** → unlock abilities, equipment, lore
3. **Build streaks** → daily motivation to code
4. **Collect achievements** → dopamine hits for good practices
5. **Show off** → GitHub badge, leaderboard

A 15-year-old in Bangalore should want to install this immediately.

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

*The system remembers. The system grows. Do not reach level 99.*
