#!/usr/bin/env python3
"""
Character classes — real hacker archetypes from the old studio.

The four classes were found etched into a whiteboard in Studio 7.
Nobody knows who wrote them. They just... fit.
"""

CLASSES = {
    "warrior": {
        "name": "Warrior",
        "title": "The Relentless Debugger",
        "icon": "⚔️",
        "description": "You dive into spaghetti code like a berserker into battle. Refactoring is your war cry.",
        "base_stats": {"STR": 8, "INT": 5, "DEX": 6, "WIS": 4, "CHA": 5},
        "bonus_xp": {"refactor": 1.5, "bugfix": 1.3},
        "abilities": [
            {
                "name": "Brute Force Debug",
                "description": "Find bugs 30% faster through sheer persistence",
                "level_required": 1,
            },
            {
                "name": "Code Armor",
                "description": "Refactored code has fewer regressions",
                "level_required": 5,
            },
            {
                "name": "Berserker Merge",
                "description": "Double XP for resolving merge conflicts",
                "level_required": 10,
            },
            {
                "name": "Titan's Resolve",
                "description": "Critical bugs yield triple XP",
                "level_required": 20,
            },
        ],
        "lore": "Warriors were the first class discovered in the studio archives. "
        "Their playbook was titled 'REFACTOR WITHOUT FEAR' — 200 pages of "
        "patterns for dismantling legacy code without breaking production.",
    },
    "mage": {
        "name": "Mage",
        "title": "The Architect",
        "icon": "🔮",
        "description": "You see patterns where others see chaos. New systems flow from your fingertips.",
        "base_stats": {"STR": 4, "INT": 9, "DEX": 5, "WIS": 7, "CHA": 4},
        "bonus_xp": {"feature": 1.5, "architecture": 1.4},
        "abilities": [
            {
                "name": "Pattern Recognition",
                "description": "New features earn 30% more XP",
                "level_required": 1,
            },
            {
                "name": "Arcane Architecture",
                "description": "System design commits yield bonus XP",
                "level_required": 5,
            },
            {
                "name": "Spell Weaving",
                "description": "Multi-file changes earn combo multiplier",
                "level_required": 10,
            },
            {
                "name": "Grand Design",
                "description": "Creating new projects grants massive XP burst",
                "level_required": 20,
            },
        ],
        "lore": "The Mage's grimoire was found on a dusty CRT monitor, still glowing. "
        "It contained architecture diagrams for a game engine that could generate "
        "worlds from code. The studio never shipped it. You might finish it.",
    },
    "rogue": {
        "name": "Rogue",
        "title": "The Speed Demon",
        "icon": "🗡️",
        "description": "Fast commits, quick fixes, zero hesitation. You ship before they finish debating.",
        "base_stats": {"STR": 5, "INT": 5, "DEX": 9, "WIS": 4, "CHA": 6},
        "bonus_xp": {"hotfix": 1.5, "speed": 1.4},
        "abilities": [
            {
                "name": "Quick Draw",
                "description": "Commits under 5min after branch creation earn 2x XP",
                "level_required": 1,
            },
            {
                "name": "Shadow Hotfix",
                "description": "Emergency fixes yield bonus XP based on speed",
                "level_required": 5,
            },
            {
                "name": "Silent Deploy",
                "description": "Zero-downtime deploys grant stealth bonus",
                "level_required": 10,
            },
            {
                "name": "Phantom Ship",
                "description": "Ship 3 features in one day for massive combo",
                "level_required": 20,
            },
        ],
        "lore": "The Rogue's manifesto was scrawled on a sticky note: 'SHIP IT OR KILL IT.' "
        "Found next to a keyboard with all keys worn smooth except ESC and ENTER. "
        "This person didn't plan. They executed.",
    },
    "healer": {
        "name": "Healer",
        "title": "The Code Medic",
        "icon": "💚",
        "description": "You review, document, and mentor. The team is stronger because you exist.",
        "base_stats": {"STR": 4, "INT": 6, "DEX": 4, "WIS": 8, "CHA": 7},
        "bonus_xp": {"review": 1.5, "documentation": 1.5, "mentoring": 1.4},
        "abilities": [
            {
                "name": "Code Review Aura",
                "description": "PR reviews earn 50% more XP",
                "level_required": 1,
            },
            {
                "name": "Documentation Ward",
                "description": "Writing docs grants XP equal to code",
                "level_required": 5,
            },
            {
                "name": "Team Buff",
                "description": "When your reviewed PR merges, both parties earn bonus",
                "level_required": 10,
            },
            {
                "name": "Grand Mentor",
                "description": "Onboarding new devs triggers XP aura for the whole team",
                "level_required": 20,
            },
        ],
        "lore": "The Healer's journal was the most personal artifact found. Page after page "
        "of code reviews, not just catching bugs but teaching. 'Good code is taught, "
        "not written' was underlined three times. The studio's only surviving team "
        "was the one this person mentored.",
    },
}


def get_class(class_name: str) -> dict:
    """Get class data by name."""
    key = class_name.lower()
    if key not in CLASSES:
        raise ValueError(
            f"Unknown class '{class_name}'. Choose from: {', '.join(CLASSES.keys())}"
        )
    return CLASSES[key]


def list_classes() -> list:
    """List all available classes."""
    return [
        {
            "key": k,
            "name": v["name"],
            "title": v["title"],
            "icon": v["icon"],
            "description": v["description"],
        }
        for k, v in CLASSES.items()
    ]


def get_class_abilities(class_name: str, player_level: int = 0) -> list:
    """Get abilities available for a class at a given level."""
    cls = get_class(class_name)
    return [a for a in cls["abilities"] if a["level_required"] <= player_level]


def get_xp_multiplier(class_name: str, action_type: str) -> float:
    """Get the XP multiplier for a class doing a specific action."""
    cls = get_class(class_name)
    return cls["bonus_xp"].get(action_type, 1.0)
