# -*- coding: utf-8 -*-
"""Install XP's opt-in, repository-local Git hooks."""

import subprocess
from pathlib import Path
from shlex import quote


MARKER = "# XP managed hook. Remove with xp uninstall-hooks."


def hooks_directory(repo_path):
    result = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "--git-path", "hooks"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError("Run this command inside a Git repository.")
    path = Path(result.stdout.strip())
    return path if path.is_absolute() else Path(repo_path) / path


def is_xp_hook(path):
    try:
        return MARKER in Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False


def hook_contents(python_executable, hook_name):
    executable = str(python_executable).replace("\\", "/")
    return (
        "#!/bin/sh\n"
        f"{MARKER}\n"
        f"exec {quote(executable)} -m engine.hook_runner {hook_name}\n"
    )


def install_hooks(repo_path, python_executable):
    directory = hooks_directory(repo_path)
    directory.mkdir(parents=True, exist_ok=True)
    targets = [directory / "post-commit", directory / "post-merge"]
    conflicts = [str(path) for path in targets if path.exists() and not is_xp_hook(path)]
    if conflicts:
        raise FileExistsError("Existing non-XP hook(s) were preserved: " + ", ".join(conflicts))

    for path in targets:
        hook_name = path.name
        with path.open("w", encoding="utf-8", newline="\n") as hook_file:
            hook_file.write(hook_contents(python_executable, hook_name))
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except OSError:
            pass


def uninstall_hooks(repo_path):
    directory = hooks_directory(repo_path)
    for name in ("post-commit", "post-merge"):
        path = directory / name
        if is_xp_hook(path):
            path.unlink()


def commit_message_command():
    """Return a fixed Git argv; commit text is read from stdout, never code."""
    return ["git", "log", "-1", "--format=%B"]
