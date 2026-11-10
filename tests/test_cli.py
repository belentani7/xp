from engine import cli, rpg
from pathlib import Path


def test_help_is_available(capsys):
    assert cli.main(["--help"]) == 0
    assert "install-hooks" in capsys.readouterr().out


def test_init_creates_character_and_is_idempotent(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rpg, "DB_PATH", tmp_path / "player.db")
    monkeypatch.setattr(rpg, "get_time_bonus", lambda: ("normal", 1.0))

    assert cli.main(["init", "--name", "Ada"]) == 0
    rpg.award_xp("feature", "test progress")
    before = rpg.get_player()

    assert cli.main(["init"]) == 0
    after = rpg.get_player()

    assert before["name"] == after["name"] == "Ada"
    assert before["xp"] == after["xp"] == 40
    assert "already initialized" in capsys.readouterr().out.lower()


def test_packaged_schema_matches_repository_schema():
    root = Path(__file__).resolve().parents[1]
    assert (root / "engine" / "schema.sql").read_bytes() == (root / "database" / "schema.sql").read_bytes()
