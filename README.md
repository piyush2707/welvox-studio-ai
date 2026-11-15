<div align="center">

# 🎬 Welvox Studio AI

### 59 FFmpeg visual effects, directed by your AI coding agent.


<p align="center">
  <img src="assets/welvox-logo.png" 
    </p>

[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![VFX Effects](https://img.shields.io/badge/VFX%20Effects-59-purple)](docs/VFX-EFFECT-CATALOG.md)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect%20with%20me-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyush2707)

Made by [Piyush Joshi](https://www.linkedin.com/in/piyush2707)

</div>

---

## ✨ What is it?

Welvox Studio AI is an open-source video production toolkit for AI coding agents. Tell **Claude Code, OpenAI Codex or Gemini CLI** what look you want. The agent picks effects, builds a JSON production plan, validates it and renders with FFmpeg.

**🎞️ 59 effects · 🔗 Stackable in any order · 🤖 3 agent integrations · ✅ Tested with real FFmpeg renders**

---

## 🎨 The VFX Library

All effect IDs are the exact names registered in `engine/effects/vfx_engine.py`. Full catalog: [`docs/VFX-EFFECT-CATALOG.md`](docs/VFX-EFFECT-CATALOG.md)



<p align="center">
  <img src="assets/welvox-effect.png" 
    </p>
  
### 🎥 Cinematic and Color Grading (27)

| Effect ID | Look |
|---|---|
| `cinematic_grade` | Balanced contrast, saturation, color balance and vignette |
| `tech_neon_grade` | High-saturation, blue-toned tech aesthetic |
| `warm_glow` | Warm highlights with soft diffusion |
| `cold_steel` | Cool metallic color |
| `sunset_tone` | Warm sunset color |
| `teal_orange` | Teal shadows, warm highlights |
| `vintage_film` | Vintage film curve, muted saturation |
| `golden_hour` | Warm golden color |
| `cool_blue` | Cool blue balance |
| `dark_cinema` | Dark cinematic contrast and vignette |
| `bright_pop` | Bright, saturated image |
| `poster_tone` | High-impact poster contrast |
| `fade_wash` | Soft faded color |
| `color_pop` | Strong color saturation |
| `warm_monochrome` | Warm-tinted monochrome |
| `cool_monochrome` | Cool-tinted monochrome |
| `noir` | High-contrast black and white |
| `monochrome` | Removes all color |
| `sepia` | Classic sepia |
| `high_contrast` | Strong contrast |
| `soft_contrast` | Reduced contrast |
| `vivid_color` | Increased saturation |
| `muted_color` | Reduced saturation |
| `bleach_bypass` | High contrast, low saturation |
| `lifted_blacks` | Lifts dark levels |
| `crushed_blacks` | Darkens black levels |
| `film_fade` | Faded film appearance |

### 🔍 Blur, Focus and Detail (12)

| Effect ID | Look |
|---|---|
| `dream_soft` | Dream-like blur and color |
| `soft_focus` | Gentle diffusion |
| `gaussian_blur` | Gaussian blur |
| `box_blur` | Box blur |
| `sharpen` | Enhanced detail |
| `clarity` | Sharpening plus contrast |
| `edge_detect` | Highlights edges |
| `emboss` | Emboss-style edges |
| `fisheye` | Fisheye lens distortion |
| `soft_vignette` | Gentle edge darkening |
| `strong_vignette` | Strong edge darkening |
| `vignette` | Adjustable edge darkening |

### ⚡ Motion and Distortion (10)

| Effect ID | Look |
|---|---|
| `motion_blend` | Blends consecutive frames |
| `frame_ghost` | Multi-frame ghosting |
| `rgb_glitch` | Shifts color channels |
| `hue_shift` | Rotates hue |
| `pixelate` | Pixelated look |
| `rotate_clockwise` | Rotates clockwise |
| `rotate_counterclockwise` | Rotates counterclockwise |
| `mirror_horizontal` | Horizontal mirror |
| `flip_vertical` | Vertical flip |
| `negative` | Inverts colors |

### 📼 Texture and Graphic Overlays (10)

| Effect ID | Look |
|---|---|
| `film_grain` | Animated grain, adjustable strength |
| `subtle_grain` | Light grain |
| `heavy_grain` | Strong grain |
| `vhs_tape` | VHS distortion and noise |
| `tv_static` | Animated TV static |
| `scanlines` | Horizontal scanlines |
| `grid_overlay` | Visible grid |
| `crosshair` | Center crosshair |
| `letterbox` | Cinematic letterbox |
| `neon_edges` | Colored edge glow |

### 🎛️ Adjustable Effects

Only two effects accept parameters. All others use built-in settings.

| Effect | Parameter | Range | Default |
|---|---|---|---|
| `vignette` | `angle` | 0.1 to 1.5 | 0.65 |
| `film_grain` | `strength` | 1 to 100 | 12 |

### 🔗 Effect Stacks

Combine effects in order. The stack is validated and turned into an FFmpeg filter chain (`engine/effects/effect_stack.py`).

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

## 🚀 Quick Start

**Requires:** Python 3.9+, FFmpeg (rendering), FFprobe (optional) and a compatible AI coding agent. No third-party Python packages needed for validation.

```bash
# Check capabilities
python engine/core/welvox_core.py capabilities

# Validate and inspect a plan
python engine/core/welvox_core.py validate examples/production-plan.example.json
python engine/core/welvox_core.py inspect examples/production-plan.example.json

# Dry run (default)
python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json

# Render for real
python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json --execute
```

---

## 🤖 Agent Integrations

| Agent | Skill file |
|---|---|
| Claude Code | `.claude/skills/welvox-studio-ai/SKILL.md` |
| OpenAI Codex | `.agents/skills/welvox-studio-ai/SKILL.md` |
| Gemini CLI | `.agents/skills/welvox-studio-ai/SKILL.md` |
| Other agents | `skills/welvox-studio-ai/SKILL.md` |

The shared skill guides agents to read the brief, check dependencies, pick exact effect IDs, validate the plan, run supported renders and report limitations honestly. Discovery may vary between tools. See `AGENTS.md` for shared guidelines.

---

## 🎞️ Rendering Engine

`engine/renderer/ffmpeg_adapter.py` supports:

- One scene with one primary video layer
- One effect or one effect stack on the primary footage
- Optional picture-in-picture overlay (`x`, `y`, `width`, `height`, start, duration). It needs a different source video, and effects on the overlay are not supported.
- Scaling and padding to the output size
- H.264 video and AAC audio (`libx264`, `yuv420p`, `aac`, `+faststart`), dry run or real execution

The validator accepts MP4, MOV and WebM, but the adapter builds an MP4-oriented pipeline only.

**Not in V1.0.0:** multi-scene rendering, arbitrary multi-layer compositing, effect stacks on overlays, a visual timeline editor, cloud rendering and text-to-video. Unsupported structures are rejected, never silently rendered.

---

## 📋 Production Plans

Each project is a JSON plan: title and brief, output size and frame rate, format, assets, timeline, scenes, layers, effects, audio and metadata.

| File | Purpose |
|---|---|
| `schemas/production-plan.schema.json` | Plan schema |
| `examples/production-plan.example.json` | Example plan |
| `engine/core/welvox_core.py` | Validation and inspection |

Validation is structural and timeline-based, not a full JSON Schema check. Not every schema layer type is supported by the renderer yet.

---

## ✅ Testing

```bash
python -m unittest discover -s tests -v
```

Tests cover plan validation, effect registration and parameters, effect stacks, real FFmpeg filter execution, the renderer, agent integrations and end-to-end renders. GitHub Actions runs them on pushes and pull requests to `main`, and V1.0.0 shipped after they passed.

A passing test confirms behavior on its test inputs. It does not guarantee every effect suits every source video.

---

## 🗂️ Repository Structure

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
├── tests/
├── AGENTS.md
├── LICENSE
└── README.md
```

## 🧭 Principles

Never claim an unimplemented feature works · Use exact effect IDs · Validate before executing · Detect dependencies first · Preserve source media · Keep engines modular and testable · Report errors honestly · Respect licenses

## 📄 License

[MIT License](LICENSE)

## 🔗 Links

[GitHub](https://github.com/piyush2707/welvox-studio-ai) · [V1.0.0 Release](https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0) · [VFX Catalog](https://github.com/piyush2707/welvox-studio-ai/blob/main/docs/VFX-EFFECT-CATALOG.md) · [Agent Skill](https://github.com/piyush2707/welvox-studio-ai/tree/main/skills/welvox-studio-ai) · [Schema](https://github.com/piyush2707/welvox-studio-ai/blob/main/schemas/production-plan.schema.json) · [LinkedIn](https://www.linkedin.com/in/piyush2707)

<div align="center">

**Welvox Studio AI V1.0.0** · Built with curiosity, creativity and code.

</div>
