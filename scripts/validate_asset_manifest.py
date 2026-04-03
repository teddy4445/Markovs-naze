from __future__ import annotations

import json
import sys
from pathlib import Path

from export_placeholder_art import ROOT, build_asset_specs


MANIFEST_PATH = ROOT / "data" / "asset_manifest.json"


def main() -> int:
    expected_specs = build_asset_specs()
    expected_by_filename = {spec.filename: spec for spec in expected_specs}

    if not MANIFEST_PATH.exists():
        print(f"Missing manifest: {MANIFEST_PATH}")
        return 1

    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_assets = payload.get("assets", [])
    errors: list[str] = []
    seen: set[str] = set()

    for entry in manifest_assets:
        filename = entry.get("filename")
        if not filename:
            errors.append("Manifest entry without filename.")
            continue
        if filename in seen:
            errors.append(f"Duplicate manifest entry: {filename}")
        seen.add(filename)

        spec = expected_by_filename.get(filename)
        if spec is None:
            errors.append(f"Unexpected asset in manifest: {filename}")
            continue

        processed_path = ROOT / entry["paths"]["processed"]
        if not processed_path.exists():
            errors.append(f"Missing processed file for {filename}: {processed_path}")

        raw_svg_path = entry["paths"].get("raw_svg")
        if spec.raw_svg and not raw_svg_path:
            errors.append(f"Expected raw SVG path for {filename}.")
        if raw_svg_path and not (ROOT / raw_svg_path).exists():
            errors.append(f"Missing raw SVG file for {filename}: {raw_svg_path}")

        dimensions = entry.get("dimensions", {})
        if dimensions.get("width") != spec.width or dimensions.get("height") != spec.height:
            errors.append(f"Dimension mismatch for {filename}.")

        animation = entry.get("animation", {})
        if animation.get("frame_count") != spec.frame_count:
            errors.append(f"Frame count mismatch for {filename}.")
        if spec.frame_count > 1:
            expected_width = (animation.get("frame_width") or 0) * animation.get("frame_count", 0)
            if expected_width != spec.width:
                errors.append(f"Sprite sheet width mismatch for {filename}.")
        if entry.get("status") != spec.status:
            errors.append(f"Status mismatch for {filename}.")

    missing = sorted(set(expected_by_filename) - seen)
    for filename in missing:
        errors.append(f"Missing manifest entry: {filename}")

    docs_to_check = [
        ROOT / "docs" / "asset_manifest.md",
        ROOT / "docs" / "art_prompt_bank.md",
        ROOT / "docs" / "markovs_maze_brief.md",
    ]
    for path in docs_to_check:
        if not path.exists():
            errors.append(f"Missing documentation file: {path}")

    if errors:
        print("Asset manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Asset manifest validation passed for {len(expected_specs)} assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
