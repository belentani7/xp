#!/usr/bin/env python3
"""
Achievement system — 50+ achievements across coding, git, collaboration, and mastery.

Each achievement is a fragment of the studio's story. Collect them all to piece
together what really happened in Studio 7.
"""

from datetime import datetime


# Each achievement: id, name, description, xp_reward, icon, category, unlock_condition
ACHIEVEMENTS = {
    # === CODING ACHIEVEMENTS ===
    "first_blood": {
        "name": "First Blood",
        "description": "Make your first commit",
        "xp_reward": 10,
        "icon": "🩸",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 1,
    },
    "getting_started": {
        "name": "Getting Started",
        "description": "Make 10 commits",
        "xp_reward": 25,
        "icon": "🌱",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 10,
    },
    "code_warrior": {
        "name": "Code Warrior",
        "description": "Make 50 commits",
        "xp_reward": 50,
        "icon": "⚔️",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 50,
    },
    "centurion": {
        "name": "Centurion",
        "description": "Make 100 commits",
        "xp_reward": 100,
        "icon": "💯",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 100,
    },
    "code_machine": {
        "name": "Code Machine",
        "description": "Make 500 commits",
        "xp_reward": 250,
        "icon": "🤖",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 500,
    },
    "legend": {
        "name": "Living Legend",
        "description": "Make 1000 commits",
        "xp_reward": 500,
        "icon": "🏆",
        "category": "coding",
        "check": lambda p: p.get("total_commits", 0) >= 1000,
    },
    "bug_squasher": {
        "name": "Bug Squasher",
        "description": "Fix 10 bugs",
        "xp_reward": 50,
        "icon": "🐛",
        "category": "coding",
        "check": lambda p: p.get("bugfix_count", 0) >= 10,
    },
    "bug_slayer": {
        "name": "Bug Slayer",
        "description": "Fix 50 bugs",
        "xp_reward": 150,
        "icon": "🗡️",
        "category": "coding",
        "check": lambda p: p.get("bugfix_count", 0) >= 50,
    },
    "exterminator": {
        "name": "Exterminator",
        "description": "Fix 100 bugs",
        "xp_reward": 300,
        "icon": "☠️",
        "category": "coding",
        "check": lambda p: p.get("bugfix_count", 0) >= 100,
    },
    "refactor_master": {
        "name": "Refactor Master",
        "description": "Complete 25 refactors",
        "xp_reward": 100,
        "icon": "♻️",
        "category": "coding",
        "check": lambda p: p.get("refactor_count", 0) >= 25,
    },
    "test_driven": {
        "name": "Test Driven",
        "description": "Write 20 test commits",
        "xp_reward": 75,
        "icon": "🧪",
        "category": "coding",
        "check": lambda p: p.get("test_count", 0) >= 20,
    },
    "doc_knight": {
        "name": "Documentation Knight",
        "description": "Write 15 documentation commits",
        "xp_reward": 60,
        "icon": "📚",
        "category": "coding",
        "check": lambda p: p.get("documentation_count", 0) >= 15,
    },

    # === GIT ACHIEVEMENTS ===
    "branch_out": {
        "name": "Branch Out",
        "description": "Create your first feature branch",
        "xp_reward": 15,
        "icon": "🌿",
        "category": "git",
        "check": lambda p: p.get("branches_created", 0) >= 1,
    },
    "merge_master": {
        "name": "Merge Master",
        "description": "Merge 10 branches",
        "xp_reward": 50,
        "icon": "🔀",
        "category": "git",
        "check": lambda p: p.get("merges", 0) >= 10,
    },
    "conflict_resolver": {
        "name": "Conflict Resolver",
        "description": "Resolve 5 merge conflicts",
        "xp_reward": 40,
        "icon": "⚡",
        "category": "git",
        "check": lambda p: p.get("conflicts_resolved", 0) >= 5,
    },
    "clean_history": {
        "name": "Clean History",
        "description": "Make 10 consecutive commits with good messages",
        "xp_reward": 30,
        "icon": "✨",
        "category": "git",
        "check": lambda p: p.get("clean_commits", 0) >= 10,
    },
    "tag_master": {
        "name": "Tag Master",
        "description": "Create 5 release tags",
        "xp_reward": 40,
        "icon": "🏷️",
        "category": "git",
        "check": lambda p: p.get("tags_created", 0) >= 5,
    },

    # === COLLABORATION ===
    "ship_it": {
        "name": "Ship It!",
        "description": "Get 1 PR merged",
        "xp_reward": 50,
        "icon": "🚀",
        "category": "collaboration",
        "check": lambda p: p.get("pr_merges", 0) >= 1,
    },
    "fleet_admiral": {
        "name": "Fleet Admiral",
        "description": "Get 10 PRs merged",
        "xp_reward": 150,
        "icon": "⚓",
        "category": "collaboration",
        "check": lambda p: p.get("pr_merges", 0) >= 10,
    },
    "review_eagle": {
        "name": "Review Eagle",
        "description": "Review 10 PRs",
        "xp_reward": 60,
        "icon": "🦅",
        "category": "collaboration",
        "check": lambda p: p.get("reviews", 0) >= 10,
    },
    "code_sage": {
        "name": "Code Sage",
        "description": "Review 50 PRs",
        "xp_reward": 200,
        "icon": "🧙",
        "category": "collaboration",
        "check": lambda p: p.get("reviews", 0) >= 50,
    },
    "open_source_hero": {
        "name": "Open Source Hero",
        "description": "Contribute to 5 different repositories",
        "xp_reward": 100,
        "icon": "🌟",
        "category": "collaboration",
        "check": lambda p: p.get("repos_contributed", 0) >= 5,
    },

    # === STREAKS ===
    "three_day_rule": {
        "name": "Three Day Rule",
        "description": "Code 3 days in a row",
        "xp_reward": 20,
        "icon": "🔥",
        "category": "streaks",
        "check": lambda p: p.get("current_streak", 0) >= 3,
    },
    "weekend_warrior": {
        "name": "Weekend Warrior",
        "description": "Code 7 days in a row",
        "xp_reward": 50,
        "icon": "📅",
        "category": "streaks",
        "check": lambda p: p.get("current_streak", 0) >= 7,
    },
    "monthly_grind": {
        "name": "Monthly Grind",
        "description": "Code 30 days in a row",
        "xp_reward": 200,
        "icon": "📆",
        "category": "streaks",
        "check": lambda p: p.get("current_streak", 0) >= 30,
    },
    "century_club": {
        "name": "Century Club",
        "description": "Code 100 days in a row",
        "xp_reward": 500,
        "icon": "💎",
        "category": "streaks",
        "check": lambda p: p.get("current_streak", 0) >= 100,
    },
    "year_of_code": {
        "name": "Year of Code",
        "description": "Code 365 days in a row",
        "xp_reward": 1000,
        "icon": "👑",
        "category": "streaks",
        "check": lambda p: p.get("current_streak", 0) >= 365,
    },

    # === TIME-BASED ===
    "night_owl": {
        "name": "Night Owl",
        "description": "Make a commit between 2am and 5am",
        "xp_reward": 30,
        "icon": "🦉",
        "category": "time",
        "check": lambda p: p.get("night_commits", 0) >= 1,
    },
    "early_bird": {
        "name": "Early Bird",
        "description": "Make a commit between 5am and 7am",
        "xp_reward": 25,
        "icon": "🌅",
        "category": "time",
        "check": lambda p: p.get("early_commits", 0) >= 1,
    },
    "witching_hour": {
        "name": "Witching Hour",
        "description": "Make 5 commits after midnight",
        "xp_reward": 50,
        "icon": "🌙",
        "category": "time",
        "check": lambda p: p.get("midnight_commits", 0) >= 5,
    },
    "friday_deploy": {
        "name": "Friday Deploy",
        "description": "Deploy on a Friday. Brave.",
        "xp_reward": 40,
        "icon": "🔥",
        "category": "time",
        "check": lambda p: p.get("friday_deploys", 0) >= 1,
    },

    # === MASTERY ===
    "level_10": {
        "name": "Apprentice",
        "description": "Reach level 10",
        "xp_reward": 50,
        "icon": "⭐",
        "category": "mastery",
        "check": lambda p: p.get("level", 1) >= 10,
    },
    "level_25": {
        "name": "Journeyman",
        "description": "Reach level 25",
        "xp_reward": 100,
        "icon": "🌟",
        "category": "mastery",
        "check": lambda p: p.get("level", 1) >= 25,
    },
    "level_50": {
        "name": "Master Coder",
        "description": "Reach level 50",
        "xp_reward": 250,
        "icon": "💫",
        "category": "mastery",
        "check": lambda p: p.get("level", 1) >= 50,
    },
    "level_75": {
        "name": "Grandmaster",
        "description": "Reach level 75",
        "xp_reward": 500,
        "icon": "🌠",
        "category": "mastery",
        "check": lambda p: p.get("level", 1) >= 75,
    },
    "level_99": {
        "name": "The System",
        "description": "Reach level 99. You know what this means now.",
        "xp_reward": 999,
        "icon": "👁️",
        "category": "mastery",
        "check": lambda p: p.get("level", 1) >= 99,
    },

    # === SPECIAL ===
    "first_class": {
        "name": "Identity Crisis",
        "description": "Choose your character class",
        "xp_reward": 20,
        "icon": "🎭",
        "category": "special",
        "check": lambda p: p.get("class") is not None,
    },
    "equipped": {
        "name": "Gear Up",
        "description": "Equip your first item",
        "xp_reward": 10,
        "icon": "🛡️",
        "category": "special",
        "check": lambda p: len(p.get("equipped", [])) >= 1,
    },
    "full_loadout": {
        "name": "Full Loadout",
        "description": "Have 3 items equipped at once",
        "xp_reward": 40,
        "icon": "🎒",
        "category": "special",
        "check": lambda p: len(p.get("equipped", [])) >= 3,
    },
    "hotfix_hero": {
        "name": "Hotfix Hero",
        "description": "Apply 5 emergency hotfixes",
        "xp_reward": 75,
        "icon": "🚑",
        "category": "coding",
        "check": lambda p: p.get("hotfix_count", 0) >= 5,
    },
    "feature_factory": {
        "name": "Feature Factory",
        "description": "Ship 25 new features",
        "xp_reward": 150,
        "icon": "🏭",
        "category": "coding",
        "check": lambda p: p.get("feature_count", 0) >= 25,
    },
    "deploy_master": {
        "name": "Deploy Master",
        "description": "Deploy 10 times",
        "xp_reward": 100,
        "icon": "🚀",
        "category": "coding",
        "check": lambda p: p.get("deploy_count", 0) >= 10,
    },
    "revert_shame": {
        "name": "Walk of Shame",
        "description": "Revert a commit. We've all been there.",
        "xp_reward": 5,
        "icon": "😅",
        "category": "special",
        "check": lambda p: p.get("revert_count", 0) >= 1,
    },
    "ten_k_club": {
        "name": "10K Club",
        "description": "Earn 10,000 total XP",
        "xp_reward": 100,
        "icon": "💰",
        "category": "mastery",
        "check": lambda p: p.get("xp", 0) >= 10000,
    },
    "hundred_k_club": {
        "name": "100K Club",
        "description": "Earn 100,000 total XP",
        "xp_reward": 500,
        "icon": "💎",
        "category": "mastery",
        "check": lambda p: p.get("xp", 0) >= 100000,
    },
    "lore_seeker": {
        "name": "Lore Seeker",
        "description": "Unlock your first hidden lore entry",
        "xp_reward": 25,
        "icon": "📖",
        "category": "special",
        "check": lambda p: p.get("lore_count", 0) >= 1,
    },
    "lore_master": {
        "name": "Lore Master",
        "description": "Unlock all hidden lore entries",
        "xp_reward": 500,
        "icon": "📜",
        "category": "special",
        "check": lambda p: p.get("lore_count", 0) >= 8,
    },
}

CATEGORIES = ["coding", "git", "collaboration", "streaks", "time", "mastery", "special"]


def get_achievement(achievement_id: str) -> dict:
    """Get achievement data by ID."""
    if achievement_id not in ACHIEVEMENTS:
        return None
    return ACHIEVEMENTS[achievement_id]


def check_achievements(player_data: dict) -> list:
    """
    Check all achievements against player data.
    Returns list of newly unlockable achievement IDs.
    """
    unlocked = []
    for ach_id, ach in ACHIEVEMENTS.items():
        try:
            if ach["check"](player_data):
                unlocked.append(ach_id)
        except Exception:
            pass  # Achievement check failed, skip
    return unlocked


def list_achievements_by_category() -> dict:
    """Group achievements by category."""
    result = {cat: [] for cat in CATEGORIES}
    for ach_id, ach in ACHIEVEMENTS.items():
        cat = ach["category"]
        if cat in result:
            result[cat].append({"id": ach_id, **ach})
    return result


def get_achievement_display(ach_id: str, unlocked: bool = False) -> str:
    """Get a formatted display string for an achievement."""
    ach = get_achievement(ach_id)
    if not ach:
        return f"Unknown achievement: {ach_id}"
    status = "✅" if unlocked else "🔒"
    xp = f"+{ach['xp_reward']} XP"
    return f"{status} {ach['icon']} {ach['name']} — {ach['description']} ({xp})"
