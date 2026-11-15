Welvox Studio AI

Made by "Piyush Joshi" (https://www.linkedin.com/in/piyush2707)

""LinkedIn" (https://img.shields.io/badge/LinkedIn-Connect%20with%20me-0A66C2?logo=linkedin&logoColor=white)" (https://www.linkedin.com/in/piyush2707)

An AI-agent-powered video production system built with Python and FFmpeg.

""Version" (https://img.shields.io/badge/Version-1.0.0-blue)" (https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
""MIT License" (https://img.shields.io/badge/License-MIT-green.svg)" (LICENSE)
""VFX Effects" (https://img.shields.io/badge/VFX%20Effects-59-purple)" (docs/VFX-EFFECT-CATALOG.md)

---

1. About Welvox Studio AI

Welvox Studio AI is an open-source, AI-agent-assisted video production toolkit. It connects compatible AI coding agents with a structured video production workflow and an FFmpeg-based rendering engine.

What the project includes

- Portable AI Agent Skill.
- Python core engine.
- Structured JSON production-plan system.
- 59 registered FFmpeg visual effects.
- Ordered visual effect stacks.
- FFmpeg rendering adapter.
- Claude Code integration.
- OpenAI Codex integration.
- Gemini CLI integration.
- Automated unit and rendering integration tests.

The objective is to make supported video production workflows accessible through natural-language instructions to compatible coding agents.

2. V1.0.0 — First Public Release

Welvox Studio AI V1.0.0 is the first public release.

Release highlights

- 59 registered visual effects.
- Effect-stack construction and validation.
- Production-plan validation.
- FFmpeg rendering integration.
- Real FFmpeg effect execution tests.
- End-to-end rendering integration tests.
- Claude Code skill integration.
- OpenAI Codex skill integration.
- Gemini CLI skill integration.
- Shared portable Agent Skill.

"View V1.0.0 Release" (https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)

---

3. Complete VFX Library — 59 Effects

All operation identifiers below are the exact registered names in "engine/effects/vfx_engine.py".

A. Cinematic and Color Grading

No.| Effect ID| Description
01| "cinematic_grade"| Balanced cinematic contrast, saturation, color balance and vignette
02| "tech_neon_grade"| High-saturation, blue-toned technology aesthetic
03| "warm_glow"| Warm highlights with soft diffusion
04| "cold_steel"| Cool metallic color treatment
05| "sunset_tone"| Warm sunset-inspired color
06| "teal_orange"| Teal shadows and warm highlights
07| "vintage_film"| Vintage film curve and muted saturation
08| "golden_hour"| Warm golden color treatment
09| "cool_blue"| Cool blue color balance
10| "dark_cinema"| Dark cinematic contrast and vignette
11| "bright_pop"| Bright, saturated image
12| "poster_tone"| High-impact poster-style contrast
13| "fade_wash"| Soft faded color treatment
14| "color_pop"| Strong color saturation
15| "warm_monochrome"| Warm-tinted monochrome
16| "cool_monochrome"| Cool-tinted monochrome
17| "noir"| High-contrast black and white
18| "monochrome"| Removes image color
19| "sepia"| Sepia color treatment
20| "high_contrast"| Strong image contrast
21| "soft_contrast"| Reduced image contrast
22| "vivid_color"| Increased saturation
23| "muted_color"| Reduced saturation
24| "bleach_bypass"| High contrast with reduced saturation
25| "lifted_blacks"| Lifts dark image levels
26| "crushed_blacks"| Darkens black levels
27| "film_fade"| Faded film appearance

B. Blur, Focus and Detail

No.| Effect ID| Description
28| "dream_soft"| Dream-like blur and color
29| "soft_focus"| Gentle image diffusion
30| "gaussian_blur"| Gaussian image blur
31| "box_blur"| Box-based image blur
32| "sharpen"| Enhances image detail
33| "clarity"| Sharpening with contrast enhancement
34| "edge_detect"| Highlights image edges
35| "emboss"| Emboss-style edge treatment
36| "fisheye"| Fisheye lens distortion
37| "soft_vignette"| Gentle darkening around edges
38| "strong_vignette"| Strong darkening around edges
39| "vignette"| Adjustable edge darkening

C. Motion and Distortion

No.| Effect ID| Description
40| "motion_blend"| Blends consecutive video frames
41| "frame_ghost"| Multi-frame ghosting
42| "rgb_glitch"| Shifts color channels
43| "hue_shift"| Rotates image hue
44| "pixelate"| Pixelated image treatment
45| "rotate_clockwise"| Rotates video clockwise
46| "rotate_counterclockwise"| Rotates video counterclockwise
47| "mirror_horizontal"| Mirrors image horizontally
48| "flip_vertical"| Flips image vertically
49| "negative"| Inverts image colors

D. Texture and Graphic Overlays

No.| Effect ID| Description
50| "film_grain"| Animated film grain with adjustable strength
51| "subtle_grain"| Light film grain
52| "heavy_grain"| Strong film grain
53| "vhs_tape"| VHS-inspired distortion and noise
54| "tv_static"| Animated television static
55| "scanlines"| Horizontal scanline overlay
56| "grid_overlay"| Visible grid overlay
57| "crosshair"| Center crosshair graphic
58| "letterbox"| Cinematic letterbox framing
59| "neon_edges"| Colored edge treatment

Total: 59 registered effects.

Full catalog: ""docs/VFX-EFFECT-CATALOG.md"" (docs/VFX-EFFECT-CATALOG.md)

Source implementation: ""engine/effects/vfx_engine.py"" (engine/effects/vfx_engine.py)

---

4. Custom Effect Parameters

Two effects currently accept custom parameters.

Vignette

Parameter| Type| Minimum| Maximum| Default
"angle"| Number| 0.1| 1.5| 0.65

Example:

{
  "engine": "vfx",
  "operation": "vignette",
  "parameters": {
    "angle": 0.65
  }
}

Film Grain

Parameter| Type| Minimum| Maximum| Default
"strength"| Integer| 1| 100| 12

Example:

{
  "engine": "vfx",
  "operation": "film_grain",
  "parameters": {
    "strength": 12
  }
}

All other effects use built-in settings and reject custom parameters.

---

5. Ordered Effect Stacks

Welvox Studio AI supports multiple VFX operations in a specified sequence.

Example:

{
  "effects": [
    {
      "operation": "cinematic_grade"
    },
    {
      "operation": "film_grain",
      "parameters": {
        "strength": 15
      }
    },
    {
      "operation": "vignette",
      "parameters": {
        "angle": 0.65
      }
    }
  ]
}

The effect-stack implementation validates effect entries and builds the corresponding FFmpeg filter chain.

Implementation: "engine/effects/effect_stack.py"

---

6. FFmpeg Rendering Engine

The rendering adapter connects supported production plans to FFmpeg.

Supported capabilities

- Exactly one scene per project.
- One primary video footage layer.
- One VFX operation or ordered VFX effect stack on primary footage.
- Optional one-video picture-in-picture overlay.
- Scaling and padding to requested output dimensions.
- H.264 video encoding.
- AAC audio encoding from primary footage.
- Dry-run FFmpeg command preparation.
- Optional actual FFmpeg execution.

Picture-in-picture overlay

The optional video overlay supports:

- "x" — horizontal position.
- "y" — vertical position.
- "width" — overlay width.
- "height" — overlay height.
- Start time and duration.

The overlay must use a different source video from the primary footage.

VFX operations and effect stacks on overlay footage are not supported in this release.

Output encoding

The current adapter builds an MP4-oriented rendering command using:

- "libx264"
- "yuv420p"
- "aac"
- "+faststart"

The production-plan validator accepts MP4, MOV and WebM format values. This does not mean the current adapter implements separate encoding pipelines for all three formats.

Current limitations

V1.0.0 is not a complete nonlinear video editor.

It does not currently provide:

- Multi-scene rendering.
- Arbitrary multi-layer compositing.
- Effect stacks on overlay footage.
- A complete visual timeline editor.
- Cloud rendering infrastructure.
- Automatic text-to-video generation.

Unsupported project structures are rejected rather than silently treated as successfully rendered.

Implementation: "engine/renderer/ffmpeg_adapter.py"

---

7. Production Plan System

Welvox Studio AI uses a structured JSON production-plan format.

The production plan describes:

- Project title and creative brief.
- Output dimensions and frame rate.
- Output format.
- Media asset references.
- Timeline duration.
- Scenes and layers.
- Engine and operation identifiers.
- Effect stacks and parameters.
- Optional audio settings.
- Project metadata.

Main files

File| Purpose
"schemas/production-plan.schema.json"| Production-plan schema
"examples/production-plan.example.json"| Example production plan
"engine/core/welvox_core.py"| Core validation and inspection

Not every layer type described by the schema is supported by the current FFmpeg renderer.

---

8. Core Engine

The Python core provides:

- FFmpeg, FFprobe and Blender capability detection.
- JSON production-plan loading.
- Basic production-plan validation.
- Asset-reference checks.
- Scene and layer timing checks.
- Project metadata inspection.

The current validator performs built-in structural and timeline checks. It is not a complete JSON Schema validation implementation.

Implementation: "engine/core/welvox_core.py"

---

9. AI Coding Agent Integrations

Welvox Studio AI includes skill instructions for compatible coding agents.

Agent| Skill File
Claude Code| ".claude/skills/welvox-studio-ai/SKILL.md"
OpenAI Codex| ".agents/skills/welvox-studio-ai/SKILL.md"
Gemini CLI| ".agents/skills/welvox-studio-ai/SKILL.md"
Other compatible agents| "skills/welvox-studio-ai/SKILL.md"

Shared Agent Skill

The portable skill is located at:

"skills/welvox-studio-ai/SKILL.md"

It guides agents to:

1. Understand the video production brief.
2. Inspect project capabilities and dependencies.
3. Read the production-plan schema.
4. Select exact registered effect identifiers.
5. Validate production plans.
6. Prepare supported rendering jobs.
7. Execute only supported and authorized operations.
8. Verify results and report limitations honestly.

Agent discovery behavior can differ between tools and versions.

Repository instructions

"AGENTS.md" contains shared development and execution guidelines for AI coding agents.

---

10. Repository Structure

welvox-studio-ai/
├── .agents/
│   └── skills/
│       └── welvox-studio-ai/
│           └── SKILL.md
├── .claude/
│   └── skills/
│       └── welvox-studio-ai/
│           └── SKILL.md
├── .github/
│   └── workflows/
│       └── core-tests.yml
├── docs/
│   └── VFX-EFFECT-CATALOG.md
├── engine/
│   ├── core/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   └── welvox_core.py
│   ├── effects/
│   │   ├── effect_stack.py
│   │   └── vfx_engine.py
│   └── renderer/
│       ├── README.md
│       ├── __init__.py
│       └── ffmpeg_adapter.py
├── examples/
│   └── production-plan.example.json
├── modules/
│   └── director/
│       └── DIRECTOR.md
├── schemas/
│   └── production-plan.schema.json
├── skills/
│   └── welvox-studio-ai/
│       ├── SKILL.md
│       └── references/
│           └── director-workflow.md
├── tests/
│   ├── README.md
│   ├── test_agent_integrations.py
│   ├── test_core.py
│   ├── test_effect_stack.py
│   ├── test_ffmpeg_integration.py
│   ├── test_renderer.py
│   ├── test_vfx_engine.py
│   ├── test_vfx_ffmpeg.py
│   └── test_vfx_render_integration.py
├── AGENTS.md
├── LICENSE
└── README.md

---

11. Requirements

- Python 3.9 or later.
- FFmpeg for actual video rendering.
- FFprobe for optional media inspection.
- A compatible AI coding agent for the Agent Skill workflow.

The core documentation specifies no third-party Python packages for basic validation.

Actual rendering requires FFmpeg to be installed and accessible in the execution environment.

---

12. Running the Project

Run commands from the repository root in a compatible Python environment.

Check available capabilities

python engine/core/welvox_core.py capabilities

Validate a production plan

python engine/core/welvox_core.py validate examples/production-plan.example.json

Inspect a production plan

python engine/core/welvox_core.py inspect examples/production-plan.example.json

Prepare an FFmpeg render job

python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json

The default behavior prepares a render job without executing FFmpeg.

Execute a render

python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json --execute

Actual rendering requires valid source footage, a supported production plan and an available FFmpeg executable.

---

13. Automated Testing

The repository includes automated tests covering:

- Production-plan validation.
- Required fields and schema versions.
- Output settings.
- Asset references.
- Scene and layer timing.
- Project inspection.
- Capability detection.
- JSON plan loading.
- VFX registration.
- Effect parameter validation.
- Effect-stack construction.
- FFmpeg filter execution.
- Renderer behavior.
- Agent integrations.
- Real video-rendering integration.

Run the test suite

python -m unittest discover -s tests -v

GitHub Actions

Workflow:

".github/workflows/core-tests.yml"

The workflow runs automated tests on pushes to the main branch and pull requests targeting main.

The V1.0.0 release was published after automated GitHub Actions tests passed, including real FFmpeg effect and rendering tests.

A successful test verifies behavior against its test inputs. It does not guarantee every effect will look suitable on every source video.

---

14. Development Principles

Welvox Studio AI follows these principles:

- Never claim an unimplemented feature works.
- Keep creative planning separate from actual rendering.
- Use exact registered effect identifiers.
- Validate production plans before execution.
- Detect dependencies before using them.
- Preserve source media unless destructive changes are authorized.
- Keep engines modular and testable.
- Report errors and unsupported operations honestly.
- Respect software and media licenses.

See "AGENTS.md" for the complete repository guidance.

---

15. License

Welvox Studio AI is released under the MIT License.

See the "LICENSE" (LICENSE) file.

---

16. Project Links

- "GitHub Repository" (https://github.com/piyush2707/welvox-studio-ai)
- "V1.0.0 Release" (https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
- "Complete VFX Catalog" (https://github.com/piyush2707/welvox-studio-ai/blob/main/docs/VFX-EFFECT-CATALOG.md)
- "Shared Agent Skill" (https://github.com/piyush2707/welvox-studio-ai/tree/main/skills/welvox-studio-ai)
- "Production Plan Schema" (https://github.com/piyush2707/welvox-studio-ai/blob/main/schemas/production-plan.schema.json)
- "LinkedIn — Piyush Joshi" (https://www.linkedin.com/in/piyush2707)

---

Welvox Studio AI V1.0.0

Made by "Piyush Joshi" (https://www.linkedin.com/in/piyush2707)

Built with curiosity, creativity and code.
