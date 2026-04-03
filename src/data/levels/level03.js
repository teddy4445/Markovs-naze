import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 3,
  slug: "narrow-passages",
  name: "Level 3: Broad Halls",
  width: 11,
  height: 8,
  tutorialText:
    "There are still pillars, but far more routes now. Two lava tiles raise the pressure while the wider spaces still let you recover from drift.",
  start: { x: 1, y: 1 },
  goal: { x: 9, y: 2 },
  layout: [
    "###########",
    "#S....#...#",
    "#...#..L#G#",
    "#..L......#",
    "#.#..#..#.#",
    "#.........#",
    "#...#.....#",
    "###########",
  ],
  probabilityProfiles: {
    A: profiles.precision,
    B: profiles.steady,
    C: profiles.leftDrift,
    D: profiles.rightDrift,
    E: profiles.hesitant,
    F: profiles.chaos,
  },
  probabilityLayout: [
    "###########",
    "#AABBC#CDA#",
    "#BBB#CCD#A#",
    "#BBCCCDDDA#",
    "#B#CE#DD#A#",
    "#CCCEEEDDA#",
    "#CCF#EEEDA#",
    "###########",
  ],
  enemies: [],
};
