# XP Commercial Product Implementation Plan

> Implementation is performed natively in the current session.

**Goal:** Ship an installable, local-first XP Coding RPG and accurate static product page.

**Architecture:** Put the CLI in `engine.cli`, keep domain rules in `engine.rpg`, package the SQLite schema, and manage opt-in per-repository Python hooks. Keep the landing static and dependency-free.

**Tech Stack:** Python 3.7+, SQLite, setuptools, pytest, HTML/CSS/JavaScript.

**Spec:** `docs/product/DESIGN.md`

## Global Constraints

- Python 3.7+, stdlib runtime only.
- No remote services or game-economy changes.
- XP data stays at `~/.xp/player.db`.
- Hooks are explicit and repository-local.
- Static site, no build step.

## Review Focus

- Existing player data must survive repeated init.
- Wheel installation must find the packaged schema after checkout is absent.
- Hook setup must not overwrite existing third-party hooks.
- Hook execution errors must not fail a commit.
- Site links, copy and accessible controls must lead somewhere useful.

---

### Task 1: Packaged CLI and safe initialization

**Files:** `engine/cli.py`, `engine/__main__.py`, `engine/rpg.py`, `engine/schema.sql`, root `xp`, `setup.py`, `tests/test_cli.py`

- [x] Make the parser/dispatcher callable as `engine.cli:main` and add `python -m engine`.
- [x] Make `xp init --name NAME` idempotent and preserve an existing character.
- [x] Package schema with `engine`; use `importlib.resources`-compatible access on Python 3.7.
- [x] Add GWT tests for init, help, entrypoint and packaged schema; run them and full suite.
- [x] Build sdist and wheel without installing project dependencies.

### Task 2: Repository-local hooks

**Files:** `engine/hooks.py`, `engine/hook_runner.py`, `tests/test_hooks.py`, `README.md`

- [x] Install post-commit and post-merge hook launchers using `sys.executable`.
- [x] Refuse third-party hook overwrite; remove only XP-owned hooks.
- [x] Invoke Git safely and classify/award activity without interpolating commit text into code.
- [x] Test temporary repositories, ownership refusal, XP award, and fail-open behavior.
- [x] Document install, opt-in integration, removal and troubleshooting.

### Task 3: Product landing page

**Files:** `index.html`, `site/index.html`, `hero.css`, `hero.js`

- [x] Replace generic template copy and colors with the actual local-first product, install command, real commands, features and FAQ.
- [x] Keep both served copies identical; ensure anchors and copy buttons work without a build.
- [x] Meet canon, contrast, keyboard, mobile and reduced-motion rules; remove unneeded shader animation.
- [x] Verify HTML structure, link targets, site copy and duplicate parity.
