# Markov's Maze Audio Sourcing Report

## Scope

Audio sourcing was limited to OpenGameArt, per project rules. Only explicitly safe redistribution licenses were accepted. The retained set uses CC0 exclusively.

## Searches and candidate review

Reviewed OpenGameArt pages for:

- Interface and UI sounds
- Fantasy / RPG SFX packs
- Footstep packs
- Ambient horror or cursed hum candidates
- Dungeon and ruins music loops
- Lava / fire burst candidates

Retained source pages:

- `Interface Sounds` by Kenney
- `80 CC0 RPG SFX` by rubberduck
- `Different steps on wood, stone, leaves, gravel and mud` by TinyWorlds
- `Fantasy Sound Effects (Tinysized SFX)` by Vehicle
- `Ambient horror` by techiew
- `Village Ruins` by isaiah658
- `Dungeon Ambience` by yd
- `Dark Cavern Ambient` by Paul Wortmann

## What was downloaded and kept

Kept source archives or files in `assets/raw/audio/` for the selected set above, then extracted or copied stable raw source files and runtime-ready processed files.

Selected outcomes:

- Movement SFX: `player_step`, `player_move_intended`, `player_move_alternate`, `player_no_move`
- Hazard / goal SFX: `player_blocked_bump`, `trap_trigger`, `lava_hiss_or_burst`, `goal_activation`, `level_complete`, `defeat_sting`
- Enemy SFX: `enemy_idle_cursed_hum`, `enemy_move_armor_scrape`, `enemy_spotted_alert`
- UI SFX: `ui_hover`, `ui_click`, `restart_reset`
- Music: `menu_theme`, `early_gameplay_theme`, `late_gameplay_theme`

All retained items are documented in `data/audio_manifest.json` with:

- asset id
- local filename
- source page URL
- direct download URL
- title
- author
- chosen license
- attribution requirement
- category
- notes

## What was skipped

Skipped after review:

- `Lava splash`
  - Page was valid and safely licensed as CC-BY 3.0, but the available download was FLAC-only and a CC0 fire-burst alternative from the retained RPG pack covered the gameplay need with less licensing overhead.
- `Scrapes`
  - Pack was valid and CC0, but the retained `Tinysized SFX` metal scrape fit the cursed knight movement role better, so the redundant trial archive was removed from the repo.

## Licensing result

- Retained downloads: CC0 only
- Attribution required for retained downloads: none
- `assets/CREDITS.md` therefore records that no non-CC0 retained downloads currently require attribution

## Remaining audio work

- Audition final mix levels in Phaser once gameplay exists.
- If desired later, transcode the mixed WAV/OGG runtime set into a single preferred delivery format.
