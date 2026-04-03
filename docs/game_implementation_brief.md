# Markov's Maze - Game Implementation Brief

## Purpose
This document defines the implementation requirements for building the playable game logic for **Markov's Maze** using the assets and documentation already prepared in this repository.

This phase is for **game implementation**, not asset generation.

The implementation must reuse:
- existing documentation
- generated assets
- manifests
- filenames
- folder structure

Do not rename assets unless absolutely necessary, and if a rename is unavoidable, update all manifests and document it clearly.

---

## Core game concept
Markov's Maze is a browser-based 2D puzzle maze game built with **Phaser 3**.

The game takes place in fantasy ruins. The player moves on a tile grid, but movement is **probabilistic** rather than deterministic.

Each walkable tile defines five probabilities:
- intended direction
- opposite direction
- 90 degree left
- 90 degree right
- no movement

These probabilities are relative to the direction chosen by the actor.

---

## Core movement rules

### Player input
The player can attempt to move:
- up
- down
- left
- right

### Probability resolution
For the tile the actor is currently standing on, movement is resolved using the tile's probability profile:
- intended
- opposite
- left
- right
- stay

### Invalid movement handling
If a sampled movement result would move the actor into a wall:
- resample until a valid movement outcome is found

For enemies:
- also treat lethal tiles as invalid destinations
- if a move would place the enemy onto trap or lava, resample until valid

### Coordinate interpretation
Relative movement mapping depends on the chosen action:

If chosen action is UP:
- intended = up
- opposite = down
- left = left
- right = right
- stay = no movement

If chosen action is RIGHT:
- intended = right
- opposite = left
- left = up
- right = down
- stay = no movement

Equivalent logic applies to DOWN and LEFT.

---

## Tile system

### Required tile categories
- wall
- floor
- start
- goal
- trap
- lava

### Probability data
Every walkable tile must contain a probability definition:
- intended
- opposite
- left
- right
- stay

These values should be stored in the level data, not hard-coded into scene logic.

### Probability visibility
The player must be able to see tile probability information.

Implement this in two ways:
1. **On-tile visualization** using the generated compass-circle assets
2. **HUD probability panel** showing exact values for the tile currently occupied by the player

---

## Win and lose conditions

### Win
The player wins the level by reaching the goal tile.

### Lose
The player loses immediately if:
- stepping on trap
- stepping on lava
- touching an enemy

There is:
- no timer
- no move limit

---

## Enemy system

### Enemy type
The MVP includes one enemy type:
- cursed knight

### Patrol behavior
Each enemy has a predefined patrol path stored in level data.

When the enemy is not chasing:
- it follows the patrol path cyclically
- if displaced from the path, it should return to the closest point on the patrol path
- after returning, it continues patrolling

### Chase behavior
If the enemy has line of sight to the player:
- same row or same column
- no walls blocking view

then the enemy enters chase mode.

In chase mode:
- it moves toward the player
- its actual movement still uses the same tile probability system as the player

If the player is no longer visible:
- enemy exits chase mode
- returns to nearest patrol point
- resumes patrol

### Enemy restrictions
Enemies:
- cannot enter walls
- cannot enter trap or lava
- use resampling for invalid outcomes

---

## Required scenes

### MenuScene
Must include:
- title
- start game
- level select
- optional credits or settings only if easy to include

### LevelSelectScene
Must include:
- 8 levels
- locked/unlocked progression
- completed state
- ability to enter unlocked levels

### GameScene
Must include:
- maze rendering
- player
- enemy/enemies if present in level
- HUD
- restart
- return to menu
- win and lose overlays

---

## Level progression
There must be 8 handcrafted levels.

Suggested progression:
1. basic movement introduction
2. more tile probability variation
3. tighter corridor puzzles
4. hazard introduction
5. patrol path introduction
6. enemy line-of-sight chase
7. mixed hazards and enemy pressure
8. final combined mastery level

Levels should be stored in data files, ideally JSON or JS modules, and not embedded directly in scene logic.

---

## Save system
Use browser localStorage to store:
- unlocked levels
- completed levels
- basic settings if present

---

## Asset usage requirements
Use the generated assets from the existing asset pipeline wherever possible.

Expected asset groups include:
- tiles
- overlays
- player sprites
- enemy sprites
- VFX
- backgrounds
- logo
- menu UI
- level buttons
- HUD panels
- icons
- audio

If any generated asset is missing or inconsistent:
- use the documented placeholder if available
- do not block implementation
- document the missing or mismatched asset in a short report

---

## Technical expectations

### Rendering and structure
- single-page web game
- Phaser 3
- one canvas
- scene-based flow

### Architecture
Implement clean, reusable modules/classes for:
- Grid or TileMap model
- Tile helpers
- Level loader
- Probability resolver
- Player
- Enemy
- HUD / UI helpers
- Save manager

### Recommended code organization
Example structure:
- src/main.js
- src/game/config.js
- src/scenes/MenuScene.js
- src/scenes/LevelSelectScene.js
- src/scenes/GameScene.js
- src/entities/Player.js
- src/entities/Enemy.js
- src/core/ProbabilityResolver.js
- src/core/LevelLoader.js
- src/core/SaveManager.js
- src/data/levels/
- src/ui/

Adapt to the existing repository structure if one already exists.

---

## Input and controls

### Desktop
- arrow keys and WASD for movement
- R for restart
- ESC for pause if pause is implemented

### Optional mobile support
If easy to include:
- on-screen movement buttons

Desktop support is required.
Mobile support is optional in this phase.

---

## Visual behavior requirements
- tile-to-tile movement should be animated
- movement feedback must be readable
- blocked/resampled outcomes should feel intentional
- win and lose transitions should be visible
- enemy alert/chase state should be readable

---

## Audio behavior requirements
If audio assets are available, wire them into:
- movement
- blocked bump
- no move
- hazards
- enemy alert
- goal
- win
- lose
- menu/UI

If some audio assets are missing, implementation should still work without failing.

---

## Level data format requirements
Each level should define:
- id
- name
- width
- height
- tile layout
- start position
- goal position
- per-walkable-tile probability profile
- hazard positions
- enemy definitions
- enemy patrol path
- optional tutorial text

The format must be documented so future levels can be added easily.

---

## Required deliverables
This phase should produce:
1. a playable Phaser 3 game
2. scene flow for menu, level select, and gameplay
3. 8 playable levels
4. probabilistic movement system
5. enemy patrol and chase logic
6. local save progression
7. asset integration
8. lightweight documentation for how the code is organized

---

## Required documentation outputs
Create or update:
- docs/game_architecture.md
- docs/level_format.md
- docs/implementation_report.md

### docs/game_architecture.md
Should explain:
- modules
- scene flow
- main systems
- how probabilities are resolved
- how enemies work

### docs/level_format.md
Should explain:
- level schema
- tile encoding
- probability encoding
- enemy path encoding
- how to add a new level

### docs/implementation_report.md
Should explain:
- what was implemented
- what assets were used
- what fallback placeholders were used
- known issues
- next suggested improvements

---

## Definition of done
This implementation phase is complete when:
- the game launches successfully
- menu works
- level select works
- at least 8 levels are playable
- player movement uses tile-based probabilities
- wall collisions are handled by resampling
- enemy patrol/chase works
- win/lose conditions work
- local progression saves
- generated assets are wired into the game where available
- documentation is updated
- the project is ready for polishing and iteration