#!/usr/bin/env python3
"""Normalize visual asset sizes and optimize PNG output for Markov's Maze."""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps, UnidentifiedImageError


ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "data" / "asset_manifest.json"


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


def filter_assets(assets: list[dict[str, Any]], only_categories: set[str], only_files: set[str]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for asset in assets:
        if only_categories and asset["category"].lower() not in only_categories:
            continue
        if only_files and asset["filename"].lower() not in only_files:
            continue
        selected.append(asset)
    return selected


def fit_to_expected_size(image: Image.Image, width: int, height: int, transparent: bool) -> tuple[Image.Image, bool]:
    expected_size = (width, height)
    working = image.convert("RGBA")
    resized = ImageOps.fit(working, expected_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    changed = image.size != expected_size

    if transparent:
        return resized, changed

    opaque = Image.new("RGBA", resized.size, (0, 0, 0, 255))
    opaque.alpha_composite(resized)
    return opaque.convert("RGB"), changed


def save_png_bytes(image: Image.Image, optimize: bool = True, compress_level: int = 9) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=optimize, compress_level=compress_level)
    return buffer.getvalue()


def quantized_png_bytes(image: Image.Image, colors: int) -> bytes | None:
    try:
        if image.mode == "RGBA":
            quantized = image.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        else:
            quantized = image.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors, dither=Image.Dither.NONE)
        buffer = io.BytesIO()
        quantized.save(buffer, format="PNG", optimize=True, compress_level=9)
        return buffer.getvalue()
    except Exception:
        return None


def choose_best_png_bytes(image: Image.Image, transparent: bool) -> tuple[bytes, str]:
    candidates: list[tuple[str, bytes]] = []
    base = save_png_bytes(image, optimize=True, compress_level=9)
    candidates.append(("optimized_png", base))

    if transparent:
        for colors in (256, 128):
            candidate = quantized_png_bytes(image.convert("RGBA"), colors)
            if candidate is not None:
                candidates.append((f"quantized_{colors}", candidate))
    else:
        for colors in (256, 128):
            candidate = quantized_png_bytes(image.convert("RGB"), colors)
            if candidate is not None:
                candidates.append((f"quantized_{colors}", candidate))

    best_name, best_bytes = min(candidates, key=lambda item: len(item[1]))
    return best_bytes, best_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Restrict processing to one or more manifest categories. Repeat or use comma-separated values.",
    )
    parser.add_argument(
        "--only-file",
        action="append",
        default=[],
        help="Restrict processing to one or more exact filenames. Repeat or use comma-separated values.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen without writing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_json(MANIFEST_PATH)
    only_categories = flatten_filters(args.only)
    only_files = flatten_filters(args.only_file)
    assets = filter_assets(manifest.get("assets", []), only_categories, only_files)

    console_log(
        "Starting visual normalization run | "
        f"assets={len(assets)} | dry_run={'yes' if args.dry_run else 'no'} | "
        f"only={args.only or 'all'} | only_file={args.only_file or 'all'}"
    )

    if not assets:
        console_log("No assets matched the current filters")
        return 1

    processed_count = 0
    resized_count = 0
    optimized_count = 0
    skipped_missing = 0
    error_count = 0

    for index, asset in enumerate(assets, start=1):
        processed_path = (ROOT_DIR / asset["paths"]["processed"]).resolve()
        expected_width = int(asset["dimensions"]["width"])
        expected_height = int(asset["dimensions"]["height"])
        transparent = bool(asset.get("transparency"))
        progress = f"[{index}/{len(assets)}]"

        if not processed_path.exists():
            skipped_missing += 1
            console_log(f"{progress} Missing file, skipped: {relative_to_root(processed_path)}")
            continue

        try:
            with Image.open(processed_path) as source:
                source.load()
                original = source.copy()
        except UnidentifiedImageError:
            error_count += 1
            console_log(f"{progress} Not a valid image, skipped with error: {relative_to_root(processed_path)}")
            continue
        except Exception as exc:
            error_count += 1
            console_log(f"{progress} Failed to open {relative_to_root(processed_path)} | error={exc}")
            continue

        original_size = original.size
        original_bytes = processed_path.stat().st_size
        normalized_image, resized = fit_to_expected_size(original, expected_width, expected_height, transparent)
        best_bytes, strategy = choose_best_png_bytes(normalized_image, transparent)
        optimized_bytes = len(best_bytes)
        size_changed = optimized_bytes != original_bytes
        wrote_file = resized or size_changed

        if resized:
            resized_count += 1
        if size_changed:
            optimized_count += 1

        console_log(
            f"{progress} {asset['filename']} | "
            f"from={original_size[0]}x{original_size[1]} {original_bytes}B "
            f"-> to={expected_width}x{expected_height} {optimized_bytes}B "
            f"| resized={'yes' if resized else 'no'} | strategy={strategy}"
        )

        if not args.dry_run and wrote_file:
            processed_path.write_bytes(best_bytes)
            console_log(f"{progress} Wrote normalized file: {relative_to_root(processed_path)}")
        elif not args.dry_run:
            console_log(f"{progress} No write needed: {relative_to_root(processed_path)}")

        processed_count += 1

    console_log(
        "Normalization complete | "
        f"processed={processed_count} | resized={resized_count} | optimized={optimized_count} | "
        f"missing={skipped_missing} | errors={error_count}"
    )
    print(
        "Processed "
        f"{processed_count} assets | resized={resized_count} | optimized={optimized_count} | "
        f"missing={skipped_missing} | errors={error_count}"
    )
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
