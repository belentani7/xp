# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import sqlite3
from shlex import quote
from pathlib import Path

import pytest

from engine import hook_runner, hooks, rpg


def git_repo(path):
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)


def git_identity(path):
    subprocess.run(["git", "-C", str(path), "config", "user.name", "XP Test"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "xp@example.test"], check=True)


def test_install_and_uninstall_only_remove_xp_hooks(tmp_path):
    git_repo(tmp_path)
    hooks.install_hooks(tmp_path, sys.executable)
    post_commit = tmp_path / ".git" / "hooks" / "post-commit"
    post_merge = tmp_path / ".git" / "hooks" / "post-merge"

    assert hooks.is_xp_hook(post_commit)
    assert hooks.is_xp_hook(post_merge)

    hooks.uninstall_hooks(tmp_path)
    assert not post_commit.exists()
    assert not post_merge.exists()


def test_install_refuses_to_overwrite_an_existing_hook(tmp_path):
    git_repo(tmp_path)
    hook_dir = tmp_path / ".git" / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    existing = hook_dir / "post-commit"
    existing.write_text("#!/bin/sh\necho another hook\n")

    with pytest.raises(FileExistsError):
        hooks.install_hooks(tmp_path, sys.executable)

    assert existing.read_text() == "#!/bin/sh\necho another hook\n"


def test_hook_launcher_quotes_interpreter_path():
    interpreter = "/opt/XP User's Python/python"
    script = hooks.hook_contents(interpreter, "post-commit")
    assert quote(interpreter) in script
    assert "engine.hook_runner post-commit" in script


def test_commit_message_is_passed_as_data_not_code(tmp_path, monkeypatch):
    message = "feat: value'; __import__('os').remove('important')"
    git_repo(tmp_path)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "XP Test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "xp@example.test"], check=True)
    (tmp_path / "note.txt").write_text("test")
    subprocess.run(["git", "-C", str(tmp_path), "add", "note.txt"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", message], check=True, capture_output=True)
    monkeypatch.chdir(tmp_path)

    assert hook_runner.read_commit_message() == message


def test_hook_fails_open_when_the_game_engine_errors(monkeypatch):
    monkeypatch.setattr(hook_runner, "read_commit_message", lambda: "feat: test")
    monkeypatch.setattr(rpg, "init_database", lambda: (_ for _ in ()).throw(OSError("disk")))

    assert hook_runner.main("post-commit") == 0


def test_post_commit_hook_awards_xp_without_blocking_git(tmp_path):
    git_repo(tmp_path)
    git_identity(tmp_path)
    hooks.install_hooks(tmp_path, sys.executable)
    profile = tmp_path / "profile"
    profile.mkdir()
    env = os.environ.copy()
    env["HOME"] = str(profile)
    env["USERPROFILE"] = str(profile)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    (tmp_path / "note.txt").write_text("first commit")
    subprocess.run(["git", "-C", str(tmp_path), "add", "note.txt"], check=True, env=env)

    result = subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "feat: initial character quest"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )

    database = profile / ".xp" / "player.db"
    with sqlite3.connect(str(database)) as connection:
        player = connection.execute("SELECT xp FROM player WHERE id = 1").fetchone()
    assert result.returncode == 0
    assert database.exists()
    assert player[0] > 0
