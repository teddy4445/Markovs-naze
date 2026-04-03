import Phaser from "phaser";

export class Enemy {
  constructor(scene, definition, toWorldPosition) {
    this.scene = scene;
    this.definition = definition;
    this.toWorldPosition = toWorldPosition;
    this.gridPosition = { ...definition.start };
    this.patrolPath = definition.patrolPath.map((point) => ({ ...point }));
    this.patrolIndex = this.findNearestPatrolIndex(this.gridPosition);
    this.mode = "patrol";

    const spawn = this.toWorldPosition(this.gridPosition);
    const texture = scene.textures.exists("enemy_idle_spritesheet")
      ? "enemy_idle_spritesheet"
      : "enemy_cursed_knight_idle_base";
    this.sprite = scene.add.sprite(spawn.x, spawn.y, texture, 0).setDepth(24);
    this.alertIcon = scene.add.image(spawn.x, spawn.y - 34, "vfx_enemy_alert_icon").setAlpha(0).setDepth(26);
    this.playIdle();
  }

  destroy() {
    this.sprite.destroy();
    this.alertIcon.destroy();
  }

  findNearestPatrolIndex(position) {
    let bestIndex = 0;
    let bestDistance = Number.POSITIVE_INFINITY;
    this.patrolPath.forEach((point, index) => {
      const distance = Math.abs(point.x - position.x) + Math.abs(point.y - position.y);
      if (distance < bestDistance) {
        bestDistance = distance;
        bestIndex = index;
      }
    });
    return bestIndex;
  }

  setGridPosition(position) {
    this.gridPosition = { ...position };
    const world = this.toWorldPosition(position);
    this.sprite.setPosition(world.x, world.y);
    this.alertIcon.setPosition(world.x, world.y - 34);
  }

  playIdle() {
    if (this.scene.anims.exists("enemy-idle")) {
      this.sprite.play("enemy-idle", true);
    }
  }

  async moveTo(position, direction, isChasing) {
    const target = this.toWorldPosition(position);
    const animationKey = isChasing ? "enemy-chase" : `enemy-walk-${direction}`;
    if (this.scene.anims.exists(animationKey)) {
      this.sprite.play(animationKey, true);
    }

    await new Promise((resolve) => {
      this.scene.tweens.add({
        targets: [this.sprite, this.alertIcon],
        x: target.x,
        y: (targetingObject) => (targetingObject === this.alertIcon ? target.y - 34 : target.y),
        duration: 190,
        ease: "Quad.Out",
        onComplete: resolve,
      });
    });

    this.gridPosition = { ...position };
    this.playIdle();
  }

  async playAlertBurst() {
    if (this.scene.anims.exists("enemy-alert")) {
      this.sprite.play("enemy-alert");
    }

    this.alertIcon.setAlpha(1);
    await new Promise((resolve) => {
      this.scene.tweens.add({
        targets: this.alertIcon,
        alpha: 0,
        y: this.alertIcon.y - 18,
        duration: 420,
        ease: "Quad.Out",
        onComplete: () => {
          this.alertIcon.y += 18;
          resolve();
        },
      });
    });
  }

  canSeePlayer(level, playerPosition, isWall) {
    if (playerPosition.x !== this.gridPosition.x && playerPosition.y !== this.gridPosition.y) {
      return false;
    }

    if (playerPosition.x === this.gridPosition.x) {
      const step = playerPosition.y > this.gridPosition.y ? 1 : -1;
      for (let y = this.gridPosition.y + step; y !== playerPosition.y; y += step) {
        if (isWall(level, playerPosition.x, y)) {
          return false;
        }
      }
      return true;
    }

    const step = playerPosition.x > this.gridPosition.x ? 1 : -1;
    for (let x = this.gridPosition.x + step; x !== playerPosition.x; x += step) {
      if (isWall(level, x, playerPosition.y)) {
        return false;
      }
    }
    return true;
  }

  chooseIntent(level, playerPosition, helpers) {
    const visible = this.canSeePlayer(level, playerPosition, helpers.isWall);
    const justSpotted = visible && this.mode !== "chase";

    if (visible) {
      this.mode = "chase";
    } else if (this.mode === "chase") {
      this.mode = "return";
      this.patrolIndex = this.findNearestPatrolIndex(this.gridPosition);
    }

    if (this.mode === "chase") {
      return {
        intendedDirection: this.directionToward(this.gridPosition, playerPosition),
        justSpotted,
        isChasing: true,
      };
    }

    const currentTarget =
      this.mode === "return" ? this.patrolPath[this.patrolIndex] : this.patrolPath[this.patrolIndex];
    if (currentTarget && currentTarget.x === this.gridPosition.x && currentTarget.y === this.gridPosition.y) {
      this.mode = "patrol";
      this.patrolIndex = (this.patrolIndex + 1) % this.patrolPath.length;
    }

    const target = this.patrolPath[this.patrolIndex];
    const path = this.findPath(level, this.gridPosition, target, helpers.canOccupy);
    const nextStep = path[1] ?? target;
    const intendedDirection =
      nextStep && (nextStep.x !== this.gridPosition.x || nextStep.y !== this.gridPosition.y)
        ? this.directionToward(this.gridPosition, nextStep)
        : "stay";

    if (this.mode === "return" && target.x === this.gridPosition.x && target.y === this.gridPosition.y) {
      this.mode = "patrol";
    }

    return {
      intendedDirection,
      justSpotted,
      isChasing: false,
    };
  }

  directionToward(from, to) {
    if (to.x > from.x) {
      return "right";
    }
    if (to.x < from.x) {
      return "left";
    }
    if (to.y > from.y) {
      return "down";
    }
    if (to.y < from.y) {
      return "up";
    }
    return "stay";
  }

  findPath(level, start, goal, canOccupy) {
    const queue = [start];
    const parents = new Map([[`${start.x},${start.y}`, null]]);
    const directions = [
      { x: 0, y: -1 },
      { x: 1, y: 0 },
      { x: 0, y: 1 },
      { x: -1, y: 0 },
    ];

    while (queue.length > 0) {
      const current = queue.shift();
      if (current.x === goal.x && current.y === goal.y) {
        break;
      }

      for (const direction of directions) {
        const next = { x: current.x + direction.x, y: current.y + direction.y };
        const key = `${next.x},${next.y}`;
        if (parents.has(key) || !canOccupy(level, next.x, next.y)) {
          continue;
        }
        parents.set(key, current);
        queue.push(next);
      }
    }

    const goalKey = `${goal.x},${goal.y}`;
    if (!parents.has(goalKey)) {
      return [start];
    }

    const path = [];
    let cursor = goal;
    while (cursor) {
      path.push(cursor);
      cursor = parents.get(`${cursor.x},${cursor.y}`);
    }
    return path.reverse();
  }
}
