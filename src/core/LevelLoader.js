import { levels } from "../data/levels/index.js";
import { applyFloorProbabilitySwaps } from "../data/levels/helpers.js";

function clone(data) {
  return JSON.parse(JSON.stringify(data));
}

function validateRows(level, rows, fieldName) {
  if (!Array.isArray(rows) || rows.length !== level.height) {
    throw new Error(`Level ${level.id} has invalid ${fieldName} height.`);
  }

  for (const row of rows) {
    if (row.length !== level.width) {
      throw new Error(`Level ${level.id} has invalid ${fieldName} width.`);
    }
  }
}

function validateLevel(level) {
  validateRows(level, level.layout, "layout");
  validateRows(level, level.probabilityLayout, "probabilityLayout");

  for (let y = 0; y < level.height; y += 1) {
    for (let x = 0; x < level.width; x += 1) {
      const tileChar = level.layout[y][x];
      const probabilityKey = level.probabilityLayout[y][x];
      const walkable = tileChar !== "#";

      if (walkable && !level.probabilityProfiles[probabilityKey]) {
        throw new Error(`Level ${level.id} is missing probability profile '${probabilityKey}' at ${x},${y}.`);
      }

      if (!walkable && probabilityKey !== "#") {
        throw new Error(`Level ${level.id} uses non-wall probability data on a wall tile at ${x},${y}.`);
      }
    }
  }

  return level;
}

function parseCell(tileChar, probabilityKey, probabilityProfiles) {
  const tileTypeMap = {
    "#": "wall",
    ".": "floor",
    S: "start",
    G: "goal",
    T: "trap",
    L: "lava",
    K: "key",
  };

  return {
    tile: tileTypeMap[tileChar] ?? "floor",
    probabilityKey,
    profile: probabilityProfiles[probabilityKey] ?? null,
  };
}

function buildParsedLevel(level) {
  const normalized = validateLevel(applyFloorProbabilitySwaps(clone(level)));
  const grid = normalized.layout.map((row, y) =>
    row.split("").map((tileChar, x) =>
      parseCell(tileChar, normalized.probabilityLayout[y][x], normalized.probabilityProfiles),
    ),
  );

  return {
    ...normalized,
    grid,
  };
}

const parsedLevels = levels.map((level) => buildParsedLevel(level));
const levelsById = new Map(parsedLevels.map((level) => [level.id, level]));

export class LevelLoader {
  static getAllLevels() {
    return parsedLevels.map((level) => clone(level));
  }

  static getLevel(levelId) {
    const level = levelsById.get(levelId);
    if (!level) {
      throw new Error(`Unknown level id: ${levelId}`);
    }
    return clone(level);
  }
}

export function getCell(level, x, y) {
  if (y < 0 || y >= level.height || x < 0 || x >= level.width) {
    return null;
  }
  return level.grid[y][x];
}

export function isWall(level, x, y) {
  return getCell(level, x, y)?.tile === "wall";
}

export function isWalkable(level, x, y) {
  return Boolean(getCell(level, x, y)) && !isWall(level, x, y);
}

export function isLethal(level, x, y) {
  const tile = getCell(level, x, y)?.tile;
  return tile === "trap" || tile === "lava";
}

export function getProbabilityProfile(level, x, y) {
  return getCell(level, x, y)?.profile ?? null;
}
