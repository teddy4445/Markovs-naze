# Visual Upgrade Report

- Generated at: `2026-04-04T06:27:35+00:00`
- Mode: `live-or-safe-run`
- Dry run: `no`
- Model preference order: `gpt-image-1.5, gpt-image-1, gpt-image-1-mini, dall-e-2`

## Summary

- Total assets processed: `80`
- Assets successfully upgraded: `0`
- Assets kept original: `80`
- Assets requiring manual review: `0`
- Assets failed: `0`
- Assets missing source files: `0`
- Backups available: `80`
- Environment-blocked assets: `0`
- Account-blocked assets: `80`

## Prompt Adjustments Made

- Added the global Markov's Maze style contract to every asset prompt.
- Added palette constraints for stone, moss, cyan/gold runes, lava, and cursed enemy glow accents.
- Added category-specific art direction for branding, backgrounds, tiles, props, sprites, VFX, UI, and icons.
- Added explicit transparency requirements for PNG overlays, sprites, tiles, and UI pieces.
- Added sprite-sheet framing instructions for animated assets using manifest frame counts and frame dimensions.
- Preferred edit/reference mode when the existing processed asset is available locally.

## Resizing And Post-Processing Notes

- The script targets documented OpenAI Images API square, landscape, and portrait sizes, then post-processes the result to the exact manifest dimensions.
- All accepted outputs are resized and cropped with Pillow to preserve the existing runtime dimensions and filenames.
- Transparent assets are preserved as PNG with an alpha channel; opaque assets are flattened back to PNG after resizing.

## Successfully Upgraded

- None in this run.

## Kept Original

- `logo_markovs_maze.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `bg_main_menu_1920x1080.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `bg_level_select_1920x1080.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `bg_gameplay_maze_1920x1080.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `bg_long_ruins_parallax.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `bg_long_ruins_parallax_alt.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_floor_a.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_floor_b.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_floor_c.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_wall_a.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_wall_b.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_wall_corner.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_start.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_goal.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_trap.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `tile_lava.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_patrol_path.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_patrol_node.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_base.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_intended_strong.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_opposite_strong.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_left_strong.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_right_strong.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_stay_strong.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `overlay_compass_active_tile.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `prop_broken_column.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `prop_rune_shard.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `prop_moss_edge.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `prop_stone_rubble.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_ruins_scholar_idle_base.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_idle_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_walk_up_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_walk_down_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_walk_left_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_walk_right_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_death_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `player_victory_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_cursed_knight_idle_base.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_idle_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_walk_up_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_walk_down_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_walk_left_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_walk_right_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_alert_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `enemy_chase_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_move_puff_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_blocked_bump_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_no_move_pulse_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_trap_trigger_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_lava_burst_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_goal_activate_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_enemy_alert_icon.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `vfx_tile_rune_pulse_spritesheet.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_menu_primary_idle.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_menu_primary_hover.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_menu_primary_pressed.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_menu_secondary_idle.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_menu_secondary_hover.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_level_locked.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_level_unlocked.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_level_completed.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `marker_level_locked.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `marker_level_complete.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_restart.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_pause.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_menu.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_sound_on.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_sound_off.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_music_on.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_music_off.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `btn_ui_info.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `panel_probability_hud.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `panel_pause_menu.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `panel_victory.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `panel_defeat.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `icon_goal.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `icon_enemy_alert.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `icon_trap.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `icon_lava.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.
- `icon_probability.png`: OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.

## Manual Review Needed

- None in this run.

## Failed

- None in this run.

## Remaining Visual Consistency Issues

- Animated assets should still receive a human frame-consistency pass before shipping, especially player and enemy sheets.
- Backgrounds and long parallax strips may need composition tuning after the first successful live generation run.
- The current report reflects environment-gated status if OPENAI_API_KEY is not set in the shell.

## Asset Log

| Asset | Category | Status | Mode | Model | Backup | Output | Manual review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `logo_markovs_maze.png` | branding | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/branding/logo_markovs_maze.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `bg_main_menu_1920x1080.png` | backgrounds | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/backgrounds/bg_main_menu_1920x1080.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `bg_level_select_1920x1080.png` | backgrounds | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/backgrounds/bg_level_select_1920x1080.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `bg_gameplay_maze_1920x1080.png` | backgrounds | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/backgrounds/bg_gameplay_maze_1920x1080.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `bg_long_ruins_parallax.png` | backgrounds | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/backgrounds/bg_long_ruins_parallax.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `bg_long_ruins_parallax_alt.png` | backgrounds | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/backgrounds/bg_long_ruins_parallax_alt.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_floor_a.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_floor_a.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_floor_b.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_floor_b.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_floor_c.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_floor_c.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_wall_a.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_wall_a.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_wall_b.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_wall_b.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_wall_corner.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_wall_corner.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_start.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_start.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_goal.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_goal.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_trap.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_trap.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `tile_lava.png` | tiles | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/tiles/tile_lava.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_patrol_path.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_patrol_path.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_patrol_node.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_patrol_node.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_base.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_base.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_intended_strong.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_intended_strong.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_opposite_strong.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_opposite_strong.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_left_strong.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_left_strong.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_right_strong.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_right_strong.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_stay_strong.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_stay_strong.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `overlay_compass_active_tile.png` | overlays | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/overlays/overlay_compass_active_tile.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `prop_broken_column.png` | props | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/props/prop_broken_column.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `prop_rune_shard.png` | props | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/props/prop_rune_shard.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `prop_moss_edge.png` | props | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/props/prop_moss_edge.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `prop_stone_rubble.png` | props | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/props/prop_stone_rubble.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_ruins_scholar_idle_base.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_ruins_scholar_idle_base.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_idle_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_idle_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_walk_up_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_walk_up_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_walk_down_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_walk_down_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_walk_left_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_walk_left_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_walk_right_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_walk_right_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_death_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_death_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `player_victory_spritesheet.png` | sprites_player | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/player/player_victory_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_cursed_knight_idle_base.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_cursed_knight_idle_base.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_idle_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_idle_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_walk_up_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_walk_up_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_walk_down_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_walk_down_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_walk_left_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_walk_left_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_walk_right_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_walk_right_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_alert_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_alert_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `enemy_chase_spritesheet.png` | sprites_enemy | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/sprites/enemy/enemy_chase_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_move_puff_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_move_puff_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_blocked_bump_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_blocked_bump_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_no_move_pulse_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_no_move_pulse_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_trap_trigger_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_trap_trigger_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_lava_burst_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_lava_burst_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_goal_activate_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_goal_activate_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_enemy_alert_icon.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_enemy_alert_icon.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `vfx_tile_rune_pulse_spritesheet.png` | vfx | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/vfx/vfx_tile_rune_pulse_spritesheet.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_menu_primary_idle.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_menu_primary_idle.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_menu_primary_hover.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_menu_primary_hover.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_menu_primary_pressed.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_menu_primary_pressed.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_menu_secondary_idle.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_menu_secondary_idle.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_menu_secondary_hover.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_menu_secondary_hover.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_level_locked.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_level_locked.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_level_unlocked.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_level_unlocked.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_level_completed.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_level_completed.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `marker_level_locked.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/marker_level_locked.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `marker_level_complete.png` | ui_menu | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/marker_level_complete.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_restart.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_restart.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_pause.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_pause.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_menu.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_menu.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_sound_on.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_sound_on.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_sound_off.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_sound_off.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_music_on.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_music_on.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_music_off.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_music_off.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `btn_ui_info.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/btn_ui_info.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `panel_probability_hud.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/panel_probability_hud.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `panel_pause_menu.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/panel_pause_menu.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `panel_victory.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/panel_victory.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `panel_defeat.png` | ui_game | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/ui/panel_defeat.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `icon_goal.png` | icons | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/icons/icon_goal.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `icon_enemy_alert.png` | icons | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/icons/icon_enemy_alert.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `icon_trap.png` | icons | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/icons/icon_trap.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `icon_lava.png` | icons | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/icons/icon_lava.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
| `icon_probability.png` | icons | blocked_account_limit | edit_reference | n/a | assets/backups/original_visuals/icons/icon_probability.png | n/a | no | OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved. |
