import Phaser from "phaser";
import { AudioController } from "../core/AudioController.js";
import { SaveManager } from "../core/SaveManager.js";
import { levels } from "../data/levels/index.js";
import { COLORS, FONT_FAMILY, GAME_HEIGHT, GAME_WIDTH } from "../game/constants.js";
import { ImageButton } from "../ui/ImageButton.js";

function coverImage(image, width, height) {
  const scale = Math.max(width / image.width, height / image.height);
  image.setScale(scale);
}

export class LevelSelectScene extends Phaser.Scene {
  constructor() {
    super("LevelSelectScene");
  }

  create() {
    this.renderBackground();
    AudioController.playMusic(this, "menu_theme", { volume: 0.32 });

    this.add
      .text(GAME_WIDTH / 2, 60, "Level Select", {
        fontFamily: FONT_FAMILY,
        fontSize: "38px",
        color: COLORS.panelText,
      })
      .setOrigin(0.5);

    new ImageButton(this, {
      x: 108,
      y: 56,
      textureKey: "btn_menu_secondary_idle",
      hoverTextureKey: "btn_menu_secondary_hover",
      pressedTextureKey: "btn_menu_secondary_hover",
      label: "Menu",
      fallbackWidth: 150,
      fallbackHeight: 52,
      scale: 0.9,
      onClick: () => {
        AudioController.playSfx(this, "ui_click");
        this.scene.start("MenuScene");
      },
    });

    this.add
      .text(GAME_WIDTH / 2, 96, "Complete a level to unlock the next chamber of the ruins.", {
        fontFamily: FONT_FAMILY,
        fontSize: "16px",
        color: COLORS.muted,
      })
      .setOrigin(0.5);

    this.renderButtons();
  }

  renderBackground() {
    if (this.textures.exists("bg_level_select_1920x1080")) {
      const background = this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, "bg_level_select_1920x1080");
      coverImage(background, GAME_WIDTH, GAME_HEIGHT);
      background.setAlpha(0.92);
    } else {
      this.cameras.main.setBackgroundColor(0x141319);
    }
  }

  renderButtons() {
    const state = SaveManager.getState();
    const columns = 6;
    const originX = 110;
    const originY = 170;
    const stepX = 176;
    const stepY = 150;

    levels.forEach((level, index) => {
      const unlocked = state.unlockedLevelIds.includes(level.id);
      const completed = state.completedLevelIds.includes(level.id);
      const textureKey = completed
        ? "btn_level_completed"
        : unlocked
          ? "btn_level_unlocked"
          : "btn_level_locked";

      const x = originX + (index % columns) * stepX;
      const y = originY + Math.floor(index / columns) * stepY;

      const button = new ImageButton(this, {
        x,
        y,
        textureKey,
        label: `${level.id}`,
        textStyle: { fontSize: "20px" },
        fallbackWidth: 72,
        fallbackHeight: 72,
        scale: 0.46,
        onClick: () => {
          if (!unlocked) {
            return;
          }
          AudioController.playSfx(this, "ui_click");
          this.scene.start("GameScene", { levelId: level.id });
        },
      });
      button.setEnabled(unlocked);

      this.add
        .text(x, y + 50, level.name.replace(/^Level \d+: /, ""), {
          fontFamily: FONT_FAMILY,
          fontSize: "12px",
          color: unlocked ? COLORS.panelText : COLORS.muted,
          align: "center",
          wordWrap: { width: 126 },
        })
        .setOrigin(0.5, 0);

      if (completed && this.textures.exists("marker_level_complete")) {
        this.add.image(x + 30, y - 30, "marker_level_complete").setScale(0.34);
      }
      if (!unlocked && this.textures.exists("marker_level_locked")) {
        this.add.image(x + 30, y - 30, "marker_level_locked").setScale(0.34);
      }
    });
  }
}
