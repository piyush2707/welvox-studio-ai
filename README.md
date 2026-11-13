
# Welvox Studio AI

**The Intelligent Video Production System**

Welvox Studio AI is an ambitious, modular AI video-production ecosystem designed to help creators turn natural-language ideas into structured, directed video projects.

It is being developed for compatible AI coding agents and extensible rendering environments.

## Vision

Describe the video you imagine. Welvox Studio AI should help turn that brief into a production plan, select suitable creative techniques, organize a timeline, and coordinate available rendering tools.

## Planned capabilities

- **AI Director** — interprets creative briefs and builds production plans.
- **VFX Engine** — visual effects, compositing, tracking, and particles.
- **Motion Engine** — animated typography, transitions, and motion graphics.
- **Cinema Engine** — cinematic looks, grading workflows, and camera effects.
- **Caption Engine** — subtitle timing, styling, and emphasis.
- **Audio Engine** — sound effects, synchronization, and mixing workflows.
- **3D Engine** — 3D-style elements and optional advanced 3D workflows.
- **Reels Engine** — vertical video, Shorts, and social-first editing.

These are development goals, not claims that every engine is already implemented.

## Architecture

The project is designed around:

1. A portable Agent Skill.
2. A shared, structured production-plan format.
3. Modular creative engines.
4. Rendering adapters for supported environments.
5. Agent-specific integration instructions.
6. A mobile-friendly project website.

## Important execution boundary

The website can be hosted with GitHub Pages. Actual video processing requires a compatible rendering environment, such as a cloud worker or a supported local runtime. GitHub Pages does not render videos.

The project will detect available capabilities and explain missing dependencies instead of claiming an unavailable render succeeded.

## Development status

**Current stage:** Foundation

The first milestone is to establish the skill, architecture, production-plan contract, and compatibility strategy before implementing rendering features.

## Repository structure

- `skills/` — portable Agent Skill and supporting references.
- `docs/` — architecture, setup, and development documentation.
- `schemas/` — structured production-plan contracts.
- `adapters/` — agent and rendering integrations.
- `website/` — GitHub Pages website.

Only implemented components will be added. No empty placeholder modules.

## Compatibility

The project targets Claude Code, Codex, Gemini CLI, and other compatible agents. Each integration will be documented and tested separately.

## License

MIT. See `LICENSE`.
