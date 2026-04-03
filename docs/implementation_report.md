# Markov's Maze Implementation Report

## Current gameplay status

The repository now contains a playable Phaser 3 game with:

- one canvas, one-page architecture
- `MenuScene`
- `HowToPlayScene`
- `LevelSelectScene`
- `GameScene`
- 18 handcrafted data-driven levels
- tile-specific probabilistic movement
- wall-resample behavior
- goal, hazard, and enemy defeat conditions
- cursed knight patrol / chase / return behavior
- key-shard levels where the goal stays locked until the key is collected
- localStorage progression and sound/music settings
- menu, level select, win, lose, and pause flow

## Changes added in this pass

This implementation pass specifically added or changed:

- kept the five probability icons above the maze while moving the level/info box below the maze
- added mouse-hover tile inspection so the top probabilities can preview any hovered rune tile
- removed the body text from the level-cleared overlay and left the title plus buttons only
- added increasing lava presence in levels 2-4
- rebuilt level 7 around a guided lava corridor with 92% intended tiles
- moved how-to-play content into a dedicated `HowToPlayScene`
- added a new main-menu How To Play button
- added the `=` menu shortcut to unlock all levels
- reduced level-select buttons and laid them out in a 6-column grid
- refined the top HUD so it shows only the five icons and percentages, with the hover/move context below the maze
- added levels 17-18 as shorter two-enemy key stages near level-16 difficulty
- stacked the win / pause / lose overlay buttons vertically
- kept lava as an instant-loss tile
- expanded the campaign from 8 levels to 18
- added levels 9-12 with two enemies and lighter wall density
- added levels 13-16 with key-shard-before-goal progression
- added extra visual life through drifting layers, pulsing special tiles, ambient particles, and rune bursts

## Assets used

The game continues to reuse the existing asset pipeline and manifest output:

- tiles, overlays, player and enemy sprite sheets, VFX, UI panels, buttons, icons, and backgrounds from `assets/processed/`
- audio from `assets/processed/audio/`
- manifests from `data/asset_manifest.json` and `data/audio_manifest.json`

Asset loading remains manifest-driven through `src/game/AssetRegistry.js`.

## Fallbacks used

- All current art is still placeholder-generated art from the previous asset phase, but filenames and dimensions are already final-runtime stable.
- UI buttons and scene visuals fall back to rectangles/text if a texture is unavailable.
- Missing audio keys are skipped safely instead of breaking gameplay.
- The new key mechanic reuses the existing `prop_rune_shard` art as the collectible key-shard marker instead of introducing a new asset filename.

## Validation completed

Completed during this pass:

- `npm run build`
- direct level-data validation for all 18 handcrafted levels
- wall/probability alignment verification for all level grids
- reachability check for all non-key levels
- key-to-goal reachability check for levels 13-18
- enemy patrol tile validation after route cleanup

## Known issues

- Art is still placeholder-grade and should be upgraded later without changing filenames.
- Audio balancing and music loop feel have not been tuned in-browser beyond basic integration.
- The production bundle is large because Phaser and all scene code currently ship in one chunk.
- Full manual playtesting is still needed for difficulty, especially across the new level 9-18 progression and the compact HUD layout.

## Suggested next improvements

1. Add a lightweight automated browser smoke test for scene transitions and localStorage progression.
2. Tune enemy pacing and hazard density after hands-on playtesting.
3. Replace placeholder art with final generated or authored art using the existing manifests and prompt bank.
4. Add extra polish passes for transition effects, sound mixing, and responsive/mobile UI if desired.
