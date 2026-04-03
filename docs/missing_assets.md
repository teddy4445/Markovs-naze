# Markov's Maze Missing Assets

## Blocking gaps

No required art filenames are missing.

No required sourced SFX slots are missing.

No required music slots are currently missing.

## Remaining non-blocking gaps

- Final art generation has not happened yet because no external image-generation provider or MCP resource was configured in this environment.
- Current art is placeholder-quality and should be replaced later using `docs/art_prompt_bank.md`.
- Audio has stable filenames and safe licenses, but it still needs an integration-time mix and loop review.

## Exact next actions

1. When an image-generation provider is available, regenerate finals using the prompt bank while keeping the same filenames and dimensions.
2. Run `python scripts/export_placeholder_art.py` again only if placeholder art needs to be refreshed from source.
3. Run `python scripts/validate_asset_manifest.py` before starting Phaser scene implementation.
4. During gameplay integration, audition `assets/processed/audio/sfx/` and `assets/processed/audio/music/` in-browser and adjust mix policy if needed.
