import Phaser from "phaser";
import { AudioController } from "../core/AudioController.js";
import { LevelLoader, getCell, getProbabilityProfile, isLethal, isWall, isWalkable } from "../core/LevelLoader.js";
import { ProbabilityResolver } from "../core/ProbabilityResolver.js";
import { SaveManager } from "../core/SaveManager.js";
import { Enemy } from "../entities/Enemy.js";
import { Player } from "../entities/Player.js";
import { COLORS, GAME_HEIGHT, GAME_WIDTH, TILE_SIZE } from "../game/constants.js";
import { HUD } from "../ui/HUD.js";

function coverImage(image, width, height) {
  const scale = Math.max(width / image.width, height / image.height);
  image.setScale(scale);
}

export class GameScene extends Phaser.Scene {
  constructor() {
    super("GameScene");
  }

  init(data) {
    this.levelId = data.levelId ?? SaveManager.getRecommendedLevelId();
  }

  create() {
    this.level = LevelLoader.getLevel(this.levelId);
    this.level.requiresKey = this.level.grid.some((row) => row.some((cell) => cell.tile === "key"));
    this.totalLevels = LevelLoader.getAllLevels().length;
    this.hasKey = false;
    this.hoveredTile = null;
    this.isBusy = false;
    this.isFinished = false;
    this.lastResolution = null;
    this.overlayKind = null;
    this.enemyHum = null;

    this.boardOrigin = this.computeBoardOrigin();
    this.boardRect = {
      x: this.boardOrigin.x,
      y: this.boardOrigin.y,
      width: this.level.width * TILE_SIZE,
      height: this.level.height * TILE_SIZE,
    };

    this.renderBackground();
    this.renderBoard();
    this.createActors();
    this.createHud();
    this.createControls();
    this.createAmbientLife();
    this.refreshHud();
    this.refreshEnemyHum();
    this.playLevelMusic();

    if (this.level.tutorialText) {
      this.hud.flashStatus(this.level.tutorialText, COLORS.muted, 5000);
    }

    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.stopEnemyHum();
      this.ambientMoteEvent?.remove(false);
      this.tileSparkEvent?.remove(false);
      this.hud?.destroy();
      this.enemies?.forEach((enemy) => enemy.destroy());
      this.specialTileTweens?.forEach((tween) => tween.remove());
      this.probabilityOverlayObjects?.forEach((overlay) => overlay.destroy());
      this.keyPickups?.forEach((pickup) => {
        pickup.tween?.remove();
        pickup.sprite?.destroy();
      });
    });
  }

  computeBoardOrigin() {
    const boardWidth = this.level.width * TILE_SIZE;
    const boardHeight = this.level.height * TILE_SIZE;
    return {
      x: Math.max(24, Math.round((GAME_WIDTH - boardWidth) / 2)),
      y: Math.max(44, Math.round((GAME_HEIGHT - boardHeight) / 2)),
    };
  }

  renderBackground() {
    if (this.textures.exists("bg_gameplay_maze_1920x1080")) {
      const background = this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, "bg_gameplay_maze_1920x1080");
      coverImage(background, GAME_WIDTH, GAME_HEIGHT);
      background.setAlpha(0.95);
    } else {
      this.cameras.main.setBackgroundColor(0x141319);
    }
  }

  createImageOrFallback(textureKey, x, y, options = {}) {
    const width = options.width ?? TILE_SIZE;
    const height = options.height ?? TILE_SIZE;
    const alpha = options.alpha ?? 1;
    const depth = options.depth ?? 1;
    const rotation = options.rotation ?? 0;
    const scale = options.scale ?? 1;

    if (textureKey && this.textures.exists(textureKey)) {
      return this.add
        .image(x, y, textureKey)
        .setDisplaySize(width, height)
        .setAlpha(alpha)
        .setRotation(rotation)
        .setScale(scale)
        .setDepth(depth);
    }

    const rectangle = this.add.rectangle(x, y, width, height, options.fillColor ?? 0x403d46, alpha).setDepth(depth);
    if (options.strokeColor) {
      rectangle.setStrokeStyle(2, options.strokeColor, 0.85);
    }
    return rectangle;
  }

  renderBoard() {
    this.tileObjects = [];
    this.patrolObjects = [];
    this.probabilityOverlayObjects = [];
    this.keyPickups = new Map();
    this.walkableTiles = [];
    this.specialTileTweens = [];

    for (let y = 0; y < this.level.height; y += 1) {
      this.tileObjects[y] = [];

      for (let x = 0; x < this.level.width; x += 1) {
        const cell = getCell(this.level, x, y);
        const world = this.tileToWorld({ x, y });
        const tileVisual = this.getTileVisual(cell, x, y);
        const tileObject = this.createImageOrFallback(tileVisual.textureKey, world.x, world.y, {
          depth: 5,
          rotation: tileVisual.rotation ?? 0,
          fillColor: cell.tile === "wall" ? 0x3d3842 : 0x7a736d,
        });
        this.tileObjects[y][x] = tileObject;

        if (cell.tile !== "wall") {
          this.walkableTiles.push({ x, y });
          tileObject.setInteractive({ useHandCursor: true });
          tileObject.on("pointerover", () => this.setHoveredTile({ x, y }));
          tileObject.on("pointerout", () => this.clearHoveredTile());
        }

        if (cell.tile === "key") {
          this.renderKeyPickup({ x, y }, world);
        }

        this.animateTile(tileObject, cell.tile);
      }
    }

    this.level.enemies.forEach((enemy) => this.renderPatrol(enemy.patrolPath));
    this.patrolObjects.forEach((marker) => {
      this.specialTileTweens.push(
        this.tweens.add({
          targets: marker,
          alpha: marker.alpha + 0.12,
          duration: 900,
          yoyo: true,
          repeat: -1,
          ease: "Sine.InOut",
        }),
      );
    });
  }

  renderProbabilityOverlay(profile, x, y) {
    const alphaForProbability = (value) => Phaser.Math.Clamp(0.03 + value * 0.58, 0, 0.66);
    const depth = 8;
    const overlays = [];
    overlays.push(this.createImageOrFallback("overlay_compass_base", x, y, { depth, alpha: 0.14 }));
    overlays.push(this.createImageOrFallback("overlay_compass_intended_strong", x, y, {
      depth: depth + 0.1,
      alpha: alphaForProbability(profile.intended),
    }));
    overlays.push(this.createImageOrFallback("overlay_compass_opposite_strong", x, y, {
      depth: depth + 0.1,
      alpha: alphaForProbability(profile.opposite),
    }));
    overlays.push(this.createImageOrFallback("overlay_compass_left_strong", x, y, {
      depth: depth + 0.1,
      alpha: alphaForProbability(profile.left),
    }));
    overlays.push(this.createImageOrFallback("overlay_compass_right_strong", x, y, {
      depth: depth + 0.1,
      alpha: alphaForProbability(profile.right),
    }));
    overlays.push(this.createImageOrFallback("overlay_compass_stay_strong", x, y, {
      depth: depth + 0.1,
      alpha: alphaForProbability(profile.stay),
    }));
    return overlays;
  }

  renderKeyPickup(position, world) {
    const sprite = this.createImageOrFallback("prop_rune_shard", world.x, world.y - 4, {
      width: 42,
      height: 42,
      depth: 17,
      alpha: 0.96,
      fillColor: 0xe0be5c,
      strokeColor: 0xf7f2e8,
    });
    const tween = this.tweens.add({
      targets: sprite,
      y: world.y - 10,
      duration: 900,
      yoyo: true,
      repeat: -1,
      ease: "Sine.InOut",
    });
    this.keyPickups.set(`${position.x},${position.y}`, { sprite, tween });
  }

  animateTile(tileObject, tileType) {
    if (tileType === "lava") {
      this.specialTileTweens.push(
        this.tweens.add({
          targets: tileObject,
          alpha: 0.82,
          scaleX: 1.03,
          scaleY: 1.03,
          duration: 760,
          yoyo: true,
          repeat: -1,
          ease: "Sine.InOut",
        }),
      );
      return;
    }

    if (tileType === "goal" || tileType === "start") {
      this.specialTileTweens.push(
        this.tweens.add({
          targets: tileObject,
          alpha: 0.9,
          duration: 1200,
          yoyo: true,
          repeat: -1,
          ease: "Sine.InOut",
        }),
      );
      return;
    }

    if (tileType === "trap") {
      this.specialTileTweens.push(
        this.tweens.add({
          targets: tileObject,
          angle: 2,
          duration: 500,
          yoyo: true,
          repeat: -1,
          ease: "Sine.InOut",
        }),
      );
    }
  }

  renderPatrol(path) {
    path.forEach((point, index) => {
      const world = this.tileToWorld(point);
      this.patrolObjects.push(
        this.createImageOrFallback("overlay_patrol_node", world.x, world.y, {
          depth: 11,
          width: 34,
          height: 34,
          alpha: 0.72,
          fillColor: 0x8ae3d5,
        }),
      );

      const next = path[(index + 1) % path.length];
      const deltaX = next.x - point.x;
      const deltaY = next.y - point.y;
      if (Math.abs(deltaX) + Math.abs(deltaY) !== 1) {
        return;
      }

      const midpoint = this.tileToWorld({
        x: point.x + deltaX * 0.5,
        y: point.y + deltaY * 0.5,
      });
      this.patrolObjects.push(
        this.createImageOrFallback("overlay_patrol_path", midpoint.x, midpoint.y, {
          depth: 10,
          width: 40,
          height: 18,
          alpha: 0.62,
          rotation: deltaY !== 0 ? Math.PI / 2 : 0,
          fillColor: 0x8ae3d5,
        }),
      );
    });
  }

  createActors() {
    this.player = new Player(this, this.level.start, (position) => this.tileToWorld(position));
    this.enemies = this.level.enemies.map(
      (enemy) => new Enemy(this, enemy, (position) => this.tileToWorld(position)),
    );

    const playerWorld = this.tileToWorld(this.player.gridPosition);
    if (this.textures.exists("overlay_compass_active_tile")) {
      this.activeTileHighlight = this.add
        .image(playerWorld.x, playerWorld.y, "overlay_compass_active_tile")
        .setDisplaySize(TILE_SIZE, TILE_SIZE)
        .setDepth(18)
        .setAlpha(0.95);
    } else {
      this.activeTileHighlight = this.add
        .rectangle(playerWorld.x, playerWorld.y, TILE_SIZE - 6, TILE_SIZE - 6)
        .setDepth(18)
        .setStrokeStyle(3, 0x8ae3d5, 0.95);
    }

    this.hoverTileHighlight = this.add
      .rectangle(playerWorld.x, playerWorld.y, TILE_SIZE - 12, TILE_SIZE - 12)
      .setDepth(17)
      .setStrokeStyle(2, 0xe0be5c, 0.95)
      .setVisible(false);
  }

  createHud() {
    this.hud = new HUD(this, {
      boardRect: this.boardRect,
      onRestart: () => this.restartLevel(),
      onMenu: () => this.returnToMenu(),
      onToggleSound: () => this.toggleSound(),
      onToggleMusic: () => this.toggleMusic(),
    });
    this.hud.setLevel(this.level);
    this.hud.setObjective({ requiresKey: this.level.requiresKey, hasKey: this.hasKey });
    this.hud.updateSettings(SaveManager.getState().settings);
  }

  createControls() {
    this.input.keyboard.on("keydown", (event) => {
      const direction = {
        ArrowUp: "up",
        KeyW: "up",
        ArrowRight: "right",
        KeyD: "right",
        ArrowDown: "down",
        KeyS: "down",
        ArrowLeft: "left",
        KeyA: "left",
      }[event.code];

      if (direction) {
        this.attemptPlayerMove(direction);
        return;
      }

      if (event.code === "KeyR") {
        this.restartLevel();
      }
    });
  }

  createAmbientLife() {
    if (!this.textures.exists("__maze_mote")) {
      const graphics = this.make.graphics({ add: false });
      graphics.fillStyle(0xffffff, 1);
      graphics.fillCircle(6, 6, 6);
      graphics.generateTexture("__maze_mote", 12, 12);
      graphics.destroy();
    }

    this.ambientMoteEvent = this.time.addEvent({
      delay: 540,
      loop: true,
      callback: () => this.spawnAmbientMote(),
    });

    this.tileSparkEvent = this.time.addEvent({
      delay: 1300,
      loop: true,
      callback: () => this.spawnTileSpark(),
    });
  }

  spawnAmbientMote() {
    const x = Phaser.Math.Between(this.boardRect.x - 18, this.boardRect.x + this.boardRect.width + 18);
    const y = Phaser.Math.Between(this.boardRect.y - 10, this.boardRect.y + this.boardRect.height + 10);
    const mote = this.add
      .image(x, y, "__maze_mote")
      .setDepth(15)
      .setAlpha(0)
      .setTint(Phaser.Utils.Array.GetRandom([0x8ae3d5, 0xe0be5c, 0xf7f2e8]));
    const driftX = Phaser.Math.Between(-18, 18);
    const driftY = Phaser.Math.Between(-16, 12);
    const scale = Phaser.Math.FloatBetween(0.2, 0.58);
    mote.setScale(scale);

    this.tweens.add({
      targets: mote,
      x: x + driftX,
      y: y + driftY,
      alpha: { from: 0, to: Phaser.Math.FloatBetween(0.08, 0.2) },
      duration: Phaser.Math.Between(1500, 2600),
      yoyo: true,
      ease: "Sine.InOut",
      onComplete: () => mote.destroy(),
    });
  }

  spawnTileSpark() {
    const candidates = this.walkableTiles.filter(({ x, y }) => {
      const tile = getCell(this.level, x, y)?.tile;
      return tile === "goal" || tile === "start" || tile === "lava" || tile === "trap";
    });
    if (!candidates.length) {
      return;
    }

    const tile = Phaser.Utils.Array.GetRandom(candidates);
    const world = this.tileToWorld(tile);
    this.spawnEffect("vfx-tile-rune-pulse", world.x, world.y, {
      alpha: getCell(this.level, tile.x, tile.y)?.tile === "lava" ? 0.4 : 0.22,
      scale: 0.82,
      depth: 16,
    });
  }

  tileToWorld(position) {
    return {
      x: this.boardOrigin.x + position.x * TILE_SIZE + TILE_SIZE / 2,
      y: this.boardOrigin.y + position.y * TILE_SIZE + TILE_SIZE / 2,
    };
  }

  getTileVisual(cell, x, y) {
    switch (cell.tile) {
      case "wall":
        return this.getWallVisual(x, y);
      case "start":
        return { textureKey: "tile_start" };
      case "goal":
        return { textureKey: "tile_goal" };
      case "trap":
        return { textureKey: "tile_trap" };
      case "lava":
        return { textureKey: "tile_lava" };
      case "key":
        return { textureKey: this.getFloorTexture(cell.probabilityKey) };
      default:
        return { textureKey: this.getFloorTexture(cell.probabilityKey) };
    }
  }

  getWallVisual(x, y) {
    const upWall = isWall(this.level, x, y - 1);
    const rightWall = isWall(this.level, x + 1, y);
    const downWall = isWall(this.level, x, y + 1);
    const leftWall = isWall(this.level, x - 1, y);

    const exactCorner =
      (upWall && rightWall && !downWall && !leftWall) ||
      (rightWall && downWall && !upWall && !leftWall) ||
      (downWall && leftWall && !upWall && !rightWall) ||
      (leftWall && upWall && !rightWall && !downWall);

    if (exactCorner) {
      let rotation = 0;
      if (rightWall && downWall) {
        rotation = Math.PI / 2;
      } else if (downWall && leftWall) {
        rotation = Math.PI;
      } else if (leftWall && upWall) {
        rotation = -Math.PI / 2;
      }

      return {
        textureKey: "tile_wall_corner",
        rotation,
      };
    }

    if ((leftWall || rightWall) && !upWall && !downWall) {
      return { textureKey: "tile_wall_a" };
    }

    if ((upWall || downWall) && !leftWall && !rightWall) {
      return { textureKey: "tile_wall_b" };
    }

    return {
      textureKey: (x + y) % 2 === 0 ? "tile_wall_a" : "tile_wall_b",
    };
  }

  getFloorTexture(probabilityKey) {
    const map = {
      A: "tile_floor_a",
      B: "tile_floor_a",
      C: "tile_floor_b",
      D: "tile_floor_b",
      E: "tile_floor_c",
      F: "tile_floor_c",
    };
    return map[probabilityKey] ?? "tile_floor_a";
  }

  canPlayerOccupy(x, y) {
    return isWalkable(this.level, x, y);
  }

  canEnemyOccupy(level, x, y) {
    return isWalkable(level, x, y) && !isLethal(level, x, y);
  }

  positionsEqual(a, b) {
    return a.x === b.x && a.y === b.y;
  }

  updateActiveTileHighlight() {
    const world = this.tileToWorld(this.player.gridPosition);
    this.activeTileHighlight.setPosition(world.x, world.y);
  }

  clearProbabilityOverlays() {
    this.probabilityOverlayObjects.forEach((overlay) => overlay.destroy());
    this.probabilityOverlayObjects = [];
  }

  updateAdjacentProbabilityOverlays() {
    this.clearProbabilityOverlays();

    const neighbors = [
      { x: this.player.gridPosition.x, y: this.player.gridPosition.y - 1 },
      { x: this.player.gridPosition.x + 1, y: this.player.gridPosition.y },
      { x: this.player.gridPosition.x, y: this.player.gridPosition.y + 1 },
      { x: this.player.gridPosition.x - 1, y: this.player.gridPosition.y },
    ];

    neighbors.forEach((position) => {
      const cell = getCell(this.level, position.x, position.y);
      if (!cell || cell.tile !== "floor") {
        return;
      }

      const world = this.tileToWorld(position);
      const profile = getProbabilityProfile(this.level, position.x, position.y);
      this.probabilityOverlayObjects.push(...this.renderProbabilityOverlay(profile, world.x, world.y));
    });
  }

  setHoveredTile(position) {
    this.hoveredTile = { ...position };
    const world = this.tileToWorld(position);
    this.hoverTileHighlight.setPosition(world.x, world.y).setVisible(true);
    this.refreshHud();
  }

  clearHoveredTile() {
    this.hoveredTile = null;
    this.hoverTileHighlight.setVisible(false);
    this.refreshHud();
  }

  refreshHud() {
    const inspectionPosition = this.hoveredTile ?? this.player.gridPosition;
    const profile = getProbabilityProfile(this.level, inspectionPosition.x, inspectionPosition.y);
    const inspectionMessage = this.hoveredTile
      ? `Inspecting tile ${inspectionPosition.x + 1},${inspectionPosition.y + 1}.`
      : null;
    this.hud.setProbability(profile, this.hoveredTile ? null : this.lastResolution);
    this.hud.setInspection(inspectionMessage);
    this.hud.setObjective({ requiresKey: this.level.requiresKey, hasKey: this.hasKey });
    this.hud.updateSettings(SaveManager.getState().settings);
    this.updateActiveTileHighlight();
    this.updateAdjacentProbabilityOverlays();
  }

  playLevelMusic() {
    const musicKey = this.level.id >= 11 ? "late_gameplay_theme" : "early_gameplay_theme";
    AudioController.playMusic(this, musicKey, { volume: 0.3 });
  }

  refreshEnemyHum() {
    this.stopEnemyHum();
    if (!this.enemies.length || !SaveManager.isSoundEnabled() || !this.cache.audio.exists("enemy_idle_cursed_hum")) {
      return;
    }

    this.enemyHum = this.sound.add("enemy_idle_cursed_hum", {
      loop: true,
      volume: 0.12,
    });
    this.enemyHum.play();
  }

  stopEnemyHum() {
    if (this.enemyHum) {
      this.enemyHum.stop();
      this.enemyHum.destroy();
      this.enemyHum = null;
    }
  }

  async attemptPlayerMove(direction) {
    if (this.isBusy || this.isFinished || this.hud.isOverlayVisible) {
      return;
    }

    this.isBusy = true;
    const origin = { ...this.player.gridPosition };
    const profile = getProbabilityProfile(this.level, origin.x, origin.y);
    const resolution = ProbabilityResolver.resolve(profile, direction, {
      origin,
      validator: (target) => this.canPlayerOccupy(target.x, target.y),
    });
    this.lastResolution = resolution;

    await this.handlePlayerResolution(origin, resolution);

    if (await this.resolvePlayerOutcome()) {
      this.isBusy = false;
      return;
    }

    const playerCaught = await this.runEnemyTurn();
    if (!playerCaught) {
      this.refreshHud();
    }
    this.isBusy = false;
  }

  async handlePlayerResolution(origin, resolution) {
    const attemptedInBounds = getCell(this.level, resolution.attemptedTarget.x, resolution.attemptedTarget.y);
    const attemptedBlocked =
      attemptedInBounds && !this.canPlayerOccupy(resolution.attemptedTarget.x, resolution.attemptedTarget.y);

    if (attemptedBlocked) {
      const blockedWorld = this.tileToWorld(resolution.attemptedTarget);
      this.spawnEffect("vfx-blocked-bump", blockedWorld.x, blockedWorld.y);
      AudioController.playSfx(this, "player_blocked_bump");
    }

    if (resolution.stayed) {
      const world = this.tileToWorld(origin);
      this.spawnEffect("vfx-no-move-pulse", world.x, world.y);
      AudioController.playSfx(this, "player_no_move");
      return;
    }

    const destinationWorld = this.tileToWorld(resolution.target);
    await this.player.moveTo(resolution.target, resolution.absoluteDirection);
    this.spawnEffect("vfx-move-puff", destinationWorld.x, destinationWorld.y);
    AudioController.playSfx(this, resolution.relativeOutcome === "intended" ? "player_move_intended" : "player_move_alternate");
    AudioController.playSfx(this, "player_step", { volume: 0.45 });
    this.updateActiveTileHighlight();
  }

  collectKeyAt(x, y) {
    const cell = getCell(this.level, x, y);
    if (!cell || cell.tile !== "key") {
      return false;
    }

    cell.tile = "floor";
    this.hasKey = true;

    const pickup = this.keyPickups.get(`${x},${y}`);
    if (pickup) {
      pickup.tween?.remove();
      pickup.sprite?.destroy();
      this.keyPickups.delete(`${x},${y}`);
    }

    const world = this.tileToWorld({ x, y });
    this.spawnEffect("vfx-goal-activate", world.x, world.y, { alpha: 0.72, scale: 0.92 });
    AudioController.playSfx(this, "goal_activation", { volume: 0.62 });
    this.hud.flashStatus("Key shard claimed. The goal seal is now open.", COLORS.accentWarm, 2800);
    this.refreshHud();
    return true;
  }

  async resolvePlayerOutcome() {
    const { x, y } = this.player.gridPosition;
    const cell = getCell(this.level, x, y);

    if (this.enemies.some((enemy) => this.positionsEqual(enemy.gridPosition, this.player.gridPosition))) {
      await this.handleDefeat();
      return true;
    }

    if (isLethal(this.level, x, y)) {
      const tile = cell?.tile;
      const effectKey = tile === "lava" ? "vfx-lava-burst" : "vfx-trap-trigger";
      const soundKey = tile === "lava" ? "lava_hiss_or_burst" : "trap_trigger";
      const world = this.tileToWorld({ x, y });
      this.spawnEffect(effectKey, world.x, world.y);
      AudioController.playSfx(this, soundKey);
      await this.handleDefeat();
      return true;
    }

    if (cell?.tile === "key" && !this.hasKey) {
      this.collectKeyAt(x, y);
    }

    if (cell?.tile === "goal") {
      if (this.level.requiresKey && !this.hasKey) {
        AudioController.playSfx(this, "ui_hover", { volume: 0.35 });
        this.hud.flashStatus("The goal seal is locked. Find the key shard first.", COLORS.accentWarm, 2600);
        return false;
      }

      const world = this.tileToWorld({ x, y });
      this.spawnEffect("vfx-goal-activate", world.x, world.y);
      AudioController.playSfx(this, "goal_activation");
      await this.handleVictory();
      return true;
    }

    return false;
  }

  async runEnemyTurn() {
    for (const enemy of this.enemies) {
      const decision = enemy.chooseIntent(this.level, this.player.gridPosition, {
        isWall,
        canOccupy: (level, x, y) => this.canEnemyOccupy(level, x, y),
      });

      if (decision.justSpotted) {
        AudioController.playSfx(this, "enemy_spotted_alert");
        await enemy.playAlertBurst();
      }

      const profile = getProbabilityProfile(this.level, enemy.gridPosition.x, enemy.gridPosition.y);
      const resolution = ProbabilityResolver.resolve(profile, decision.intendedDirection, {
        origin: enemy.gridPosition,
        validator: (target) => this.canEnemyOccupy(this.level, target.x, target.y),
      });

      if (!resolution.stayed) {
        AudioController.playSfx(this, "enemy_move_armor_scrape", { volume: 0.4 });
        await enemy.moveTo(resolution.target, resolution.absoluteDirection, decision.isChasing);
      } else {
        enemy.playIdle();
      }

      if (this.positionsEqual(enemy.gridPosition, this.player.gridPosition)) {
        await this.handleDefeat();
        return true;
      }
    }

    return false;
  }

  spawnEffect(animationKey, x, y, options = {}) {
    const textureMap = {
      "vfx-move-puff": "vfx_move_puff_spritesheet",
      "vfx-blocked-bump": "vfx_blocked_bump_spritesheet",
      "vfx-no-move-pulse": "vfx_no_move_pulse_spritesheet",
      "vfx-trap-trigger": "vfx_trap_trigger_spritesheet",
      "vfx-lava-burst": "vfx_lava_burst_spritesheet",
      "vfx-goal-activate": "vfx_goal_activate_spritesheet",
      "vfx-tile-rune-pulse": "vfx_tile_rune_pulse_spritesheet",
    };
    const textureKey = textureMap[animationKey];
    if (!textureKey || !this.textures.exists(textureKey)) {
      return null;
    }

    const sprite = this.add.sprite(x, y, textureKey).setDepth(options.depth ?? 32);
    sprite.setAlpha(options.alpha ?? 1);
    sprite.setScale(options.scale ?? 1);
    if (this.anims.exists(animationKey)) {
      sprite.play(animationKey);
      sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE, () => sprite.destroy());
    } else {
      this.time.delayedCall(240, () => sprite.destroy());
    }
    return sprite;
  }

  async handleVictory() {
    this.isFinished = true;
    SaveManager.completeLevel(this.level.id);
    await this.player.playVictory();
    AudioController.playSfx(this, "level_complete");
    this.hud.showOverlay({
      title: "Level Cleared",
      body: "",
      panelTexture: "panel_victory",
      buttons: [
        this.level.id < this.totalLevels
          ? {
              label: "Next Level",
              onClick: () => this.scene.start("GameScene", { levelId: this.level.id + 1 }),
            }
          : {
              label: "Level Select",
              onClick: () => this.scene.start("LevelSelectScene"),
            },
        {
          label: "Restart",
          variant: "secondary",
          onClick: () => this.restartLevel(),
        },
        {
          label: "Menu",
          variant: "secondary",
          onClick: () => this.returnToMenu(),
        },
      ],
    });
    this.overlayKind = "victory";
  }

  async handleDefeat() {
    this.isFinished = true;
    AudioController.playSfx(this, "defeat_sting");
    await this.player.playDeath();
    this.hud.showOverlay({
      title: "Defeat",
      body: "",
      panelTexture: "panel_defeat",
      buttons: [
        {
          label: "Restart",
          onClick: () => this.restartLevel(),
        },
        {
          label: "Level Select",
          variant: "secondary",
          onClick: () => this.scene.start("LevelSelectScene"),
        },
        {
          label: "Menu",
          variant: "secondary",
          onClick: () => this.returnToMenu(),
        },
      ],
    });
    this.overlayKind = "defeat";
  }

  restartLevel() {
    this.stopEnemyHum();
    this.scene.restart({ levelId: this.levelId });
  }

  returnToMenu() {
    this.stopEnemyHum();
    this.scene.start("MenuScene");
  }

  toggleSound() {
    SaveManager.toggleSound();
    this.refreshHud();
    this.refreshEnemyHum();
  }

  toggleMusic() {
    const state = SaveManager.toggleMusic();
    this.hud.updateSettings(state.settings);
    if (state.settings.musicEnabled) {
      this.playLevelMusic();
    } else {
      AudioController.stopMusic(this);
    }
  }
}
