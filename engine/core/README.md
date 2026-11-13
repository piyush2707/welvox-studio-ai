# Welvox Core Engine

The Core Engine provides the initial executable foundation for Welvox Studio AI.

## Current capabilities

- Detect FFmpeg, FFprobe, and Blender availability.
- Load production plans from JSON files.
- Perform basic production-plan validation.
- Check asset references.
- Check scene and layer timing.
- Inspect project metadata.

## Requirements

- Python 3.9 or later.
- No third-party packages required for basic validation.

## Commands

Run these commands from the repository root in a compatible Python environment.

### Detect available tools

```bash
python engine/core/welvox_core.py capabilities
```

### Validate a production plan

```bash
python engine/core/welvox_core.py validate examples/production-plan.example.json
```

### Inspect a production plan

```bash
python engine/core/welvox_core.py inspect examples/production-plan.example.json
```

## Validation limitations

The current validator performs built-in structural and timeline checks. It is not yet a complete JSON Schema validator.

A future integration can use a JSON Schema validation library to enforce the complete schema.

## Rendering limitations

This version does not render, encode, or modify video files.

Detecting FFmpeg only indicates that the executable is available. It does not confirm that a particular rendering operation will succeed.

## Development roadmap

- Full JSON Schema validation.
- Asset accessibility checks.
- Rendering adapter interface.
- Execution-job tracking.
- Output verification.
- Automated tests.
- 
