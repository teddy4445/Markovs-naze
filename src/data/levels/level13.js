import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 13,
  slug: "sealed-antechamber",
  name: "Level 13: Sealed Antechamber",
  width: 11,
  height: 8,
  tutorialText:
    "This chamber is sealed. Lava now guards two approaches, and the key shard waits on the last row before you can finish.",
  start: { x: 1, y: 1 },
  goal: { x: 9, y: 1 },
  layout: [
    "###########",
    "#S....#..G#",
    "#...#L.#..#",
    "#......#..#",
    "#...#.....#",
    "#..L..#...#",
    "#.....K...#",
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
    "#AABBC#CDA#",
    "#BBB#CC#AA#",
    "#BBEEDD#AA#",
    "#CCB#DDDEA#",
    "#CCDDE#EEA#",
    "#BBBCCCDDA#",
    "###########",
  ],
  enemies: [],
};
