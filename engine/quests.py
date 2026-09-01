#!/usr/bin/env python3
"""
Quest system — auto-generates quests from git activity.

The studio used quests to gamify their own development sprints.
Each quest was tied to a real deliverable. Some were never completed.
The incomplete ones still linger in the system, waiting.
"""

from datetime import datetime, timedelta

# Quest templates: id, name, description, target, xp_reward, icon, category, condition
QUESTS = {
    # === DAILY QUESTS ===
    "daily_commits": {
        "name": "Daily Grind",
        "description": "Make 3 commits today",
        "target": 3,
        "xp_reward": 30,
        "icon": "📝",
        "category": "daily",
        "action_type": "commit",
        "recurring": True,
    },
    "daily_tests": {
        "name": "Test Your Code",
        "description": "Write 2 test commits today",
        "target": 2,
        "xp_reward": 40,
        "icon": "🧪",
        "category": "daily",
        "action_type": "test",
        "recurring": True,
    },
    "daily_docs": {
        "name": "Document Everything",
        "description": "Write 1 documentation commit today",
        "target": 1,
        "xp_reward": 25,
        "icon": "📚",
        "category": "daily",
        "action_type": "documentation",
        "recurring": True,
    },

    # === WEEKLY QUESTS ===
    "weekly_features": {
        "name": "Feature Complete",
        "description": "Ship 5 feature commits this week",
        "target": 5,
        "xp_reward": 100,
        "icon": "🚀",
        "category": "weekly",
        "action_type": "feature",
        "recurring": True,
    },
    "weekly_bugs": {
        "name": "Bug Hunter",
        "description": "Fix 10 bugs this week",
        "target": 10,
        "xp_reward": 120,
        "icon": "🐛",
        "category": "weekly",
        "action_type": "bugfix",
        "recurring": True,
    },
    "weekly_refactor": {
        "name": "Code Gardener",
        "description": "Complete 3 refactors this week",
        "target": 3,
        "xp_reward": 90,
        "icon": "♻️",
        "category": "weekly",
        "action_type": "refactor",
        "recurring": True,
    },

    # === EPIC QUESTS ===
    "clear_the_backlog": {
        "name": "Clear the Backlog",
        "description": "Fix 50 bugs total",
        "target": 50,
        "xp_reward": 300,
        "icon": "📋",
        "category": "epic",
        "action_type": "bugfix",
        "recurring": False,
    },
    "ship_a_feature": {
        "name": "Ship a Feature",
        "description": "Merge a feature branch (PR merge)",
        "target": 1,
        "xp_reward": 150,
        "icon": "🎯",
        "category": "epic",
        "action_type": "pr_merge",
        "recurring": False,
    },
    "hotfix_hero_quest": {
        "name": "Hotfix Hero",
        "description": "Apply 3 critical hotfixes",
        "target": 3,
        "xp_reward": 200,
        "icon": "🚑",
        "category": "epic",
        "action_type": "hotfix",
        "recurring": False,
    },
    "review_champion": {
        "name": "Code Review Champion",
        "description": "Review 10 PRs",
        "target": 10,
        "xp_reward": 200,
        "icon": "🦅",
        "category": "epic",
        "action_type": "review",
        "recurring": False,
    },
    "the_century": {
        "name": "The Century",
        "description": "Make 100 total commits",
        "target": 100,
        "xp_reward": 500,
        "icon": "💯",
        "category": "epic",
        "action_type": "commit",
        "recurring": False,
    },
    "full_stack": {
        "name": "Full Stack",
        "description": "Make commits in 5 different categories (bugfix, feature, refactor, test, docs)",
        "target": 5,
        "xp_reward": 150,
        "icon": "🥞",
        "category": "epic",
        "action_type": "any",
        "recurring": False,
    },
    "streak_seven": {
        "name": "Unstoppable Week",
        "description": "Maintain a 7-day coding streak",
        "target": 7,
        "xp_reward": 200,
        "icon": "🔥",
        "category": "epic",
        "action_type": "streak",
        "recurring": False,
    },
    "boss_fight_pr": {
        "name": "Boss Fight: The Mega PR",
        "description": "Get a PR merged with 10+ commits",
        "target": 1,
        "xp_reward": 300,
        "icon": "👹",
        "category": "boss",
        "action_type": "pr_merge",
        "recurring": False,
    },
    "boss_fight_deploy": {
        "name": "Boss Fight: Production Deploy",
        "description": "Successfully deploy to production",
        "target": 1,
        "xp_reward": 250,
        "icon": "🐉",
        "category": "boss",
        "action_type": "deploy",
        "recurring": False,
    },
    "boss_fight_refactor": {
        "name": "Boss Fight: The Big Rewrite",
        "description": "Complete a massive refactor (10+ refactor commits)",
        "target": 10,
        "xp_reward": 400,
        "icon": "🏰",
        "category": "boss",
        "action_type": "refactor",
        "recurring": False,
    },
}

# Lore fragments hidden in quest completions
QUEST_LORE = {
    "clear_the_backlog": "📜 Quest log note: 'Studio 7 had 847 open bugs when they shut down. Nobody fixed them. They're still in the system somewhere.'",
    "boss_fight_pr": "📜 Hidden in the PR description: 'The final build compiled at 3:47am. The team cheered. Nobody noticed the warning in the logs.'",
    "the_century": "📜 Achievement note: 'One hundred commits. The system has enough data now. It's learning your patterns. Your style. Your weaknesses.'",
}

CATEGORIES = ["daily", "weekly", "epic", "boss"]


def get_quest(quest_id: str) -> dict:
    """Get quest data by ID."""
    if quest_id not in QUESTS:
        return None
    return QUESTS[quest_id]


def get_active_quests(player_data: dict) -> list:
    """Get quests that are relevant to the player's current progress."""
    active = []
    for quest_id, quest in QUESTS.items():
        # Daily/weekly quests are always available
        if quest["recurring"]:
            active.append({
                "id": quest_id,
                **quest,
                "status": "active",
                "progress": 0,
            })
        else:
            # Epic/boss quests show based on progress
            active.append({
                "id": quest_id,
                **quest,
                "status": "active",
                "progress": 0,
            })
    return active


def get_quest_for_action(action_type: str) -> list:
    """Get quests that track a specific action type."""
    matching = []
    for quest_id, quest in QUESTS.items():
        if quest["action_type"] == action_type or quest["action_type"] == "any":
            matching.append({"id": quest_id, **quest})
    return matching


def generate_daily_quests() -> list:
    """Generate today's daily quests."""
    today = datetime.now().strftime("%Y-%m-%d")
    dailies = []
    for quest_id, quest in QUESTS.items():
        if quest["category"] == "daily":
            dailies.append({
                "id": f"{quest_id}_{today}",
                "base_id": quest_id,
                **quest,
                "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            })
    return dailies


def list_quests_by_category() -> dict:
    """Group quests by category."""
    result = {cat: [] for cat in CATEGORIES}
    for quest_id, quest in QUESTS.items():
        cat = quest["category"]
        if cat in result:
            result[cat].append({"id": quest_id, **quest})
    return result


def get_quest_display(quest_id: str, progress: int = 0) -> str:
    """Get a formatted display string for a quest."""
    quest = get_quest(quest_id)
    if not quest:
        return f"Unknown quest: {quest_id}"
    pct = min(100, int((progress / quest["target"]) * 100))
    bar_len = 20
    filled = int(bar_len * progress / quest["target"])
    bar = "█" * filled + "░" * (bar_len - filled)
    xp = f"+{quest['xp_reward']} XP"
    status = "✅ COMPLETE" if progress >= quest["target"] else f"[{bar}] {progress}/{quest['target']}"
    return f"{quest['icon']} {quest['name']} — {quest['description']}\n   {status} ({xp})"


def get_quest_lore(quest_id: str) -> str:
    """Get lore fragment for completing a quest, if any."""
    return QUEST_LORE.get(quest_id)
