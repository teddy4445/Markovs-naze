import Phaser from "phaser";
import { AudioController } from "../core/AudioController.js";
import { COLORS, FONT_FAMILY, GAME_HEIGHT, GAME_WIDTH } from "../game/constants.js";
import { ImageButton } from "../ui/ImageButton.js";

function coverImage(image, width, height) {
  const scale = Math.max(width / image.width, height / image.height);
  image.setScale(scale);
}

function createPanel(scene, x, y, width, height) {
  return scene.add
    .rectangle(x, y, width, height, COLORS.panelLightTextured, 0.95)
    .setStrokeStyle(2, COLORS.panelLightStroke, 0.72);
}

export class HowToPlayScene extends Phaser.Scene {
  constructor() {
    super("HowToPlayScene");
  }

  create() {
    this.renderBackground();
    this.renderContent();
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
  }

  renderContent() {
    createPanel(this, GAME_WIDTH / 2, GAME_HEIGHT / 2 + 8, 1116, 600).setAlpha(0.98);

    new ImageButton(this, {
      x: GAME_WIDTH / 2,
      y: 56,
      textureKey: "btn_menu_secondary_idle",
      hoverTextureKey: "btn_menu_secondary_hover",
      pressedTextureKey: "btn_menu_secondary_hover",
      label: "Menu",
      fallbackWidth: 170,
      fallbackHeight: 58,
      onClick: () => {
        AudioController.playSfx(this, "ui_click");
        this.scene.start("MenuScene");
      },
    });

    const instructions = [
      "Choose a direction with arrow keys or WASD. Each rune tile resolves that move using its five probabilities.",
      "If an outcome would move into a wall, that blocked result is resampled until a valid move remains.",
      "Reach the goal seal to clear the level.",
      "Trap tiles and lava tiles are instant defeat.",
      "Cursed knights patrol, chase when they see you in the same row or column, and return to patrol if sight is broken.",
      "In sealed levels, collect the key shard before the goal can finish the stage.",
      "Hover the mouse over maze tiles to inspect their exact probabilities.",
    ];

    let currentInstructionY = 116;
    instructions.forEach((line, index) => {
      const text = this.add
        .text(112, currentInstructionY, `- ${line}`, {
          fontFamily: FONT_FAMILY,
          fontSize: "18px",
          fontStyle: "bold",
          color: COLORS.ink,
          wordWrap: { width: 470 },
          lineSpacing: 6,
        })
        .setOrigin(0, 0);
      currentInstructionY += text.height + 20;
    });

    this.add
      .text(956, 126, "Tile Types", {
        fontFamily: FONT_FAMILY,
        fontSize: "28px",
        fontStyle: "bold",
        color: COLORS.ink,
      })
      .setOrigin(0.5);

    const samples = [
      { label: "Start", textureKey: "tile_start" },
      { label: "Goal", textureKey: "tile_goal" },
      { label: "Trap", textureKey: "tile_trap" },
      { label: "Lava", textureKey: "tile_lava" },
      { label: "Wall", textureKey: "tile_wall_a" },
      { label: "Floor", textureKey: "tile_floor_a" },
      { label: "Key Shard", textureKey: "prop_rune_shard" },
      { label: "Knight", textureKey: "enemy_cursed_knight_idle_base" },
    ];

    samples.forEach((sample, index) => {
      const x = 894 + (index % 2) * 188;
      const y = 214 + Math.floor(index / 2) * 92;

      if (this.textures.exists(sample.textureKey)) {
        this.add.image(x - 46, y, sample.textureKey).setDisplaySize(54, 54);
      } else {
        this.add.rectangle(x - 46, y, 54, 54, 0x2d2b33, 0.92).setStrokeStyle(2, 0x8ae3d5, 0.65);
      }

      this.add
        .text(x, y, sample.label, {
          fontFamily: FONT_FAMILY,
          fontSize: "18px",
          fontStyle: "bold",
          color: COLORS.ink,
        })
        .setOrigin(0, 0.5);
    });

    this.add
      .text(956, 610, "Top compass icons always show Intended / Opposite / Left / Right / Stay for the inspected tile.", {
        fontFamily: FONT_FAMILY,
        fontSize: "16px",
        fontStyle: "bold",
        color: COLORS.ink,
        align: "center",
        wordWrap: { width: 320 },
      })
      .setOrigin(0.5, 0.5);
  }
}
