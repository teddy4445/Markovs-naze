import Phaser from "phaser";

export class Player {
  constructor(scene, startPosition, toWorldPosition) {
    this.scene = scene;
    this.toWorldPosition = toWorldPosition;
    this.gridPosition = { ...startPosition };
    const spawn = this.toWorldPosition(startPosition);

    const texture = scene.textures.exists("player_idle_spritesheet")
      ? "player_idle_spritesheet"
      : "player_ruins_scholar_idle_base";

    this.sprite = scene.add.sprite(spawn.x, spawn.y, texture, 0).setDepth(20);
    this.facing = "down";
    this.playIdle();
  }

  setGridPosition(position) {
    this.gridPosition = { ...position };
    const world = this.toWorldPosition(position);
    this.sprite.setPosition(world.x, world.y);
  }

  playIdle() {
    if (this.scene.anims.exists("player-idle")) {
      this.sprite.play("player-idle", true);
    }
  }

  async moveTo(position, direction) {
    this.facing = direction;
    const target = this.toWorldPosition(position);
    const animationKey = `player-walk-${direction}`;
    if (this.scene.anims.exists(animationKey)) {
      this.sprite.play(animationKey, true);
    }

    await new Promise((resolve) => {
      this.scene.tweens.add({
        targets: this.sprite,
        x: target.x,
        y: target.y,
        duration: 180,
        ease: "Quad.Out",
        onComplete: resolve,
      });
    });

    this.gridPosition = { ...position };
    this.playIdle();
  }

  async playDeath() {
    if (!this.scene.anims.exists("player-death")) {
      return;
    }

    await new Promise((resolve) => {
      this.sprite.play("player-death");
      this.sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE, resolve);
    });
  }

  async playVictory() {
    if (!this.scene.anims.exists("player-victory")) {
      return;
    }

    await new Promise((resolve) => {
      this.sprite.play("player-victory");
      this.sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE, resolve);
    });
    this.playIdle();
  }
}
