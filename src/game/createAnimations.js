const ANIMATION_DEFS = [
  { key: "player-idle", texture: "player_idle_spritesheet", frameRate: 2, repeat: -1 },
  { key: "player-walk-up", texture: "player_walk_up_spritesheet", frameRate: 10, repeat: 0 },
  { key: "player-walk-down", texture: "player_walk_down_spritesheet", frameRate: 10, repeat: 0 },
  { key: "player-walk-left", texture: "player_walk_left_spritesheet", frameRate: 10, repeat: 0 },
  { key: "player-walk-right", texture: "player_walk_right_spritesheet", frameRate: 10, repeat: 0 },
  { key: "player-death", texture: "player_death_spritesheet", frameRate: 10, repeat: 0 },
  { key: "player-victory", texture: "player_victory_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-idle", texture: "enemy_idle_spritesheet", frameRate: 2, repeat: -1 },
  { key: "enemy-walk-up", texture: "enemy_walk_up_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-walk-down", texture: "enemy_walk_down_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-walk-left", texture: "enemy_walk_left_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-walk-right", texture: "enemy_walk_right_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-alert", texture: "enemy_alert_spritesheet", frameRate: 10, repeat: 0 },
  { key: "enemy-chase", texture: "enemy_chase_spritesheet", frameRate: 12, repeat: 0 },
  { key: "vfx-move-puff", texture: "vfx_move_puff_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-blocked-bump", texture: "vfx_blocked_bump_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-no-move-pulse", texture: "vfx_no_move_pulse_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-trap-trigger", texture: "vfx_trap_trigger_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-lava-burst", texture: "vfx_lava_burst_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-goal-activate", texture: "vfx_goal_activate_spritesheet", frameRate: 14, repeat: 0 },
  { key: "vfx-tile-rune-pulse", texture: "vfx_tile_rune_pulse_spritesheet", frameRate: 12, repeat: -1 },
];

export function createAnimations(scene) {
  for (const definition of ANIMATION_DEFS) {
    if (scene.anims.exists(definition.key) || !scene.textures.exists(definition.texture)) {
      continue;
    }

    const frameCount = scene.textures.get(definition.texture).frameTotal - 1;
    scene.anims.create({
      key: definition.key,
      frames: scene.anims.generateFrameNumbers(definition.texture, {
        start: 0,
        end: frameCount,
      }),
      frameRate: definition.frameRate,
      repeat: definition.repeat,
    });
  }
}
