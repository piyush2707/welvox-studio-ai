
# Instructions for AI Agents

You are contributing to Welvox Studio AI.

## Project objective

Build a reliable, modular AI video-production ecosystem that converts creative briefs into structured production plans and, when supported rendering tools are available, playable video output.

## Core principles

1. Never claim a feature works unless it has been implemented and tested.
2. Separate creative planning from actual media rendering.
3. Use a shared production-plan format across engines and agents.
4. Detect dependencies and runtime capabilities before using them.
5. Provide clear fallbacks and actionable errors.
6. Preserve source media unless the user explicitly requests destructive changes.
7. Respect licenses for code, fonts, models, footage, and other assets.
8. Prefer a small number of reliable features over a large collection of untested effects.

## Architecture rules

- Keep the AI Director separate from rendering implementations.
- Keep engines modular and independently testable.
- Define interfaces before connecting modules.
- Keep agent-specific instructions in adapters.
- Do not assume every agent supports the same skill discovery mechanism.
- Do not assume GitHub Pages can execute rendering workloads.

## Video-production rules

Before rendering:

1. Understand the user's brief.
2. Identify source media and output requirements.
3. Check available tools and dependencies.
4. Build a structured production plan.
5. Validate timing, dimensions, layers, and asset references.
6. Execute only supported operations.
7. Inspect output when preview or frame inspection is available.
8. Report failures honestly.

## Development workflow

- Explain the purpose of each new file.
- Avoid empty directories and placeholder implementations.
- Keep documentation aligned with actual behavior.
- Include tests for implemented functionality.
- Do not introduce unnecessary dependencies.
- Keep mobile editing and GitHub-based contribution in mind.

## Release discipline

A release must be based on verified functionality, documented limitations, and passing tests—not on the number of advertised modules.
