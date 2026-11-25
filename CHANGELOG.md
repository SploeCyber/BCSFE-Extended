# Changelog

This changelog starts with the BCSFE-Extended fork. History for upstream releases (3.5.x and
earlier) is kept in
[upstream BCSFE](https://codeberg.org/fieryhenry/BCSFE-Python/src/branch/main/CHANGELOG.md).

## [3.7.1] - 2026-11-25

### Changed

- Removed the multi-language locale system; the editor is now English only. The language config
option, external locale support and the bundled Traditional Chinese and Vietnamese locales were
removed.

### Added

- Game data version picker in `Editor` -> `Game data version`, listing the versions published by
the configured data repository (plus `Auto` to match the save file). A 15.7.0 save can be edited
with 15.7.1 data even when 15.7.0 data is already downloaded.

## [3.7.0] - 2026-11-25

First release of BCSFE-Extended, based on upstream BCSFE 3.6.0.

### Added

- **Max All** menu: pick any combination of items and max them all at once (catfood, XP, rare and
normal tickets, platinum shards, NP, leadership, battle items, catfruit, catseyes, catamins,
labyrinth medals and more), with a before/after summary of what changed.

- **Clear All Stages**: clears every stage in every chapter type (story, SoL, events, collab,
Uncanny Legends, Catamin stages, Legend Quest, towers, gauntlets, Enigma, Behemoth Culling, Zero
Legends, Dojo and Aku Realms). Existing clear counts are kept and the next chapters are unlocked.

- **Energy editor**: sets the current energy up to the game's maximum and resets the energy penalty
timestamp so energy regenerates again.

- Catfruit maxing, which upstream had left disabled.

### Changed

- Game data now comes from [BCData-Auto](https://github.com/SploeCyber/BCData-Auto) by default, a
self-updating repo that publishes new game versions. Existing configs are migrated automatically and
the URL can still be overridden in the config.

- The fork is now named BCSFE-Extended and installs as the `bcsfe-extended` distribution. The
`bcsfe` command and `python -m bcsfe` are unchanged.

### Fixed

- Event tickets being written to the wrong item when some entries were not editable.

- The special skills storage check counting the wrong list.

- Gamatoto helpers crashing the editor with too many helpers.

- The ITF timed score editor recursing until it hit Python's recursion limit on bad input.

- Treasure editing aborting when a chapter had no treasure group data.

- Crashes on saves with unreadable or out of range dates.

- `all` in range inputs skipping the maximum value.

- `python -m bcsfe` running the editor twice on import.

- The game not being relaunched when `monkey` is missing, falling back to `am start`.
