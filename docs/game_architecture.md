# Markov's Maze Game Architecture

## Runtime shape

The game is a single-page Phaser 3 application booted from `src/main.js` with one canvas and four scenes:

- `MenuScene`
- `HowToPlayScene`
- `LevelSelectScene`
- `GameScene`

`src/game/config.js` defines the Phaser configuration, canvas size, scale behavior, and scene order.

The local run workflow is:

1. `npm install`
2. `npm run dev`
3. Open the local Vite URL, by default `http://127.0.0.1:4173`

## Scene flow

### MenuScene

- Preloads all runtime art and audio from the existing manifests.
- Creates the shared animation definitions once assets are loaded.
- Plays menu music.
- Shows the main action buttons and routes to the dedicated how-to-play scene.
- Supports the `=` keyboard shortcut to unlock every mapped level in localStorage.
- Routes to the recommended unlocked level or the level select screen.

### HowToPlayScene

- Reuses the menu asset set and music.
- Shows the control rules, win/lose conditions, tile examples, and probability explanation in a dedicated reference scene.

### LevelSelectScene

- Reads progression from localStorage through `SaveManager`.
- Displays 18 smaller level buttons in a 6-column grid using unlocked / completed / locked UI assets.
- Starts `GameScene` for any unlocked level.

### GameScene

- Loads parsed level data from `LevelLoader`.
- Renders the board from tile data, probability overlays, patrol markers, and collectible key shards.
- Spawns the player and any cursed knight enemy definitions.
- Uses a top-of-board probability legend for the five movement outcomes.
- Shows level/objective/status info in a compact box below the maze.
- Lets the player hover tiles with the mouse to inspect that tile's exact probabilities.
- Places gameplay controls in the bottom-right corner.
- Runs turn-based movement, hazards, key pickup logic, win / lose flow, HUD updates, pause handling, and progression saving.
- Adds subtle background drift, pulsing special tiles, and randomized ambient rune / mote effects for extra scene life.

## Core modules

### `src/game/AssetRegistry.js`

- Reads `data/asset_manifest.json` and `data/audio_manifest.json`.
- Resolves processed asset paths to Vite-managed URLs through `import.meta.glob`.
- Keeps art and audio loading tied to the existing asset pipeline instead of hard-coded file paths.

### `src/game/preloadAssets.js`

- Preloads every runtime texture, sprite sheet, and audio file found through the manifests.

### `src/game/createAnimations.js`

- Defines reusable Phaser animation keys for player, enemy, and VFX sprite sheets.

### `src/core/SaveManager.js`

- Stores unlocked levels, completed levels, and sound/music settings in browser localStorage.
- Exposes helpers for progression gating and recommended level selection.
- Exposes a full-unlock helper used by the menu shortcut.

### `src/core/ProbabilityResolver.js`

- Maps relative outcomes (`intended`, `opposite`, `left`, `right`, `stay`) into absolute movement directions.
- Filters invalid destinations and samples from the valid conditional distribution, which matches the required resample behavior.
- Returns metadata used by HUD feedback and movement/VFX/audio decisions.

### `src/core/LevelLoader.js`

- Validates all level data modules at import time.
- Builds parsed grid cells with tile type, probability key, and resolved probability profile.
- Supports wall, floor, start, goal, trap, lava, and key tiles.
- Exposes helper functions for wall checks, lethal checks, walkability, and current-tile profile lookup.

### `src/core/AudioController.js`

- Centralizes scene-safe music switching and SFX playback.
- Respects sound/music settings and gracefully skips missing audio keys.

## Entities

### `src/entities/Player.js`

- Owns the scholar sprite, grid position, and movement/death/victory animation flow.

### `src/entities/Enemy.js`

- Owns cursed knight state, patrol index, chase/return mode, line-of-sight checks, and pathfinding back to patrol.
- Uses the same probability resolution pipeline as the player for actual movement.

## UI modules

### `src/ui/ImageButton.js`

- Reusable image-backed button with hover/press support and rectangle fallback.

### `src/ui/HUD.js`

- Renders the compact probability legend above the maze.
- Shows exact percentages for the current or hovered tile.
- Shows level name, objective state, and short status text in a compact panel below the maze.
- Places gameplay control buttons in the bottom-right corner.
- Renders vertically stacked overlay buttons for pause / win / lose panels.

## Gameplay loop in GameScene

1. Read the player tile's probability profile.
2. Resolve the intended input through `ProbabilityResolver`.
3. Resample away wall outcomes by excluding invalid destinations.
4. Animate the final player movement or stay result.
5. Check lose conditions:
   - hazard tile
   - direct enemy contact
6. Check collectible / objective conditions:
   - key shard pickup
   - locked goal without key
7. Check win condition:
   - goal tile after any required key has been collected
8. For each enemy:
   - detect line of sight
   - switch between patrol, chase, and return modes
   - choose an intended direction
   - resolve movement through the same probability system
   - apply enemy collision defeat if contact occurs
9. Update the HUD and active-tile highlight.

## Enemy behavior summary

- Patrols cyclically along `patrolPath`.
- If it sees the player in the same row or column with no wall between them, it switches to chase mode.
- If sight is broken after a chase, it finds the nearest patrol point and returns via grid pathfinding.
- Enemy movement still uses the tile under the enemy, not a separate AI-only probability table.
- Enemy movement treats walls, trap, and lava as invalid and therefore resamples away from them.

## Content structure

- Levels 1-4: more open onboarding layouts with multiple valid routes.
- Levels 5-8: original core arc of patrols, line-of-sight chase, and combined pressure.
- Level 7 now uses a guided 92% intended lava corridor.
- Levels 9-12: two-enemy stages with lighter wall density and more trap pressure.
- Levels 13-16: sealed-goal stages that require a key shard pickup before the exit counts.
- Levels 17-18: shorter mastery stages with two enemies, a key, and level-16-style pressure.

## Asset fallback strategy

- The current repository art is still placeholder-generated but fully wired in.
- Missing textures fall back to simple rectangles or text-backed controls where practical.
- Missing audio keys are skipped without breaking scene flow.
- Key levels reuse the existing `prop_rune_shard` art as the collectible key-shard marker.

## Extension guidance

For future work, keep the current data-driven boundary:

- Add new levels in `src/data/levels/`
- Add new probability profiles in `src/data/levels/profiles.js`
- Extend scenes by calling the existing resolver, loader, and save APIs rather than bypassing them
