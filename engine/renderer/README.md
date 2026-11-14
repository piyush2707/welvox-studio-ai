
# Welvox Rendering Engine

The rendering engine connects validated production plans to media-rendering tools.

## Current adapter

The initial FFmpeg adapter supports a deliberately limited workflow:

- One scene.
- One video footage layer.
- One video asset.
- Scene and footage start at zero.
- Scene, footage, and project durations match.
- MP4-style H.264 video output.
- AAC audio output.

The adapter scales and pads footage to the requested output dimensions.

## Dry-run mode

Dry-run is the default. It prepares an FFmpeg command without executing it.

Example:

```bash
python engine/renderer/ffmpeg_adapter.py \
  examples/simple-video-plan.json \
  --project-root . \
  --output output/preview.mp4
```

## Execute a render

Actual rendering requires FFmpeg to be installed and available in PATH.

```bash
python engine/renderer/ffmpeg_adapter.py \
  examples/simple-video-plan.json \
  --project-root . \
  --output output/preview.mp4 \
  --execute
```

Only use `--execute` when the source asset and rendering environment are ready.

## Current limitations

The adapter does not yet support:

- Multiple scenes or clips.
- Transitions.
- Text overlays.
- VFX or motion operations.
- Separate audio tracks.
- 3D assets.
- Automated visual quality review.

Unsupported projects are rejected rather than silently rendered incorrectly.

## Safety

- Project asset and output paths must remain inside the project root.
- Output cannot overwrite the source video.
- Dry-run does not execute external programs.
- Rendering is only reported as successful after FFmpeg exits successfully and the output file exists.
