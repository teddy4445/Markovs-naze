from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DATA_DIR = ROOT / "data"
RAW_ART_DIR = ROOT / "assets" / "raw" / "art"
PROCESSED_DIR = ROOT / "assets" / "processed"

GLOBAL_VISUAL_STYLE = [
    "top-down 2D game asset",
    "orthographic view",
    "low-detail flat fantasy",
    "ancient magical ruins theme",
    "clean readable silhouette",
    "minimal texture",
    "soft flat shading",
    "strong contrast",
    "elegant rune details",
    "gameplay readability first",
    "no photorealism",
    "no isometric angle",
    "no perspective distortion",
    "no text unless the asset is the logo",
]

PALETTE = {
    "shadow": (29, 27, 30, 255),
    "shadow_soft": (40, 38, 46, 255),
    "stone_dark": (68, 63, 71, 255),
    "stone": (112, 104, 110, 255),
    "stone_light": (171, 161, 154, 255),
    "sand": (203, 182, 147, 255),
    "parchment": (223, 212, 179, 255),
    "gold": (224, 190, 92, 255),
    "teal": (90, 184, 173, 255),
    "teal_bright": (138, 227, 213, 255),
    "moss": (94, 125, 86, 255),
    "crimson": (178, 82, 78, 255),
    "ember": (238, 112, 53, 255),
    "lava": (244, 150, 52, 255),
    "violet": (136, 108, 169, 255),
    "silver": (176, 186, 197, 255),
    "ink": (15, 19, 22, 255),
    "white": (247, 244, 238, 255),
    "transparent": (0, 0, 0, 0),
}


@dataclass
class AssetSpec:
    filename: str
    group: str
    category: str
    processed_subdir: str
    purpose: str
    prompt_subject: str
    consistency_notes: str
    placeholder_kind: str
    width: int
    height: int
    transparency: bool
    frame_count: int = 1
    frame_width: int | None = None
    frame_height: int | None = None
    raw_svg: bool = False
    status: str = "placeholder_generated"
    placeholder_source: str = "local_procedural_png"

    @property
    def asset_id(self) -> str:
        return Path(self.filename).stem

    @property
    def processed_path(self) -> Path:
        return PROCESSED_DIR / self.processed_subdir / self.filename

    @property
    def raw_svg_path(self) -> Path | None:
        if not self.raw_svg:
            return None
        return RAW_ART_DIR / self.filename.replace(".png", ".svg")

    def to_manifest_entry(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "filename": self.filename,
            "group": self.group,
            "category": self.category,
            "status": self.status,
            "placeholder": True,
            "final_ready_filename": True,
            "placeholder_source": self.placeholder_source,
            "purpose": self.purpose,
            "dimensions": {"width": self.width, "height": self.height},
            "transparency": self.transparency,
            "animation": {
                "animated": self.frame_count > 1,
                "frame_count": self.frame_count,
                "frame_width": self.frame_width or self.width,
                "frame_height": self.frame_height or self.height,
                "layout": "horizontal_strip" if self.frame_count > 1 else "single_frame",
            },
            "paths": {
                "processed": relpath(self.processed_path),
                "raw_svg": relpath(self.raw_svg_path) if self.raw_svg_path else None,
            },
            "prompt_subject": self.prompt_subject,
            "consistency_notes": self.consistency_notes,
        }


def relpath(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.relative_to(ROOT).as_posix()


def static_asset(
    filename: str,
    *,
    group: str,
    category: str,
    processed_subdir: str,
    purpose: str,
    prompt_subject: str,
    consistency_notes: str,
    placeholder_kind: str,
    size: tuple[int, int],
    transparency: bool,
    raw_svg: bool = True,
) -> AssetSpec:
    return AssetSpec(
        filename=filename,
        group=group,
        category=category,
        processed_subdir=processed_subdir,
        purpose=purpose,
        prompt_subject=prompt_subject,
        consistency_notes=consistency_notes,
        placeholder_kind=placeholder_kind,
        width=size[0],
        height=size[1],
        transparency=transparency,
        raw_svg=raw_svg,
    )


def sheet_asset(
    filename: str,
    *,
    group: str,
    category: str,
    processed_subdir: str,
    purpose: str,
    prompt_subject: str,
    consistency_notes: str,
    placeholder_kind: str,
    frame_count: int,
    frame_size: tuple[int, int] = (64, 64),
    transparency: bool = True,
) -> AssetSpec:
    return AssetSpec(
        filename=filename,
        group=group,
        category=category,
        processed_subdir=processed_subdir,
        purpose=purpose,
        prompt_subject=prompt_subject,
        consistency_notes=consistency_notes,
        placeholder_kind=placeholder_kind,
        width=frame_size[0] * frame_count,
        height=frame_size[1],
        transparency=transparency,
        frame_count=frame_count,
        frame_width=frame_size[0],
        frame_height=frame_size[1],
        raw_svg=False,
    )


def build_asset_specs() -> list[AssetSpec]:
    specs: list[AssetSpec] = []

    specs.append(
        static_asset(
            "logo_markovs_maze.png",
            group="A. Branding",
            category="branding",
            processed_subdir="branding",
            purpose="Primary logo for menu and repository branding.",
            prompt_subject="stylized Markov's Maze logo with a rune-ring motif and elegant stone fantasy lettering",
            consistency_notes="Keep gold and teal rune accents aligned with the rest of the UI; the logo is the only art asset allowed to contain text.",
            placeholder_kind="logo",
            size=(1024, 512),
            transparency=True,
        )
    )

    specs.extend(
        [
            static_asset(
                "bg_main_menu_1920x1080.png",
                group="B. Backgrounds",
                category="backgrounds",
                processed_subdir="backgrounds",
                purpose="Main menu backdrop with strong title readability.",
                prompt_subject="wide ruins courtyard seen from a puzzle-friendly top-down orthographic angle, broken columns, glowing runes, broad negative space for menu UI",
                consistency_notes="Use warm torchlight and teal rune light to establish the fantasy ruins mood without adding gameplay objects.",
                placeholder_kind="background_menu",
                size=(1920, 1080),
                transparency=False,
                raw_svg=False,
            ),
            static_asset(
                "bg_level_select_1920x1080.png",
                group="B. Backgrounds",
                category="backgrounds",
                processed_subdir="backgrounds",
                purpose="Level-select backdrop with implied route progression.",
                prompt_subject="ruined stone map hall with inset maze slabs, corridor fragments, and subtle glowing rune pathways",
                consistency_notes="Keep the center and lower thirds calm so level nodes can sit on top without readability loss.",
                placeholder_kind="background_select",
                size=(1920, 1080),
                transparency=False,
                raw_svg=False,
            ),
            static_asset(
                "bg_gameplay_maze_1920x1080.png",
                group="B. Backgrounds",
                category="backgrounds",
                processed_subdir="backgrounds",
                purpose="Gameplay backdrop behind the active maze board.",
                prompt_subject="subdued ancient ruins floor plane with low-contrast stone geometry, faint rune circles, and soft edge vignette",
                consistency_notes="Prioritize quiet values so the maze tiles, sprites, and overlays remain dominant.",
                placeholder_kind="background_gameplay",
                size=(1920, 1080),
                transparency=False,
                raw_svg=False,
            ),
            static_asset(
                "bg_long_ruins_parallax.png",
                group="B. Backgrounds",
                category="backgrounds",
                processed_subdir="backgrounds",
                purpose="Primary looping parallax strip for long ruins vistas.",
                prompt_subject="long horizontal ruined skyline with arches, pillars, banners, and layered rune-lit stone silhouettes",
                consistency_notes="Designed as a horizontal strip for later parallax reuse; keep silhouettes rhythmic and loop-friendly.",
                placeholder_kind="background_parallax_a",
                size=(2048, 512),
                transparency=False,
                raw_svg=False,
            ),
            static_asset(
                "bg_long_ruins_parallax_alt.png",
                group="B. Backgrounds",
                category="backgrounds",
                processed_subdir="backgrounds",
                purpose="Secondary looping parallax strip for variation.",
                prompt_subject="alternate long horizontal ruined skyline with collapsed towers, moonlit masonry, and cooler rune glows",
                consistency_notes="Use the same silhouette language as the primary strip but shift the lighting and ruin density.",
                placeholder_kind="background_parallax_b",
                size=(2048, 512),
                transparency=False,
                raw_svg=False,
            ),
        ]
    )

    tile_notes = "All maze tiles should stay readable at gameplay zoom, with clean edge contrast and rune detailing kept secondary to pathing clarity."
    specs.extend(
        [
            static_asset("tile_floor_a.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Baseline walkable floor tile.", prompt_subject="single stone floor tile with broad slabs and a faint circular rune seam", consistency_notes=tile_notes, placeholder_kind="tile_floor_a", size=(64, 64), transparency=True),
            static_asset("tile_floor_b.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Secondary walkable floor variation.", prompt_subject="single stone floor tile with offset slab seams and minimal moss detail", consistency_notes=tile_notes, placeholder_kind="tile_floor_b", size=(64, 64), transparency=True),
            static_asset("tile_floor_c.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Tertiary walkable floor variation.", prompt_subject="single stone floor tile with an angled crack and tiny rune chips", consistency_notes=tile_notes, placeholder_kind="tile_floor_c", size=(64, 64), transparency=True),
            static_asset("tile_wall_a.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Baseline blocking wall tile.", prompt_subject="single heavy stone wall tile viewed from top-down, dark capstones and rune-cut edges", consistency_notes=tile_notes, placeholder_kind="tile_wall_a", size=(64, 64), transparency=True),
            static_asset("tile_wall_b.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Secondary blocking wall variation.", prompt_subject="single stone wall tile with more broken corners and a moss-darkened top edge", consistency_notes=tile_notes, placeholder_kind="tile_wall_b", size=(64, 64), transparency=True),
            static_asset("tile_wall_corner.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Corner wall tile for readable turns.", prompt_subject="single corner wall tile with clear L-shaped mass and rune-carved corner brace", consistency_notes=tile_notes, placeholder_kind="tile_wall_corner", size=(64, 64), transparency=True),
            static_asset("tile_start.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Player start tile.", prompt_subject="single start tile with a teal rune ring and welcoming compass mark on ancient stone", consistency_notes=tile_notes, placeholder_kind="tile_start", size=(64, 64), transparency=True),
            static_asset("tile_goal.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Level goal tile.", prompt_subject="single goal tile with a radiant gold rune seal and layered concentric stones", consistency_notes=tile_notes, placeholder_kind="tile_goal", size=(64, 64), transparency=True),
            static_asset("tile_trap.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Forbidden trap tile.", prompt_subject="single trap tile with a crimson rune hazard symbol and sharp stone spikes hinted inside the rune circle", consistency_notes=tile_notes, placeholder_kind="tile_trap", size=(64, 64), transparency=True),
            static_asset("tile_lava.png", group="C. Tiles", category="tiles", processed_subdir="tiles", purpose="Forbidden lava tile.", prompt_subject="single lava tile with a contained molten rune pool inside broken stone borders", consistency_notes=tile_notes, placeholder_kind="tile_lava", size=(64, 64), transparency=True),
        ]
    )

    overlay_notes = "Probability and path overlays should read instantly above tiles, using high contrast, transparent backgrounds, and restrained rune styling."
    specs.extend(
        [
            static_asset("overlay_patrol_path.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Patrol path segment overlay.", prompt_subject="transparent path overlay with a thin glowing patrol line across a tile", consistency_notes=overlay_notes, placeholder_kind="overlay_path", size=(64, 64), transparency=True),
            static_asset("overlay_patrol_node.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Patrol node overlay.", prompt_subject="transparent patrol node overlay with a compact glowing circular marker", consistency_notes=overlay_notes, placeholder_kind="overlay_node", size=(64, 64), transparency=True),
            static_asset("overlay_compass_base.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Neutral compass probability base overlay.", prompt_subject="transparent compass-circle overlay with subtle rune ticks and no highlighted direction", consistency_notes=overlay_notes, placeholder_kind="compass_base", size=(64, 64), transparency=True),
            static_asset("overlay_compass_intended_strong.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Strong intended-direction probability overlay.", prompt_subject="transparent compass-circle overlay with the forward arrow strongly highlighted in teal", consistency_notes=overlay_notes, placeholder_kind="compass_intended", size=(64, 64), transparency=True),
            static_asset("overlay_compass_opposite_strong.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Strong opposite-direction probability overlay.", prompt_subject="transparent compass-circle overlay with the reverse arrow strongly highlighted in crimson", consistency_notes=overlay_notes, placeholder_kind="compass_opposite", size=(64, 64), transparency=True),
            static_asset("overlay_compass_left_strong.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Strong left-direction probability overlay.", prompt_subject="transparent compass-circle overlay with the left arrow strongly highlighted in gold", consistency_notes=overlay_notes, placeholder_kind="compass_left", size=(64, 64), transparency=True),
            static_asset("overlay_compass_right_strong.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Strong right-direction probability overlay.", prompt_subject="transparent compass-circle overlay with the right arrow strongly highlighted in gold", consistency_notes=overlay_notes, placeholder_kind="compass_right", size=(64, 64), transparency=True),
            static_asset("overlay_compass_stay_strong.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Strong no-move probability overlay.", prompt_subject="transparent compass-circle overlay with the center stay rune strongly highlighted in violet", consistency_notes=overlay_notes, placeholder_kind="compass_stay", size=(64, 64), transparency=True),
            static_asset("overlay_compass_active_tile.png", group="D. Overlays and path markers", category="overlays", processed_subdir="overlays", purpose="Active probability tile selection highlight.", prompt_subject="transparent active-tile highlight with a glowing rune ring hugging the tile edges", consistency_notes=overlay_notes, placeholder_kind="compass_active", size=(64, 64), transparency=True),
        ]
    )

    prop_notes = "Props should feel like maze dressing, not blockers, and should stay compact enough to read against the floor."
    specs.extend(
        [
            static_asset("prop_broken_column.png", group="E. Props", category="props", processed_subdir="props", purpose="Broken column prop.", prompt_subject="collapsed stone column segment with cracked rune bands", consistency_notes=prop_notes, placeholder_kind="prop_column", size=(64, 64), transparency=True),
            static_asset("prop_rune_shard.png", group="E. Props", category="props", processed_subdir="props", purpose="Loose rune shard prop.", prompt_subject="floating or fallen rune shard crystal carved from pale stone", consistency_notes=prop_notes, placeholder_kind="prop_rune", size=(64, 64), transparency=True),
            static_asset("prop_moss_edge.png", group="E. Props", category="props", processed_subdir="props", purpose="Moss edging prop.", prompt_subject="soft moss fringe that can sit along a stone edge without blocking readability", consistency_notes=prop_notes, placeholder_kind="prop_moss", size=(64, 64), transparency=True),
            static_asset("prop_stone_rubble.png", group="E. Props", category="props", processed_subdir="props", purpose="Stone rubble prop.", prompt_subject="small pile of broken ruin stones and dust", consistency_notes=prop_notes, placeholder_kind="prop_rubble", size=(64, 64), transparency=True),
        ]
    )

    player_notes = "Keep the ruins scholar silhouette consistent across all player assets: parchment robe, teal sash, dark hair, bronze satchel, and readable top-down pose."
    specs.extend(
        [
            static_asset("player_ruins_scholar_idle_base.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Single-frame player reference pose.", prompt_subject="ruins scholar seen from top-down, calm idle stance, parchment robe, teal sash, satchel", consistency_notes=player_notes, placeholder_kind="player_base", size=(64, 64), transparency=True),
            sheet_asset("player_idle_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player idle animation.", prompt_subject="2-frame top-down ruins scholar idle animation with subtle breathing and cloth shift", consistency_notes=player_notes, placeholder_kind="player_idle", frame_count=2),
            sheet_asset("player_walk_up_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player walk-up animation.", prompt_subject="4-frame top-down ruins scholar walk cycle facing up, measured and readable", consistency_notes=player_notes, placeholder_kind="player_walk_up", frame_count=4),
            sheet_asset("player_walk_down_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player walk-down animation.", prompt_subject="4-frame top-down ruins scholar walk cycle facing down, readable feet and sash motion", consistency_notes=player_notes, placeholder_kind="player_walk_down", frame_count=4),
            sheet_asset("player_walk_left_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player walk-left animation.", prompt_subject="4-frame top-down ruins scholar walk cycle facing left with a compact profile", consistency_notes=player_notes, placeholder_kind="player_walk_left", frame_count=4),
            sheet_asset("player_walk_right_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player walk-right animation.", prompt_subject="4-frame top-down ruins scholar walk cycle facing right with a compact profile", consistency_notes=player_notes, placeholder_kind="player_walk_right", frame_count=4),
            sheet_asset("player_death_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player defeat animation.", prompt_subject="4-frame top-down ruins scholar defeat animation collapsing into a faint rune burst", consistency_notes=player_notes, placeholder_kind="player_death", frame_count=4),
            sheet_asset("player_victory_spritesheet.png", group="F. Player art", category="sprites_player", processed_subdir="sprites/player", purpose="Player victory animation.", prompt_subject="4-frame top-down ruins scholar victory animation with lifted compass hand and warm rune glow", consistency_notes=player_notes, placeholder_kind="player_victory", frame_count=4),
        ]
    )

    enemy_notes = "Keep the cursed knight silhouette broad and readable: dark armor, pale curse glow, red-violet accents, and heavier weight than the player."
    specs.extend(
        [
            static_asset("enemy_cursed_knight_idle_base.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Single-frame enemy reference pose.", prompt_subject="cursed knight seen from top-down, dark plate armor, glowing visor slit, rune cracks in the armor", consistency_notes=enemy_notes, placeholder_kind="enemy_base", size=(64, 64), transparency=True),
            sheet_asset("enemy_idle_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy idle animation.", prompt_subject="2-frame top-down cursed knight idle animation with faint armor pulse", consistency_notes=enemy_notes, placeholder_kind="enemy_idle", frame_count=2),
            sheet_asset("enemy_walk_up_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy walk-up animation.", prompt_subject="4-frame top-down cursed knight walk cycle facing up, deliberate armored movement", consistency_notes=enemy_notes, placeholder_kind="enemy_walk_up", frame_count=4),
            sheet_asset("enemy_walk_down_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy walk-down animation.", prompt_subject="4-frame top-down cursed knight walk cycle facing down, heavy armor silhouette", consistency_notes=enemy_notes, placeholder_kind="enemy_walk_down", frame_count=4),
            sheet_asset("enemy_walk_left_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy walk-left animation.", prompt_subject="4-frame top-down cursed knight walk cycle facing left, shield-like shoulder mass", consistency_notes=enemy_notes, placeholder_kind="enemy_walk_left", frame_count=4),
            sheet_asset("enemy_walk_right_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy walk-right animation.", prompt_subject="4-frame top-down cursed knight walk cycle facing right, shield-like shoulder mass", consistency_notes=enemy_notes, placeholder_kind="enemy_walk_right", frame_count=4),
            sheet_asset("enemy_alert_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy alert animation.", prompt_subject="4-frame top-down cursed knight alert animation with a bright curse flare and rigid posture", consistency_notes=enemy_notes, placeholder_kind="enemy_alert", frame_count=4),
            sheet_asset("enemy_chase_spritesheet.png", group="G. Enemy art", category="sprites_enemy", processed_subdir="sprites/enemy", purpose="Enemy chase animation.", prompt_subject="4-frame top-down cursed knight chase animation with faster stride and brighter curse glow", consistency_notes=enemy_notes, placeholder_kind="enemy_chase", frame_count=4),
        ]
    )

    vfx_notes = "Effects should stay crisp and legible over the maze without hiding core tile information."
    specs.extend(
        [
            sheet_asset("vfx_move_puff_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Movement dust puff effect.", prompt_subject="4-frame top-down dust and rune spark puff for a successful move", consistency_notes=vfx_notes, placeholder_kind="vfx_move_puff", frame_count=4),
            sheet_asset("vfx_blocked_bump_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Blocked move bump effect.", prompt_subject="3-frame top-down bump star and stone chip effect for colliding with a wall", consistency_notes=vfx_notes, placeholder_kind="vfx_blocked_bump", frame_count=3),
            sheet_asset("vfx_no_move_pulse_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="No-move pulse effect.", prompt_subject="4-frame top-down center pulse effect for a probabilistic stay-in-place result", consistency_notes=vfx_notes, placeholder_kind="vfx_no_move", frame_count=4),
            sheet_asset("vfx_trap_trigger_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Trap trigger effect.", prompt_subject="4-frame top-down trap rune snap effect with crimson shards", consistency_notes=vfx_notes, placeholder_kind="vfx_trap", frame_count=4),
            sheet_asset("vfx_lava_burst_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Lava burst effect.", prompt_subject="5-frame top-down lava burst effect with molten splash and ember sparks", consistency_notes=vfx_notes, placeholder_kind="vfx_lava", frame_count=5),
            sheet_asset("vfx_goal_activate_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Goal activation effect.", prompt_subject="4-frame top-down goal activation rune bloom with gold and teal light", consistency_notes=vfx_notes, placeholder_kind="vfx_goal", frame_count=4),
            static_asset("vfx_enemy_alert_icon.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Enemy alert icon.", prompt_subject="transparent alert icon with an eye-like rune and sharp gold flare", consistency_notes=vfx_notes, placeholder_kind="vfx_alert_icon", size=(64, 64), transparency=True),
            sheet_asset("vfx_tile_rune_pulse_spritesheet.png", group="H. VFX", category="vfx", processed_subdir="vfx", purpose="Tile rune pulse effect.", prompt_subject="4-frame top-down rune pulse effect that can sit above a special tile", consistency_notes=vfx_notes, placeholder_kind="vfx_tile_pulse", frame_count=4),
        ]
    )

    menu_button_notes = "Buttons should feel carved and magical, with clear state differences and enough empty center space for later text rendering in code."
    specs.extend(
        [
            static_asset("btn_menu_primary_idle.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Primary menu button idle state.", prompt_subject="transparent carved stone button, primary idle state, teal rune inlay, broad center panel", consistency_notes=menu_button_notes, placeholder_kind="button_primary_idle", size=(256, 80), transparency=True),
            static_asset("btn_menu_primary_hover.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Primary menu button hover state.", prompt_subject="transparent carved stone button, primary hover state, brighter teal and gold edge glow", consistency_notes=menu_button_notes, placeholder_kind="button_primary_hover", size=(256, 80), transparency=True),
            static_asset("btn_menu_primary_pressed.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Primary menu button pressed state.", prompt_subject="transparent carved stone button, primary pressed state, inset center panel and compact glow", consistency_notes=menu_button_notes, placeholder_kind="button_primary_pressed", size=(256, 80), transparency=True),
            static_asset("btn_menu_secondary_idle.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Secondary menu button idle state.", prompt_subject="transparent carved stone button, secondary idle state, restrained silver-rune detailing", consistency_notes=menu_button_notes, placeholder_kind="button_secondary_idle", size=(256, 80), transparency=True),
            static_asset("btn_menu_secondary_hover.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Secondary menu button hover state.", prompt_subject="transparent carved stone button, secondary hover state, brighter silver and teal edge highlights", consistency_notes=menu_button_notes, placeholder_kind="button_secondary_hover", size=(256, 80), transparency=True),
            static_asset("btn_level_locked.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Locked level-select button.", prompt_subject="transparent square level button with a dark lock rune on carved stone", consistency_notes=menu_button_notes, placeholder_kind="level_locked", size=(160, 160), transparency=True),
            static_asset("btn_level_unlocked.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Unlocked level-select button.", prompt_subject="transparent square level button with a glowing open rune gate on carved stone", consistency_notes=menu_button_notes, placeholder_kind="level_unlocked", size=(160, 160), transparency=True),
            static_asset("btn_level_completed.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Completed level-select button.", prompt_subject="transparent square level button with a completed gold rune seal on carved stone", consistency_notes=menu_button_notes, placeholder_kind="level_completed", size=(160, 160), transparency=True),
            static_asset("marker_level_locked.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Locked level marker.", prompt_subject="transparent small lock marker icon matching level button styling", consistency_notes=menu_button_notes, placeholder_kind="marker_locked", size=(64, 64), transparency=True),
            static_asset("marker_level_complete.png", group="I. Menu and level-select UI", category="ui_menu", processed_subdir="ui", purpose="Completed level marker.", prompt_subject="transparent small completion marker icon with a rune check seal", consistency_notes=menu_button_notes, placeholder_kind="marker_complete", size=(64, 64), transparency=True),
        ]
    )

    game_ui_notes = "In-game UI elements should share the same stone-and-rune language as the menu, with crisp icon centers and transparent edges."
    specs.extend(
        [
            static_asset("btn_ui_restart.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Restart button.", prompt_subject="transparent square UI button with a restart rune arrow engraved in stone", consistency_notes=game_ui_notes, placeholder_kind="ui_restart", size=(64, 64), transparency=True),
            static_asset("btn_ui_pause.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Pause button.", prompt_subject="transparent square UI button with a pause rune carved into stone", consistency_notes=game_ui_notes, placeholder_kind="ui_pause", size=(64, 64), transparency=True),
            static_asset("btn_ui_menu.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Return-to-menu button.", prompt_subject="transparent square UI button with a doorway rune icon carved into stone", consistency_notes=game_ui_notes, placeholder_kind="ui_menu", size=(64, 64), transparency=True),
            static_asset("btn_ui_sound_on.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Sound-on button.", prompt_subject="transparent square UI button with a speaker rune and active teal waves", consistency_notes=game_ui_notes, placeholder_kind="ui_sound_on", size=(64, 64), transparency=True),
            static_asset("btn_ui_sound_off.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Sound-off button.", prompt_subject="transparent square UI button with a speaker rune crossed out by a crimson slash", consistency_notes=game_ui_notes, placeholder_kind="ui_sound_off", size=(64, 64), transparency=True),
            static_asset("btn_ui_music_on.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Music-on button.", prompt_subject="transparent square UI button with a note-like rune and active glow", consistency_notes=game_ui_notes, placeholder_kind="ui_music_on", size=(64, 64), transparency=True),
            static_asset("btn_ui_music_off.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Music-off button.", prompt_subject="transparent square UI button with a note-like rune crossed out by a crimson slash", consistency_notes=game_ui_notes, placeholder_kind="ui_music_off", size=(64, 64), transparency=True),
            static_asset("btn_ui_info.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Info button.", prompt_subject="transparent square UI button with a rune sigil that implies help or legend information", consistency_notes=game_ui_notes, placeholder_kind="ui_info", size=(64, 64), transparency=True),
            static_asset("panel_probability_hud.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Probability HUD panel.", prompt_subject="transparent HUD panel with carved stone frame, circular rune slots, and a clear center strip for probability info", consistency_notes=game_ui_notes, placeholder_kind="panel_probability", size=(512, 160), transparency=True),
            static_asset("panel_pause_menu.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Pause menu panel.", prompt_subject="transparent large pause menu panel with elegant rune corners and calm stone interior", consistency_notes=game_ui_notes, placeholder_kind="panel_pause", size=(960, 540), transparency=True),
            static_asset("panel_victory.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Victory panel.", prompt_subject="transparent large victory panel with celebratory gold rune arcs and a clean content area", consistency_notes=game_ui_notes, placeholder_kind="panel_victory", size=(960, 540), transparency=True),
            static_asset("panel_defeat.png", group="J. In-game UI", category="ui_game", processed_subdir="ui", purpose="Defeat panel.", prompt_subject="transparent large defeat panel with darker stone tones and a restrained crimson rune fracture motif", consistency_notes=game_ui_notes, placeholder_kind="panel_defeat", size=(960, 540), transparency=True),
        ]
    )

    icon_notes = "Icons should match the same rune language as the overlays and remain readable at 64x64 with no text."
    specs.extend(
        [
            static_asset("icon_goal.png", group="K. Icons", category="icons", processed_subdir="icons", purpose="Goal icon.", prompt_subject="transparent rune goal icon combining a gate shape and radiant ring", consistency_notes=icon_notes, placeholder_kind="icon_goal", size=(64, 64), transparency=True),
            static_asset("icon_enemy_alert.png", group="K. Icons", category="icons", processed_subdir="icons", purpose="Enemy alert icon.", prompt_subject="transparent enemy alert icon with an eye rune and pointed flare", consistency_notes=icon_notes, placeholder_kind="icon_enemy_alert", size=(64, 64), transparency=True),
            static_asset("icon_trap.png", group="K. Icons", category="icons", processed_subdir="icons", purpose="Trap icon.", prompt_subject="transparent trap icon with a crimson spike rune inside a circle", consistency_notes=icon_notes, placeholder_kind="icon_trap", size=(64, 64), transparency=True),
            static_asset("icon_lava.png", group="K. Icons", category="icons", processed_subdir="icons", purpose="Lava icon.", prompt_subject="transparent lava icon with a molten droplet rune and ember sparks", consistency_notes=icon_notes, placeholder_kind="icon_lava", size=(64, 64), transparency=True),
            static_asset("icon_probability.png", group="K. Icons", category="icons", processed_subdir="icons", purpose="Probability icon.", prompt_subject="transparent probability icon with a compass circle and weighted rune wedges", consistency_notes=icon_notes, placeholder_kind="icon_probability", size=(64, 64), transparency=True),
        ]
    )

    return specs


def ensure_directories(specs: list[AssetSpec]) -> None:
    RAW_ART_DIR.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        spec.processed_path.parent.mkdir(parents=True, exist_ok=True)


def clamp(value: float, minimum: int = 0, maximum: int = 255) -> int:
    return max(minimum, min(maximum, int(value)))


def color(name: str, alpha: int | None = None) -> tuple[int, int, int, int]:
    base = PALETTE[name]
    if alpha is None:
        return base
    return (base[0], base[1], base[2], alpha)


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int] | None = None,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def radial_glow(image: Image.Image, center: tuple[int, int], radius: int, tint: tuple[int, int, int, int]) -> None:
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    for step in range(radius, 0, -6):
        alpha = clamp(tint[3] * (step / max(radius, 1)) * 0.32)
        draw.ellipse(
            (center[0] - step, center[1] - step, center[0] + step, center[1] + step),
            fill=(tint[0], tint[1], tint[2], alpha),
        )
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))


def draw_ruin_frame(draw: ImageDraw.ImageDraw, width: int, height: int, fill_name: str = "stone", line_name: str = "stone_dark") -> None:
    inset = max(4, min(width, height) // 12)
    rounded_rect(draw, (inset, inset, width - inset, height - inset), max(6, inset), color(fill_name), color(line_name), 3)
    draw.line((inset + 8, height // 2, width - inset - 8, height // 2), fill=color("shadow_soft", 80), width=2)


def draw_tile(spec: AssetSpec, image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    w, h = image.size
    draw_ruin_frame(draw, w, h, "stone", "stone_dark")
    inset = 10
    inner = (inset, inset, w - inset, h - inset)
    draw.rounded_rectangle(inner, radius=10, fill=color("stone_light"), outline=color("stone_dark"), width=2)
    if spec.placeholder_kind.startswith("tile_floor"):
        draw.line((16, 18, 48, 14), fill=color("stone"), width=3)
        draw.line((18, 46, 44, 20), fill=color("stone"), width=2)
        radial_glow(image, (32, 32), 18, color("teal", 48 if spec.placeholder_kind == "tile_floor_a" else 36))
    elif spec.placeholder_kind.startswith("tile_wall"):
        draw.rounded_rectangle((9, 9, 55, 55), radius=8, fill=color("shadow_soft"), outline=color("ink"), width=3)
        draw.rectangle((12, 16, 52, 27), fill=color("stone_dark"))
        draw.rectangle((12, 30, 52, 46), fill=color("stone"))
        if spec.placeholder_kind == "tile_wall_corner":
            draw.polygon([(12, 12), (40, 12), (40, 28), (52, 28), (52, 52), (12, 52)], fill=color("shadow_soft"), outline=color("ink"))
    elif spec.placeholder_kind == "tile_start":
        draw.ellipse((13, 13, 51, 51), outline=color("teal_bright"), width=4)
        draw.polygon([(32, 16), (40, 32), (32, 48), (24, 32)], fill=color("teal"))
        radial_glow(image, (32, 32), 20, color("teal", 84))
    elif spec.placeholder_kind == "tile_goal":
        draw.ellipse((12, 12, 52, 52), outline=color("gold"), width=4)
        draw.ellipse((22, 22, 42, 42), fill=color("gold", 96), outline=color("gold"), width=2)
        radial_glow(image, (32, 32), 22, color("gold", 96))
    elif spec.placeholder_kind == "tile_trap":
        draw.ellipse((12, 12, 52, 52), outline=color("crimson"), width=4)
        draw.polygon([(32, 14), (46, 48), (18, 48)], fill=color("crimson"))
        draw.line((22, 32, 42, 32), fill=color("white"), width=3)
    elif spec.placeholder_kind == "tile_lava":
        draw.ellipse((10, 12, 54, 52), fill=color("ember"), outline=color("gold"), width=2)
        draw.polygon([(20, 36), (28, 20), (36, 34), (44, 22), (42, 44), (24, 46)], fill=color("lava"))
        radial_glow(image, (32, 34), 22, color("ember", 120))


def draw_overlay(spec: AssetSpec, image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    if spec.placeholder_kind == "overlay_path":
        draw.line((10, 32, 54, 32), fill=color("teal", 220), width=8)
        draw.ellipse((24, 24, 40, 40), outline=color("teal_bright"), width=3)
    elif spec.placeholder_kind == "overlay_node":
        draw.ellipse((18, 18, 46, 46), fill=color("teal", 160), outline=color("teal_bright"), width=3)
        draw.ellipse((26, 26, 38, 38), fill=color("white", 200))
    else:
        draw.ellipse((6, 6, 58, 58), outline=color("stone_light", 140), width=3)
        arrow_fill = color("stone_light", 140)
        center_fill = color("stone_light", 100)
        if spec.placeholder_kind == "compass_intended":
            arrow_fill = color("teal_bright", 230)
        elif spec.placeholder_kind == "compass_opposite":
            arrow_fill = color("crimson", 230)
        elif spec.placeholder_kind in {"compass_left", "compass_right"}:
            arrow_fill = color("gold", 230)
        elif spec.placeholder_kind == "compass_stay":
            center_fill = color("violet", 220)
        elif spec.placeholder_kind == "compass_active":
            draw.rounded_rectangle((5, 5, 59, 59), radius=10, outline=color("teal_bright", 220), width=3)
            radial_glow(image, (32, 32), 22, color("teal", 80))
        draw.polygon([(32, 12), (38, 24), (26, 24)], fill=arrow_fill)
        draw.polygon([(52, 32), (40, 38), (40, 26)], fill=arrow_fill if spec.placeholder_kind == "compass_right" else color("stone_light", 120))
        draw.polygon([(32, 52), (26, 40), (38, 40)], fill=arrow_fill if spec.placeholder_kind == "compass_opposite" else color("stone_light", 120))
        draw.polygon([(12, 32), (24, 26), (24, 38)], fill=arrow_fill if spec.placeholder_kind == "compass_left" else color("stone_light", 120))
        draw.ellipse((24, 24, 40, 40), fill=center_fill, outline=color("shadow", 160), width=2)


def draw_prop(spec: AssetSpec, image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    if spec.placeholder_kind == "prop_column":
        draw.rectangle((22, 8, 42, 48), fill=color("stone"), outline=color("stone_dark"), width=2)
        draw.polygon([(18, 48), (46, 48), (54, 58), (12, 58)], fill=color("stone_dark"))
        draw.line((24, 22, 40, 18), fill=color("shadow"), width=3)
    elif spec.placeholder_kind == "prop_rune":
        draw.polygon([(32, 8), (48, 28), (38, 56), (20, 56), (12, 28)], fill=color("stone_light"), outline=color("teal_bright"))
        draw.line((22, 32, 42, 32), fill=color("teal"), width=3)
        draw.line((32, 18, 32, 46), fill=color("teal"), width=3)
        radial_glow(image, (32, 32), 18, color("teal", 96))
    elif spec.placeholder_kind == "prop_moss":
        draw.pieslice((4, 18, 60, 58), 180, 360, fill=color("moss"), outline=color("stone_dark"))
        draw.ellipse((18, 30, 30, 44), fill=color("teal", 80))
    elif spec.placeholder_kind == "prop_rubble":
        for box in [(12, 34, 24, 50), (22, 28, 38, 48), (36, 34, 50, 52)]:
            draw.rounded_rectangle(box, radius=4, fill=color("stone"), outline=color("stone_dark"), width=2)


def draw_character_frame(kind: str, direction: str, frame_index: int, frame_count: int, size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, color("transparent"))
    draw = ImageDraw.Draw(image)
    cx, cy = size[0] // 2, size[1] // 2 + 2
    bob = int(math.sin((frame_index / max(frame_count, 1)) * math.tau) * 2)
    if "player" in kind:
        body = color("parchment")
        accent = color("teal")
        head = color("sand")
        outline = color("shadow")
        satchel = color("gold")
        width_scale = 16
        shoulder = 18
    else:
        body = color("stone_dark")
        accent = color("crimson")
        head = color("silver")
        outline = color("ink")
        satchel = color("violet")
        width_scale = 18
        shoulder = 22
    body_box = (cx - width_scale, cy - 12 + bob, cx + width_scale, cy + 14 + bob)
    draw.ellipse((cx - 9, cy - 26 + bob, cx + 9, cy - 8 + bob), fill=head, outline=outline, width=2)
    draw.rounded_rectangle(body_box, radius=8, fill=body, outline=outline, width=2)
    draw.line((cx, cy - 8 + bob, cx, cy + 12 + bob), fill=accent, width=4)
    if "player" in kind:
        draw.ellipse((cx + 4, cy - 4 + bob, cx + 14, cy + 8 + bob), fill=satchel, outline=outline, width=2)
    else:
        draw.polygon([(cx - shoulder, cy - 10 + bob), (cx - 6, cy - 20 + bob), (cx - 2, cy - 10 + bob)], fill=satchel, outline=outline)
        draw.polygon([(cx + shoulder, cy - 10 + bob), (cx + 6, cy - 20 + bob), (cx + 2, cy - 10 + bob)], fill=satchel, outline=outline)
        radial_glow(image, (cx, cy - 16 + bob), 10, color("crimson", 72))
    if direction == "up":
        draw.line((cx, cy - 12 + bob, cx, cy - 24 + bob), fill=accent, width=3)
    elif direction == "down":
        draw.line((cx, cy + 4 + bob, cx, cy + 18 + bob), fill=accent, width=3)
    elif direction == "left":
        draw.line((cx - 4, cy - 4 + bob, cx - 18, cy - 2 + bob), fill=accent, width=3)
    elif direction == "right":
        draw.line((cx + 4, cy - 4 + bob, cx + 18, cy - 2 + bob), fill=accent, width=3)
    step = -4 if frame_index % 2 == 0 else 4
    draw.line((cx - 7, cy + 14 + bob, cx - 7 + step, cy + 24 + bob), fill=outline, width=4)
    draw.line((cx + 7, cy + 14 + bob, cx + 7 - step, cy + 24 + bob), fill=outline, width=4)
    return image


def draw_sprite_sheet(spec: AssetSpec, image: Image.Image) -> None:
    frame_w = spec.frame_width or spec.width
    frame_h = spec.frame_height or spec.height
    for frame_index in range(spec.frame_count):
        direction = "down"
        if "walk_up" in spec.placeholder_kind:
            direction = "up"
        elif "walk_left" in spec.placeholder_kind:
            direction = "left"
        elif "walk_right" in spec.placeholder_kind:
            direction = "right"
        elif "enemy_alert" in spec.placeholder_kind:
            direction = "up"
        frame = draw_character_frame(spec.placeholder_kind, direction, frame_index, spec.frame_count, (frame_w, frame_h))
        if "death" in spec.placeholder_kind:
            overlay = Image.new("RGBA", frame.size, color("transparent"))
            overlay_draw = ImageDraw.Draw(overlay)
            spread = 8 + frame_index * 3
            overlay_draw.ellipse((32 - spread, 32 - spread, 32 + spread, 32 + spread), outline=color("crimson", clamp(220 - frame_index * 35)), width=3)
            frame.alpha_composite(overlay)
            frame = frame.rotate(frame_index * 6, resample=Image.Resampling.BICUBIC)
        if "victory" in spec.placeholder_kind:
            radial_glow(frame, (32, 20), 10 + frame_index * 3, color("gold", 88))
        if "enemy_alert" in spec.placeholder_kind:
            radial_glow(frame, (32, 12), 10 + frame_index * 2, color("gold", 110))
        if "enemy_chase" in spec.placeholder_kind:
            radial_glow(frame, (32, 20), 12 + frame_index, color("crimson", 72))
        image.alpha_composite(frame, (frame_index * frame_w, 0))


def draw_vfx(spec: AssetSpec, image: Image.Image) -> None:
    frame_w = spec.frame_width or spec.width
    frame_h = spec.frame_height or spec.height
    for frame_index in range(spec.frame_count):
        frame = Image.new("RGBA", (frame_w, frame_h), color("transparent"))
        draw = ImageDraw.Draw(frame)
        center = (frame_w // 2, frame_h // 2)
        progress = (frame_index + 1) / max(spec.frame_count, 1)
        if spec.placeholder_kind == "vfx_move_puff":
            radius = 10 + int(progress * 10)
            draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=color("stone_light", 220), width=3)
            draw.ellipse((center[0] - radius // 2, center[1] - radius // 2, center[0] + radius // 2, center[1] + radius // 2), fill=color("teal", clamp(140 - frame_index * 20)))
        elif spec.placeholder_kind == "vfx_blocked_bump":
            for angle in range(0, 360, 45):
                distance = 8 + frame_index * 4
                x = center[0] + math.cos(math.radians(angle)) * distance
                y = center[1] + math.sin(math.radians(angle)) * distance
                draw.line((center[0], center[1], x, y), fill=color("crimson"), width=3)
        elif spec.placeholder_kind == "vfx_no_move":
            radius = 8 + int(progress * 16)
            draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=color("violet", 220), width=4)
            draw.ellipse((center[0] - 6, center[1] - 6, center[0] + 6, center[1] + 6), fill=color("white", 180))
        elif spec.placeholder_kind == "vfx_trap":
            draw.polygon([(32, 8 + frame_index), (52, 50 - frame_index), (12, 50 - frame_index)], outline=color("crimson"), fill=color("crimson", clamp(120 - frame_index * 12)))
        elif spec.placeholder_kind == "vfx_lava":
            radius = 8 + frame_index * 4
            draw.ellipse((32 - radius, 32 - radius, 32 + radius, 32 + radius), fill=color("ember", clamp(160 - frame_index * 12)), outline=color("gold"), width=2)
            draw.polygon([(32, 10), (40, 26), (52, 20), (44, 38), (56, 50), (32, 42), (8, 50), (20, 38), (12, 20), (24, 26)], fill=color("lava", clamp(200 - frame_index * 12)))
        elif spec.placeholder_kind == "vfx_goal":
            radius = 10 + frame_index * 5
            draw.ellipse((32 - radius, 32 - radius, 32 + radius, 32 + radius), outline=color("gold"), width=3)
            draw.ellipse((32 - radius // 2, 32 - radius // 2, 32 + radius // 2, 32 + radius // 2), outline=color("teal_bright"), width=2)
        elif spec.placeholder_kind == "vfx_tile_pulse":
            radius = 12 + frame_index * 4
            draw.rectangle((10, 10, 54, 54), outline=color("teal", clamp(200 - frame_index * 25)), width=3)
            draw.ellipse((32 - radius // 2, 32 - radius // 2, 32 + radius // 2, 32 + radius // 2), outline=color("teal_bright", clamp(180 - frame_index * 20)), width=2)
        image.alpha_composite(frame, (frame_index * frame_w, 0))


def draw_static_ui(spec: AssetSpec, image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    w, h = image.size
    if spec.placeholder_kind.startswith("button_"):
        fill = "stone"
        glow = "teal"
        if "secondary" in spec.placeholder_kind:
            glow = "silver"
        if "hover" in spec.placeholder_kind:
            fill = "stone_light"
        if "pressed" in spec.placeholder_kind:
            fill = "stone_dark"
        rounded_rect(draw, (6, 6, w - 6, h - 6), 22, color(fill), color("shadow"), 3)
        draw.line((22, h // 2, w - 22, h // 2), fill=color(glow, 120), width=5)
        radial_glow(image, (w // 2, h // 2), min(w, h) // 3, color(glow, 64))
    elif spec.placeholder_kind.startswith("level_"):
        rounded_rect(draw, (8, 8, w - 8, h - 8), 18, color("stone"), color("shadow"), 4)
        if spec.placeholder_kind == "level_locked":
            draw.rectangle((54, 74, 106, 118), fill=color("shadow_soft"), outline=color("stone_light"), width=3)
            draw.arc((54, 36, 106, 90), start=180, end=360, fill=color("stone_light"), width=4)
        elif spec.placeholder_kind == "level_unlocked":
            draw.polygon([(80, 30), (118, 80), (80, 130), (42, 80)], fill=color("teal", 120), outline=color("teal_bright"))
        elif spec.placeholder_kind == "level_completed":
            draw.ellipse((34, 34, 126, 126), fill=color("gold", 110), outline=color("gold"), width=4)
            draw.line((54, 82, 74, 102), fill=color("white"), width=8)
            draw.line((74, 102, 110, 56), fill=color("white"), width=8)
    elif spec.placeholder_kind.startswith("marker_"):
        draw.ellipse((10, 10, w - 10, h - 10), fill=color("shadow_soft"), outline=color("stone_light"), width=3)
        if spec.placeholder_kind == "marker_locked":
            draw.arc((18, 16, w - 18, h - 20), start=180, end=360, fill=color("stone_light"), width=3)
            draw.rectangle((20, 28, w - 20, h - 14), fill=color("stone"), outline=color("white"), width=2)
        else:
            draw.line((18, 34, 28, 44), fill=color("gold"), width=5)
            draw.line((28, 44, 46, 18), fill=color("gold"), width=5)
    elif spec.placeholder_kind.startswith("ui_"):
        rounded_rect(draw, (4, 4, w - 4, h - 4), 14, color("stone"), color("shadow"), 3)
        if spec.placeholder_kind == "ui_restart":
            draw.arc((14, 14, 50, 50), start=20, end=320, fill=color("teal_bright"), width=4)
            draw.polygon([(42, 12), (52, 14), (46, 24)], fill=color("teal_bright"))
        elif spec.placeholder_kind == "ui_pause":
            draw.rectangle((20, 16, 28, 48), fill=color("gold"))
            draw.rectangle((36, 16, 44, 48), fill=color("gold"))
        elif spec.placeholder_kind == "ui_menu":
            draw.rectangle((18, 18, 46, 46), outline=color("teal_bright"), width=3)
            draw.line((22, 46, 32, 36), fill=color("teal_bright"), width=3)
            draw.line((42, 46, 32, 36), fill=color("teal_bright"), width=3)
        elif spec.placeholder_kind in {"ui_sound_on", "ui_sound_off"}:
            draw.polygon([(16, 28), (24, 28), (34, 18), (34, 46), (24, 36), (16, 36)], fill=color("stone_light"))
            draw.arc((30, 20, 48, 44), start=-60, end=60, fill=color("teal_bright"), width=3)
            if spec.placeholder_kind.endswith("off"):
                draw.line((16, 16, 48, 48), fill=color("crimson"), width=4)
        elif spec.placeholder_kind in {"ui_music_on", "ui_music_off"}:
            draw.line((28, 16, 28, 44), fill=color("teal_bright"), width=4)
            draw.line((28, 16, 42, 12), fill=color("teal_bright"), width=4)
            draw.ellipse((20, 36, 32, 48), fill=color("stone_light"))
            if spec.placeholder_kind.endswith("off"):
                draw.line((16, 16, 48, 48), fill=color("crimson"), width=4)
        elif spec.placeholder_kind == "ui_info":
            draw.ellipse((24, 14, 40, 30), fill=color("teal_bright"))
            draw.line((32, 28, 32, 44), fill=color("teal_bright"), width=4)
            draw.ellipse((28, 46, 36, 54), fill=color("teal_bright"))
    elif spec.placeholder_kind.startswith("panel_"):
        rounded_rect(draw, (8, 8, w - 8, h - 8), 26, color("stone", 220), color("shadow"), 4)
        rounded_rect(draw, (28, 28, w - 28, h - 28), 20, color("shadow_soft", 150), color("stone_light", 180), 2)
        accent = "teal"
        if spec.placeholder_kind == "panel_victory":
            accent = "gold"
        elif spec.placeholder_kind == "panel_defeat":
            accent = "crimson"
        for px, py in [(42, 42), (w - 42, 42), (42, h - 42), (w - 42, h - 42)]:
            draw.ellipse((px - 12, py - 12, px + 12, py + 12), outline=color(accent, 200), width=3)
        radial_glow(image, (w // 2, 58), 40, color(accent, 88))


def draw_icon(spec: AssetSpec, image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill=color("shadow_soft", 180), outline=color("stone_light"), width=3)
    if spec.placeholder_kind == "icon_goal":
        draw.ellipse((18, 18, 46, 46), outline=color("gold"), width=3)
        draw.rectangle((28, 16, 36, 48), fill=color("teal_bright"))
    elif spec.placeholder_kind in {"icon_enemy_alert", "vfx_alert_icon"}:
        draw.polygon([(32, 10), (50, 32), (32, 54), (14, 32)], outline=color("gold"), fill=color("crimson", 90))
        draw.ellipse((22, 24, 42, 40), fill=color("white"), outline=color("shadow"), width=2)
        draw.ellipse((28, 28, 36, 36), fill=color("shadow"))
    elif spec.placeholder_kind == "icon_trap":
        draw.polygon([(32, 14), (48, 46), (16, 46)], fill=color("crimson"), outline=color("white"))
    elif spec.placeholder_kind == "icon_lava":
        draw.polygon([(24, 12), (42, 28), (36, 52), (18, 42)], fill=color("ember"), outline=color("gold"))
    elif spec.placeholder_kind == "icon_probability":
        draw.ellipse((16, 16, 48, 48), outline=color("teal_bright"), width=3)
        draw.polygon([(32, 14), (38, 28), (26, 28)], fill=color("gold"))
        draw.polygon([(50, 32), (36, 38), (36, 26)], fill=color("stone_light"))
        draw.ellipse((26, 26, 38, 38), fill=color("violet"))


def draw_logo(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    w, h = image.size
    radial_glow(image, (w // 2, h // 2), 180, color("teal", 76))
    radial_glow(image, (w // 2, h // 2), 140, color("gold", 68))
    draw.ellipse((180, 70, w - 180, h - 70), outline=color("gold"), width=8)
    draw.ellipse((220, 110, w - 220, h - 110), outline=color("teal_bright"), width=4)
    font_large = find_font(94)
    font_small = find_font(38)
    title = "Markov's Maze"
    subtitle = "Ancient Ruins. Uncertain Paths."
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_x = (w - (title_bbox[2] - title_bbox[0])) // 2
    title_y = 156
    draw.text((title_x + 4, title_y + 4), title, fill=color("shadow"), font=font_large)
    draw.text((title_x, title_y), title, fill=color("parchment"), font=font_large)
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_x = (w - (subtitle_bbox[2] - subtitle_bbox[0])) // 2
    draw.text((subtitle_x, 286), subtitle, fill=color("gold"), font=font_small)


def draw_background(spec: AssetSpec, image: Image.Image) -> None:
    base = Image.new("RGBA", image.size, color("shadow"))
    width, height = image.size
    draw = ImageDraw.Draw(base)
    for y in range(height):
        blend = y / max(height - 1, 1)
        r = clamp(PALETTE["shadow"][0] * (1 - blend) + PALETTE["stone"][0] * blend)
        g = clamp(PALETTE["shadow"][1] * (1 - blend) + PALETTE["stone"][1] * blend)
        b = clamp(PALETTE["shadow"][2] * (1 - blend) + PALETTE["sand"][2] * blend * 0.75)
        draw.line((0, y, width, y), fill=(r, g, b, 255))
    haze = Image.new("RGBA", image.size, color("transparent"))
    haze_draw = ImageDraw.Draw(haze)
    for index in range(10):
        band_y = int(height * (0.24 + index * 0.07))
        haze_draw.ellipse((-200, band_y - 100, width + 200, band_y + 80), fill=color("teal", 10 + (index % 3) * 4))
    base.alpha_composite(haze.filter(ImageFilter.GaussianBlur(24)))
    silhouette = Image.new("RGBA", image.size, color("transparent"))
    sdraw = ImageDraw.Draw(silhouette)
    layers = 4 if "parallax" in spec.placeholder_kind else 3
    for layer in range(layers):
        ground = int(height * (0.72 - layer * 0.12))
        width_step = 120 + layer * 50
        offset = (layer * 37) % width_step
        fill_name = "stone_dark" if layer < 2 else "shadow"
        for x in range(-offset, width + width_step, width_step):
            tower_w = width_step - 18
            tower_h = 140 + (layer * 30) + ((x // max(width_step, 1)) % 4) * 22
            sdraw.rectangle((x, ground - tower_h, x + tower_w, ground), fill=color(fill_name, 210))
            sdraw.rectangle((x + tower_w // 3, ground - tower_h - 28, x + (tower_w // 3) * 2, ground - tower_h), fill=color(fill_name, 210))
            sdraw.arc((x + 16, ground - 70, x + tower_w - 16, ground + 10), start=180, end=360, fill=color("stone_light", 100), width=2)
    base.alpha_composite(silhouette)
    accent = "teal"
    if spec.placeholder_kind == "background_select":
        accent = "gold"
    elif spec.placeholder_kind == "background_gameplay":
        accent = "stone_light"
    elif spec.placeholder_kind == "background_parallax_b":
        accent = "violet"
    glow = Image.new("RGBA", image.size, color("transparent"))
    gdraw = ImageDraw.Draw(glow)
    for x in range(180, width, 320):
        size = 48 if "parallax" in spec.placeholder_kind else 60
        y = int(height * (0.28 + (x % 3) * 0.06))
        gdraw.ellipse((x - size, y - size, x + size, y + size), outline=color(accent, 120), width=3)
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
    if spec.placeholder_kind == "background_menu":
        radial_glow(base, (width // 2, height // 3), 180, color("gold", 60))
    elif spec.placeholder_kind == "background_select":
        radial_glow(base, (width // 2, height // 2), 160, color("teal", 40))
    elif spec.placeholder_kind == "background_gameplay":
        radial_glow(base, (width // 2, height // 2), 220, color("teal", 26))
    image.alpha_composite(base)


def build_placeholder_image(spec: AssetSpec) -> Image.Image:
    background = color("transparent") if spec.transparency else color("shadow")
    image = Image.new("RGBA", (spec.width, spec.height), background)
    if spec.placeholder_kind == "logo":
        draw_logo(image)
    elif spec.group == "B. Backgrounds":
        draw_background(spec, image)
    elif spec.group == "C. Tiles":
        draw_tile(spec, image)
    elif spec.group == "D. Overlays and path markers":
        draw_overlay(spec, image)
    elif spec.group == "E. Props":
        draw_prop(spec, image)
    elif spec.group in {"F. Player art", "G. Enemy art"} and spec.frame_count == 1:
        frame = draw_character_frame(spec.placeholder_kind, "down", 0, 1, (spec.width, spec.height))
        image.alpha_composite(frame)
    elif spec.group in {"F. Player art", "G. Enemy art"}:
        draw_sprite_sheet(spec, image)
    elif spec.group == "H. VFX" and spec.frame_count == 1:
        draw_icon(spec, image)
    elif spec.group == "H. VFX":
        draw_vfx(spec, image)
    elif spec.group in {"I. Menu and level-select UI", "J. In-game UI"}:
        draw_static_ui(spec, image)
    elif spec.group == "K. Icons":
        draw_icon(spec, image)
    return image


def svg_color(name: str, alpha: float = 1.0) -> str:
    rgba = PALETTE[name]
    return f"rgba({rgba[0]}, {rgba[1]}, {rgba[2]}, {alpha:.3f})"


def build_static_svg(spec: AssetSpec) -> str:
    w, h = spec.width, spec.height
    shapes: list[str] = []
    if spec.placeholder_kind == "logo":
        shapes.extend(
            [
                f'<ellipse cx="{w // 2}" cy="{h // 2}" rx="{w // 2 - 180}" ry="{h // 2 - 70}" fill="none" stroke="{svg_color("gold")}" stroke-width="8" />',
                f'<ellipse cx="{w // 2}" cy="{h // 2}" rx="{w // 2 - 220}" ry="{h // 2 - 110}" fill="none" stroke="{svg_color("teal_bright")}" stroke-width="4" />',
                f'<text x="{w // 2}" y="240" fill="{svg_color("parchment")}" font-size="92" font-family="Georgia, serif" text-anchor="middle">Markov&apos;s Maze</text>',
            ]
        )
    elif spec.group == "C. Tiles":
        shapes.append(f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="10" fill="{svg_color("stone_light")}" stroke="{svg_color("stone_dark")}" stroke-width="3" />')
        if spec.placeholder_kind == "tile_goal":
            shapes.append(f'<circle cx="{w // 2}" cy="{h // 2}" r="20" fill="{svg_color("gold", 0.35)}" stroke="{svg_color("gold")}" stroke-width="4" />')
        elif spec.placeholder_kind == "tile_start":
            shapes.append(f'<circle cx="{w // 2}" cy="{h // 2}" r="20" fill="{svg_color("teal", 0.25)}" stroke="{svg_color("teal_bright")}" stroke-width="4" />')
        elif spec.placeholder_kind == "tile_trap":
            shapes.append(f'<polygon points="32,14 46,48 18,48" fill="{svg_color("crimson")}" />')
        elif spec.placeholder_kind == "tile_lava":
            shapes.append(f'<ellipse cx="{w // 2}" cy="34" rx="22" ry="18" fill="{svg_color("ember")}" stroke="{svg_color("gold")}" stroke-width="2" />')
        elif spec.placeholder_kind.startswith("tile_wall"):
            shapes.append(f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" rx="8" fill="{svg_color("shadow_soft")}" stroke="{svg_color("ink")}" stroke-width="3" />')
        else:
            shapes.append(f'<line x1="16" y1="18" x2="48" y2="14" stroke="{svg_color("stone")}" stroke-width="3" />')
    elif spec.group == "D. Overlays and path markers":
        if spec.placeholder_kind == "overlay_path":
            shapes.append(f'<line x1="10" y1="32" x2="54" y2="32" stroke="{svg_color("teal_bright", 0.9)}" stroke-width="8" stroke-linecap="round" />')
        elif spec.placeholder_kind == "overlay_node":
            shapes.append(f'<circle cx="32" cy="32" r="14" fill="{svg_color("teal", 0.55)}" stroke="{svg_color("teal_bright")}" stroke-width="3" />')
        else:
            shapes.append(f'<circle cx="32" cy="32" r="26" fill="none" stroke="{svg_color("stone_light", 0.65)}" stroke-width="3" />')
            shapes.append(f'<circle cx="32" cy="32" r="8" fill="{svg_color("violet", 0.5 if spec.placeholder_kind == "compass_stay" else 0.2)}" />')
    elif spec.group == "E. Props":
        if spec.placeholder_kind == "prop_column":
            shapes.append(f'<rect x="22" y="8" width="20" height="40" fill="{svg_color("stone")}" stroke="{svg_color("stone_dark")}" stroke-width="2" />')
            shapes.append(f'<polygon points="18,48 46,48 54,58 12,58" fill="{svg_color("stone_dark")}" />')
        elif spec.placeholder_kind == "prop_rune":
            shapes.append(f'<polygon points="32,8 48,28 38,56 20,56 12,28" fill="{svg_color("stone_light")}" stroke="{svg_color("teal_bright")}" stroke-width="2" />')
        elif spec.placeholder_kind == "prop_moss":
            shapes.append(f'<path d="M6,40 C14,22 28,20 38,28 C48,22 58,28 60,44 L60,58 L6,58 Z" fill="{svg_color("moss")}" />')
        else:
            shapes.append(f'<circle cx="20" cy="44" r="10" fill="{svg_color("stone")}" /><circle cx="34" cy="36" r="10" fill="{svg_color("stone_light")}" /><circle cx="46" cy="46" r="8" fill="{svg_color("stone")}" />')
    elif spec.group in {"I. Menu and level-select UI", "J. In-game UI", "K. Icons", "H. VFX"}:
        shapes.append(f'<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="{max(12, min(w, h) // 8)}" fill="{svg_color("stone", 0.85)}" stroke="{svg_color("shadow")}" stroke-width="3" />')
        shapes.append(f'<circle cx="{w // 2}" cy="{h // 2}" r="{max(8, min(w, h) // 5)}" fill="{svg_color("teal", 0.25)}" stroke="{svg_color("teal_bright")}" stroke-width="3" />')
    elif spec.group in {"F. Player art", "G. Enemy art"}:
        shapes.append(f'<circle cx="{w // 2}" cy="20" r="9" fill="{svg_color("sand" if spec.group == "F. Player art" else "silver")}" stroke="{svg_color("shadow")}" stroke-width="2" />')
        shapes.append(f'<rect x="{w // 2 - 18}" y="24" width="36" height="28" rx="10" fill="{svg_color("parchment" if spec.group == "F. Player art" else "stone_dark")}" stroke="{svg_color("shadow")}" stroke-width="2" />')
        shapes.append(f'<line x1="{w // 2}" y1="26" x2="{w // 2}" y2="48" stroke="{svg_color("teal" if spec.group == "F. Player art" else "crimson")}" stroke-width="4" />')
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            "<!-- Local placeholder source generated for Markov's Maze -->",
            *shapes,
            "</svg>",
        ]
    )


def save_art_assets(specs: list[AssetSpec]) -> None:
    for spec in specs:
        image = build_placeholder_image(spec)
        image.save(spec.processed_path)
        if spec.raw_svg_path:
            spec.raw_svg_path.write_text(build_static_svg(spec), encoding="utf-8")


def build_prompt_text(spec: AssetSpec) -> str:
    size_text = f"{spec.width}x{spec.height}"
    base_style = ", ".join(GLOBAL_VISUAL_STYLE)
    if spec.frame_count > 1:
        return (
            f"Create a horizontal sprite sheet for {spec.filename}. Purpose: {spec.purpose} "
            f"Use {spec.frame_count} evenly sized frames at {spec.frame_width}x{spec.frame_height} each "
            f"for a total sheet size of {size_text}. Subject: {spec.prompt_subject}. "
            f"Style: {base_style}. Transparent background. Keep animation readable and compact. "
            f"Maintain consistency with the rest of Markov's Maze: {spec.consistency_notes}"
        )
    transparency_text = "Transparent background." if spec.transparency else "Opaque background."
    return (
        f"Create {spec.filename} for Markov's Maze. Purpose: {spec.purpose} "
        f"Dimensions: {size_text}. Subject: {spec.prompt_subject}. "
        f"Style: {base_style}. {transparency_text} "
        f"Maintain consistency with the rest of Markov's Maze: {spec.consistency_notes}"
    )


def write_asset_manifest_json(specs: list[AssetSpec]) -> None:
    payload = {
        "project": "Markov's Maze",
        "art_generation_mode": "local_placeholder_fallback",
        "image_provider_status": "No external image-generation provider or MCP resource was configured in this environment.",
        "global_visual_style": GLOBAL_VISUAL_STYLE,
        "assets": [spec.to_manifest_entry() for spec in specs],
        "summary": {
            "asset_count": len(specs),
            "placeholder_generated_count": len(specs),
            "groups": sorted({spec.group for spec in specs}),
        },
    }
    (DATA_DIR / "asset_manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_asset_manifest_markdown(specs: list[AssetSpec]) -> None:
    lines = [
        "# Markov's Maze Asset Manifest",
        "",
        "Readable summary of the complete art inventory prepared for the later Phaser implementation phase.",
        "",
        "Status legend:",
        "- `placeholder_generated`: local procedural PNG placeholder exists at the final runtime filename.",
        "- `raw_svg`: editable SVG source exists for static assets where practical.",
        "",
    ]
    groups = sorted({spec.group for spec in specs}, key=lambda value: value[0])
    for group in groups:
        lines.append(f"## {group}")
        lines.append("")
        lines.append("| Filename | Processed path | Dimensions | Frames | Transparency | Status |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for spec in [item for item in specs if item.group == group]:
            dims = f"{spec.width}x{spec.height}"
            frames = str(spec.frame_count)
            transparency = "yes" if spec.transparency else "no"
            status = spec.status if not spec.raw_svg else f"{spec.status} + raw_svg"
            lines.append(f"| `{spec.filename}` | `{relpath(spec.processed_path)}` | `{dims}` | `{frames}` | `{transparency}` | `{status}` |")
        lines.append("")
    (DOCS_DIR / "asset_manifest.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_prompt_bank(specs: list[AssetSpec]) -> None:
    lines = [
        "# Markov's Maze Art Prompt Bank",
        "",
        "Production-oriented prompt bank for final art generation. These prompts preserve the current design brief and the stable runtime filenames already used by the placeholder export.",
        "",
    ]
    for spec in specs:
        lines.extend(
            [
                f"## {spec.filename}",
                "",
                f"- Filename: `{spec.filename}`",
                f"- Purpose: {spec.purpose}",
                f"- Dimensions: `{spec.width}x{spec.height}`",
                f"- Transparency: `{'yes' if spec.transparency else 'no'}`",
                f"- Frame count: `{spec.frame_count}`",
                f"- Notes for consistency: {spec.consistency_notes}",
                "- Prompt text:",
                "",
                f"```text\n{build_prompt_text(spec)}\n```",
                "",
            ]
        )
    (DOCS_DIR / "art_prompt_bank.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    specs = build_asset_specs()
    ensure_directories(specs)
    save_art_assets(specs)
    write_asset_manifest_json(specs)
    write_asset_manifest_markdown(specs)
    write_prompt_bank(specs)
    print(f"Exported {len(specs)} placeholder art assets.")


if __name__ == "__main__":
    main()
