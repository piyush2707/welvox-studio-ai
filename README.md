Welvox Studio AI

Made by "Piyush Joshi" (https://www.linkedin.com/in/piyush2707)

""LinkedIn" (https://img.shields.io/badge/LinkedIn-Piyush%20Joshi-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)" (https://www.linkedin.com/in/piyush2707)

An AI-agent-powered video production system built with Python and FFmpeg.

""Release" (https://img.shields.io/badge/Release-V1.0.0-blue?style=flat-square)" (https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)
""License" (https://img.shields.io/github/license/piyush2707/welvox-studio-ai?style=flat-square)" (LICENSE)
""GitHub" (https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)" (https://github.com/piyush2707/welvox-studio-ai)

---

1. About the project

Welvox Studio AI is an open-source, AI-agent-assisted video production toolkit. It connects coding agents with a structured production workflow and an FFmpeg-based rendering engine.

The project provides:

- A reusable Agent Skill.
- A structured video production-plan format.
- A Python core engine.
- A library of 59 registered FFmpeg visual effects.
- Ordered visual effect stacks.
- An FFmpeg rendering adapter.
- Automated unit and integration tests.
- Instructions for Claude Code, OpenAI Codex, and Gemini CLI.

The goal is to make video production workflows accessible through natural-language instructions to compatible coding agents, while keeping actual rendering grounded in implemented software capabilities.

2. V1.0.0 release

Welvox Studio AI V1.0.0 is the first public release.

Release highlights

- 59 registered visual effects.
- Effect-stack construction and validation.
- Structured production-plan validation.
- FFmpeg rendering integration.
- Real FFmpeg effect execution tests.
- End-to-end rendering integration tests.
- Claude Code skill integration.
- OpenAI Codex skill integration.
- Gemini CLI skill integration.
- Shared portable Agent Skill.

Release: "Welvox Studio AI V1.0.0" (https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0)

3. Visual effects catalog — all 59 effects

The following identifiers are the exact registered operation names in "engine/effects/vfx_engine.py".

A. Cinematic and color grading

#| Operation ID| Description
1| "cinematic_grade"| Balanced cinematic contrast, saturation, color balance, and vignette.
2| "tech_neon_grade"| High-saturation, blue-toned technology aesthetic.
3| "warm_glow"| Warm highlights, increased saturation, and soft diffusion.
4| "cold_steel"| Cool metallic color treatment with restrained saturation.
5| "sunset_tone"| Warm sunset-inspired color balance.
6| "teal_orange"| Teal shadows and warm highlights.
7| "vintage_film"| Vintage film curve with muted saturation.
8| "golden_hour"| Warm golden color treatment.
9| "cool_blue"| Cool blue color balance.
10| "dark_cinema"| Dark cinematic contrast and vignette.
11| "bright_pop"| Brighter image with energetic saturation.
12| "poster_tone"| High-impact poster-style contrast and sharpening.
13| "fade_wash"| Soft, faded color treatment.
14| "color_pop"| Strong color saturation and contrast.
15| "warm_monochrome"| Black and white with a warm tint.
16| "cool_monochrome"| Black and white with a cool tint.
17| "noir"| High-contrast black-and-white cinematic treatment.
18| "monochrome"| Removes image color.
19| "sepia"| Classic sepia color treatment.
20| "high_contrast"| Stronger image contrast.
21| "soft_contrast"| Reduced image contrast.
22| "vivid_color"| Increased color saturation.
23| "muted_color"| Reduced saturation and restrained color.
24| "bleach_bypass"| High contrast with reduced saturation.
25| "lifted_blacks"| Lifts dark image levels.
26| "crushed_blacks"| Darkens black levels.
27| "film_fade"| Faded film appearance with lifted tones.

B. Blur, focus, and detail

#| Operation ID| Description
28| "dream_soft"| Dream-like blur with brighter, saturated tones.
29| "soft_focus"| Gentle image diffusion.
30| "gaussian_blur"| Gaussian image blur.
31| "box_blur"| Box-based image blur.
32| "sharpen"| Enhances image detail.
33| "clarity"| Sharpening combined with contrast enhancement.
34| "edge_detect"| Highlights image edges.
35| "emboss"| Emboss-style edge treatment.
36| "fisheye"| Lens distortion for a fisheye appearance.
37| "soft_vignette"| Gentle darkening around image edges.
38| "strong_vignette"| Strong darkening around image edges.
39| "vignette"| Adjustable edge darkening.

C. Motion and distortion

#| Operation ID| Description
40| "motion_blend"| Blends consecutive video frames.
41| "frame_ghost"| Creates multi-frame ghosting.
42| "rgb_glitch"| Shifts color channels for a glitch appearance.
43| "hue_shift"| Rotates image hue.
44| "pixelate"| Produces a pixelated image treatment.
45| "rotate_clockwise"| Rotates video clockwise.
46| "rotate_counterclockwise"| Rotates video counterclockwise.
47| "mirror_horizontal"| Mirrors the image horizontally.
48| "flip_vertical"| Flips the image vertically.
49| "negative"| Inverts image colors.

D. Texture and graphic overlays

#| Operation ID| Description
50| "film_grain"| Animated film grain with adjustable strength.
51| "subtle_grain"| Light film grain.
52| "heavy_grain"| Strong film grain.
53| "vhs_tape"| VHS-inspired color distortion and noise.
54| "tv_static"| Animated television static.
55| "scanlines"| Horizontal scanline overlay.
56| "grid_overlay"| Visible grid overlay.
57| "crosshair"| Center crosshair graphic.
58| "letterbox"| Cinematic letterbox framing.
59| "neon_edges"| Colored edge-detection treatment.

Total: 59 registered effects.

Official implementation: ""engine/effects/vfx_engine.py"" (engine/effects/vfx_engine.py)

Full effect catalog documentation: ""docs/VFX-EFFECT-CATALOG.md"" (docs/VFX-EFFECT-CATALOG.md)

4. Effect parameters

Two effects expose custom parameters in the current VFX engine.

Vignette

Operation: "vignette"

Parameter| Type| Accepted range| Default
"angle"| Number| 0.1–1.5| 0.65

Example:

{
  "engine": "vfx",
  "operation": "vignette",
  "parameters": {
    "angle": 0.65
  }
}

Film grain

Operation: "film_grain"

Parameter| Type| Accepted range| Default
"strength"| Integer| 1–100| 12

Example:

{
  "engine": "vfx",
  "operation": "film_grain",
  "parameters": {
    "strength": 12
  }
}

Other registered effects use their built-in filter settings and reject custom parameters.

5. Ordered effect stacks

Welvox Studio AI supports ordered VFX effect stacks.

An effect stack lets a production plan apply multiple registered operations in a defined sequence.

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

6. Rendering engine

The rendering adapter connects supported production plans to FFmpeg.

Current supported workflow

- Exactly one scene per project.
- One primary video footage layer.
- One VFX operation or ordered VFX effect stack on primary footage.
- Optional one-video picture-in-picture overlay.
- Scaling and padding to requested output dimensions.
- H.264 video encoding.
- AAC audio encoding from the primary footage.
- Dry-run command preparation.
- Optional real FFmpeg execution.

Picture-in-picture overlay

The renderer supports one additional video overlay.

Its position and dimensions are configured with:

- "x"
- "y"
- "width"
- "height"

The overlay can also have a start time and duration within the project timeline.

The overlay must reference a different video source from the primary footage. VFX operations and effect stacks on overlay footage are not currently supported.

Rendering output

The current FFmpeg adapter builds an MP4-oriented rendering command using:

- "libx264"
- "yuv420p"
- "aac"
- "+faststart"

The production-plan validator accepts "mp4", "mov", and "webm" format values, but that does not mean the current adapter implements separate encoding pipelines for all three formats.

Rendering limitations

V1.0.0 does not provide:

- Full multi-scene rendering.
- Arbitrary multi-layer compositing.
- Effect stacks on overlay footage.
- A complete visual timeline editor.
- Cloud rendering infrastructure.
- Automatic text-to-video generation.
- A browser-based video rendering service.

Unsupported project structures are rejected instead of being silently treated as successfully rendered.

Implementation: "engine/renderer/ffmpeg_adapter.py"

7. Production-plan system

Welvox Studio AI uses a structured JSON production plan.

The schema defines:

- Project title and creative brief.
- Output dimensions, frame rate, and format.
- Media asset references.
- Timeline duration.
- Scenes and layers.
- Engine and operation identifiers.
- Effect stacks and parameters.
- Optional audio settings.
- Project metadata.

Main schema

"schemas/production-plan.schema.json"

Example production plan

"examples/production-plan.example.json"

The example demonstrates the production-plan structure. Not every engine or layer type described by the schema is implemented by the current FFmpeg renderer.

8. Core engine

The Python core provides foundational project and production-plan operations.

Current documented capabilities include:

- Detecting FFmpeg, FFprobe, and Blender availability.
- Loading production plans from JSON.
- Basic production-plan validation.
- Checking asset references.
- Checking scene and layer timing.
- Inspecting project metadata.

The core validator performs built-in structural and timeline checks. It should not be confused with a complete JSON Schema validation implementation.

Implementation: "engine/core/welvox_core.py"

9. AI coding agent integrations

Welvox Studio AI includes Agent Skill instructions for compatible coding agents.

Agent| Skill file
Claude Code| ".claude/skills/welvox-studio-ai/SKILL.md"
OpenAI Codex| ".agents/skills/welvox-studio-ai/SKILL.md"
Gemini CLI| ".agents/skills/welvox-studio-ai/SKILL.md"
Other compatible agents| "skills/welvox-studio-ai/SKILL.md"

Shared Agent Skill

The portable skill is located at:

"skills/welvox-studio-ai/SKILL.md"

It explains how an agent should:

1. Understand the user's video brief.
2. Inspect project capabilities and dependencies.
3. Read the production-plan schema.
4. Select exact registered effect identifiers.
5. Validate production plans.
6. Prepare supported rendering jobs.
7. Execute rendering only when authorized and available.
8. Verify results and report limitations honestly.

Agent instructions

The root "AGENTS.md" provides shared repository instructions and development principles.

Agent discovery behavior can differ between tools and versions. Follow each agent's own skill-discovery conventions.

10. Repository structure

welvox-studio-ai/
│
├── .agents/
│   └── skills/
│       └── welvox-studio-ai/
│           └── SKILL.md
│
├── .claude/
│   └── skills/
│       └── welvox-studio-ai/
│           └── SKILL.md
│
├── .github/
│   └── workflows/
│       └── core-tests.yml
│
├── docs/
│   └── VFX-EFFECT-CATALOG.md
│
├── engine/
│   ├── core/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   └── welvox_core.py
│   │
│   ├── effects/
│   │   ├── effect_stack.py
│   │   └── vfx_engine.py
│   │
│   └── renderer/
│       ├── README.md
│       ├── __init__.py
│       └── ffmpeg_adapter.py
│
├── examples/
│   └── production-plan.example.json
│
├── modules/
│   └── director/
│       └── DIRECTOR.md
│
├── schemas/
│   └── production-plan.schema.json
│
├── skills/
│   └── welvox-studio-ai/
│       ├── SKILL.md
│       └── references/
│           └── director-workflow.md
│
├── tests/
│   ├── README.md
│   ├── test_agent_integrations.py
│   ├── test_core.py
│   ├── test_effect_stack.py
│   ├── test_ffmpeg_integration.py
│   ├── test_renderer.py
│   ├── test_vfx_engine.py
│   └── test_vfx_ffmpeg.py
│   └── test_vfx_render_integration.py
│
├── AGENTS.md
├── LICENSE
└── README.md

11. Requirements

The project uses Python and FFmpeg.

- Python 3.9 or later.
- FFmpeg for actual video rendering.
- FFprobe is useful for media inspection.
- A compatible coding agent for the Agent Skill workflow.

The basic core documentation specifies no third-party Python packages for basic validation.

Actual rendering requires FFmpeg to be installed and accessible in the execution environment.

12. Running the project

Run these commands from the repository root in a compatible Python environment.

Check available capabilities

python engine/core/welvox_core.py capabilities

Validate a production plan

python engine/core/welvox_core.py validate examples/production-plan.example.json

Inspect a production plan

python engine/core/welvox_core.py inspect examples/production-plan.example.json

Prepare an FFmpeg render job

python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json

The default behavior prepares a rendering job without executing FFmpeg.

Execute a render

python engine/renderer/ffmpeg_adapter.py examples/production-plan.example.json --execute

Actual rendering requires valid source media, a supported production plan, and an available FFmpeg executable.

13. Automated testing

The repository includes automated tests for:

- Production-plan validation.
- Required fields and schema versions.
- Output settings.
- Asset references.
- Scene and layer timing.
- Project inspection.
- Capability detection.
- JSON plan loading.
- Effect registration.
- Effect parameter validation.
- Effect-stack construction.
- FFmpeg filter execution.
- Renderer behavior.
- Agent integration instructions.
- Real video rendering integration.

Run the test suite

python -m unittest discover -s tests -v

GitHub Actions

Automated tests are configured in:

".github/workflows/core-tests.yml"

The workflow runs tests when changes are pushed to the main branch or when a pull request targets main.

The V1.0.0 release was published with automated GitHub Actions tests passing, including real FFmpeg effect and rendering tests.

A successful test verifies the tested operation against its test inputs. It does not guarantee that every effect is visually suitable for every source video.

14. Development principles

The project follows these principles:

- Do not advertise unimplemented capabilities.
- Keep creative planning separate from actual rendering.
- Use exact registered operation identifiers.
- Validate production plans before execution.
- Detect dependencies before using them.
- Preserve source media unless destructive changes are explicitly requested.
- Keep engines modular and testable.
- Report unsupported operations and rendering failures honestly.
- Respect software and media licenses.

See "AGENTS.md" for the repository's development instructions.

15. License

Welvox Studio AI is released under the MIT License.

See the ""LICENSE"" (LICENSE) file for the complete license text.

16. Links

- GitHub repository: https://github.com/piyush2707/welvox-studio-ai
- V1.0.0 release: https://github.com/piyush2707/welvox-studio-ai/releases/tag/v1.0.0
- VFX effect catalog: https://github.com/piyush2707/welvox-studio-ai/blob/main/docs/VFX-EFFECT-CATALOG.md
- Agent Skill: https://github.com/piyush2707/welvox-studio-ai/tree/main/skills/welvox-studio-ai
- LinkedIn: https://www.linkedin.com/in/piyush2707

---

Welvox Studio AI V1.0.0

Created by Piyush Joshi.

Built with curiosity, creativity, and code.
