"""Fail-open entry point used by repository-local Git hooks."""

import subprocess
import sys

from . import rpg
from .hooks import commit_message_command


def read_commit_message():
    result = subprocess.run(
        commit_message_command(),
        check=False,
        capture_output=True,
        text=True,
        errors="replace",
    )
    if result.returncode:
        return ""
    return result.stdout.strip()


def main(hook_name=None):
    hook_name = hook_name or (sys.argv[1] if len(sys.argv) > 1 else "")
    try:
        if hook_name not in ("post-commit", "post-merge"):
            return 0
        message = read_commit_message()
        if not message:
            return 0
        rpg.init_database()
        if not rpg.get_player():
            rpg.create_player()
        action = rpg.classify_commit(message) if hook_name == "post-commit" else "pr_merge"
        result = rpg.award_xp(action, message[:100])
        rpg.update_streak()
        print(f"  +{result['xp_gained']} XP — {action}")
    except Exception:
        # A game integration must never interrupt a successful Git operation.
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
