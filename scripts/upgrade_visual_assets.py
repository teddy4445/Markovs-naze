#!/usr/bin/env python3
"""Upgrade Markov's Maze visual assets with OpenAI image generation."""

from __future__ import annotations

import argparse
import base64
import copy
import io
import json
import os
import re
import shutil
import sys
import textwrap
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageOps, UnidentifiedImageError

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]


ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "data" / "asset_manifest.json"
PROMPT_BANK_PATH = ROOT_DIR / "docs" / "art_prompt_bank.md"
REPORT_PATH = ROOT_DIR / "docs" / "visual_upgrade_report.md"
STYLE_GUIDE_PATH = ROOT_DIR / "docs" / "visual_style_guide.md"
BACKUP_ROOT = ROOT_DIR / "assets" / "backups" / "original_visuals"
REVIEW_ROOT = ROOT_DIR / "assets" / "review_candidates"

DEFAULT_MODELS = ["gpt-image-1"]
COMPATIBILITY_FALLBACK_MODELS = ["gpt-image-1"]
SAFE_REMOVABLE_REQUEST_PARAMS = {
    "background",
    "input_fidelity",
    "moderation",
    "n",
    "output_compression",
    "output_format",
    "partial_images",
    "quality",
    "response_format",
    "size",
    "style",
    "user",
}
SUPPORTED_SIZES = [
    ("1024x1024", 1024, 1024),
    ("1536x1024", 1536, 1024),
    ("1024x1536", 1024, 1536),
]
RETRYABLE_MODEL_ERRORS = (
    "model",
    "not found",
    "unknown",
    "unsupported",
    "rate limit",
    "overloaded",
    "timeout",
    "temporarily",
)
ACCOUNT_BLOCKING_ERROR_TOKENS = (
    "billing hard limit",
    "billing_hard_limit_reached",
    "insufficient_quota",
    "quota exceeded",
)
STATIC_AUTO_REPLACE_CATEGORIES = {
    "backgrounds",
    "tiles",
    "overlays",
    "props",
    "icons",
}
MANUAL_REVIEW_CATEGORIES = {"branding", "sprites_player", "sprites_enemy", "ui_menu", "ui_game", "vfx"}

CATEGORY_ENRICHMENTS = {
    "branding": (
        "Logo treatment only. Use elegant ancient-stone fantasy typography with a rune-ring motif, "
        "high readability on menu screens, and no extra decorative text beyond the title mark."
    ),
    "backgrounds": (
        "Create calm, polished magical-ruins backdrops that leave room for UI and gameplay readability. "
        "Keep orthographic/top-down logic and avoid perspective drama."
    ),
    "tiles": (
        "Treat this as a gameplay tile first: crisp silhouette, clean edge contrast, subtle rune detailing, "
        "and readable behavior cues at small scale."
    ),
    "overlays": (
        "This overlay must stay extremely readable above maze tiles, with clear iconography and minimal noise."
    ),
    "props": (
        "Keep prop silhouettes simple and top-down, with ancient stone, moss, shard, or rubble language that "
        "matches the ruins palette."
    ),
    "sprites_player": (
        "The player is a ruins scholar: practical explorer clothing, readable top-down silhouette, restrained gear, "
        "cyan-gold rune accents, and consistent anatomy across frames."
    ),
    "sprites_enemy": (
        "The enemy is a cursed knight: worn armor, spectral glow accents in cursed purple or green, readable menace, "
        "and consistent proportions across frames."
    ),
    "vfx": (
        "Effects should feel magical and readable at a glance, with soft flat shading, strong silhouettes, and clean "
        "timing cues for gameplay."
    ),
    "ui_menu": (
        "Menu UI should look like carved fantasy-ruins stone with refined rune framing, strong contrast, and no random "
        "symbols or unreadable details."
    ),
    "ui_game": (
        "In-game UI should be readable at small sizes, built from carved stone and rune framing, and visually subordinate "
        "to the maze itself."
    ),
    "icons": (
        "Icons should be bold, simplified, and legible at a glance, with one clear motif and no extra clutter."
    ),
}


@dataclass
class AssetResult:
    asset_id: str
    filename: str
    category: str
    old_path: str
    backup_path: str | None
    new_path: str | None
    review_candidate_path: str | None
    model_used: str | None
    transparency_requested: bool
    generation_mode: str
    post_processing_applied: bool
    manual_review_recommended: bool
    status: str
    note: str
    prompt_source: str
    revised_prompt: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Regenerate even if an asset already has an upgraded status.")
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
    parser.add_argument("--dry-run", action="store_true", help="Plan the run without writing backups, assets, report, or manifest.")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Refresh the markdown report from the current manifest metadata without contacting OpenAI or changing assets.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def console_log(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def flatten_filters(values: list[str]) -> set[str]:
    flattened: set[str] = set()
    for value in values:
        for part in value.split(","):
            normalized = part.strip().lower()
            if normalized:
                flattened.add(normalized)
    return flattened


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


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT_DIR.resolve()).as_posix()


def choose_api_size(width: int, height: int) -> str:
    aspect = width / height
    best_label = "1024x1024"
    best_score = float("inf")
    for label, supported_w, supported_h in SUPPORTED_SIZES:
        supported_aspect = supported_w / supported_h
        aspect_score = abs(aspect - supported_aspect)
        area_score = abs((width * height) - (supported_w * supported_h)) / max(width * height, 1)
        score = aspect_score + area_score * 0.15
        if score < best_score:
            best_score = score
            best_label = label
    return best_label


def prefers_manual_review(asset: dict[str, Any]) -> bool:
    animation = asset.get("animation", {})
    return bool(animation.get("animated")) or asset.get("category") in MANUAL_REVIEW_CATEGORIES


def can_auto_replace(asset: dict[str, Any]) -> bool:
    return not prefers_manual_review(asset) and asset.get("category") in STATIC_AUTO_REPLACE_CATEGORIES


def choose_generation_mode(asset: dict[str, Any], source_path: Path) -> str:
    if source_path.exists():
        return "edit_reference"
    return "fresh_generation"


def choose_quality(asset: dict[str, Any]) -> str:
    if asset.get("category") in {"backgrounds", "branding", "sprites_player", "sprites_enemy", "ui_menu", "ui_game"}:
        return "high"
    return "medium"


def choose_models() -> list[str]:
    override = os.environ.get("OPENAI_IMAGE_MODEL", "").strip()
    ordered = [override] if override else list(DEFAULT_MODELS)
    for model in COMPATIBILITY_FALLBACK_MODELS:
        if model not in ordered:
            ordered.append(model)
    return ordered


def make_client() -> OpenAI | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or OpenAI is None:
        return None
    kwargs: dict[str, Any] = {"api_key": api_key}
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def build_backup_path(processed_path: Path) -> Path:
    relative_processed = processed_path.resolve().relative_to((ROOT_DIR / "assets" / "processed").resolve())
    return BACKUP_ROOT / relative_processed


def build_review_candidate_path(processed_path: Path) -> Path:
    relative_processed = processed_path.resolve().relative_to((ROOT_DIR / "assets" / "processed").resolve())
    stem = processed_path.stem
    suffix = processed_path.suffix or ".png"
    return (REVIEW_ROOT / relative_processed.parent / f"{stem}__candidate{suffix}").resolve()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def backup_original(source_path: Path, backup_path: Path, force: bool, dry_run: bool) -> bool:
    if not source_path.exists():
        console_log(f"Backup skipped because source file is missing: {relative_to_root(source_path)}")
        return False
    if dry_run:
        console_log(f"Dry run: backup planned {relative_to_root(source_path)} -> {relative_to_root(backup_path)}")
        return not backup_path.exists()
    ensure_parent(backup_path)
    if backup_path.exists() and not force:
        console_log(f"Backup already exists, keeping current copy: {relative_to_root(backup_path)}")
        return False
    shutil.copy2(source_path, backup_path)
    console_log(f"Backup written: {relative_to_root(backup_path)}")
    return True


def download_url_bytes(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:  # nosec B310 - OpenAI signed URL
        return response.read()


def decode_image_bytes(response: Any) -> tuple[bytes, str | None]:
    if not getattr(response, "data", None):
        raise RuntimeError("OpenAI returned no image data.")
    image = response.data[0]
    if getattr(image, "b64_json", None):
        return base64.b64decode(image.b64_json), getattr(image, "revised_prompt", None)
    if getattr(image, "url", None):
        return download_url_bytes(image.url), getattr(image, "revised_prompt", None)
    raise RuntimeError("OpenAI returned neither b64_json nor url.")


def open_image_from_bytes(image_bytes: bytes) -> Image.Image:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
        return image
    except UnidentifiedImageError as exc:  # pragma: no cover
        raise RuntimeError("Generated bytes were not a valid image.") from exc


def post_process_image(image: Image.Image, width: int, height: int, transparent: bool) -> tuple[Image.Image, bool]:
    target_size = (width, height)
    working = image.convert("RGBA")
    processed = ImageOps.fit(working, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    if not transparent:
        background = Image.new("RGBA", processed.size, (0, 0, 0, 255))
        background.alpha_composite(processed)
        processed = background.convert("RGB")
    return processed, image.size != target_size


def save_image(image: Image.Image, output_path: Path, transparent: bool) -> None:
    ensure_parent(output_path)
    if transparent:
        image.save(output_path, format="PNG")
    else:
        image.save(output_path, format="PNG")


def evaluate_candidate(image: Image.Image, asset: dict[str, Any], output_path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    dimensions = asset["dimensions"]
    expected_size = (dimensions["width"], dimensions["height"])
    if image.size != expected_size:
        issues.append(f"expected {expected_size[0]}x{expected_size[1]} but found {image.size[0]}x{image.size[1]}")

    rgba = image.convert("RGBA")
    if rgba.getbbox() is None:
        issues.append("image is fully blank or fully transparent")

    if asset.get("transparency"):
        alpha = rgba.getchannel("A")
        _min_alpha, max_alpha = alpha.getextrema()
        if max_alpha == 0:
            issues.append("transparent asset became fully transparent")
    else:
        opaque_background = Image.new("RGBA", rgba.size, rgba.getpixel((0, 0)))
        diff_bbox = ImageChops.difference(rgba, opaque_background).getbbox()
        if diff_bbox is None:
            issues.append("opaque image appears uniformly flat")

    if output_path.exists() and output_path.stat().st_size < 512:
        issues.append("output file is suspiciously small")

    return not issues, issues


def build_enriched_prompt(asset: dict[str, Any], base_prompt: str, mode: str) -> str:
    dimensions = asset["dimensions"]
    animation = asset.get("animation", {})
    parts = [
        base_prompt.strip(),
        (
            "Enforce the established Markov's Maze visual language: top-down 2D game asset, orthographic view, "
            "low-detail flat fantasy, ancient magical ruins theme, clean readable silhouette, minimal texture, soft "
            "flat shading, strong contrast, elegant rune details, gameplay readability first, magical and mysterious "
            "tone, no photorealism, no isometric angle, and no perspective distortion."
        ),
        (
            "Palette guidance: muted stone gray, sand beige, and moss green base palette; glowing cyan and magical gold "
            "rune accents; orange-red for lava; cursed purple or green glow for enemy accents."
        ),
        f"Role-specific direction: {CATEGORY_ENRICHMENTS.get(asset['category'], 'Preserve readability and category consistency.')}",
        f"Output must exactly fit {dimensions['width']}x{dimensions['height']} after post-processing.",
        f"Preserve compatibility with the existing filename {asset['filename']} and the current Phaser loading path.",
        f"Consistency note: {asset.get('consistency_notes', 'Match sibling assets in this visual set.')}",
    ]

    if mode == "edit_reference":
        parts.append("Use the supplied current asset as a visual reference and improve it without drifting away from the established game identity.")
    else:
        parts.append("Generate a fresh image that still matches the established Markov's Maze visual identity.")

    if asset.get("transparency"):
        parts.append("Transparent background required. No baked backdrop, no drop shadow box, no random framing.")
    else:
        parts.append("Opaque background allowed. Keep values controlled so gameplay objects stay readable on top.")

    if asset["category"] != "branding":
        parts.append("Do not add any text, letters, or symbols that read like UI labels.")

    if animation.get("animated"):
        parts.append(
            "This is an animated sprite sheet. Deliver a single horizontal sprite sheet with "
            f"{animation['frame_count']} evenly sized frames at {animation['frame_width']}x{animation['frame_height']} "
            "per frame. Keep proportions, lighting, and silhouette consistent across frames."
        )
    else:
        parts.append("Deliver one polished final frame with strong gameplay readability.")

    return "\n\n".join(parts)


def normalize_prompt_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_compact_prompt(asset: dict[str, Any], mode: str, include_notes: bool = True, include_category_rule: bool = True) -> str:
    parts = [
        f"Markov's Maze asset {asset['filename']}.",
        f"Purpose: {asset.get('purpose', 'Visual runtime asset.')}",
        f"Subject: {asset.get('prompt_subject', asset.get('purpose', asset['filename']))}",
        (
            "Style: top-down orthographic 2D, low-detail flat fantasy, ancient magical ruins, readable silhouette, "
            "minimal texture, soft flat shading, strong contrast, elegant rune details, mysterious tone, no photorealism, "
            "no isometric, no perspective distortion."
        ),
        (
            "Palette: muted stone gray, sand beige, moss green, cyan and gold runes, orange-red lava, cursed purple or green enemy glow."
        ),
    ]
    if include_category_rule:
        parts.append(f"Category rule: {CATEGORY_ENRICHMENTS.get(asset['category'], 'Preserve readability and category consistency.')}")
    if include_notes:
        parts.append(f"Consistency: {asset.get('consistency_notes', 'Match sibling assets in the game.')}")

    if asset.get("transparency"):
        parts.append("Transparent PNG background required.")
    else:
        parts.append("Opaque background allowed.")

    if asset["category"] != "branding":
        parts.append("No text.")

    animation = asset.get("animation", {})
    if animation.get("animated"):
        parts.append(
            f"Horizontal sprite sheet with {animation['frame_count']} even frames at {animation['frame_width']}x{animation['frame_height']}."
        )
    else:
        parts.append("Single polished frame.")

    if mode == "edit_reference":
        parts.append("Use the current asset as visual reference if supported.")

    return normalize_prompt_text(" ".join(parts))


def fit_prompt_length(asset: dict[str, Any], prompt: str, mode: str, max_chars: int = 950) -> str:
    compact = normalize_prompt_text(prompt)
    if len(compact) <= max_chars:
        return compact

    compact = build_compact_prompt(asset, mode, include_notes=True, include_category_rule=True)
    if len(compact) <= max_chars:
        return compact

    compact = build_compact_prompt(asset, mode, include_notes=False, include_category_rule=True)
    if len(compact) <= max_chars:
        return compact

    compact = build_compact_prompt(asset, mode, include_notes=False, include_category_rule=False)
    if len(compact) <= max_chars:
        return compact

    return compact[: max_chars - 3].rstrip() + "..."


def extract_error_param_name(error_message: str) -> str | None:
    patterns = [
        r"unknown parameter:\s*'([^']+)'",
        r"invalid value for '([^']+)'",
        r"'param':\s*'([^']+)'",
    ]
    for pattern in patterns:
        match = re.search(pattern, error_message, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_required_model(error_message: str) -> str | None:
    match = re.search(r"value must be '([^']+)'", error_message, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def build_request_params(prompt: str, model: str, transparency_mode: str, quality: str, size: str, mode: str) -> dict[str, Any]:
    params: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "response_format": "b64_json",
        "size": size,
    }
    if mode == "edit_reference":
        params["input_fidelity"] = "high"
    return params


def run_image_request(client: OpenAI, mode: str, processed_path: Path, request_params: dict[str, Any]) -> Any:
    if mode == "edit_reference":
        with processed_path.open("rb") as image_file:
            return client.images.edit(image=image_file, **request_params)
    return client.images.generate(**request_params)


def generate_with_openai(
    client: OpenAI,
    asset: dict[str, Any],
    processed_path: Path,
    prompt: str,
    model_candidates: list[str],
    max_attempts: int = 3,
) -> tuple[bytes, str, str | None, str]:
    dimensions = asset["dimensions"]
    size = choose_api_size(dimensions["width"], dimensions["height"])
    transparent = "transparent" if asset.get("transparency") else "opaque"
    quality = choose_quality(asset)
    base_mode = choose_generation_mode(asset, processed_path)
    last_error: Exception | None = None
    console_log(
        "Generation start for "
        f"{asset['filename']} | base_mode={base_mode} | target_size={dimensions['width']}x{dimensions['height']} "
        f"| api_size={size} | transparency={transparent} | quality={quality}"
    )

    for model in model_candidates:
        console_log(f"Trying model '{model}' for {asset['filename']}")
        for attempt in range(1, max_attempts + 1):
            current_mode = base_mode
            request_params = build_request_params(
                fit_prompt_length(asset, prompt, current_mode),
                model,
                transparent,
                quality,
                size,
                current_mode,
            )
            should_retry_attempt = False
            console_log(
                f"Attempt {attempt}/{max_attempts} for {asset['filename']} | mode={current_mode} "
                f"| model={request_params.get('model')} | prompt_len={len(str(request_params.get('prompt', '')))}"
            )

            while True:
                try:
                    response = run_image_request(client, current_mode, processed_path, request_params)
                    image_bytes, revised_prompt = decode_image_bytes(response)
                    console_log(
                        f"Generation succeeded for {asset['filename']} | mode={current_mode} "
                        f"| model={request_params.get('model')} | bytes={len(image_bytes)}"
                    )
                    return image_bytes, str(request_params.get("model", model)), revised_prompt, current_mode
                except Exception as exc:  # pragma: no cover
                    last_error = exc
                    error_message = str(exc)
                    error_text = error_message.lower()
                    param_name = extract_error_param_name(error_message)
                    console_log(
                        f"Generation error for {asset['filename']} | mode={current_mode} "
                        f"| model={request_params.get('model')} | error={error_message}"
                    )

                    if param_name == "model":
                        suggested_model = extract_required_model(error_message)
                        current_model = request_params.get("model")
                        if suggested_model and suggested_model != current_model:
                            console_log(
                                f"Server requested model switch for {asset['filename']}: "
                                f"{current_model} -> {suggested_model}"
                            )
                            request_params["model"] = suggested_model
                            if suggested_model in COMPATIBILITY_FALLBACK_MODELS and current_mode == "edit_reference":
                                current_mode = "fresh_generation"
                                console_log(
                                    f"Switching to fresh_generation for {asset['filename']} because "
                                    f"compatibility model '{suggested_model}' may not support edit mode"
                                )
                                request_params = build_request_params(
                                    fit_prompt_length(asset, prompt, current_mode),
                                    str(request_params["model"]),
                                    transparent,
                                    quality,
                                    size,
                                    current_mode,
                                )
                            continue
                    elif param_name and param_name in SAFE_REMOVABLE_REQUEST_PARAMS and param_name in request_params:
                        console_log(f"Removing unsupported parameter '{param_name}' for {asset['filename']}")
                        request_params.pop(param_name, None)
                        continue

                    if param_name == "prompt":
                        tightened_prompt = fit_prompt_length(asset, str(request_params.get("prompt", prompt)), current_mode, max_chars=700)
                        if tightened_prompt != request_params.get("prompt"):
                            console_log(
                                f"Tightening prompt for {asset['filename']} due to API prompt-length validation "
                                f"({len(str(request_params.get('prompt', '')))} -> {len(tightened_prompt)})"
                            )
                            request_params["prompt"] = tightened_prompt
                            continue

                    if "missing required arguments" in error_text and current_mode == "edit_reference":
                        current_mode = "fresh_generation"
                        console_log(
                            f"Falling back from edit_reference to fresh_generation for {asset['filename']} "
                            "because the API rejected the edit argument set"
                        )
                        request_params = build_request_params(
                            fit_prompt_length(asset, prompt, current_mode),
                            str(request_params.get("model", model)),
                            transparent,
                            quality,
                            size,
                            current_mode,
                        )
                        continue

                    retryable = any(token in error_text for token in RETRYABLE_MODEL_ERRORS)
                    if attempt < max_attempts and retryable:
                        console_log(
                            f"Retryable error for {asset['filename']}; waiting before retry {attempt + 1}/{max_attempts}"
                        )
                        time.sleep(min(2 ** (attempt - 1), 4))
                        should_retry_attempt = True
                    break

            if should_retry_attempt:
                continue
            break
        if last_error and "model" in str(last_error).lower():
            console_log(f"Moving to next model for {asset['filename']} after model-related failure")
            continue

    console_log(f"Generation exhausted for {asset['filename']} with final error: {last_error}")
    raise RuntimeError(str(last_error) if last_error else "Image generation failed without an error message.")


def update_asset_metadata(asset: dict[str, Any], result: AssetResult) -> None:
    asset["backup_path"] = result.backup_path
    asset["upgraded_path"] = result.new_path
    asset["review_candidate_path"] = result.review_candidate_path
    asset["model_used"] = result.model_used
    asset["generated_at"] = now_iso() if result.status in {"upgraded", "review_candidate_saved", "failed"} else asset.get("generated_at")
    asset["manual_review_needed"] = result.manual_review_recommended
    asset["upgrade_status"] = result.status
    asset["upgrade_mode"] = result.generation_mode
    asset["upgrade_post_processing"] = result.post_processing_applied
    asset["upgrade_note"] = result.note
    if result.revised_prompt:
        asset["revised_prompt"] = result.revised_prompt


def status_counts(results: list[AssetResult]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def build_report(manifest: dict[str, Any], results: list[AssetResult], args: argparse.Namespace) -> str:
    counts = status_counts(results)
    processed = len(results)
    upgraded = counts.get("upgraded", 0)
    kept_original = sum(
        1
        for result in results
        if result.status in {"kept_original", "blocked_missing_openai_api_key", "blocked_account_limit", "skipped_existing_upgrade"}
    )
    manual_review = counts.get("review_candidate_saved", 0)
    failed = counts.get("failed", 0)
    missing = counts.get("missing_source_asset", 0)
    blocked = counts.get("blocked_missing_openai_api_key", 0)
    account_blocked = counts.get("blocked_account_limit", 0)
    backups_ready = sum(1 for result in results if result.backup_path)
    model_list = ", ".join(choose_models())

    prompt_adjustments = [
        "Added the global Markov's Maze style contract to every asset prompt.",
        "Added palette constraints for stone, moss, cyan/gold runes, lava, and cursed enemy glow accents.",
        "Added category-specific art direction for branding, backgrounds, tiles, props, sprites, VFX, UI, and icons.",
        "Added explicit transparency requirements for PNG overlays, sprites, tiles, and UI pieces.",
        "Added sprite-sheet framing instructions for animated assets using manifest frame counts and frame dimensions.",
        "Preferred edit/reference mode when the existing processed asset is available locally.",
    ]
    resizing_notes = [
        "The script targets documented OpenAI Images API square, landscape, and portrait sizes, then post-processes the result to the exact manifest dimensions.",
        "All accepted outputs are resized and cropped with Pillow to preserve the existing runtime dimensions and filenames.",
        "Transparent assets are preserved as PNG with an alpha channel; opaque assets are flattened back to PNG after resizing.",
    ]
    remaining_consistency_issues = [
        "Animated assets should still receive a human frame-consistency pass before shipping, especially player and enemy sheets.",
        "Backgrounds and long parallax strips may need composition tuning after the first successful live generation run.",
        "The current report reflects environment-gated status if OPENAI_API_KEY is not set in the shell.",
    ]

    lines: list[str] = [
        "# Visual Upgrade Report",
        "",
        f"- Generated at: `{now_iso()}`",
        f"- Mode: `{'report-only' if args.report_only else 'live-or-safe-run'}`",
        f"- Dry run: `{'yes' if args.dry_run else 'no'}`",
        f"- Model preference order: `{model_list}`",
        "",
        "## Summary",
        "",
        f"- Total assets processed: `{processed}`",
        f"- Assets successfully upgraded: `{upgraded}`",
        f"- Assets kept original: `{kept_original}`",
        f"- Assets requiring manual review: `{manual_review}`",
        f"- Assets failed: `{failed}`",
        f"- Assets missing source files: `{missing}`",
        f"- Backups available: `{backups_ready}`",
        f"- Environment-blocked assets: `{blocked}`",
        f"- Account-blocked assets: `{account_blocked}`",
        "",
        "## Prompt Adjustments Made",
        "",
    ]
    for item in prompt_adjustments:
        lines.append(f"- {item}")

    lines.extend(["", "## Resizing And Post-Processing Notes", ""])
    for item in resizing_notes:
        lines.append(f"- {item}")

    lines.extend(["", "## Successfully Upgraded", ""])
    upgraded_assets = [result.filename for result in results if result.status == "upgraded"]
    if upgraded_assets:
        for filename in upgraded_assets:
            lines.append(f"- `{filename}`")
    else:
        lines.append("- None in this run.")

    lines.extend(["", "## Kept Original", ""])
    kept_assets = [
        result
        for result in results
        if result.status in {"kept_original", "blocked_missing_openai_api_key", "blocked_account_limit", "skipped_existing_upgrade"}
    ]
    if kept_assets:
        for result in kept_assets:
            lines.append(f"- `{result.filename}`: {result.note}")
    else:
        lines.append("- None in this run.")

    lines.extend(["", "## Manual Review Needed", ""])
    review_assets = [result for result in results if result.status == "review_candidate_saved"]
    if review_assets:
        for result in review_assets:
            lines.append(f"- `{result.filename}`: review candidate at `{result.review_candidate_path}`")
    else:
        lines.append("- None in this run.")

    lines.extend(["", "## Failed", ""])
    failed_assets = [result for result in results if result.status == "failed"]
    if failed_assets:
        for result in failed_assets:
            lines.append(f"- `{result.filename}`: {result.note}")
    else:
        lines.append("- None in this run.")

    lines.extend(["", "## Remaining Visual Consistency Issues", ""])
    for item in remaining_consistency_issues:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Asset Log",
            "",
            "| Asset | Category | Status | Mode | Model | Backup | Output | Manual review | Notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result.filename}`",
                    result.category,
                    result.status,
                    result.generation_mode,
                    result.model_used or "n/a",
                    result.backup_path or "n/a",
                    result.new_path or result.review_candidate_path or "n/a",
                    "yes" if result.manual_review_recommended else "no",
                    result.note.replace("|", "/"),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def build_report_only_results(manifest: dict[str, Any], assets: list[dict[str, Any]]) -> list[AssetResult]:
    results: list[AssetResult] = []
    for asset in assets:
        results.append(
            AssetResult(
                asset_id=asset["asset_id"],
                filename=asset["filename"],
                category=asset["category"],
                old_path=asset["paths"]["processed"],
                backup_path=asset.get("backup_path"),
                new_path=asset.get("upgraded_path"),
                review_candidate_path=asset.get("review_candidate_path"),
                model_used=asset.get("model_used"),
                transparency_requested=bool(asset.get("transparency")),
                generation_mode=asset.get("upgrade_mode", "not_run"),
                post_processing_applied=bool(asset.get("upgrade_post_processing", False)),
                manual_review_recommended=bool(asset.get("manual_review_needed", False)),
                status=asset.get("upgrade_status", asset.get("status", "unknown")),
                note=asset.get("upgrade_note", "No upgrade run metadata recorded yet."),
                prompt_source="manifest_only",
                revised_prompt=asset.get("revised_prompt"),
            )
        )
    return results


def process_asset(
    asset: dict[str, Any],
    prompt_text: str,
    client: OpenAI | None,
    args: argparse.Namespace,
    model_candidates: list[str],
    asset_index: int | None = None,
    asset_total: int | None = None,
) -> AssetResult:
    processed_path = (ROOT_DIR / asset["paths"]["processed"]).resolve()
    backup_path = build_backup_path(processed_path)
    review_candidate_path = build_review_candidate_path(processed_path)
    transparency = bool(asset.get("transparency"))
    generation_mode = choose_generation_mode(asset, processed_path)
    prompt = build_enriched_prompt(asset, prompt_text, generation_mode)
    prompt_source = "docs/art_prompt_bank.md"
    progress_prefix = f"[{asset_index}/{asset_total}] " if asset_index is not None and asset_total is not None else ""
    console_log(
        f"{progress_prefix}Asset start: {asset['filename']} | category={asset['category']} | "
        f"processed={asset['paths']['processed']} | mode={generation_mode}"
    )

    if not processed_path.exists():
        console_log(f"{progress_prefix}Source asset missing: {asset['paths']['processed']}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=None,
            new_path=None,
            review_candidate_path=None,
            model_used=None,
            transparency_requested=transparency,
            generation_mode=generation_mode,
            post_processing_applied=False,
            manual_review_recommended=False,
            status="missing_source_asset",
            note="Source visual asset was missing, so no backup or replacement could be made.",
            prompt_source=prompt_source,
        )

    backup_original(processed_path, backup_path, force=False, dry_run=args.dry_run or args.report_only)

    if asset.get("upgrade_status") == "upgraded" and not args.force:
        console_log(f"{progress_prefix}Skipping already-upgraded asset without --force: {asset['filename']}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
            new_path=asset["paths"]["processed"],
            review_candidate_path=asset.get("review_candidate_path"),
            model_used=asset.get("model_used"),
            transparency_requested=transparency,
            generation_mode=asset.get("upgrade_mode", generation_mode),
            post_processing_applied=bool(asset.get("upgrade_post_processing", False)),
            manual_review_recommended=bool(asset.get("manual_review_needed", False)),
            status="skipped_existing_upgrade",
            note="Asset was already marked as upgraded; rerun with --force to replace it again.",
            prompt_source=prompt_source,
            revised_prompt=asset.get("revised_prompt"),
        )

    if args.dry_run:
        console_log(f"{progress_prefix}Dry run: no API request will be made for {asset['filename']}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=relative_to_root(backup_path),
            new_path=None,
            review_candidate_path=relative_to_root(review_candidate_path),
            model_used=model_candidates[0] if model_candidates else None,
            transparency_requested=transparency,
            generation_mode=generation_mode,
            post_processing_applied=True,
            manual_review_recommended=prefers_manual_review(asset),
            status="kept_original",
            note="Dry run only: no generation or file writes were performed.",
            prompt_source=prompt_source,
        )

    if client is None:
        console_log(f"{progress_prefix}OPENAI_API_KEY missing; preserving original for {asset['filename']}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
            new_path=None,
            review_candidate_path=None,
            model_used=None,
            transparency_requested=transparency,
            generation_mode=generation_mode,
            post_processing_applied=False,
            manual_review_recommended=False,
            status="blocked_missing_openai_api_key",
            note="OPENAI_API_KEY is not set in the environment, so the original asset was preserved.",
            prompt_source=prompt_source,
        )

    try:
        image_bytes, model_used, revised_prompt, actual_mode = generate_with_openai(client, asset, processed_path, prompt, model_candidates)
        raw_image = open_image_from_bytes(image_bytes)
        processed_image, post_processed = post_process_image(
            raw_image,
            asset["dimensions"]["width"],
            asset["dimensions"]["height"],
            transparent=transparency,
        )

        manual_review = prefers_manual_review(asset)
        output_target = processed_path if (args.force or can_auto_replace(asset)) else review_candidate_path
        console_log(
            f"{progress_prefix}Saving generated image for {asset['filename']} to {relative_to_root(output_target)} "
            f"| model={model_used} | post_processed={'yes' if post_processed else 'no'}"
        )
        save_image(processed_image, output_target, transparent=transparency)
        is_valid, issues = evaluate_candidate(processed_image, asset, output_target)
        issue_text = "; ".join(issues) if issues else "Passed the automated checks."
        console_log(
            f"{progress_prefix}Validation for {asset['filename']}: "
            f"{'passed' if is_valid else 'failed'} | {issue_text}"
        )

        if not is_valid:
            if output_target == processed_path:
                save_image(processed_image, review_candidate_path, transparent=transparency)
                console_log(
                    f"{progress_prefix}Saved invalid candidate for manual review: {relative_to_root(review_candidate_path)}"
                )
            return AssetResult(
                asset_id=asset["asset_id"],
                filename=asset["filename"],
                category=asset["category"],
                old_path=asset["paths"]["processed"],
                backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
                new_path=None,
                review_candidate_path=relative_to_root(review_candidate_path),
                model_used=model_used,
                transparency_requested=transparency,
                generation_mode=actual_mode,
                post_processing_applied=post_processed,
                manual_review_recommended=True,
                status="review_candidate_saved",
                note=f"Candidate failed automated acceptance checks and was kept for review. {issue_text}",
                prompt_source=prompt_source,
                revised_prompt=revised_prompt,
            )

        if manual_review and not args.force:
            if output_target != review_candidate_path:
                save_image(processed_image, review_candidate_path, transparent=transparency)
            console_log(
                f"{progress_prefix}Manual review required for {asset['filename']}; candidate stored at "
                f"{relative_to_root(review_candidate_path)}"
            )
            return AssetResult(
                asset_id=asset["asset_id"],
                filename=asset["filename"],
                category=asset["category"],
                old_path=asset["paths"]["processed"],
                backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
                new_path=None,
                review_candidate_path=relative_to_root(review_candidate_path),
                model_used=model_used,
                transparency_requested=transparency,
                generation_mode=actual_mode,
                post_processing_applied=post_processed,
                manual_review_recommended=True,
                status="review_candidate_saved",
                note="Candidate looks structurally valid but still needs a human art pass before replacement.",
                prompt_source=prompt_source,
                revised_prompt=revised_prompt,
            )

        if output_target != processed_path:
            save_image(processed_image, processed_path, transparent=transparency)
            console_log(f"{progress_prefix}Accepted candidate promoted to runtime path: {asset['paths']['processed']}")

        console_log(f"{progress_prefix}Asset upgraded successfully: {asset['filename']} | model={model_used}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
            new_path=asset["paths"]["processed"],
            review_candidate_path=None,
            model_used=model_used,
            transparency_requested=transparency,
            generation_mode=actual_mode,
            post_processing_applied=post_processed,
            manual_review_recommended=False,
            status="upgraded",
            note="OpenAI-generated replacement accepted and written to the runtime asset path.",
            prompt_source=prompt_source,
            revised_prompt=revised_prompt,
        )
    except Exception as exc:
        error_text = str(exc).lower()
        if any(token in error_text for token in ACCOUNT_BLOCKING_ERROR_TOKENS):
            console_log(
                f"{progress_prefix}Account-level block while processing {asset['filename']}: "
                "billing or quota limit reached"
            )
            return AssetResult(
                asset_id=asset["asset_id"],
                filename=asset["filename"],
                category=asset["category"],
                old_path=asset["paths"]["processed"],
                backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
                new_path=None,
                review_candidate_path=None,
                model_used=None,
                transparency_requested=transparency,
                generation_mode=generation_mode,
                post_processing_applied=False,
                manual_review_recommended=False,
                status="blocked_account_limit",
                note="OpenAI image generation is blocked by the current account billing or quota limit, so the original asset was preserved.",
                prompt_source=prompt_source,
            )
        console_log(f"{progress_prefix}Asset failed: {asset['filename']} | error={exc}")
        return AssetResult(
            asset_id=asset["asset_id"],
            filename=asset["filename"],
            category=asset["category"],
            old_path=asset["paths"]["processed"],
            backup_path=relative_to_root(backup_path) if backup_path.exists() else None,
            new_path=None,
            review_candidate_path=None,
            model_used=None,
            transparency_requested=transparency,
            generation_mode=generation_mode,
            post_processing_applied=False,
            manual_review_recommended=False,
            status="failed",
            note=f"Generation failed and the original asset was kept. {exc}",
            prompt_source=prompt_source,
        )


def filter_assets(assets: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    only_categories = flatten_filters(args.only)
    only_files = flatten_filters(args.only_file)
    selected: list[dict[str, Any]] = []
    for asset in assets:
        if only_categories and asset["category"].lower() not in only_categories:
            continue
        if only_files and asset["filename"].lower() not in only_files:
            continue
        selected.append(asset)
    return selected


def synthesize_prompt(asset: dict[str, Any]) -> str:
    dimensions = asset["dimensions"]
    transparency = "Transparent background." if asset.get("transparency") else "Opaque background."
    return textwrap.dedent(
        f"""
        Create {asset['filename']} for Markov's Maze.
        Purpose: {asset.get('purpose', 'Visual runtime asset.')}.
        Dimensions: {dimensions['width']}x{dimensions['height']}.
        Subject: {asset.get('prompt_subject', asset.get('purpose', asset['filename']))}.
        {transparency}
        """
    ).strip()


def main() -> int:
    args = parse_args()
    console_log("Starting visual asset upgrade run")
    console_log(
        "Run options: "
        f"force={'yes' if args.force else 'no'} | dry_run={'yes' if args.dry_run else 'no'} | "
        f"report_only={'yes' if args.report_only else 'no'} | only={args.only or 'all'} | only_file={args.only_file or 'all'}"
    )
    manifest = load_json(MANIFEST_PATH)
    prompt_bank = parse_prompt_bank(PROMPT_BANK_PATH)
    source_assets = manifest.get("assets", [])
    assets = filter_assets(source_assets, args)
    console_log(f"Loaded manifest with {len(source_assets)} assets; selected {len(assets)} asset(s) for this run")

    if not assets:
        print("No assets matched the current filters.", file=sys.stderr)
        return 1

    if args.report_only:
        console_log("Report-only mode enabled; rebuilding markdown report from manifest metadata")
        results = build_report_only_results(manifest, assets)
        report = build_report(manifest, results, args)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"Report refreshed for {len(results)} assets at {relative_to_root(REPORT_PATH)}.")
        return 0

    if not args.dry_run:
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        REVIEW_ROOT.mkdir(parents=True, exist_ok=True)

    client = make_client()
    model_candidates = choose_models()
    console_log(f"Model order: {', '.join(model_candidates)}")
    console_log(f"OpenAI client available: {'yes' if client is not None else 'no'}")
    manifest_copy = copy.deepcopy(manifest)
    manifest_assets = {asset["asset_id"]: asset for asset in manifest_copy.get("assets", [])}
    results: list[AssetResult] = []

    for index, asset in enumerate(assets, start=1):
        prompt_text = prompt_bank.get(asset["filename"], synthesize_prompt(asset))
        result = process_asset(asset, prompt_text, client, args, model_candidates, asset_index=index, asset_total=len(assets))
        results.append(result)
        console_log(
            f"[{index}/{len(assets)}] Asset finished: {asset['filename']} | status={result.status} | "
            f"manual_review={'yes' if result.manual_review_recommended else 'no'}"
        )
        if not args.dry_run:
            update_asset_metadata(manifest_assets[asset["asset_id"]], result)

    if not args.dry_run:
        manifest_copy["visual_upgrade"] = {
            "last_run_at": now_iso(),
            "last_run_mode": "report_only" if args.report_only else "safe_or_live",
            "dry_run": args.dry_run,
            "preferred_model_order": model_candidates,
            "report_path": "docs/visual_upgrade_report.md",
            "style_guide_path": "docs/visual_style_guide.md",
            "backup_root": "assets/backups/original_visuals",
            "review_root": "assets/review_candidates",
        }
        write_json(MANIFEST_PATH, manifest_copy)
        report = build_report(manifest_copy, results, args)
        REPORT_PATH.write_text(report, encoding="utf-8")
        console_log(f"Manifest written: {relative_to_root(MANIFEST_PATH)}")
        console_log(f"Report written: {relative_to_root(REPORT_PATH)}")

    counts = status_counts(results)
    summary_bits = [f"{key}={value}" for key, value in sorted(counts.items())]
    console_log(f"Run complete. Summary: {', '.join(summary_bits)}")
    print(f"Processed {len(results)} assets: {', '.join(summary_bits)}")
    if not args.dry_run:
        print(f"Manifest updated: {relative_to_root(MANIFEST_PATH)}")
        print(f"Report written: {relative_to_root(REPORT_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
