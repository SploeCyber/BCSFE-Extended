# BCSFE-Extended

An extended fork of [fieryhenry's BCSFE](https://codeberg.org/fieryhenry/BCSFE-Python) — a Python command
line save editor for The Battle Cats.

BCSFE-Extended is based on upstream `3.6.0`. Everything upstream does still works the same
way; it just adds a few new features and bug fixes.

## What's new in BCSFE-Extended

### New features

- **Max All** — pick any combination of items from one menu and max them all at once (catfood, XP,
  tickets, platinum shards, NP, leadership, battle items, catfruit, catseyes, catamins, labyrinth
  medals and more), then see a before/after summary of what changed.
- **Clear All Stages** — clears every stage in every chapter type from the same Max All menu
  (story, SoL, events, collab, Uncanny Legends, Catamin stages, Legend Quest, towers, gauntlets,
  Enigma, Behemoth Culling, Zero Legends, Dojo and Aku Realms). Existing clear counts are kept,
  never lowered, and the next chapters are unlocked so you can keep playing.
- **Energy editor** — set your current energy directly, capped at the game's maximum, and reset the
  energy penalty timestamp so energy actually regenerates.
- **Catfruit maxing** — catfruit can now be maxed.
…and more.

> [!WARNING]
> **Max All is risky.** It writes large values straight into your save, and injected currencies or
> items are the most common reason accounts get banned. Back up your save and read
> [Keeping your account unbanned](#keeping-your-account-unbanned) before using it.

### Game data

- Game data now comes from [BCData-Auto](https://github.com/SploeCyber/BCData-Auto) by default.

### Bug fixes

Fixes for bugs that exist in upstream BCSFE:

- Fixed event tickets being written to the wrong item when some entries weren't editable.
- Fixed the special skills storage check counting the wrong list.
- Fixed Gamatoto helpers crashing the editor with too many helpers.
- Fixed the ITF timed score editor recursing until it hit Python's recursion limit on bad input.
- Fixed treasure editing aborting when a chapter had no treasure group data.
- Fixed crashes on saves with unreadable or out of range dates.
- Fixed `all` in range inputs skipping the maximum value.
- Fixed `python -m bcsfe` running the editor twice on import.
…and more.

## Installation

**BCSFE-Extended is not on PyPI.** `pip install bcsfe` installs the *upstream* release, not this fork, so
install from source or from git. Your install method decides how you update later, so pick one and
stick with it.

Requirements: Python 3.9+ and git. On Linux you may also want `tk` (`python3-tk`) for the graphical
file picker, and depending on your distro you may need a virtual environment because of PEP 668.

### Option 1: editable install from a clone (recommended)

Easy to update — `git pull` applies changes immediately, no reinstall needed.

```sh
git clone https://github.com/SploeCyber/BCSFE-Extended.git
cd BCSFE-Extended
python -m pip install -e .
python -m bcsfe
```

### Option 2: install straight from git (no clone)

```sh
python -m pip install -U git+https://github.com/SploeCyber/BCSFE-Extended.git
python -m bcsfe
```

### Option 3: virtual environment (recommended on Linux / macOS)

Keep everything in a project-local environment so it can't clash with system packages:

```sh
git clone https://github.com/SploeCyber/BCSFE-Extended.git
cd BCSFE-Extended
python -m venv .venv
source .venv/bin/activate
pip install -e .
bcsfe
```

### Platform notes

#### Windows

Same commands as above:

```powershell
git clone https://github.com/SploeCyber/BCSFE-Extended.git
cd BCSFE-Extended
python -m pip install -e .
python -m bcsfe
```

#### Android (Termux)

```sh
pkg install python git
git clone https://github.com/SploeCyber/BCSFE-Extended.git
cd BCSFE-Extended
pip install -e .
python -m bcsfe
```

Ignore tkinter warnings on mobile — instead of a file picker you just type the path, e.g.
`/storage/emulated/0/Download/SAVE_DATA`.

### Running it

Either run `bcsfe` (if your `~/.local/bin` or scripts directory is on `PATH`) or
`python -m bcsfe`.

## Updating

Use the row for the install method you chose above.

| Install method | How to update |
| --- | --- |
| Option 1: editable clone | `cd BCSFE-Extended`, `git pull` |
| Option 2: pip install from git | Rerun `python -m pip install -U git+https://github.com/SploeCyber/BCSFE-Extended.git` |
| Option 3: virtual environment | Activate it (`source .venv/bin/activate`), then `cd BCSFE-Extended` and `git pull` |
| Windows | Same as your install method |
| Termux | `cd BCSFE-Extended` and `git pull` |

An editable install (the default for Options 1 and 3) picks up pulled changes the next time you
start the editor. A non-editable git install (Option 2) must be rerun with `-U` to get new commits.

If `bcsfe` suddenly can't be found after updating a virtual environment, activate the environment
again before running it.

## Usage

Same workflow as upstream:

1. In The Battle Cats go to `Settings` -> `Change Account / Device` -> `Change Device` ->
   `Retrieve Data from Old Device` -> `Save Data to Server`. Note the transfer and confirmation
   codes.
2. In the editor pick `Download save file using transfer and confirmation code` (option `1`),
   enter both codes, then choose your country code: `en`, `kr`, `jp`, `tw` (`en` also covers `it`,
   `es`, `fr`, `th`, `de`).
3. Make your edits. `q` backs out of most prompts.
4. Go to `Save Management` -> `Save changes and upload to game servers` — this gives you new codes.
5. In-game tap `Close Game` -> `Cancel Data Transfer`, then `Resume Data Transfer` ->
   `Transfer Data to New Device` and enter the new codes.

On a rooted device you can skip the transfer code dance and pull/push the save with adb or straight
from root storage.

### Keeping your account unbanned

- Use `Platinum Shards` instead of injecting platinum tickets.
- Use `Rare Ticket Trade` / normal ticket trade progress instead of injecting rare tickets.
- Instead of injecting catfood, edit things you'd buy with it (battle items, catamins, XP,
  leaderships), or farm catfood with `Catnip Challenges / Missions`.
- Instead of injecting tickets, just add the cats and upgrades you want directly.

If you do get banned, `Account` -> `Unban account` (or just re-uploading the save) usually clears it.

## Credits

- **fieryhenry** — original author of BCSFE. This fork is his work; all credit for the editor
  itself goes to him. Upstream lives on
  [Codeberg](https://codeberg.org/fieryhenry/BCSFE-Python) — upstream issues and PRs belong there.
  If you want to support him: [Ko-Fi](https://ko-fi.com/fieryhenry) /
  [LiberaPay](https://liberapay.com/fieryhenry).
- **Lethal** — the original editor that inspired BCSFE and helped work out save patching and
  catfood/XP editing.
- **Beeven** ([beeven/battlecats](https://github.com/beeven/battlecats)) and **csehydrogen**
  ([csehydrogen/BattleCatsHacker](https://github.com/csehydrogen/BattleCatsHacker)) — open source
  code that helped figure out how to patch save data.
- **HungJoesifer** — Vietnamese localization and the `discord` theme.
- **LinYuAn** — Traditional Chinese localization.
- Everyone who donated saves for testing.

BCSFE-Extended changes by [SploeCyber](https://github.com/SploeCyber).

## License

GPL-3.0-or-later, same as upstream. See [LICENSE](./LICENSE).
