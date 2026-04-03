import { COLORS, FONT_FAMILY, GAME_HEIGHT, GAME_WIDTH } from "../game/constants.js";
import { ImageButton } from "./ImageButton.js";

function createPanel(scene, x, y, textureKey, width, height, alpha = 0.92) {
  if (scene.textures.exists(textureKey)) {
    return scene.add.image(x, y, textureKey).setDisplaySize(width, height).setAlpha(alpha);
  }

  return scene.add
    .rectangle(x, y, width, height, 0x211f27, alpha)
    .setStrokeStyle(2, 0x8ae3d5, 0.6);
}

function createLegendIcon(scene, textureKey, x, y) {
  if (scene.textures.exists(textureKey)) {
    return scene.add.image(x, y, textureKey).setDisplaySize(24, 24);
  }

  return scene.add.circle(x, y, 10, 0x8ae3d5, 0.18).setStrokeStyle(2, 0x8ae3d5, 0.8);
}

export class HUD {
  constructor(scene, config) {
    this.scene = scene;
    this.config = config;
    this.root = scene.add.container(0, 0).setDepth(50);
    this.overlayRoot = scene.add.container(0, 0).setDepth(80);
    this.overlayButtons = [];
    this.buttonBackplates = [];
    this.statusOverride = false;
    this.inspectMessage = null;
    this.lastMoveMessage = "Hover a tile to inspect its movement odds.";
    this.state = {
      levelName: "",
      objective: "",
      status: this.lastMoveMessage,
    };

    this.createControlButtons();
    this.createProbabilityStrip(config.boardRect);
    this.createInfoPanel(config.boardRect);
    this.createOverlay();
    this.refreshInfoText();
  }

  createControlButtons() {
    const entries = [
      { key: "btn_ui_pause", handler: () => this.config.onPause?.(), name: "pause" },
      { key: "btn_ui_restart", handler: () => this.config.onRestart?.(), name: "restart" },
      { key: "btn_ui_menu", handler: () => this.config.onMenu?.(), name: "menu" },
      { key: "btn_ui_sound_on", handler: () => this.config.onToggleSound?.(), name: "sound" },
      { key: "btn_ui_music_on", handler: () => this.config.onToggleMusic?.(), name: "music" },
    ];

    const x = GAME_WIDTH - 50;
    const startY = GAME_HEIGHT - 274;
    const spacing = 56;

    this.iconButtons = {};
    entries.forEach((entry, index) => {
      const y = startY + index * spacing;
      const backplate = this.scene.add
        .circle(x, y, 30, 0x120f18, 0.66)
        .setDepth(54)
        .setStrokeStyle(2, 0x8ae3d5, 0.2);
      this.root.add(backplate);
      this.buttonBackplates.push(backplate);

      const control = new ImageButton(this.scene, {
        x,
        y,
        textureKey: entry.key,
        onClick: entry.handler,
        label: "",
        fallbackWidth: 48,
        fallbackHeight: 48,
        scale: 0.82,
        depth: 55,
      });
      this.iconButtons[entry.name] = control;
    });
  }

  createProbabilityStrip(boardRect) {
    const stripWidth = Math.min(Math.max(boardRect.width * 0.72, 420), 560);
    const stripX = GAME_WIDTH / 2;
    const stripY = Math.max(24, boardRect.y - 24);

    this.stripBackground = this.scene.add
      .rectangle(stripX, stripY, stripWidth, 50, 0x120f18, 0.8)
      .setStrokeStyle(2, 0x8ae3d5, 0.26);
    this.root.add(this.stripBackground);

    const items = [
      { textureKey: "overlay_compass_intended_strong" },
      { textureKey: "overlay_compass_opposite_strong" },
      { textureKey: "overlay_compass_left_strong" },
      { textureKey: "overlay_compass_right_strong" },
      { textureKey: "overlay_compass_stay_strong" },
    ];

    const startX = stripX - stripWidth / 2 + 42;
    const spacing = (stripWidth - 84) / 4;
    this.probabilityItems = items.map((item, index) => {
      const itemX = startX + index * spacing;
      const icon = createLegendIcon(this.scene, item.textureKey, itemX, stripY - 8);
      const value = this.scene.add
        .text(itemX, stripY + 12, "--", {
          fontFamily: FONT_FAMILY,
          fontSize: "14px",
          color: COLORS.panelText,
        })
        .setOrigin(0.5);
      this.root.add([icon, value]);
      return { value };
    });
  }

  createInfoPanel(boardRect) {
    const panelWidth = Math.min(Math.max(boardRect.width + 120, 620), GAME_WIDTH - 130);
    const panelX = GAME_WIDTH / 2;
    const panelY = Math.min(GAME_HEIGHT - 26, boardRect.y + boardRect.height + 30);

    this.infoPanel = this.scene.add
      .rectangle(panelX, panelY, panelWidth, 56, 0x120f18, 0.88)
      .setStrokeStyle(2, 0x8ae3d5, 0.32);
    this.root.add(this.infoPanel);

    this.levelText = this.scene.add
      .text(panelX - panelWidth / 2 + 18, panelY - 12, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "16px",
        color: COLORS.panelText,
      })
      .setOrigin(0, 0.5);

    this.objectiveText = this.scene.add
      .text(panelX + panelWidth / 2 - 18, panelY - 12, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "14px",
        color: COLORS.accentWarm,
        align: "right",
      })
      .setOrigin(1, 0.5);

    this.statusText = this.scene.add
      .text(panelX, panelY + 12, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "13px",
        color: COLORS.accent,
        align: "center",
        wordWrap: { width: panelWidth - 40 },
      })
      .setOrigin(0.5, 0.5);

    this.root.add([this.levelText, this.objectiveText, this.statusText]);
  }

  createOverlay() {
    this.overlayShade = this.scene.add
      .rectangle(GAME_WIDTH / 2, GAME_HEIGHT / 2, GAME_WIDTH, GAME_HEIGHT, 0x050608, 0.68)
      .setVisible(false);
    this.overlayPanel = createPanel(this.scene, GAME_WIDTH / 2, GAME_HEIGHT / 2, "panel_pause_menu", 560, 420);
    this.overlayPanel.setVisible(false);

    this.overlayTitle = this.scene.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 142, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "36px",
        color: COLORS.panelText,
      })
      .setOrigin(0.5);
    this.overlayBody = this.scene.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 52, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "20px",
        align: "center",
        wordWrap: { width: 420 },
        color: COLORS.muted,
      })
      .setOrigin(0.5);

    this.overlayRoot.add([this.overlayShade, this.overlayPanel, this.overlayTitle, this.overlayBody]);
    this.isOverlayVisible = false;
  }

  setLevel(level) {
    this.state.levelName = level.name;
    this.refreshInfoText();
  }

  setObjective({ requiresKey = false, hasKey = false } = {}) {
    this.state.objective = !requiresKey ? "Reach the goal seal" : hasKey ? "Key shard claimed" : "Find the key shard";
    this.refreshInfoText();
  }

  setInspection(message = null) {
    this.inspectMessage = message;
    if (!this.statusOverride) {
      this.state.status = this.inspectMessage ?? this.lastMoveMessage;
      this.refreshInfoText();
    }
  }

  setProbability(profile, metadata = null) {
    if (!profile) {
      this.probabilityItems.forEach((item) => item.value.setText("--"));
      return;
    }

    const values = [profile.intended, profile.opposite, profile.left, profile.right, profile.stay];
    values.forEach((value, index) => {
      this.probabilityItems[index].value.setText(`${Math.round(value * 100)}%`);
    });

    if (!metadata) {
      if (!this.statusOverride && !this.inspectMessage) {
        this.lastMoveMessage = "Hover a tile to inspect its movement odds.";
        this.state.status = this.lastMoveMessage;
        this.refreshInfoText();
      }
      return;
    }

    if (metadata.stayed) {
      this.lastMoveMessage = "Last move resolved as stay.";
    } else {
      const resampleText = metadata.resampled ? " after wall resample" : "";
      this.lastMoveMessage = `Last move resolved ${metadata.absoluteDirection}${resampleText}.`;
    }

    if (!this.statusOverride && !this.inspectMessage) {
      this.state.status = this.lastMoveMessage;
      this.refreshInfoText();
    }
  }

  refreshInfoText() {
    this.levelText.setText(this.state.levelName);
    this.objectiveText.setText(this.state.objective);
    this.statusText.setColor(this.statusColor ?? COLORS.accent).setText(this.state.status);
  }

  flashStatus(message, color = COLORS.accent, duration = 2200) {
    this.statusOverride = true;
    this.statusColor = color;
    this.state.status = message;
    this.refreshInfoText();
    if (this.statusTimer) {
      this.statusTimer.remove(false);
    }
    this.statusTimer = this.scene.time.delayedCall(duration, () => {
      this.statusOverride = false;
      this.statusColor = COLORS.accent;
      this.state.status = this.inspectMessage ?? this.lastMoveMessage;
      this.refreshInfoText();
      this.statusTimer = null;
    });
  }

  updateSettings(settings) {
    const soundKey = settings.soundEnabled ? "btn_ui_sound_on" : "btn_ui_sound_off";
    const musicKey = settings.musicEnabled ? "btn_ui_music_on" : "btn_ui_music_off";

    if (this.scene.textures.exists(soundKey)) {
      this.iconButtons.sound.background.setTexture(soundKey);
    }
    if (this.scene.textures.exists(musicKey)) {
      this.iconButtons.music.background.setTexture(musicKey);
    }
  }

  hideOverlay() {
    this.isOverlayVisible = false;
    this.overlayShade.setVisible(false);
    this.overlayPanel.setVisible(false);
    this.overlayTitle.setVisible(false);
    this.overlayBody.setVisible(false);
    this.overlayButtons.forEach((button) => button.destroy());
    this.overlayButtons = [];
  }

  showOverlay({ title, body = "", panelTexture = "panel_pause_menu", buttons = [] }) {
    this.hideOverlay();
    this.isOverlayVisible = true;
    this.overlayShade.setVisible(true);
    this.overlayPanel.destroy();

    const hasBody = Boolean(body.trim());
    const panelHeight = hasBody ? Math.max(360, 248 + buttons.length * 86) : Math.max(300, 188 + buttons.length * 86);
    this.overlayPanel = createPanel(this.scene, GAME_WIDTH / 2, GAME_HEIGHT / 2, panelTexture, 560, panelHeight).setDepth(81);
    this.overlayTitle.setText(title).setVisible(true);
    this.overlayBody.setText(body).setVisible(hasBody);
    this.overlayBody.setY(GAME_HEIGHT / 2 - 52);
    this.overlayShade.setDepth(80);
    this.overlayRoot.add(this.overlayPanel);

    const buttonsStartY = hasBody ? GAME_HEIGHT / 2 + 58 : GAME_HEIGHT / 2 - 4;
    buttons.forEach((button, index) => {
      const instance = new ImageButton(this.scene, {
        x: GAME_WIDTH / 2,
        y: buttonsStartY + index * 82,
        textureKey: button.variant === "secondary" ? "btn_menu_secondary_idle" : "btn_menu_primary_idle",
        hoverTextureKey: button.variant === "secondary" ? "btn_menu_secondary_hover" : "btn_menu_primary_hover",
        pressedTextureKey: button.variant === "secondary" ? "btn_menu_secondary_hover" : "btn_menu_primary_pressed",
        label: button.label,
        onClick: button.onClick,
        fallbackWidth: 220,
        fallbackHeight: 68,
        depth: 82,
      });
      this.overlayButtons.push(instance);
    });
  }

  destroy() {
    Object.values(this.iconButtons).forEach((button) => button.destroy());
    if (this.statusTimer) {
      this.statusTimer.remove(false);
      this.statusTimer = null;
    }
    this.hideOverlay();
    this.root.destroy(true);
    this.overlayRoot.destroy(true);
  }
}
