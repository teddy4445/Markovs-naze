# Markov's Maze Visual Style Guide

This guide defines the target look for OpenAI-assisted visual upgrades while preserving the filenames, dimensions, and runtime paths already used by the Phaser build.

## Core Style Rules

- Top-down 2D game asset
- Orthographic view only
- Low-detail flat fantasy
- Ancient magical ruins theme
- Clean readable silhouette
- Minimal texture
- Soft flat shading
- Strong contrast
- Elegant rune details
- Gameplay readability first
- Magical and mysterious tone
- No photorealism
- No isometric angle
- No perspective distortion
- No stray text unless the asset is the logo

## Palette Guidance

- Base palette: muted stone gray, sand beige, moss green
- Rune accents: glowing cyan and magical gold
- Lava: orange-red with bright hot centers and darker ember edges
- Enemy accents: cursed purple or sickly green glow
- Background values should stay calmer than active gameplay elements

## Character Rules

- Player character is a ruins scholar with a practical explorer silhouette
- Keep the player readable from a top-down game camera with restrained costume detail
- Enemy is a cursed knight with worn armor and a spectral glow
- Character proportions, lighting direction, and accent placement should remain consistent across sheets
- Avoid broken anatomy, extra limbs, mirrored weapon clutter, and unreadable face detail

## Tile, Prop, And Overlay Rules

- Tiles must read clearly at gameplay scale before decorative detail is considered
- Hazard tiles should communicate danger primarily through color and shape contrast
- Compass and probability overlays should remain lighter, simpler, and cleaner than base tiles
- Props should feel ancient and ruined without looking like blockers unless their silhouette clearly implies it

## UI Rules

- UI should look like carved ruins stone with rune framing
- Buttons and panels must remain readable over bright and dark backgrounds
- Menu and HUD elements should avoid noisy texture that competes with maze readability
- Icons should communicate with one dominant shape and a small amount of rune detail

## Background Rules

- Backgrounds should support the board instead of stealing focus
- Main menu and level-select backgrounds can be more atmospheric, but still need calm space for UI
- Gameplay backgrounds should be subdued and value-controlled
- Long parallax backgrounds should favor wide rhythm, loop-friendly silhouettes, and restrained perspective

## Animation Review Rules

- Treat all animated sprite sheets as manual-review assets even after generation
- Confirm frame counts, frame dimensions, and horizontal sheet layout match the manifest exactly
- Reject sheets with obvious frame-to-frame design drift, anatomy glitches, or lighting flips
- Prefer keeping the existing sheet plus a review candidate over auto-replacing a questionable result

## Acceptance Rules

- Accept only assets that stay readable at game scale
- Accept only assets that preserve correct transparency behavior for the category
- Reject results with random text, watermarks, broken anatomy, perspective mismatch, or muddy silhouettes
- If the result is uncertain, keep the original asset and store the generated candidate under `assets/review_candidates/`
