import { COLORS, FONT_FAMILY } from "../game/constants.js";

export class ImageButton {
  constructor(
    scene,
    {
      x,
      y,
      textureKey = null,
      hoverTextureKey = null,
      pressedTextureKey = null,
      label = "",
      onClick = null,
      enabled = true,
      textStyle = {},
      fallbackWidth = 220,
      fallbackHeight = 72,
      scale = 1,
      depth = 10,
    },
  ) {
    this.scene = scene;
    this.textureKey = textureKey;
    this.hoverTextureKey = hoverTextureKey;
    this.pressedTextureKey = pressedTextureKey;
    this.onClick = onClick;
    this.enabled = enabled;
    this.usesImage = Boolean(textureKey && scene.textures.exists(textureKey));
    this.baseScale = scale;

    this.container = scene.add.container(x, y).setDepth(depth);

    if (this.usesImage) {
      this.background = scene.add.image(0, 0, textureKey).setScale(scale);
    } else {
      this.background = scene.add
        .rectangle(0, 0, fallbackWidth, fallbackHeight, 0x2d2b33, 0.9)
        .setStrokeStyle(2, 0x8ae3d5, 0.8);
    }

    this.label = scene.add
      .text(0, 0, label, {
        fontFamily: FONT_FAMILY,
        fontSize: "22px",
        color: COLORS.panelText,
        align: "center",
        ...textStyle,
      })
      .setOrigin(0.5);

    this.container.add([this.background, this.label]);
    this.hitArea = this.background;

    this.hitArea.setInteractive({ useHandCursor: true });
    this.registerEvents();
    this.setEnabled(enabled);
  }

  registerEvents() {
    this.hitArea.on("pointerover", () => {
      if (!this.enabled) {
        return;
      }
      if (this.usesImage && this.hoverTextureKey && this.scene.textures.exists(this.hoverTextureKey)) {
        this.background.setTexture(this.hoverTextureKey);
      } else {
        this.background.setScale(this.baseScale * 1.03);
      }
    });

    this.hitArea.on("pointerout", () => {
      if (this.usesImage && this.textureKey && this.scene.textures.exists(this.textureKey)) {
        this.background.setTexture(this.textureKey);
      }
      this.background.setScale(this.baseScale);
    });

    this.hitArea.on("pointerdown", () => {
      if (!this.enabled) {
        return;
      }
      if (this.usesImage && this.pressedTextureKey && this.scene.textures.exists(this.pressedTextureKey)) {
        this.background.setTexture(this.pressedTextureKey);
      } else {
        this.background.setScale(this.baseScale * 0.98);
      }
    });

    this.hitArea.on("pointerup", () => {
      if (!this.enabled) {
        return;
      }
      if (this.usesImage && this.hoverTextureKey && this.scene.textures.exists(this.hoverTextureKey)) {
        this.background.setTexture(this.hoverTextureKey);
      } else if (this.usesImage && this.textureKey && this.scene.textures.exists(this.textureKey)) {
        this.background.setTexture(this.textureKey);
      }
      this.background.setScale(this.baseScale);
      this.onClick?.();
    });
  }

  setEnabled(enabled) {
    this.enabled = enabled;
    this.hitArea.disableInteractive();
    if (enabled) {
      this.hitArea.setInteractive({ useHandCursor: true });
      this.container.setAlpha(1);
    } else {
      this.container.setAlpha(0.45);
    }
  }

  setLabel(text) {
    this.label.setText(text);
  }

  destroy() {
    this.container.destroy(true);
  }
}
