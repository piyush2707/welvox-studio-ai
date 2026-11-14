
# Welvox Rendering Engine

The rendering engine connects validated production plans to media-rendering tools.

## Current FFmpeg Adapter

The first functional FFmpeg adapter supports a deliberately limited workflow:

- One scene.
- One video footage layer.
- One video asset.
- Scene and footage start at zero.
- Scene, footage, and project durations match.
- MP4 output using H.264 video.
- AAC audio output.
- Scaling and padding to requested output dimensions.

## VFX Integration

The adapter supports VFX operations directly on the footage layer.

Currently supported operations:

- `cinematic_grade` — cinematic contrast, saturation, color balance, and vignette.
- `tech_neon_grade` — stronger saturation and a blue-toned technology aesthetic.
- `vignette` — adjustable vignette using a validated angle parameter.

Example production-plan layer:

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
```

The VFX engine builds the FFmpeg filter chain, and the renderer applies it during video rendering.

Separate VFX layers and complex compositing are not supported yet.

## Dry-run Mode

Dry-run is the default. It prepares an FFmpeg command without executing it.

```bash
python engine/renderer/ffmpeg_adapter.py \
  examples/simple-video-plan.json \
  --project-root . \
  --output output/preview.mp4
```

## Execute a Render

Actual rendering requires FFmpeg to be installed and available in PATH.

```bash
python engine/renderer/ffmpeg_adapter.py \
  examples/simple-video-plan.json \
  --project-root . \
  --output output/preview.mp4 \
  --execute
```

Only use `--execute` when the source asset and rendering environment are ready.

## Current Limitations

The adapter does not yet support:

- Multiple scenes or clips.
- Transitions.
- Text overlays.
- Separate VFX or motion layers.
- Advanced compositing.
- Separate audio tracks.
- 3D assets.
- Automated visual quality review.

Unsupported projects are rejected rather than silently rendered incorrectly.

## Safety

- Project asset and output paths must remain inside the project root.
- Output cannot overwrite the source video.
- Dry-run does not execute external programs.
- Rendering is only reported as successful after FFmpeg exits successfully and the output file exists.
- 
