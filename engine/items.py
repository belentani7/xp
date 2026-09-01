#!/usr/bin/env python3
"""
Equipment system — weapons, armor, and accessories for the coding warrior.

Every tool you use is a weapon. Choose wisely.
"""

ITEMS = {
    # === WEAPONS ===
    "vim": {
        "name": "Vim",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "🗡️",
        "stats": {"STR": 3, "DEX": 5},
        "flavor": "Ancient blade. Lightweight. Deadly in skilled hands. Exit not included.",
        "level_required": 1,
        "rarity": "common",
    },
    "neovim": {
        "name": "Neovim",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "⚔️",
        "stats": {"STR": 4, "DEX": 6, "INT": 2},
        "flavor": "Forged from Vim's essence. Async. Extensible. The modern warrior's choice.",
        "level_required": 5,
        "rarity": "rare",
    },
    "vscode": {
        "name": "VS Code",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "🔮",
        "stats": {"INT": 5, "WIS": 3, "CHA": 2},
        "flavor": "A staff of immense power. Extension marketplace adds infinite spells.",
        "level_required": 1,
        "rarity": "common",
    },
    "emacs": {
        "name": "Emacs",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "📕",
        "stats": {"INT": 7, "WIS": 5},
        "flavor": "The Tome of All Knowledge. Also an editor, allegedly. Requires pinky of steel.",
        "level_required": 10,
        "rarity": "epic",
    },
    "cursor": {
        "name": "Cursor",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "✨",
        "stats": {"INT": 6, "DEX": 4, "WIS": 2},
        "flavor": "AI-enchanted blade. The code writes itself... mostly.",
        "level_required": 8,
        "rarity": "rare",
    },
    "jetbrains": {
        "name": "JetBrains IDE",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "🔨",
        "stats": {"STR": 5, "INT": 4, "WIS": 3},
        "flavor": "Heavy warhammer. Slow to start. Unstoppable once running. Costs gold monthly.",
        "level_required": 3,
        "rarity": "rare",
    },
    "nano": {
        "name": "GNU Nano",
        "type": "weapon",
        "slot": "main_hand",
        "icon": "🪓",
        "stats": {"STR": 1, "DEX": 2},
        "flavor": "Humble hatchet. Everyone's first weapon. Nothing to be ashamed of.",
        "level_required": 1,
        "rarity": "common",
    },
    # === ARMOR ===
    "hoodie": {
        "name": "Dev Hoodie",
        "type": "armor",
        "slot": "body",
        "icon": "🧥",
        "stats": {"WIS": 5, "CHA": -1},
        "flavor": "+5 Focus. -1 Social Skills. Worth it.",
        "level_required": 1,
        "rarity": "common",
    },
    "headphones": {
        "name": "Noise-Canceling Headphones",
        "type": "armor",
        "slot": "head",
        "icon": "🎧",
        "stats": {"INT": 3, "DEX": 3},
        "flavor": "Blocks out the world. Lets the code in.",
        "level_required": 1,
        "rarity": "common",
    },
    "coffee": {
        "name": "Bottomless Coffee",
        "type": "armor",
        "slot": "accessory",
        "icon": "☕",
        "stats": {"DEX": 2, "STR": 2},
        "flavor": "Energy +2. Sleep -10. The programmer's elixir.",
        "level_required": 1,
        "rarity": "common",
    },
    "energy_drink": {
        "name": "Energy Drink of Haste",
        "type": "armor",
        "slot": "accessory",
        "icon": "⚡",
        "stats": {"DEX": 5, "STR": 1, "WIS": -2},
        "flavor": "Speed +5. Judgment -2. Your commits at 3am tell the story.",
        "level_required": 3,
        "rarity": "uncommon",
    },
    "standing_desk": {
        "name": "Standing Desk of Fortitude",
        "type": "armor",
        "slot": "body",
        "icon": "🖥️",
        "stats": {"STR": 3, "WIS": 3},
        "flavor": "Stand while coding. Your back thanks you. Your legs hate you.",
        "level_required": 5,
        "rarity": "uncommon",
    },
    # === ACCESSORIES ===
    "mech_keyboard": {
        "name": "Mechanical Keyboard",
        "type": "accessory",
        "slot": "accessory",
        "icon": "⌨️",
        "stats": {"DEX": 5, "CHA": 1},
        "flavor": "Click clack click clack. The rhythm of creation. Coworkers beware.",
        "level_required": 1,
        "rarity": "common",
    },
    "dual_monitors": {
        "name": "Dual Monitor Array",
        "type": "accessory",
        "slot": "accessory",
        "icon": "🖥️🖥️",
        "stats": {"WIS": 3, "INT": 2},
        "flavor": "One screen for code. One for Stack Overflow. +3 Awareness.",
        "level_required": 3,
        "rarity": "uncommon",
    },
    "triple_monitors": {
        "name": "Triple Monitor Fortress",
        "type": "accessory",
        "slot": "accessory",
        "icon": "🖥️🖥️🖥️",
        "stats": {"WIS": 5, "INT": 3, "CHA": 2},
        "flavor": "The command center. Visitors assume you're hacking the mainframe.",
        "level_required": 10,
        "rarity": "epic",
    },
    "rubber_duck": {
        "name": "Rubber Duck of Clarity",
        "type": "accessory",
        "slot": "accessory",
        "icon": "🦆",
        "stats": {"WIS": 4, "INT": 1},
        "flavor": "Explain your bug to the duck. The duck already knows. The duck always knows.",
        "level_required": 1,
        "rarity": "common",
    },
    "stickers": {
        "name": "Laptop Sticker Collection",
        "type": "accessory",
        "slot": "accessory",
        "icon": "🏷️",
        "stats": {"CHA": 5},
        "flavor": "Each sticker is a conference attended, a tool mastered, a story told.",
        "level_required": 1,
        "rarity": "common",
    },
    "arch_linux": {
        "name": "Arch Linux (btw)",
        "type": "accessory",
        "slot": "accessory",
        "icon": "🐧",
        "stats": {"INT": 4, "CHA": -2, "WIS": 3},
        "flavor": "I use Arch, btw. Intelligence +4. Social interaction -2. Worth it, btw.",
        "level_required": 15,
        "rarity": "legendary",
    },
}

RARITY_COLORS = {
    "common": "\033[37m",     # white
    "uncommon": "\033[32m",   # green
    "rare": "\033[34m",       # blue
    "epic": "\033[35m",       # purple
    "legendary": "\033[33m",  # yellow
}

RARITY_RESET = "\033[0m"


def get_item(item_id: str) -> dict:
    """Get item data by ID."""
    if item_id not in ITEMS:
        raise ValueError(
            f"Unknown item '{item_id}'. Use 'xp equip --list' to see available items."
        )
    return ITEMS[item_id]


def list_items(item_type: str = None, rarity: str = None) -> list:
    """List all items, optionally filtered by type or rarity."""
    results = []
    for item_id, item in ITEMS.items():
        if item_type and item["type"] != item_type:
            continue
        if rarity and item["rarity"] != rarity:
            continue
        results.append({"id": item_id, **item})
    return results


def get_item_display(item_id: str) -> str:
    """Get a formatted display string for an item."""
    item = get_item(item_id)
    color = RARITY_COLORS.get(item["rarity"], "")
    stats_str = ", ".join(f"{k}+{v}" if v > 0 else f"{k}{v}" for k, v in item["stats"].items())
    return f"{color}{item['icon']} {item['name']} [{item['rarity'].upper()}] — {stats_str}{RARITY_RESET}"


def get_equip_bonus(equipped_items: list) -> dict:
    """Calculate total stat bonuses from equipped items."""
    total = {"STR": 0, "INT": 0, "DEX": 0, "WIS": 0, "CHA": 0}
    for item_id in equipped_items:
        if item_id in ITEMS:
            for stat, bonus in ITEMS[item_id]["stats"].items():
                total[stat] += bonus
    return total
