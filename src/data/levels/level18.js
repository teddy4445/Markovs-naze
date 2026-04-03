import { probabilityProfiles as profiles } from "./profiles.js";
import { point } from "./helpers.js";

export default {
  id: 18,
  slug: "compressed-mastery",
  name: "Level 18: Compressed Mastery",
  width: 12,
  height: 8,
  tutorialText:
    "Another short final chamber: two knights patrol around the key while lava and broken lines leave very little room for recovery.",
  start: { x: 1, y: 1 },
  goal: { x: 10, y: 1 },
  layout: [
    "############",
    "#S...#...#G#",
    "#..L.#.#...#",
    "#....L#....#",
    "#.##...L.#.#",
    "#.....#....#",
    "#..#..K..#.#",
    "############",
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
    "############",
    "#AABB#CCD#A#",
    "#BBEC#C#DDA#",
    "#CCCDD#EEAA#",
    "#A##DDDEA#A#",
    "#BCDDE#ECCA#",
    "#BB#CCDEA#A#",
    "############",
  ],
  enemies: [
    {
      id: "knight-18a",
      start: { x: 1, y: 5 },
      patrolPath: [
        point(1, 5),
        point(2, 5),
        point(3, 5),
        point(4, 5),
        point(5, 5),
        point(5, 6),
        point(4, 6),
      ],
    },
    {
      id: "knight-18b",
      start: { x: 8, y: 5 },
      patrolPath: [
        point(8, 5),
        point(7, 5),
        point(7, 6),
        point(8, 6),
        point(8, 5),
        point(9, 5),
        point(10, 5),
        point(10, 6),
      ],
    },
  ],
};
