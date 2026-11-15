
# Welvox Studio AI — VFX Effect Catalog

## Purpose

This document describes the named FFmpeg effects currently exposed by
`engine/effects/vfx_engine.py`.

Agents should select an effect by its exact operation identifier.
Do not invent operation names or supply raw FFmpeg filter expressions.

## Cinematic and color

| Operation | Purpose |
|---|---|
| cinematic_grade | Balanced cinematic contrast and color |
| tech_neon_grade | High-saturation neon-inspired grade |
| warm_glow | Warm highlights with soft diffusion |
| cold_steel | Cool, restrained metallic color |
| sunset_tone | Warm sunset-inspired color |
| teal_orange | Teal shadows and warm highlights |
| vintage_film | Vintage film curve and muted saturation |
| golden_hour | Golden warm color treatment |
| cool_blue | Cool blue color balance |
| dark_cinema | Dark cinematic contrast and vignette |
| bright_pop | Bright, saturated, energetic image |
| poster_tone | High-impact poster-style contrast |
| fade_wash | Soft faded color treatment |
| color_pop | Strong color saturation |
| warm_monochrome | Warm-tinted monochrome |
| cool_monochrome | Cool-tinted monochrome |
| noir | High-contrast black and white |
| monochrome | Remove color |
| sepia | Sepia color treatment |
| high_contrast | Strong contrast |
| soft_contrast | Reduced contrast |
| vivid_color | Increased saturation |
| muted_color | Reduced saturation |
| bleach_bypass | High contrast with reduced saturation |
| lifted_blacks | Lift dark image levels |
| crushed_blacks | Darken image levels |
| film_fade | Lifted, faded film appearance |

## Blur, focus and detail

| Operation | Purpose |
|---|---|
| dream_soft | Soft dream-like blur and color |
| soft_focus | Gentle image diffusion |
| gaussian_blur | Gaussian blur |
| box_blur | Box blur |
| sharpen | Sharpen image detail |
| clarity | Sharpening with contrast enhancement |
| edge_detect | Highlight image edges |
| emboss | Emboss-style edge treatment |
| fisheye | Lens distortion |
| soft_vignette | Gentle darkened edges |
| strong_vignette | Strong darkened edges |
| vignette | Adjustable edge darkening |

## Motion and distortion

| Operation | Purpose |
|---|---|
| motion_blend | Blend consecutive frames |
| frame_ghost | Multi-frame ghosting |
| rgb_glitch | Shift color channels |
| hue_shift | Rotate image hue |
| pixelate | Pixelated image treatment |
| rotate_clockwise | Rotate video clockwise |
| rotate_counterclockwise | Rotate video counterclockwise |
| mirror_horizontal | Mirror image horizontally |
| flip_vertical | Flip image vertically |
| negative | Invert image colors |

## Texture and graphic overlays

| Operation | Purpose |
|---|---|
| film_grain | Adjustable animated grain |
| subtle_grain | Light film grain |
| heavy_grain | Strong film grain |
| vhs_tape | VHS-inspired distortion and noise |
| tv_static | Animated television static |
| scanlines | Horizontal scanline overlay |
| grid_overlay | Visible grid overlay |
| crosshair | Center crosshair graphic |
| letterbox | Cinematic letterbox framing |
| neon_edges | Colored edge treatment |

## Parameters

Only the following effects currently accept custom parameters.

### vignette

```json
{
  "engine": "vfx",
  "operation": "vignette",
  "parameters": {
    "angle": 0.65
  }
}
```

- `angle`: number from 0.1 to 1.5.
- Default: `0.65`.

### film_grain

```json
{
  "engine": "vfx",
  "operation": "film_grain",
  "parameters": {
    "strength": 12
  }
}
```

- `strength`: integer from 1 to 100.
- Default: `12`.

Other effects currently use their built-in settings and reject custom parameters.

## Agent usage rules

1. Inspect the effect catalog before selecting an effect.
2. Use exact operation identifiers.
3. Use `engine: "vfx"` for VFX operations.
4. Supply only documented parameters.
5. Never inject user-provided text into raw FFmpeg filter expressions.
6. Validate the production plan before rendering.
7. Report rendering errors honestly.
8. Do not claim an effect was rendered unless the renderer confirms success.

## Verification

The repository includes:
- Unit tests for the effect catalog.
- Parameter validation tests.
- FFmpeg smoke tests that attempt to render every registered effect.

A successful smoke test verifies filter execution against generated test footage. It does not guarantee that every effect is visually suitable for every source video.
