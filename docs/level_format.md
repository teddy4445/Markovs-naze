# Markov's Maze Level Format

## File layout

Levels live in `src/data/levels/` as individual JS modules:

- `level01.js`
- `level02.js`
- ...
- `level18.js`

`src/data/levels/index.js` exports the ordered array consumed by `LevelLoader`.

## Level object schema

Each level module exports a plain object with these fields:

```js
{
  id: 13,
  slug: "sealed-antechamber",
  name: "Level 13: Sealed Antechamber",
  width: 11,
  height: 8,
  tutorialText: "Optional helper text shown briefly when the level starts.",
  start: { x: 1, y: 1 },
  goal: { x: 9, y: 1 },
  layout: [
    "###########",
    "#S....#..G#",
    "#...#..#..#",
    "#..K...#..#",
    "###########"
  ],
  probabilityProfiles: {
    A: { label: "Precision", intended: 0.88, opposite: 0.03, left: 0.03, right: 0.03, stay: 0.03 }
  },
  probabilityLayout: [
    "###########",
    "#AABBC#CDA#",
    "#BBB#CC#AA#",
    "#BBEEDD#AA#",
    "###########"
  ],
  enemies: [
    {
      id: "knight-15",
      start: { x: 8, y: 1 },
      patrolPath: [{ x: 7, y: 1 }, { x: 8, y: 1 }]
    }
  ]
}
```

## Tile encoding

`layout` is a rectangular array of strings using these tile characters:

- `#` = wall
- `.` = normal walkable floor
- `S` = start
- `G` = goal
- `T` = trap
- `L` = lava
- `K` = key shard

Rules:

- `layout.length` must equal `height`
- every `layout` row length must equal `width`
- `start` and `goal` coordinates should match the `S` and `G` positions in `layout`
- if a level contains `K`, the goal is considered locked until the player has collected that key shard

## Probability encoding

`probabilityLayout` mirrors the same dimensions as `layout`.

Rules:

- every wall tile must use `#` in the probability layout
- every non-wall tile must use a letter key found in `probabilityProfiles`
- probability profiles are relative to the actor's intended direction, not absolute map directions
- key, goal, start, trap, and lava tiles still need probability keys because they are walkable cells

Profile object format:

```js
{
  label: "Steady",
  intended: 0.72,
  opposite: 0.06,
  left: 0.08,
  right: 0.08,
  stay: 0.06
}
```

The five numeric values should sum to `1`.

## Enemy schema

Each enemy entry uses:

```js
{
  id: "knight-10a",
  start: { x: 8, y: 1 },
  patrolPath: [
    { x: 8, y: 1 },
    { x: 9, y: 1 },
    { x: 10, y: 1 }
  ]
}
```

Rules:

- patrol points should be contiguous orthogonal steps whenever practical
- patrol points must be walkable, non-lethal cells
- enemy start should be on or near the patrol path

## How the runtime uses the schema

`LevelLoader` validates:

- row counts
- row widths
- wall/probability alignment
- probability key existence

At load time it builds a parsed `grid[y][x]` cell structure with:

- `tile`
- `probabilityKey`
- `profile`

`GameScene` additionally infers whether a level requires a key by checking for `K` tiles in the parsed grid.

## Adding a new level

1. Copy an existing level file in `src/data/levels/`.
2. Update `id`, `slug`, `name`, `width`, `height`, `start`, `goal`, and `tutorialText`.
3. Edit `layout`.
4. Define or reuse any needed `probabilityProfiles`.
5. Edit `probabilityLayout` so every non-wall tile has a valid profile key.
6. Add enemy definitions if needed.
7. Export the new level from `src/data/levels/index.js`.
8. Run `npm run build`.
9. Run a quick schema or reachability check if you changed patrol routes or key requirements.

## Current shared profiles

Common profiles live in `src/data/levels/profiles.js`:

- `precision`
- `steady`
- `leftDrift`
- `rightDrift`
- `hesitant`
- `chaos`
- `guided`

These are reused across the 18 handcrafted levels to keep the visual overlays and HUD language consistent.
