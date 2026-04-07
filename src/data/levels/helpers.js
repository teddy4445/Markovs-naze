export function point(x, y) {
  return { x, y };
}

const FLOOR_SWAP_RULES = [
  { id: "swapOpposite", ratio: 0.1, a: "intended", b: "opposite", label: "Reversed" },
  { id: "swapLeft", ratio: 0.07, a: "intended", b: "left", label: "Left Shifted" },
  { id: "swapRight", ratio: 0.07, a: "intended", b: "right", label: "Right Shifted" },
  { id: "swapStay", ratio: 0.03, a: "intended", b: "stay", label: "Sticky" },
];

const PROFILE_KEY_POOL = "GHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@$%&?!+=*";

function cloneProfile(profile, labelSuffix, a, b) {
  return {
    ...profile,
    label: `${profile.label} ${labelSuffix}`,
    [a]: profile[b],
    [b]: profile[a],
  };
}

function hashTile(levelId, x, y) {
  let hash = (levelId * 2654435761) >>> 0;
  hash ^= Math.imul(x + 1, 2246822519);
  hash ^= Math.imul(y + 1, 3266489917);
  hash = Math.imul(hash ^ (hash >>> 15), 2246822519) >>> 0;
  hash = Math.imul(hash ^ (hash >>> 13), 3266489917) >>> 0;
  return (hash ^ (hash >>> 16)) >>> 0;
}

function allocateVariantKey(usedKeys) {
  const nextKey = [...PROFILE_KEY_POOL].find((candidate) => !usedKeys.has(candidate));
  if (!nextKey) {
    throw new Error("Ran out of probability profile keys for floor swap variants.");
  }
  usedKeys.add(nextKey);
  return nextKey;
}

export function applyFloorProbabilitySwaps(level) {
  const probabilityLayout = level.probabilityLayout.map((row) => row.split(""));
  const probabilityProfiles = { ...level.probabilityProfiles };
  const usedKeys = new Set([...Object.keys(probabilityProfiles), "#"]);
  const floorTiles = [];

  for (let y = 0; y < level.height; y += 1) {
    for (let x = 0; x < level.width; x += 1) {
      if (level.layout[y][x] !== ".") {
        continue;
      }

      floorTiles.push({
        x,
        y,
        probabilityKey: probabilityLayout[y][x],
        score: hashTile(level.id, x, y),
      });
    }
  }

  if (!floorTiles.length) {
    return level;
  }

  const orderedTiles = floorTiles
    .slice()
    .sort((a, b) => a.score - b.score || a.y - b.y || a.x - b.x);
  const variantKeyByRuleAndBase = new Map();
  let cursor = 0;

  FLOOR_SWAP_RULES.forEach((rule) => {
    const count = Math.floor(floorTiles.length * rule.ratio);
    for (let index = 0; index < count && cursor < orderedTiles.length; index += 1, cursor += 1) {
      const tile = orderedTiles[cursor];
      const mapKey = `${rule.id}:${tile.probabilityKey}`;

      if (!variantKeyByRuleAndBase.has(mapKey)) {
        const variantKey = allocateVariantKey(usedKeys);
        probabilityProfiles[variantKey] = cloneProfile(
          probabilityProfiles[tile.probabilityKey],
          `(${rule.label})`,
          rule.a,
          rule.b,
        );
        variantKeyByRuleAndBase.set(mapKey, variantKey);
      }

      probabilityLayout[tile.y][tile.x] = variantKeyByRuleAndBase.get(mapKey);
    }
  });

  return {
    ...level,
    probabilityProfiles,
    probabilityLayout: probabilityLayout.map((row) => row.join("")),
  };
}
