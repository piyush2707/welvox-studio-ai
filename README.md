# Welvox Studio AI

An AI-agent-powered video production system built with Python and FFmpeg.

[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![VFX Effects](https://img.shields.io/badge/VFX%20Effects-59-purple)](docs/VFX-EFFECT-CATALOG.md)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect%20with%20me-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyush2707)

Made by [Piyush Joshi](https://www.linkedin.com/in/piyush2707)

---

## Overview

Welvox Studio AI is an open-source toolkit that connects AI coding agents to a structured video production workflow and an FFmpeg rendering engine. Describe what you want in natural language, and your agent plans, validates and renders it.

**What's included**

- Portable AI Agent Skill
- Python core engine
- JSON production-plan system
- 59 FFmpeg visual effects with ordered effect stacks
- FFmpeg rendering adapter
- Integrations for Claude Code, OpenAI Codex and Gemini CLI
- Unit and rendering integration tests

## V1.0.0: First Public Release

- 59 registered visual effects
- Effect-stack construction and validation
- Production-plan validation
- FFmpeg rendering with real execution tests
- Shared portable Agent Skill

[View the release](https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)

---

## VFX Library

59 effects, registered in `engine/effects/vfx_engine.py`. Full catalog: [`docs/VFX-EFFECT-CATALOG.md`](docs/VFX-EFFECT-CATALOG.md)

| Category | Count | Effect IDs |
|---|---|---|
| Cinematic and color grading | 27 | `cinematic_grade`, `tech_neon_grade`, `warm_glow`, `cold_steel`, `sunset_tone`, `teal_orange`, `vintage_film`, `golden_hour`, `cool_blue`, `dark_cinema`, `bright_pop`, `poster_tone`, `fade_wash`, `color_pop`, `warm_monochrome`, `cool_monochrome`, `noir`, `monochrome`, `sepia`, `high_contrast`, `soft_contrast`, `vivid_color`, `muted_color`, `bleach_bypass`, `lifted_blacks`, `crushed_blacks`, `film_fade` |
| Blur, focus and detail | 12 | `dream_soft`, `soft_focus`, `gaussian_blur`, `box_blur`, `sharpen`, `clarity`, `edge_detect`, `emboss`, `fisheye`, `soft_vignette`, `strong_vignette`, `vignette` |
| Motion and distortion | 10 | `motion_blend`, `frame_ghost`, `rgb_glitch`, `hue_shift`, `pixelate`, `rotate_clockwise`, `rotate_counterclockwise`, `mirror_horizontal`, `flip_vertical`, `negative` |
| Texture and overlays | 10 | `film_grain`, `subtle_grain`, `heavy_grain`, `vhs_tape`, `tv_static`, `scanlines`, `grid_overlay`, `crosshair`, `letterbox`, `neon_edges` |

### Custom parameters

Only two effects accept parameters. All others use built-in settings and reject custom values.

| Effect | Parameter | Type | Range | Default |
|---|---|---|---|---|
| `vignette` | `angle` | Number | 0.1 to 1.5 | 0.65 |
| `film_grain` | `strength` | Integer | 1 to 100 | 12 |

### Effect stacks

Chain multiple effects in order. The stack is validated and converted into an FFmpeg filter chain (`engine/effects/effect_stack.py`).

```json
{
  "effects": [
    { "operation": "cinematic_grade" },
    { "operation": "film_grain", "parameters": { "strength": 15 } },
    { "operation": "vignette", "parameters": { "angle": 0.65 } }
  ]
}
```

---

## Rendering Engine

The FFmpeg adapter (`engine/renderer/ffmpeg_adapter.py`) supports:

- One scene per project with one primary video layer
- One VFX operation or effect stack on the primary footage
- Optional picture-in-picture overlay (`x`, `y`, `width`, `height`, start time, duration). It must use a different source video, and effects on the overlay are not supported.
- Scaling and padding to the requested output size
- H.264 video and AAC audio, with dry-run or real execution

Output uses `libx264`, `yuv420p`, `aac` and `+faststart`. The validator accepts MP4, MOV and WebM values, but the adapter currently builds an MP4-oriented pipeline only.

### Current limitations

V1.0.0 is not a full nonlinear editor. It does not provide:

- Multi-scene rendering
- Arbitrary multi-layer compositing
- Effect stacks on overlay footage
- A visual timeline editor
- Cloud rendering
- Automatic text-to-video generation

Unsupported project structures are rejected, never silently rendered.

---

## Production Plans

Projects are described in a structured JSON plan covering title and brief, output size and frame rate, format, assets, timeline, scenes and layers, effects, audio and metadata.

| File | Purpose |
|---|---|
| `schemas/production-plan.schema.json` | Plan schema |
| `examples/production-plan.example.json` | Example plan |
| `engine/core/welvox_core.py` | Validation and inspection |

The core engine also detects FFmpeg, FFprobe and Blender, checks asset references and timing, and inspects project metadata. Validation is structural and timeline-based. It is not a full JSON Schema implementation, and not every schema layer type is supported by the renderer yet.

---

## AI Agent Integrations

| Agent | Skill file |
|---|---|
| Claude Code | `.claude/skills/welvox-studio-ai/SKILL.md` |
| OpenAI Codex | `.agents/skills/welvox-studio-ai/SKILL.md` |
| Gemini CLI | `.agents/skills/welvox-studio-ai/SKILL.md` |
| Other agents | `skills/welvox-studio-ai/SKILL.md` |

The shared skill guides an agent to understand the brief, check dependencies, read the schema, pick exact effect IDs, validate the plan, prepare and run supported renders, then verify results and report limitations honestly. Discovery behavior may vary between tools and versions. Shared guidelines live in `AGENTS.md`.

---

## Getting Started

**Requirements:** Python 3.9+, FFmpeg (for rendering), FFprobe (optional, for inspection) and a compatible AI coding agent. Basic validation needs no third-party Python packages.

Run all commands from the repository root:

```bash
# Check available capabilities
python engine/core/welvox_core.py capabilities

# Validate and inspect a plan
python engine/core/welvox_core.py validate examples/production-plan.example.json
python engine/core/welvox_core.py inspect examples/production-plan.example.json

# Prepare a render job (dry run, default)
python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json

# Execute the render
python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json --execute
```

Rendering requires valid source footage, a supported plan and FFmpeg on your PATH.

## Testing

```bash
python -m unittest discover -s tests -v
```

Tests cover plan validation, timing, asset references, VFX registration and parameters, effect stacks, real FFmpeg filter execution, renderer behavior, agent integrations and end-to-end rendering. GitHub Actions (`.github/workflows/core-tests.yml`) runs them on pushes and pull requests to `main`. V1.0.0 was released after these passed.

A passing test confirms behavior on its test inputs. It does not guarantee every effect suits every source video.

---

## Repository Structure

```
welvox-studio-ai/
├── .agents/skills/welvox-studio-ai/SKILL.md
├── .claude/skills/welvox-studio-ai/SKILL.md
├── .github/workflows/core-tests.yml
├── docs/VFX-EFFECT-CATALOG.md
├── engine/
│   ├── core/welvox_core.py
│   ├── effects/{effect_stack.py, vfx_engine.py}
│   └── renderer/ffmpeg_adapter.py
├── examples/production-plan.example.json
├── modules/director/DIRECTOR.md
├── schemas/production-plan.schema.json
├── skills/welvox-studio-ai/
│   ├── SKILL.md
│   └── references/director-workflow.md
├── tests/
├── AGENTS.md
├── LICENSE
└── README.md
```

## Development Principles

- Never claim an unimplemented feature works
- Keep creative planning separate from rendering
- Use exact registered effect identifiers
- Validate plans before execution
- Detect dependencies before using them
- Preserve source media unless destructive changes are authorized
- Keep engines modular and testable
- Report errors and unsupported operations honestly
- Respect software and media licenses

## License

Released under the [MIT License](LICENSE).

## Links

- [GitHub Repository](https://github.com/piyush2707/welvox-studio-ai)
- [V1.0.0 Release](https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
- [VFX Catalog](https://github.com/piyush2707/welvox-studio-ai/blob/main/docs/VFX-EFFECT-CATALOG.md)
- [Shared Agent Skill](https://github.com/piyush2707/welvox-studio-ai/tree/main/skills/welvox-studio-ai)
- [Production Plan Schema](https://github.com/piyush2707/welvox-studio-ai/blob/main/schemas/production-plan.schema.json)
- [Piyush Joshi on LinkedIn](https://www.linkedin.com/in/piyush2707)

---

**Welvox Studio AI V1.0.0** · Built with curiosity, creativity and code.
