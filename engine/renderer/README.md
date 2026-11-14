# Welvox Rendering Engine

The rendering engine connects validated production plans to media-rendering tools.

## Current FFmpeg Adapter

The current FFmpeg adapter supports a limited but functional workflow:

- One scene per project.
- One primary video footage layer.
- Optional one-video picture-in-picture overlay.
- VFX operations on the primary footage.
- MP4 output using H.264 video.
- AAC audio output from the primary footage.
- Scaling and padding to requested output dimensions.
- Dry-run command preparation.
- Optional real FFmpeg execution.

Unsupported projects are rejected instead of being silently rendered incorrectly.

## Primary Footage

The primary footage layer must:

- Reference a video asset.
- Start at zero.
- Match the project duration.
- Use a supported VFX operation if an engine operation is specified.

## Supported VFX Operations

The adapter currently supports these operations on primary footage:

- `cinematic_grade` — cinematic contrast, saturation, color balance, and vignette.
- `tech_neon_grade` — stronger saturation and a blue-toned technology aesthetic.
- `vignette` — adjustable vignette using a validated angle parameter.
- `film_grain` — animated film grain using a validated strength parameter.

Example:

```json
{
  "id": "main-footage",
  "type": "footage",
  "asset_id": "main-footage",
  "start_seconds": 0,
  "duration_seconds": 5,
  "engine": "vfx",
  "operation": "cinematic_grade"
}
