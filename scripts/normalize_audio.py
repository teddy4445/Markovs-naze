from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_AUDIO_DIR = ROOT / "assets" / "raw" / "audio"
PROCESSED_SFX_DIR = ROOT / "assets" / "processed" / "audio" / "sfx"
PROCESSED_MUSIC_DIR = ROOT / "assets" / "processed" / "audio" / "music"
MANIFEST_PATH = ROOT / "data" / "audio_manifest.json"


def archive_item(
    asset_id: str,
    category: str,
    raw_filename: str,
    processed_subdir: str,
    processed_filename: str,
    source_archive: str,
    archive_member: str,
    page_url: str,
    download_url: str,
    asset_title: str,
    author: str,
    notes: str,
) -> dict:
    return {
        "asset_id": asset_id,
        "category": category,
        "status": "sourced",
        "local_filename": raw_filename,
        "raw_path": f"assets/raw/audio/{raw_filename}",
        "processed_path": f"assets/processed/audio/{processed_subdir}/{processed_filename}",
        "source_type": "archive_member",
        "source_archive": f"assets/raw/audio/{source_archive}",
        "archive_member": archive_member,
        "source_page_url": page_url,
        "direct_download_url": download_url,
        "asset_title": asset_title,
        "author": author,
        "chosen_license": "CC0",
        "attribution_required": False,
        "exact_attribution_text": "",
        "notes": notes,
    }


def direct_item(
    asset_id: str,
    category: str,
    raw_filename: str,
    processed_subdir: str,
    processed_filename: str,
    page_url: str,
    download_url: str,
    asset_title: str,
    author: str,
    notes: str,
    downloaded_filename: str | None = None,
) -> dict:
    item = {
        "asset_id": asset_id,
        "category": category,
        "status": "sourced",
        "local_filename": raw_filename,
        "raw_path": f"assets/raw/audio/{raw_filename}",
        "processed_path": f"assets/processed/audio/{processed_subdir}/{processed_filename}",
        "source_type": "direct_download",
        "source_page_url": page_url,
        "direct_download_url": download_url,
        "asset_title": asset_title,
        "author": author,
        "chosen_license": "CC0",
        "attribution_required": False,
        "exact_attribution_text": "",
        "notes": notes,
    }
    if downloaded_filename:
        item["downloaded_source_path"] = f"assets/raw/audio/{downloaded_filename}"
    return item


def build_audio_items() -> list[dict]:
    return [
        archive_item("player_step", "movement_sfx", "player_step_source.ogg", "sfx", "player_step.ogg", "kddDifferentSteps_0.zip", "stone01.ogg", "https://opengameart.org/content/different-steps-on-wood-stone-leaves-gravel-and-mud", "https://opengameart.org/sites/default/files/%5Bkdd%5DDifferentSteps_0.zip", "Different steps on wood, stone, leaves, gravel and mud", "TinyWorlds", "Stone footstep chosen as the baseline maze movement cue."),
        archive_item("player_move_intended", "movement_sfx", "player_move_intended_source.wav", "sfx", "player_move_intended.wav", "tinysized.zip", "sfx-cc0/boots-leather-step-01.wav", "https://opengameart.org/content/fantasy-sound-effects-tinysized-sfx", "https://opengameart.org/sites/default/files/tinysized.zip", "Fantasy Sound Effects (Tinysized SFX)", "Vehicle", "Leather step adds a slightly stronger committed move variant."),
        archive_item("player_move_alternate", "movement_sfx", "player_move_alternate_source.ogg", "sfx", "player_move_alternate.ogg", "kddDifferentSteps_0.zip", "gravel.ogg", "https://opengameart.org/content/different-steps-on-wood-stone-leaves-gravel-and-mud", "https://opengameart.org/sites/default/files/%5Bkdd%5DDifferentSteps_0.zip", "Different steps on wood, stone, leaves, gravel and mud", "TinyWorlds", "Gravel variation distinguishes alternate movement outcomes without sounding like failure."),
        archive_item("player_no_move", "movement_sfx", "player_no_move_source.ogg", "sfx", "player_no_move.ogg", "kenney_interfaceSounds.zip", "Audio/tick_001.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Soft tick used for the probabilistic stay-in-place result."),
        archive_item("player_blocked_bump", "hazard_sfx", "player_blocked_bump_source.ogg", "sfx", "player_blocked_bump.ogg", "80-CC0-RPG-SFX_0.zip", "item_stone_02.ogg", "https://opengameart.org/content/80-cc0-rpg-sfx", "https://opengameart.org/sites/default/files/80-CC0-RPG-SFX_0.zip", "80 CC0 RPG SFX", "rubberduck", "Stone impact variant selected for bumping into walls."),
        archive_item("trap_trigger", "hazard_sfx", "trap_trigger_source.ogg", "sfx", "trap_trigger.ogg", "80-CC0-RPG-SFX_0.zip", "spell_01.ogg", "https://opengameart.org/content/80-cc0-rpg-sfx", "https://opengameart.org/sites/default/files/80-CC0-RPG-SFX_0.zip", "80 CC0 RPG SFX", "rubberduck", "Magical spell snap used as the trap trigger cue."),
        archive_item("lava_hiss_or_burst", "hazard_sfx", "lava_hiss_or_burst_source.ogg", "sfx", "lava_hiss_or_burst.ogg", "80-CC0-RPG-SFX_0.zip", "spell_fire_04.ogg", "https://opengameart.org/content/80-cc0-rpg-sfx", "https://opengameart.org/sites/default/files/80-CC0-RPG-SFX_0.zip", "80 CC0 RPG SFX", "rubberduck", "CC0 fire spell burst selected instead of retaining a CC-BY lava FLAC."),
        archive_item("goal_activation", "goal_sfx", "goal_activation_source.ogg", "sfx", "goal_activation.ogg", "80-CC0-RPG-SFX_0.zip", "spell_02.ogg", "https://opengameart.org/content/80-cc0-rpg-sfx", "https://opengameart.org/sites/default/files/80-CC0-RPG-SFX_0.zip", "80 CC0 RPG SFX", "rubberduck", "Bright magic cue for the level goal activation."),
        archive_item("level_complete", "goal_sfx", "level_complete_source.ogg", "sfx", "level_complete.ogg", "kenney_interfaceSounds.zip", "Audio/confirmation_004.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Confirmation chime selected for end-of-level success."),
        archive_item("defeat_sting", "goal_sfx", "defeat_sting_source.ogg", "sfx", "defeat_sting.ogg", "kenney_interfaceSounds.zip", "Audio/error_007.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Short negative UI sting for defeat."),
        direct_item("enemy_idle_cursed_hum", "enemy_sfx", "enemy_idle_cursed_hum_source.ogg", "sfx", "enemy_idle_cursed_hum.ogg", "https://opengameart.org/content/ambient-horror", "https://opengameart.org/sites/default/files/ambient_horror_0.ogg", "Ambient horror", "techiew", "Loop-like ambient drone used as the cursed knight idle hum.", downloaded_filename="ambient_horror_0.ogg"),
        archive_item("enemy_move_armor_scrape", "enemy_sfx", "enemy_move_armor_scrape_source.wav", "sfx", "enemy_move_armor_scrape.wav", "tinysized.zip", "sfx-cc0/metal-knife-scrape-02.wav", "https://opengameart.org/content/fantasy-sound-effects-tinysized-sfx", "https://opengameart.org/sites/default/files/tinysized.zip", "Fantasy Sound Effects (Tinysized SFX)", "Vehicle", "Metal scrape emphasizes the knight's armored movement."),
        archive_item("enemy_spotted_alert", "enemy_sfx", "enemy_spotted_alert_source.ogg", "sfx", "enemy_spotted_alert.ogg", "kenney_interfaceSounds.zip", "Audio/question_003.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Readable alert ping chosen for the line-of-sight detection moment."),
        archive_item("ui_hover", "ui_sfx", "ui_hover_source.ogg", "sfx", "ui_hover.ogg", "kenney_interfaceSounds.zip", "Audio/select_006.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Menu hover cue."),
        archive_item("ui_click", "ui_sfx", "ui_click_source.ogg", "sfx", "ui_click.ogg", "kenney_interfaceSounds.zip", "Audio/click_002.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Menu confirm click."),
        archive_item("restart_reset", "ui_sfx", "restart_reset_source.ogg", "sfx", "restart_reset.ogg", "kenney_interfaceSounds.zip", "Audio/back_002.ogg", "https://opengameart.org/content/interface-sounds", "https://opengameart.org/sites/default/files/kenney_interfaceSounds.zip", "Interface Sounds", "Kenney", "Restart/reset action cue."),
        direct_item("menu_theme", "music", "music_menu_theme_source.ogg", "music", "menu_theme.ogg", "https://opengameart.org/content/village-ruins", "https://opengameart.org/sites/default/files/Village%20Ruins%20-%20isaiah658.ogg", "Village Ruins", "isaiah658", "Selected for menu mood: wistful ruins theme.", downloaded_filename="music_menu_theme_source.ogg"),
        direct_item("early_gameplay_theme", "music", "music_early_gameplay_source.ogg", "music", "early_gameplay_theme.ogg", "https://opengameart.org/content/dungeon-ambience", "https://opengameart.org/sites/default/files/dungeon002.ogg", "Dungeon Ambience", "yd", "Selected for early handcrafted maze levels.", downloaded_filename="music_early_gameplay_source.ogg"),
        direct_item("late_gameplay_theme", "music", "music_late_gameplay_source.ogg", "music", "late_gameplay_theme.ogg", "https://opengameart.org/content/dark-cavern-ambient", "https://opengameart.org/sites/default/files/dark_cavern_ambient_002.ogg", "Dark Cavern Ambient", "Paul Wortmann", "Continuous loop selected for the later, tenser maze levels.", downloaded_filename="music_late_gameplay_source.ogg"),
    ]


def ensure_raw_source(item: dict) -> None:
    raw_path = ROOT / item["raw_path"]
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists():
        return

    if item["source_type"] == "archive_member":
        archive_path = ROOT / item["source_archive"]
        if not archive_path.exists():
            raise FileNotFoundError(f"Missing source archive: {archive_path}")
        with zipfile.ZipFile(archive_path) as archive:
            with archive.open(item["archive_member"]) as source, raw_path.open("wb") as target:
                shutil.copyfileobj(source, target)
        return

    download_path = ROOT / item.get("downloaded_source_path", item["raw_path"])
    if not download_path.exists():
        raise FileNotFoundError(f"Missing downloaded source file: {download_path}")
    if download_path != raw_path:
        shutil.copy2(download_path, raw_path)


def write_processed_copy(item: dict) -> None:
    raw_path = ROOT / item["raw_path"]
    processed_path = ROOT / item["processed_path"]
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(raw_path, processed_path)


def write_manifest(items: list[dict]) -> None:
    payload = {
        "project": "Markov's Maze",
        "source_policy": {
            "download_domain": "OpenGameArt only",
            "accepted_licenses": ["CC0", "CC-BY", "OGA-BY"],
            "selected_license_set": ["CC0"],
            "normalization_mode": "Stable filenames with extracted or copied runtime-ready WAV/OGG files. No loudness conversion was applied in this environment.",
        },
        "items": items,
        "summary": {
            "count": len(items),
            "sfx_count": len([item for item in items if item["category"] != "music"]),
            "music_count": len([item for item in items if item["category"] == "music"]),
        },
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    items = build_audio_items()
    PROCESSED_SFX_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    for item in items:
        ensure_raw_source(item)
        write_processed_copy(item)
    write_manifest(items)
    print(f"Prepared {len(items)} audio assets and wrote {MANIFEST_PATH.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
