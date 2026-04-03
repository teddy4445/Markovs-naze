import Phaser from "phaser";
import { AudioController } from "../core/AudioController.js";
import { SaveManager } from "../core/SaveManager.js";
import { levels } from "../data/levels/index.js";
import { COLORS, FONT_FAMILY, GAME_HEIGHT, GAME_WIDTH } from "../game/constants.js";
import { createAnimations } from "../game/createAnimations.js";
import { preloadAllAssets } from "../game/preloadAssets.js";
import { ImageButton } from "../ui/ImageButton.js";

function coverImage(image, width, height) {
  const scale = Math.max(width / image.width, height / image.height);
  image.setScale(scale);
}

export class MenuScene extends Phaser.Scene {
  constructor() {
    super("MenuScene");
  }

  preload() {
    if (this.game.__markovsMazeAssetsLoaded) {
      return;
    }

    const loadingLabel = this.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 20, "Loading Markov's Maze...", {
        fontFamily: FONT_FAMILY,
        fontSize: "30px",
        color: COLORS.panelText,
      })
      .setOrigin(0.5);
    const progressLabel = this.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 24, "0%", {
        fontFamily: FONT_FAMILY,
        fontSize: "20px",
        color: COLORS.accent,
      })
      .setOrigin(0.5);

    this.load.on("progress", (value) => {
      progressLabel.setText(`${Math.round(value * 100)}%`);
    });

    this.load.once("complete", () => {
      loadingLabel.destroy();
      progressLabel.destroy();
      this.game.__markovsMazeAssetsLoaded = true;
    });

    preloadAllAssets(this);
  }

  create() {
    createAnimations(this);
    this.renderBackground();
    this.renderMenu();
    this.registerUnlockShortcut();
    AudioController.playMusic(this, "menu_theme", { volume: 0.32 });
  }

  renderBackground() {
    if (this.textures.exists("bg_main_menu_1920x1080")) {
      const background = this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, "bg_main_menu_1920x1080");
      coverImage(background, GAME_WIDTH, GAME_HEIGHT);
      background.setAlpha(0.94);
      this.tweens.add({
        targets: background,
        scaleX: background.scaleX * 1.02,
        scaleY: background.scaleY * 1.02,
        duration: 14000,
        yoyo: true,
        repeat: -1,
        ease: "Sine.InOut",
      });
    } else {
      this.cameras.main.setBackgroundColor(0x141319);
    }

    if (this.textures.exists("bg_long_ruins_parallax")) {
      const strip = this.add.image(GAME_WIDTH / 2, GAME_HEIGHT - 110, "bg_long_ruins_parallax");
      strip.setDisplaySize(GAME_WIDTH + 80, 210).setAlpha(0.22);
      this.tweens.add({
        targets: strip,
        x: GAME_WIDTH / 2 + 24,
        duration: 12000,
        yoyo: true,
        repeat: -1,
        ease: "Sine.InOut",
      });
    }
  }

  renderMenu() {
    const recommendedLevel = SaveManager.getRecommendedLevelId();
    const state = SaveManager.getState();
    const completedCount = state.completedLevelIds.length;

    if (this.textures.exists("logo_markovs_maze")) {
      const logo = this.add.image(GAME_WIDTH / 2, 136, "logo_markovs_maze");
      logo.setScale(0.56);
    } else {
      this.add
        .text(GAME_WIDTH / 2, 130, "Markov's Maze", {
          fontFamily: FONT_FAMILY,
          fontSize: "54px",
          color: COLORS.panelText,
        })
        .setOrigin(0.5);
    }

    this.add
      .text(GAME_WIDTH / 2, 226, "Ancient ruins. Uncertain paths.", {
        fontFamily: FONT_FAMILY,
        fontSize: "24px",
        color: COLORS.muted,
      })
      .setOrigin(0.5);

    this.add
      .text(GAME_WIDTH / 2, 270, `Recommended start: Level ${recommendedLevel}`, {
        fontFamily: FONT_FAMILY,
        fontSize: "20px",
        color: COLORS.accentWarm,
      })
      .setOrigin(0.5);

    new ImageButton(this, {
      x: GAME_WIDTH / 2,
      y: 366,
      textureKey: "btn_menu_primary_idle",
      hoverTextureKey: "btn_menu_primary_hover",
      pressedTextureKey: "btn_menu_primary_pressed",
      label: "Start Game",
      onClick: () => {
        AudioController.playSfx(this, "ui_click");
        this.scene.start("GameScene", { levelId: SaveManager.getRecommendedLevelId() });
      },
    });

    new ImageButton(this, {
      x: GAME_WIDTH / 2,
      y: 452,
      textureKey: "btn_menu_secondary_idle",
      hoverTextureKey: "btn_menu_secondary_hover",
      pressedTextureKey: "btn_menu_secondary_hover",
      label: "Level Select",
      onClick: () => {
        AudioController.playSfx(this, "ui_click");
        this.scene.start("LevelSelectScene");
      },
    });

    new ImageButton(this, {
      x: GAME_WIDTH / 2,
      y: 538,
      textureKey: "btn_menu_secondary_idle",
      hoverTextureKey: "btn_menu_secondary_hover",
      pressedTextureKey: "btn_menu_secondary_hover",
      label: "How To Play",
      onClick: () => {
        AudioController.playSfx(this, "ui_click");
        this.scene.start("HowToPlayScene");
      },
    });

    this.progressText = this.add
      .text(GAME_WIDTH / 2, 620, `${completedCount} of ${levels.length} levels completed`, {
        fontFamily: FONT_FAMILY,
        fontSize: "18px",
        color: COLORS.panelText,
      })
      .setOrigin(0.5);

  }

  registerUnlockShortcut() {
    this.handleMenuKey = (event) => {
      if (event.code !== "Equal" && event.key !== "=") {
        return;
      }

      SaveManager.unlockAllLevels();
      this.progressText.setText(`All ${levels.length} levels unlocked.`);
      this.progressText.setColor(COLORS.accentWarm);
      AudioController.playSfx(this, "ui_click", { volume: 0.55 });
    };

    this.input.keyboard.on("keydown", this.handleMenuKey);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.input.keyboard.off("keydown", this.handleMenuKey);
    });
  }
}
