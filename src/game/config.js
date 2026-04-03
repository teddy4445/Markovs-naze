import Phaser from "phaser";
import { GAME_HEIGHT, GAME_WIDTH } from "./constants.js";
import { GameScene } from "../scenes/GameScene.js";
import { HowToPlayScene } from "../scenes/HowToPlayScene.js";
import { LevelSelectScene } from "../scenes/LevelSelectScene.js";
import { MenuScene } from "../scenes/MenuScene.js";

export const gameConfig = {
  type: Phaser.AUTO,
  parent: "app",
  width: GAME_WIDTH,
  height: GAME_HEIGHT,
  backgroundColor: "#141319",
  render: {
    antialias: true,
    pixelArt: false,
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  scene: [MenuScene, HowToPlayScene, LevelSelectScene, GameScene],
};
