import { COLORS, FONT_FAMILY, GAME_HEIGHT, GAME_WIDTH } from "../game/constants.js";
import { ImageButton } from "./ImageButton.js";

function createPanel(scene, x, y, width, height, alpha = 0.97) {
  return scene.add
    .rectangle(x, y, width, height, COLORS.panelLightTextured, alpha)
    .setStrokeStyle(2, COLORS.panelLightStroke, 0.72);
}

function createOverlayPanel(scene, x, y, width, height, textureKey = null, alpha = 0.985) {
  if (textureKey && scene.textures.exists(textureKey)) {
    return scene.add.image(x, y, textureKey).setDisplaySize(width, height).setAlpha(alpha);
  }

  return createPanel(scene, x, y, width, height, alpha);
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
      { key: "btn_ui_restart", handler: () => this.config.onRestart?.(), name: "restart" },
      { key: "btn_ui_menu", handler: () => this.config.onMenu?.(), name: "menu" },
      { key: "btn_ui_sound_on", handler: () => this.config.onToggleSound?.(), name: "sound" },
      { key: "btn_ui_music_on", handler: () => this.config.onToggleMusic?.(), name: "music" },
    ];

    const x = 44;
    const startY = 56;
    const spacing = 54;

    this.iconButtons = {};
    entries.forEach((entry, index) => {
      const y = startY + index * spacing;
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
    const stripWidth = 162;
    const stripHeight = 344;
    const stripX = GAME_WIDTH - 96;
    const stripY = Math.max(214, boardRect.y + boardRect.height / 2);

    this.stripBackground = this.scene.add
      .rectangle(stripX, stripY, stripWidth, stripHeight, 0x120f18, 0.84)
      .setStrokeStyle(2, 0x8ae3d5, 0.28);
    this.root.add(this.stripBackground);

    const items = [
      { textureKey: "overlay_compass_intended_strong", label: "Intended" },
      { textureKey: "overlay_compass_opposite_strong", label: "Opposite" },
      { textureKey: "overlay_compass_left_strong", label: "Left" },
      { textureKey: "overlay_compass_right_strong", label: "Right" },
      { textureKey: "overlay_compass_stay_strong", label: "Stay" },
    ];

    const rowStartY = stripY - stripHeight / 2 + 38;
    const rowSpacing = 62;
    this.probabilityItems = items.map((item, index) => {
      const itemY = rowStartY + index * rowSpacing;
      const label = this.scene.add
        .text(stripX, itemY - 16, item.label, {
          fontFamily: FONT_FAMILY,
          fontSize: "11px",
          fontStyle: "bold",
          color: "#ffffff",
        })
        .setOrigin(0.5);
      const icon = createLegendIcon(this.scene, item.textureKey, stripX - 32, itemY + 12);
      const value = this.scene.add
        .text(stripX + 18, itemY + 12, "--", {
          fontFamily: FONT_FAMILY,
          fontSize: "14px",
          fontStyle: "bold",
          color: COLORS.panelText,
        })
        .setOrigin(0, 0.5);
      this.root.add([label, icon, value]);
      return { value };
    });
  }

  createInfoPanel(boardRect) {
    const panelWidth = 260;
    const panelHeight = 134;
    const panelX = 154;
    const panelY = GAME_HEIGHT - 92;

    this.infoPanel = createPanel(this.scene, panelX, panelY, panelWidth, panelHeight, 0.97);
    this.root.add(this.infoPanel);

    this.levelText = this.scene.add
      .text(panelX, panelY - 40, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "15px",
        fontStyle: "bold",
        color: COLORS.ink,
      })
      .setOrigin(0.5);

    this.objectiveText = this.scene.add
      .text(panelX, panelY - 14, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "13px",
        fontStyle: "bold",
        color: COLORS.ink,
        align: "center",
        wordWrap: { width: panelWidth - 30 },
      })
      .setOrigin(0.5);

    this.statusText = this.scene.add
      .text(panelX, panelY + 30, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "13px",
        fontStyle: "bold",
        color: COLORS.ink,
        align: "center",
        wordWrap: { width: panelWidth - 30 },
      })
      .setOrigin(0.5, 0.5);

    this.root.add([this.levelText, this.objectiveText, this.statusText]);
  }

  createOverlay() {
    this.overlayShade = this.scene.add
      .rectangle(GAME_WIDTH / 2, GAME_HEIGHT / 2, GAME_WIDTH, GAME_HEIGHT, 0x050608, 0.68)
      .setVisible(false);
    this.overlayPanel = createOverlayPanel(this.scene, GAME_WIDTH / 2, GAME_HEIGHT / 2, 560, 320, null, 0.98).setVisible(false);

    this.overlayTitle = this.scene.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 110, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "36px",
        fontStyle: "bold",
        color: COLORS.ink,
      })
      .setOrigin(0.5)
      .setVisible(false);
    this.overlayBody = this.scene.add
      .text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 34, "", {
        fontFamily: FONT_FAMILY,
        fontSize: "18px",
        fontStyle: "bold",
        align: "center",
        wordWrap: { width: 420 },
        color: COLORS.ink,
      })
      .setOrigin(0.5)
      .setVisible(false);

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
    this.statusText.setColor(this.statusColor ?? COLORS.ink).setText(this.state.status);
  }

  flashStatus(message, color = COLORS.ink, duration = 2200) {
    this.statusOverride = true;
    this.statusColor = color;
    this.state.status = message;
    this.refreshInfoText();
    if (this.statusTimer) {
      this.statusTimer.remove(false);
    }
    this.statusTimer = this.scene.time.delayedCall(duration, () => {
      this.statusOverride = false;
      this.statusColor = COLORS.ink;
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

  showOverlay({ title, body = "", panelTexture = null, buttons = [] }) {
    this.hideOverlay();
    this.isOverlayVisible = true;
    this.overlayShade.setVisible(true);
    this.overlayPanel.destroy();

    const hasBody = Boolean(body.trim());
    const panelHeight = hasBody ? Math.max(340, 236 + buttons.length * 80) : Math.max(280, 156 + buttons.length * 80);
    this.overlayPanel = createOverlayPanel(
      this.scene,
      GAME_WIDTH / 2,
      GAME_HEIGHT / 2,
      560,
      panelHeight,
      panelTexture,
      0.985,
    ).setDepth(81);
    this.overlayShade.setDepth(80);
    this.overlayTitle.setText(title).setY(GAME_HEIGHT / 2 - (hasBody ? 118 : 108)).setVisible(true);
    this.overlayBody.setText(body).setY(GAME_HEIGHT / 2 - 30).setVisible(hasBody);
    this.overlayRoot.add(this.overlayPanel);

    const buttonsStartY = hasBody ? GAME_HEIGHT / 2 + 18 : GAME_HEIGHT / 2 - 44;
    buttons.forEach((button, index) => {
      const instance = new ImageButton(this.scene, {
        x: GAME_WIDTH / 2,
        y: buttonsStartY + index * 78,
        textureKey: button.variant === "secondary" ? "btn_menu_secondary_idle" : "btn_menu_primary_idle",
        hoverTextureKey: button.variant === "secondary" ? "btn_menu_secondary_hover" : "btn_menu_primary_hover",
        pressedTextureKey: button.variant === "secondary" ? "btn_menu_secondary_hover" : "btn_menu_primary_pressed",
        label: button.label,
        onClick: button.onClick,
        fallbackWidth: 220,
        fallbackHeight: 68,
        depth: 82,
        textStyle: {
          color: COLORS.ink,
          fontStyle: "bold",
        },
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
