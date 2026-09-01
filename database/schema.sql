-- XP Terminal RPG — Database Schema
-- SQLite 3.35+ compatible
-- The system remembers everything.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Player character
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

-- Character stats
CREATE TABLE IF NOT EXISTS stats (
    player_id INTEGER PRIMARY KEY REFERENCES player(id),
    str INTEGER NOT NULL DEFAULT 5,
    "int" INTEGER NOT NULL DEFAULT 5,
    dex INTEGER NOT NULL DEFAULT 5,
    wis INTEGER NOT NULL DEFAULT 5,
    cha INTEGER NOT NULL DEFAULT 5
);

-- Inventory / equipment
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES player(id),
    item_id TEXT NOT NULL,
    equipped INTEGER NOT NULL DEFAULT 0,
    equipped_slot TEXT DEFAULT NULL,
    acquired_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inventory_player ON inventory(player_id);

-- Achievements unlocked
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES player(id),
    achievement_id TEXT NOT NULL,
    unlocked_at TEXT NOT NULL,
    UNIQUE(player_id, achievement_id)
);

CREATE INDEX IF NOT EXISTS idx_achievements_player ON achievements(player_id);

-- Quest log
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

CREATE INDEX IF NOT EXISTS idx_quest_log_player ON quest_log(player_id);
CREATE INDEX IF NOT EXISTS idx_quest_log_status ON quest_log(player_id, status);

-- XP transaction log
CREATE TABLE IF NOT EXISTS xp_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES player(id),
    amount INTEGER NOT NULL,
    reason TEXT NOT NULL,
    action_type TEXT DEFAULT NULL,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_xp_log_player ON xp_log(player_id);
CREATE INDEX IF NOT EXISTS idx_xp_log_timestamp ON xp_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_xp_log_action ON xp_log(player_id, action_type);

-- Coding streaks
CREATE TABLE IF NOT EXISTS streaks (
    player_id INTEGER PRIMARY KEY REFERENCES player(id),
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_commit_date TEXT DEFAULT NULL
);

-- Hidden lore entries
CREATE TABLE IF NOT EXISTS lore_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES player(id),
    entry_id TEXT NOT NULL,
    unlocked_at TEXT NOT NULL,
    UNIQUE(player_id, entry_id)
);

CREATE INDEX IF NOT EXISTS idx_lore_player ON lore_entries(player_id);

-- Combat log (bugs defeated)
CREATE TABLE IF NOT EXISTS combat_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES player(id),
    enemy_name TEXT NOT NULL,
    enemy_hp INTEGER NOT NULL,
    damage_dealt INTEGER NOT NULL,
    xp_earned INTEGER NOT NULL,
    defeated INTEGER NOT NULL DEFAULT 0,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_combat_player ON combat_log(player_id);
