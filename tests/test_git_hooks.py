"""Exercise the installed hooks with real Git commits in a disposable profile."""

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GitHookIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.bash = os.environ.get("XP_TEST_BASH") or shutil.which("bash")
        if not self.bash or not shutil.which("git"):
            self.skipTest("Bash and Git are required")

        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.profile = self.workspace / "xp-profile"
        self.repository = self.workspace / "git-repo"
        self.global_config = self.workspace / "gitconfig"
        self.global_config.write_text(
            "[core]\n\thooksPath = /existing/hooks\n", encoding="utf-8"
        )
        self.env = os.environ.copy()
        self.env.update({
            "XP_HOME": self.profile.as_posix(),
            "XP_BIN_DIR": (self.workspace / "bin").as_posix(),
            "XP_PYTHON": Path(sys.executable).as_posix(),
            "GIT_CONFIG_GLOBAL": self.global_config.as_posix(),
        })

        self.run_checked([self.bash, "install.sh"], cwd=ROOT)
        self.assertIn("hooksPath = /existing/hooks", self.global_config.read_text(encoding="utf-8"))
        self.assertTrue((self.workspace / "bin" / "xp").exists())
        self.run_checked(["git", "init", "-q", "-b", "main", str(self.repository)], cwd=ROOT)
        self.git("config", "user.name", "XP Test")
        self.git("config", "user.email", "xp-test@example.invalid")
        self.git("config", "core.hooksPath", (self.profile / "hooks").as_posix())

    def run_checked(self, command, cwd=None):
        result = subprocess.run(
            command,
            cwd=cwd or self.repository,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def git(self, *arguments):
        return self.run_checked(["git", *arguments])

    def xp_log(self):
        with closing(sqlite3.connect(self.profile / "player.db")) as connection:
            return connection.execute(
                "SELECT action_type, amount, reason FROM xp_log ORDER BY id"
            ).fetchall()

    def test_opt_in_preserves_an_existing_global_hooks_path(self):
        self.env["XP_INSTALL_GLOBAL_HOOKS"] = "1"
        result = self.run_checked([self.bash, "install.sh"], cwd=ROOT)
        self.assertIn("Existing global Git hooks preserved", result.stdout)
        self.assertIn("hooksPath = /existing/hooks", self.global_config.read_text(encoding="utf-8"))

    def test_commit_and_merge_messages_are_data_not_code(self):
        commit_message = (
            "fix: '''; __import__('pathlib').Path('COMMIT_EXECUTED')"
            ".write_text('bad'); '''"
        )
        (self.repository / "sample.txt").write_text("hello\n", encoding="utf-8")
        self.git("add", "sample.txt")
        self.git("commit", "-q", "-m", commit_message)

        rows = self.xp_log()
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0][0], "bugfix")
        self.assertIn(commit_message, rows[0][2])
        self.assertFalse((self.repository / "COMMIT_EXECUTED").exists())

        self.git("checkout", "-q", "-b", "feature")
        (self.repository / "feature.txt").write_text("feature\n", encoding="utf-8")
        self.git("add", "feature.txt")
        self.git("commit", "-q", "-m", "feat: second commit")
        self.git("checkout", "-q", "main")

        merge_message = (
            "Merge feature '''; __import__('pathlib').Path('MERGE_EXECUTED')"
            ".write_text('bad'); '''"
        )
        self.git("merge", "--no-ff", "-q", "feature", "-m", merge_message)

        rows = self.xp_log()
        self.assertEqual(len(rows), 3, rows)
        self.assertEqual(rows[-1][0], "pr_merge")
        self.assertIn(merge_message, rows[-1][2])
        self.assertFalse((self.repository / "MERGE_EXECUTED").exists())

    def test_fast_forward_merge_does_not_award_boss_xp(self):
        (self.repository / "sample.txt").write_text("hello\n", encoding="utf-8")
        self.git("add", "sample.txt")
        self.git("commit", "-q", "-m", "feat: initial commit")
        self.git("checkout", "-q", "-b", "feature")
        (self.repository / "feature.txt").write_text("feature\n", encoding="utf-8")
        self.git("add", "feature.txt")
        self.git("commit", "-q", "-m", "feat: branch commit")
        self.git("checkout", "-q", "main")
        self.git("merge", "--ff-only", "-q", "feature")

        rows = self.xp_log()
        self.assertEqual(len(rows), 2, rows)
        self.assertNotIn("pr_merge", [row[0] for row in rows])


if __name__ == "__main__":
    unittest.main()
