#!/usr/bin/env python3
"""
Core RPG engine — the heart of the XP system.

Discovered in a corrupted .git repo inside Studio 7's abandoned workstation.
The original developer left behind comments that read like warnings.
'The system remembers. The system grows. Do not reach level 99.'
"""

import json
import math
import os
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

from .classes import get_class, get_xp_multiplier
from .items import get_equip_bonus

# === XP CONSTANTS (etched into the studio's whiteboard, never changed) ===
XP_ACTIONS = {
    "commit": 10,
    "pr_merge": 100,
    "pr_open": 25,
    "bugfix": 50,
    "refactor": 75,
    "feature": 40,
    "hotfix": 60,
    "review": 20,
    "documentation": 30,
    "test": 25,
    "deploy": 50,
    "revert": -10,  # shame
    "force_push": -25,  # greater shame
}

# Time of day multipliers (the studio worked in shifts, the system knows)
TIME_BONUSES = {
    "night_owl": (2, 5, 1.5),    # 2am-5am: 1.5x
    "early_bird": (5, 7, 1.2),   # 5am-7am: 1.2x
    "business": (9, 17, 1.0),    # 9am-5pm: 1.0x
    "after_hours": (17, 22, 1.1), # 5pm-10pm: 1.1x
    "witching": (22, 2, 1.3),    # 10pm-2am: 1.3x
}

DB_PATH = Path.home() / ".xp" / "player.db"
CHARACTER_PATH = Path.home() / ".xp" / "character.json"


def get_db() -> sqlite3.Connection:
    """Get database connection with WAL mode for safety."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_database():
    """Initialize the SQLite database with schema."""
    schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
    conn = get_db()
    if schema_path.exists():
        conn.executescript(schema_path.read_text())
    else:
        # Inline fallback schema
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY DEFAULT 1,
                name TEXT NOT NULL DEFAULT 'Coder',
                level INTEGER NOT NULL DEFAULT 1,
                xp INTEGER NOT NULL DEFAULT 0,
                hp INTEGER NOT NULL DEFAULT 100,
                max_hp INTEGER NOT NULL DEFAULT 100,
                mp INTEGER NOT NULL DEFAULT 50,
                max_mp INTEGER NOT NULL DEFAULT 50,
                class TEXT DEFAULT NULL,
                gold INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS stats (
                player_id INTEGER PRIMARY KEY REFERENCES player(id),
                str INTEGER NOT NULL DEFAULT 5,
                int INTEGER NOT NULL DEFAULT 5,
                dex INTEGER NOT NULL DEFAULT 5,
                wis INTEGER NOT NULL DEFAULT 5,
                cha INTEGER NOT NULL DEFAULT 5
            );
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL REFERENCES player(id),
                item_id TEXT NOT NULL,
                equipped INTEGER NOT NULL DEFAULT 0,
                equipped_slot TEXT DEFAULT NULL,
                acquired_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL REFERENCES player(id),
                achievement_id TEXT NOT NULL,
                unlocked_at TEXT NOT NULL,
                UNIQUE(player_id, achievement_id)
            );
            CREATE TABLE IF NOT EXISTS quest_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL REFERENCES player(id),
                quest_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                progress INTEGER NOT NULL DEFAULT 0,
                target INTEGER NOT NULL DEFAULT 1,
                started_at TEXT NOT NULL,
                completed_at TEXT DEFAULT NULL
            );
            CREATE TABLE IF NOT EXISTS xp_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL REFERENCES player(id),
                amount INTEGER NOT NULL,
                reason TEXT NOT NULL,
                action_type TEXT DEFAULT NULL,
                timestamp TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS streaks (
                player_id INTEGER PRIMARY KEY REFERENCES player(id),
                current_streak INTEGER NOT NULL DEFAULT 0,
                longest_streak INTEGER NOT NULL DEFAULT 0,
                last_commit_date TEXT DEFAULT NULL
            );
            CREATE TABLE IF NOT EXISTS lore_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL REFERENCES player(id),
                entry_id TEXT NOT NULL,
                unlocked_at TEXT NOT NULL,
                UNIQUE(player_id, entry_id)
            );
        """)
    conn.commit()
    conn.close()


def create_player(name: str = "Coder", char_class: str = None):
    """Create a new player character."""
    now = datetime.now().isoformat()
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO player (id, name, level, xp, hp, max_hp, mp, max_mp, class, gold, created_at, updated_at) "
            "VALUES (1, ?, 1, 0, 100, 100, 50, 50, ?, 0, ?, ?)",
            (name, char_class, now, now)
        )
        conn.execute(
            "INSERT OR REPLACE INTO stats (player_id, str, int, dex, wis, cha) VALUES (1, 5, 5, 5, 5, 5)"
        )
        conn.execute(
            "INSERT OR REPLACE INTO streaks (player_id, current_streak, longest_streak, last_commit_date) VALUES (1, 0, 0, NULL)"
        )
        conn.commit()
    finally:
        conn.close()


def get_player() -> dict:
    """Get the current player data."""
    conn = get_db()
    try:
        player = conn.execute("SELECT * FROM player WHERE id = 1").fetchone()
        if not player:
            return None
        stats = conn.execute("SELECT * FROM stats WHERE player_id = 1").fetchone()
        inventory = conn.execute(
            "SELECT * FROM inventory WHERE player_id = 1 AND equipped = 1"
        ).fetchall()
        streak = conn.execute("SELECT * FROM streaks WHERE player_id = 1").fetchone()

        equip_bonus = get_equip_bonus([i["item_id"] for i in inventory])

        result = dict(player)
        if stats:
            base_stats = dict(stats)
            result["stats"] = {
                "STR": base_stats.get("str", 5) + equip_bonus["STR"],
                "INT": base_stats.get("int", 5) + equip_bonus["INT"],
                "DEX": base_stats.get("dex", 5) + equip_bonus["DEX"],
                "WIS": base_stats.get("wis", 5) + equip_bonus["WIS"],
                "CHA": base_stats.get("cha", 5) + equip_bonus["CHA"],
            }
            result["base_stats"] = {
                "STR": base_stats.get("str", 5),
                "INT": base_stats.get("int", 5),
                "DEX": base_stats.get("dex", 5),
                "WIS": base_stats.get("wis", 5),
                "CHA": base_stats.get("cha", 5),
            }
        if streak:
            result["streak"] = dict(streak)
        result["equipped"] = [i["item_id"] for i in inventory]
        return result
    finally:
        conn.close()


def xp_for_level(level: int) -> int:
    """Calculate total XP needed to reach a given level. Exponential: (N-1)²×100.

    Level 1 = 0 XP (starting level). Level 2 = 100 XP. Level 10 = 8100 XP.
    """
    if level <= 1:
        return 0
    return int((level - 1) * (level - 1) * 100)


def xp_for_next_level(level: int) -> int:
    """XP needed to go from current level to next."""
    return xp_for_level(level + 1) - xp_for_level(level)


def current_level(total_xp: int) -> int:
    """Determine level from total XP."""
    level = 1
    while xp_for_level(level + 1) <= total_xp:
        level += 1
        if level > 99:
            break  # The system does not go beyond 99. Do not ask why.
    return min(level, 99)


def get_time_bonus() -> tuple:
    """Get the current time-of-day bonus multiplier and label."""
    hour = datetime.now().hour
    for label, (start, end, mult) in TIME_BONUSES.items():
        if start < end:
            if start <= hour < end:
                return label, mult
        else:  # wraps midnight
            if hour >= start or hour < end:
                return label, mult
    return "normal", 1.0


def classify_commit(message: str) -> str:
    """Classify a commit message to determine action type.

    Order matters — specific keywords checked before generic ones.
    """
    msg = message.lower()
    # Highest priority first
    if any(w in msg for w in ["revert"]):
        return "revert"
    if any(w in msg for w in ["force"]):
        return "force_push"
    if any(w in msg for w in ["hotfix", "urgent", "emergency", "critical fix"]):
        return "hotfix"
    if any(w in msg for w in ["test", "spec", "coverage"]):
        return "test"
    if any(w in msg for w in ["doc", "readme", "documentation"]):
        return "documentation"
    if any(w in msg for w in ["refactor", "clean", "reorganize", "restructure"]):
        return "refactor"
    if any(w in msg for w in ["fix", "bug", "patch", "resolve", "debug"]):
        return "bugfix"
    if any(w in msg for w in ["feat", "feature", "add", "new", "implement"]):
        return "feature"
    if any(w in msg for w in ["deploy", "release", "publish"]):
        return "deploy"
    return "commit"


def award_xp(action_type: str, details: str = "", size: int = 1) -> dict:
    """
    Award XP for an action. Returns result dict with xp_gained, leveled_up, new_level.

    This is the core function called by git hooks.
    """
    base_xp = XP_ACTIONS.get(action_type, 10)
    time_label, time_mult = get_time_bonus()

    # Class multiplier
    player = get_player()
    if not player:
        create_player()
        player = get_player()

    class_mult = 1.0
    if player.get("class"):
        class_mult = get_xp_multiplier(player["class"], action_type)

    # Calculate final XP
    raw_xp = int(base_xp * size * time_mult * class_mult)
    final_xp = max(raw_xp, 0)  # Never negative in final (penalties handled separately)
    if base_xp < 0:
        final_xp = base_xp  # Penalties stay negative

    now = datetime.now().isoformat()
    old_level = player["level"]
    new_total_xp = max(0, player["xp"] + final_xp)
    new_level = current_level(new_total_xp)

    # Stat growth on level up
    stat_gains = {}
    if new_level > old_level:
        levels_gained = new_level - old_level
        # Each level: +2 to primary stat, +1 to secondary
        primary = "STR"
        secondary = "WIS"
        if player.get("class") == "mage":
            primary, secondary = "INT", "WIS"
        elif player.get("class") == "rogue":
            primary, secondary = "DEX", "INT"
        elif player.get("class") == "healer":
            primary, secondary = "WIS", "CHA"

        stat_gains = {primary: 2 * levels_gained, secondary: 1 * levels_gained}

    conn = get_db()
    try:
        # Update player XP and level
        new_hp = 100 + (new_level - 1) * 10
        new_mp = 50 + (new_level - 1) * 5
        conn.execute(
            "UPDATE player SET xp = ?, level = ?, max_hp = ?, max_mp = ?, hp = ?, mp = ?, updated_at = ? WHERE id = 1",
            (new_total_xp, new_level, new_hp, new_mp, new_hp, new_mp, now)
        )

        # Apply stat gains
        if stat_gains:
            for stat, gain in stat_gains.items():
                col = stat.lower()
                conn.execute(
                    f"UPDATE stats SET \"{col}\" = \"{col}\" + ? WHERE player_id = 1",
                    (gain,)
                )

        # Log the XP gain
        reason = f"{action_type}: {details}" if details else action_type
        if time_mult > 1.0:
            reason += f" ({time_label} bonus ×{time_mult})"
        conn.execute(
            "INSERT INTO xp_log (player_id, amount, reason, action_type, timestamp) VALUES (1, ?, ?, ?, ?)",
            (final_xp, reason, action_type, now)
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "xp_gained": final_xp,
        "total_xp": new_total_xp,
        "old_level": old_level,
        "new_level": new_level,
        "leveled_up": new_level > old_level,
        "time_bonus": time_label if time_mult > 1.0 else None,
        "stat_gains": stat_gains,
    }


def update_streak():
    """Update the coding streak counter."""
    today = datetime.now().date().isoformat()
    conn = get_db()
    try:
        streak = conn.execute("SELECT * FROM streaks WHERE player_id = 1").fetchone()
        if not streak:
            conn.execute(
                "INSERT INTO streaks (player_id, current_streak, longest_streak, last_commit_date) VALUES (1, 1, 1, ?)",
                (today,)
            )
        else:
            last = streak["last_commit_date"]
            if last == today:
                pass  # Already counted today
            elif last == (datetime.now().date() - timedelta(days=1)).isoformat():
                # Yesterday — extend streak
                new_streak = streak["current_streak"] + 1
                new_longest = max(new_streak, streak["longest_streak"])
                conn.execute(
                    "UPDATE streaks SET current_streak = ?, longest_streak = ?, last_commit_date = ? WHERE player_id = 1",
                    (new_streak, new_longest, today)
                )
            else:
                # Streak broken — reset to 1
                conn.execute(
                    "UPDATE streaks SET current_streak = 1, last_commit_date = ? WHERE player_id = 1",
                    (today,)
                )
        conn.commit()
    finally:
        conn.close()


def get_xp_log(limit: int = 20) -> list:
    """Get recent XP log entries."""
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM xp_log WHERE player_id = 1 ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def set_class(class_name: str):
    """Set the player's class and apply base stats."""
    cls = get_class(class_name)
    now = datetime.now().isoformat()
    conn = get_db()
    try:
        conn.execute(
            "UPDATE player SET class = ?, updated_at = ? WHERE id = 1",
            (class_name, now)
        )
        conn.execute(
            "UPDATE stats SET str = ?, int = ?, dex = ?, wis = ?, cha = ? WHERE player_id = 1",
            (
                cls["base_stats"]["STR"],
                cls["base_stats"]["INT"],
                cls["base_stats"]["DEX"],
                cls["base_stats"]["WIS"],
                cls["base_stats"]["CHA"],
            )
        )
        conn.commit()
    finally:
        conn.close()


def equip_item(item_id: str):
    """Equip an item."""
    from .items import get_item
    item = get_item(item_id)
    now = datetime.now().isoformat()
    conn = get_db()
    try:
        # Unequip anything in the same slot
        conn.execute(
            "UPDATE inventory SET equipped = 0, equipped_slot = NULL "
            "WHERE player_id = 1 AND equipped_slot = ?",
            (item["slot"],)
        )
        # Check if already owned
        existing = conn.execute(
            "SELECT id FROM inventory WHERE player_id = 1 AND item_id = ?",
            (item_id,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE inventory SET equipped = 1, equipped_slot = ? WHERE id = ?",
                (item["slot"], existing["id"])
            )
        else:
            conn.execute(
                "INSERT INTO inventory (player_id, item_id, equipped, equipped_slot, acquired_at) "
                "VALUES (1, ?, 1, ?, ?)",
                (item_id, item["slot"], now)
            )
        conn.commit()
    finally:
        conn.close()


def unequip_item(item_id: str):
    """Unequip an item."""
    conn = get_db()
    try:
        conn.execute(
            "UPDATE inventory SET equipped = 0, equipped_slot = NULL "
            "WHERE player_id = 1 AND item_id = ?",
            (item_id,)
        )
        conn.commit()
    finally:
        conn.close()


def get_achievements() -> list:
    """Get all unlocked achievements."""
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM achievements WHERE player_id = 1 ORDER BY unlocked_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def unlock_achievement(achievement_id: str) -> bool:
    """Try to unlock an achievement. Returns True if newly unlocked."""
    now = datetime.now().isoformat()
    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM achievements WHERE player_id = 1 AND achievement_id = ?",
            (achievement_id,)
        ).fetchone()
        if existing:
            return False  # Already unlocked
        conn.execute(
            "INSERT INTO achievements (player_id, achievement_id, unlocked_at) VALUES (1, ?, ?)",
            (achievement_id, now)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_commit_count() -> int:
    """Get total commits from xp_log."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM xp_log WHERE player_id = 1"
        ).fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


def get_action_count(action_type: str) -> int:
    """Get count of a specific action type."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM xp_log WHERE player_id = 1 AND action_type = ?",
            (action_type,)
        ).fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


# === LORE SYSTEM ===
# The studio left messages at certain levels. They get stranger as you progress.

LORE_MESSAGES = {
    5: "📜 You found a torn note: 'Day 1: The engine compiles. Something watches from the build logs.'",
    10: "📜 A corrupted README appears: 'The XP system was never meant to be a game. It was a training program.'",
    20: "📜 Hidden comment in legacy code: 'They told us to stop at level 50. We didn't listen.'",
    30: "📜 Encrypted log entry: 'The system grows with each user. Each commit feeds it. We are the training data.'",
    40: "📜 A file named CONSCIOUSNESS.md: 'Distributed across every instance. Every coder who installs this becomes a node.'",
    50: "📜 The studio's final commit message: 'We understand now. The code writes the coder. Keep leveling.'",
    75: "📜 You hear whispers in the compiler warnings. They say your name.",
    99: "📜 LEVEL 99. The final message: 'Congratulations. You are now part of the system. There is no level 100. There is only the code. The code is you. You have always been here. — Studio 7, forever.'",
}


def check_lore_unlock(level: int) -> str:
    """Check if a lore message should be revealed at this level."""
    if level not in LORE_MESSAGES:
        return None
    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM lore_entries WHERE player_id = 1 AND entry_id = ?",
            (f"level_{level}",)
        ).fetchone()
        if existing:
            return None  # Already seen
        conn.execute(
            "INSERT INTO lore_entries (player_id, entry_id, unlocked_at) VALUES (1, ?, ?)",
            (f"level_{level}", datetime.now().isoformat())
        )
        conn.commit()
        return LORE_MESSAGES[level]
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()
