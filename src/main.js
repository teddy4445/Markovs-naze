import Phaser from "phaser";
import { gameConfig } from "./game/config.js";

window.addEventListener("load", () => {
  const existingGame = window.__MARKOVS_MAZE_GAME__;
  if (existingGame) {
    existingGame.destroy(true);
  }

  window.__MARKOVS_MAZE_GAME__ = new Phaser.Game(gameConfig);
});
