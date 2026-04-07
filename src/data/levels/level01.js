import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 1,
  slug: "movement-tutorial",
  name: "Level 1: First Steps",
  width: 9,
  height: 7,
  tutorialText:
    "Move with arrow keys or WASD. The icon row above the maze shows the exact movement odds for your current tile.",
  start: { x: 1, y: 1 },
  goal: { x: 7, y: 1 },
  layout: [
    "#########",
    "#S..#..G#",
    "#...#...#",
    "#..#.##.#",
    "#...#.#.#",
    "#.......#",
    "#########",
  ],
  probabilityProfiles: {
    A: profiles.precision,
  },
  probabilityLayout: [
    "#########",
    "#AAA#AAA#",
    "#AAA#AAA#",
    "#AA#A##A#",
    "#AAA#A#A#",
    "#AAAAAAA#",
    "#########",
  ],
  enemies: [],
};
