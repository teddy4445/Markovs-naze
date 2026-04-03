import { probabilityProfiles as profiles } from "./profiles.js";

export default {
  id: 4,
  slug: "hazards",
  name: "Level 4: Hazard Memory",
  width: 11,
  height: 8,
  tutorialText:
    "Trap and lava tiles are lethal. This room now mixes several lava pools into the open layout, so route around danger instead of being forced into it.",
  start: { x: 1, y: 1 },
  goal: { x: 9, y: 1 },
  layout: [
    "###########",
    "#S..T....G#",
    "#...#..L..#",
    "#..L...T..#",
    "#.....#...#",
    "#..T.L..L.#",
    "#.........#",
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
    "#AABBAAAAA#",
    "#BBB#AAAAA#",
    "#BBECDDDBA#",
    "#BBCCB#DDA#",
    "#CCEEDDDEA#",
    "#BBBBCCCCA#",
    "###########",
  ],
  enemies: [],
};
