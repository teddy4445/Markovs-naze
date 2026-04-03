import { probabilityProfiles as profiles } from "./profiles.js";
import { point } from "./helpers.js";

export default {
  id: 9,
  slug: "twin-sentries",
  name: "Level 9: Twin Sentries",
  width: 12,
  height: 9,
  tutorialText:
    "Two knights now patrol at once. The layout stays open, so keep moving and use the traps as space-control rather than a dead end.",
  start: { x: 1, y: 1 },
  goal: { x: 10, y: 4 },
  layout: [
    "############",
    "#S....T....#",
    "#..#....#..#",
    "#....##....#",
    "#..T....T.G#",
    "#....##....#",
    "#..#....#..#",
    "#..........#",
    "############",
  ],
  probabilityProfiles: {
    A: profiles.precision,
    B: profiles.steady,
  },
  probabilityLayout: [
    "############",
    "#AABBBAABBA#",
    "#BB#AABB#AA#",
    "#AABB##BBAA#",
    "#ABBBAABBAA#",
    "#BBAA##AABB#",
    "#AA#BBBB#AA#",
    "#BBBBAAAABB#",
    "############",
  ],
  enemies: [
    {
      id: "knight-9a",
      start: { x: 3, y: 7 },
      patrolPath: [
        point(1, 7),
        point(2, 7),
        point(3, 7),
        point(4, 7),
        point(4, 6),
        point(4, 5),
        point(3, 5),
        point(2, 5),
        point(1, 5),
        point(1, 6),
      ],
    },
    {
      id: "knight-9b",
      start: { x: 10, y: 1 },
      patrolPath: [
        point(10, 1),
        point(9, 1),
        point(8, 1),
        point(7, 1),
        point(7, 2),
        point(7, 3),
        point(8, 3),
        point(9, 3),
        point(10, 3),
        point(10, 2),
      ],
    },
  ],
};
