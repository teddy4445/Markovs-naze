#!/usr/bin/env python3
"""Create a manual visual-replacement todo file for Gemini/Nano Banana."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "data" / "asset_manifest.json"
PROMPT_BANK_PATH = ROOT_DIR / "docs" / "art_prompt_bank.md"
DEFAULT_OUTPUT_PATH = ROOT_DIR / "docs" / "visual_manual_todo.md"

REFERENCE_CATEGORIES = {
    "branding",
    "backgrounds",
    "overlays",
    "sprites_player",
    "sprites_enemy",
    "ui_menu",
    "ui_game",
    "vfx",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def console_log(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_filters(values: list[str]) -> set[str]:
    flattened: set[str] = set()
    for value in values:
        for part in value.split(","):
            normalized = part.strip().lower()
            if normalized:
                flattened.add(normalized)
    return flattened


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT_DIR.resolve()).as_posix()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_prompt_bank(prompt_path: Path) -> dict[str, str]:
    content = prompt_path.read_text(encoding="utf-8")
    sections = re.split(r"^##\s+", content, flags=re.MULTILINE)
    prompts: dict[str, str] = {}
    for section in sections[1:]:
        lines = section.splitlines()
        if not lines:
            continue
        filename = lines[0].strip()
        match = re.search(r"Prompt text:\s*```text\s*(.*?)\s*```", section, flags=re.DOTALL)
        if match:
            prompts[filename] = match.group(1).strip()
    return prompts


def synthesize_prompt(asset: dict[str, Any]) -> str:
    dimensions = asset["dimensions"]
    transparency = "Transparent background." if asset.get("transparency") else "Opaque background."
    return normalize_whitespace(
        (
            f"Create {asset['filename']} for Markov's Maze. "
            f"Purpose: {asset.get('purpose', 'Visual runtime asset.')}. "
            f"Dimensions: {dimensions['width']}x{dimensions['height']}. "
            f"Subject: {asset.get('prompt_subject', asset.get('purpose', asset['filename']))}. "
            f"{transparency}"
        )
    )


def filter_assets(assets: list[dict[str, Any]], only_categories: set[str], only_files: set[str]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for asset in assets:
        if only_categories and asset["category"].lower() not in only_categories:
            continue
        if only_files and asset["filename"].lower() not in only_files:
            continue
        selected.append(asset)
    return selected


def should_show_original(asset: dict[str, Any], processed_path: Path) -> tuple[bool, str]:
    if not processed_path.exists():
        return False, "Current processed image is missing, so there is no local reference to show."
    animation = asset.get("animation", {})
    if animation.get("animated"):
        return True, "Animated sheet: use the current image to preserve framing, character continuity, and timing layout."
    if asset["category"] in REFERENCE_CATEGORIES:
        return True, "This category benefits from keeping layout, silhouette language, or UI composition consistent."
    return False, "Simple isolated asset: prompt-first regeneration is usually enough and avoids overfitting to placeholders."


def build_manual_prompt(asset: dict[str, Any], base_prompt: str, show_original: bool) -> str:
    dimensions = asset["dimensions"]
    animation = asset.get("animation", {})
    transparency_line = "transparent background" if asset.get("transparency") else "opaque background"
    manual_notes = [
        normalize_whitespace(base_prompt),
        normalize_whitespace(
            "Keep the established Markov's Maze art direction: top-down 2D game asset, orthographic view, low-detail flat fantasy, "
            "ancient magical ruins theme, clean readable silhouette, minimal texture, soft flat shading, strong contrast, elegant rune details, "
            "magical and mysterious tone, no photorealism, no isometric angle, no perspective distortion."
        ),
        normalize_whitespace(
            "Palette guidance: muted stone gray, sand beige, moss green base palette; glowing cyan and magical gold rune accents; "
            "orange-red for lava; cursed purple or green glow for enemy accents."
        ),
        f"Output requirements: exact final size {dimensions['width']}x{dimensions['height']}, PNG, {transparency_line}.",
    ]

    if asset["category"] != "branding":
        manual_notes.append("Do not add readable text or random symbols.")

    if animation.get("animated"):
        manual_notes.append(
            f"Deliver a single horizontal sprite sheet with {animation['frame_count']} evenly sized frames at "
            f"{animation['frame_width']}x{animation['frame_height']} per frame."
        )
    else:
        manual_notes.append("Deliver a single polished final frame.")

    if show_original:
        manual_notes.append("Use the current in-repo image as a reference for composition, framing, and readability, but improve the final polish.")
    else:
        manual_notes.append("Do not copy placeholder roughness from the current asset; use the prompt as the main driver.")

    manual_notes.append(f"Consistency note: {asset.get('consistency_notes', 'Match sibling assets in the same game set.')}")
    return "\n\n".join(manual_notes)


def build_task_block(index: int, total: int, asset: dict[str, Any], prompt_text: str) -> str:
    processed_path = (ROOT_DIR / asset["paths"]["processed"]).resolve()
    show_original, reason = should_show_original(asset, processed_path)
    reference_path = relative_to_root(processed_path) if processed_path.exists() else "n/a"
    target_path = relative_to_root(processed_path)
    manual_prompt = build_manual_prompt(asset, prompt_text, show_original)
    dimensions = asset["dimensions"]
    upgrade_status = asset.get("upgrade_status", asset.get("status", "unknown"))

    lines = [
        f"## [{index}/{total}] {asset['filename']}",
        "",
        "- [ ] Replace this asset",
        f"- Asset id: `{asset['asset_id']}`",
        f"- Category: `{asset['category']}`",
        f"- Current status: `{upgrade_status}`",
        f"- Image to replace: `{target_path}`",
        f"- Show original to Gemini Nano Banana: `{'yes' if show_original else 'no'}`",
        f"- Reference image path: `{reference_path}`",
        f"- Why this reference choice: {reason}",
        f"- New image final path: `{target_path}`",
        f"- Dimensions: `{dimensions['width']}x{dimensions['height']}`",
        f"- Transparency: `{'yes' if asset.get('transparency') else 'no'}`",
        "",
        "Prompt to use:",
        "",
        "```text",
        manual_prompt,
        "```",
        "",
    ]
    return "\n".join(lines)


def build_todo_document(assets: list[dict[str, Any]], prompt_bank: dict[str, str], output_path: Path) -> str:
    show_original_count = 0
    task_blocks: list[str] = []

    for index, asset in enumerate(assets, start=1):
        prompt_text = prompt_bank.get(asset["filename"], synthesize_prompt(asset))
        processed_path = (ROOT_DIR / asset["paths"]["processed"]).resolve()
        show_original, _reason = should_show_original(asset, processed_path)
        if show_original:
            show_original_count += 1
        task_blocks.append(build_task_block(index, len(assets), asset, prompt_text))

    lines = [
        "# Visual Manual Todo",
        "",
        f"- Generated at: `{now_iso()}`",
        f"- Output file: `{relative_to_root(output_path)}`",
        f"- Total assets listed: `{len(assets)}`",
        f"- Assets that should show the current image as reference: `{show_original_count}`",
        f"- Assets that should be prompt-only: `{len(assets) - show_original_count}`",
        "",
        "## How To Use",
        "",
        "1. Open the current image path listed for the asset.",
        "2. If `Show original to Gemini Nano Banana` is `yes`, attach that current image as the reference image.",
        "3. Paste the prompt from the block into Gemini Nano Banana.",
        "4. Save the finished PNG to the exact `New image final path` listed for the asset.",
        "5. Keep the filename, dimensions, and transparency behavior unchanged.",
        "",
        "## Tasks",
        "",
    ]
    lines.extend(task_blocks)
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Restrict output to one or more manifest categories. Repeat or use comma-separated values.",
    )
    parser.add_argument(
        "--only-file",
        action="append",
        default=[],
        help="Restrict output to one or more exact filenames. Repeat or use comma-separated values.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Path to the markdown todo file to generate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (ROOT_DIR / output_path).resolve()

    console_log("Starting manual visual todo generation")
    console_log(f"Output path: {output_path}")

    manifest = load_json(MANIFEST_PATH)
    prompt_bank = parse_prompt_bank(PROMPT_BANK_PATH)
    only_categories = flatten_filters(args.only)
    only_files = flatten_filters(args.only_file)
    assets = filter_assets(manifest.get("assets", []), only_categories, only_files)

    console_log(f"Loaded {len(manifest.get('assets', []))} manifest assets")
    console_log(f"Selected {len(assets)} asset(s) for the todo file")

    if not assets:
        console_log("No assets matched the current filters")
        return 1

    document = build_todo_document(assets, prompt_bank, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")

    console_log(f"Manual todo file written: {output_path}")
    print(f"Generated manual todo for {len(assets)} assets at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
