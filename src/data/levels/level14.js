import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 14,
  slug: "sealed-hazards",
  name: "Level 14: Sealed Hazards",
  width: 11,
  height: 8,
  tutorialText:
    "Now the key sits on the last row beside lava. The goal will not clear the level until the shard has been picked up.",
  start: { x: 1, y: 1 },
  goal: { x: 8, y: 1 },
  layout: [
    "###########",
    "#S..T...G.#",
    "#...#..L..#",
    "#......L..#",
    "#.....L...#",
    "#..T......#",
    "#....LK...#",
    "###########",
  ],
  probabilityProfiles: {
    A: profiles.precision,
    B: profiles.steady,
    C: profiles.leftDrift,
    D: profiles.rightDrift,
    E: profiles.hesitant,
  },
  probabilityLayout: [
    "###########",
    "#AABBAADAA#",
    "#BBB#CCDAA#",
    "#BBEEDDDAA#",
    "#CCCDDDEEA#",
    "#BBEECCDDA#",
    "#BBBCCCDDA#",
    "###########",
  ],
  enemies: [],
};
