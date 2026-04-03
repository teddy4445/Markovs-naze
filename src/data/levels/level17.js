import { probabilityProfiles as profiles } from "./profiles.js";
import { point } from "./helpers.js";

export default {
  id: 17,
  slug: "compressed-seal",
  name: "Level 17: Compressed Seal",
  width: 12,
  height: 8,
  tutorialText:
    "A shorter mastery chamber: two knights pressure the lower half while lava and walls keep the key route tight.",
  start: { x: 1, y: 1 },
  goal: { x: 10, y: 1 },
  layout: [
    "############",
    "#S..#....#G#",
    "#..L#..#...#",
    "#....L##...#",
    "#.##.....#.#",
    "#....#.....#",
    "#..#..K.#..#",
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
    "#AAB#CCDD#A#",
    "#BBE#CC#DAA#",
    "#CCCDD##EEA#",
    "#A##DDEED#A#",
    "#BCDD#EECCA#",
    "#BB#CCDE#AA#",
    "############",
  ],
  enemies: [
    {
      id: "knight-17a",
      start: { x: 1, y: 5 },
      patrolPath: [
        point(1, 5),
        point(2, 5),
        point(3, 5),
        point(4, 5),
        point(4, 6),
        point(5, 6),
        point(6, 6),
        point(7, 6),
      ],
    },
    {
      id: "knight-17b",
      start: { x: 10, y: 5 },
      patrolPath: [
        point(10, 5),
        point(9, 5),
        point(8, 5),
        point(7, 5),
        point(6, 5),
        point(6, 6),
        point(5, 6),
        point(4, 6),
      ],
    },
  ],
};
