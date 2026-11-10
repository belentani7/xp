# Acceptance tests — GWT

## Installable CLI

- **Given** XP is installed without the source checkout, **when** a user runs `xp --help`, **then** the actual command list is shown and exits successfully.
- **Given** an empty data directory, **when** a user runs `xp init --name Ada`, **then** a level-one Ada character is created.
- **Given** an existing character with earned XP, **when** `xp init` runs again, **then** the character and XP are unchanged.

## Repository integration

- **Given** a repository with no XP hook, **when** `xp install-hooks` runs, **then** post-commit and post-merge XP hooks are installed for that repository.
- **Given** an unrelated existing hook, **when** installation runs, **then** it refuses and preserves the file.
- **Given** XP-owned hooks, **when** `xp uninstall-hooks` runs, **then** only those hooks are removed.
- **Given** XP raises an internal error during post-commit, **when** Git commits, **then** the commit remains successful.

## Landing page

- **Given** the static site is served from the repository root or `/site/`, **when** a visitor follows navigation or copies the install command, **then** each destination/action works and the instructions match the packaged product.
