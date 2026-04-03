import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 2,
  slug: "tile-variation",
  name: "Level 2: Rune Variations",
  width: 10,
  height: 7,
  tutorialText:
    "Some runes drift left or right. A first lava tile appears here, so use the compass odds to choose the safer lane.",
  start: { x: 1, y: 1 },
  goal: { x: 8, y: 2 },
  layout: [
    "##########",
    "#S.......#",
    "#..#..#.G#",
    "#...L....#",
    "#.#....#.#",
    "#........#",
    "##########",
  ],
  probabilityProfiles: {
    A: profiles.precision,
    B: profiles.steady,
    C: profiles.leftDrift,
    D: profiles.rightDrift,
  },
  probabilityLayout: [
    "##########",
    "#AACDDDDD#",
    "#BC#CD#DA#",
    "#BBCCDDDA#",
    "#B#CCDD#A#",
    "#BBBCCDDA#",
    "##########",
  ],
  enemies: [],
};
