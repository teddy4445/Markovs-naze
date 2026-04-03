# Markov's Maze Asset Strategy

## Purpose

This repository is prepared for the next Phaser 3 implementation phase without changing the game design in `docs/markovs_maze_brief.md`.

The asset pipeline now provides:

- Stable final runtime filenames for every required art asset.
- Local placeholder art for every required visual asset.
- Machine-readable manifests for art and audio.
- Reproducible scripts for re-exporting placeholder art, validating the art manifest, and normalizing selected audio sources.
- OpenGameArt-only sourced audio with explicit license metadata.

## Organization

### Raw assets

- `assets/raw/art/`
  - Editable SVG placeholder source for static art where practical.
- `assets/raw/audio/`
  - Downloaded OpenGameArt source archives.
  - Stable extracted raw source clips used by the project.
  - Stable raw music source files.

### Processed runtime assets

- `assets/processed/backgrounds/`
- `assets/processed/branding/`
- `assets/processed/icons/`
- `assets/processed/overlays/`
- `assets/processed/props/`
- `assets/processed/sprites/player/`
- `assets/processed/sprites/enemy/`
- `assets/processed/tiles/`
- `assets/processed/ui/`
- `assets/processed/vfx/`
- `assets/processed/audio/sfx/`
- `assets/processed/audio/music/`

The processed folder is the expected runtime source for the later Phaser game task.

## Placeholder vs Final

### Current state

- All required visual assets exist as local procedural placeholders.
- All visual placeholders use the final runtime filenames documented in the brief.
- The placeholder export also emits `data/asset_manifest.json`, `docs/asset_manifest.md`, and `docs/art_prompt_bank.md`.
- All selected audio assets are sourced from OpenGameArt and copied to final runtime paths.

### Not final yet

- The art is placeholder-grade and should be replaced by generated or human-authored final art later.
- Audio filenames and sourcing are stable, but a final loudness and mix pass is still recommended during gameplay integration.

## Scripts

- `scripts/export_placeholder_art.py`
  - Source of truth for the visual asset inventory.
  - Rebuilds placeholder PNGs and static SVGs.
  - Rewrites the visual manifest and prompt bank.
- `scripts/validate_asset_manifest.py`
  - Checks that the generated art files match the manifest.
- `scripts/normalize_audio.py`
  - Extracts selected OpenGameArt clips from retained source archives or direct downloads.
  - Copies runtime-ready WAV/OGG files into processed audio folders.
  - Rewrites `data/audio_manifest.json`.

## Human Review Still Needed

- Replace placeholder art with final generated or hand-authored art using the existing prompt bank and filenames.
- Review sprite readability at the actual gameplay scale once Phaser scenes exist.
- Audition the sourced SFX and music in-browser to confirm pacing, loop feel, and volume balance.
- Decide later whether the mixed WAV/OGG set should be converted to a single preferred runtime format for shipping.
