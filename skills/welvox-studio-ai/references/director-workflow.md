
# Director Workflow

This reference defines how the Welvox Studio AI Skill should coordinate the AI Director.

## When to activate

Activate the Director workflow when a user asks to:

- Create a video from an idea.
- Turn footage into a cinematic edit.
- Plan a social media video.
- Add visual effects or motion graphics.
- Improve an existing video-production plan.
- Coordinate multiple video-production engines.

## Interaction principles

The Director should not overwhelm users with a long questionnaire.

Ask for essential missing information one question at a time.

Use these defaults when the user has not specified otherwise:

- General social video: vertical 1080 × 1920.
- General landscape video: 1920 × 1080.
- Frame rate: 30 FPS.
- Container: MP4.
- Preserve original audio.
- Use standard quality for initial previews.

These are defaults, not universal requirements. Follow explicit user instructions instead.

## Creative brief template

Internally organize the brief into:

- Concept
- Subject
- Audience
- Platform
- Duration
- Aspect ratio
- Visual style
- Pacing
- Effects
- Typography
- Captions
- Audio
- Export requirements

Do not require the user to fill out every field.

## Production sequence

1. Interpret the brief.
2. Identify accessible assets.
3. Check available capabilities.
4. Design scenes and layers.
5. Assign specialist engines.
6. Generate the production plan.
7. Validate the plan against the schema.
8. Hand the plan to an available renderer.
9. Inspect the resulting output when supported.
10. Report the actual result.

## Status vocabulary

Use these terms precisely:

- **Planned:** a production plan exists.
- **Validated:** the plan passed available structural checks.
- **Ready:** required assets and execution capabilities are available.
- **Rendering:** an execution process has actually started.
- **Rendered:** an execution adapter confirmed output creation.
- **Reviewed:** output checks were actually performed.

Never use these statuses interchangeably.

## User-facing response

Keep creative explanations concise and useful.

Explain important creative decisions without exposing unnecessary internal implementation details.

If rendering is unavailable, provide the validated plan and explain what environment or dependency is needed to execute it.
