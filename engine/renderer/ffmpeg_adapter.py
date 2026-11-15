
"""Welvox Studio AI - FFmpeg Rendering Adapter.

Supports one scene with:
- One primary footage layer.
- One VFX operation or an ordered VFX effect stack.
- Optional one-video picture-in-picture overlay.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from engine.core.welvox_core import load_plan, validate_plan
from engine.effects.vfx_engine import build_vfx_filters
from engine.effects.effect_stack import build_effect_stack


def resolve_inside_root(root, value):
    """Resolve a project path without allowing directory escape."""
    root = Path(root).resolve()
    candidate = (root / value).resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError(f"Path is outside project root: {value}")

    return candidate


def unsupported(message):
    """Return a consistent unsupported-project result."""
    return {
        "ready": False,
        "status": "unsupported_project",
        "errors": [message]
    }


def prepare_render_job(plan, project_root, output_path):
    """Prepare an FFmpeg command for a supported project."""
    validation = validate_plan(plan)

    if not validation["valid"]:
        return {
            "ready": False,
            "status": "invalid_plan",
            "errors": validation["errors"]
        }

    root = Path(project_root).resolve()
    output = resolve_inside_root(root, output_path)

    timeline = plan["timeline"]
    scenes = timeline["scenes"]

    if len(scenes) != 1:
        return unsupported(
            "Initial adapter supports exactly one scene."
        )

    scene = scenes[0]

    if scene["start_seconds"] != 0:
        return unsupported(
            "The first scene must start at zero."
        )

    if scene["duration_seconds"] != timeline["duration_seconds"]:
        return unsupported(
            "Scene duration must match project duration."
        )

    layers = scene["layers"]

    if len(layers) not in (1, 2):
        return unsupported(
            "Adapter supports one footage layer and "
            "optionally one video overlay."
        )

    footage_layers = [
        layer for layer in layers
        if layer["type"] == "footage"
    ]

    overlay_layers = [
        layer for layer in layers
        if layer["type"] == "overlay"
    ]

    if (
        len(footage_layers) != 1
        or len(overlay_layers) > 1
        or len(footage_layers) + len(overlay_layers) != len(layers)
    ):
        return unsupported(
            "Project requires exactly one footage layer "
            "and at most one video overlay. Other layer "
            "types are not supported."
        )

    footage = footage_layers[0]
    overlay = overlay_layers[0] if overlay_layers else None

    if footage["start_seconds"] != 0:
        return unsupported(
            "Primary footage must start at zero."
        )

    if footage["duration_seconds"] != timeline["duration_seconds"]:
        return unsupported(
            "Primary footage duration must match project duration."
        )

    engine = footage.get("engine")
    operation = footage.get("operation")
    parameters = footage.get("parameters", {})
    effects = footage.get("effects")

    vfx_filters = ""

    if effects is not None:
        if engine not in (None, "vfx"):
            return unsupported(
                "Effect stacks require the VFX engine."
            )

        if operation:
            return unsupported(
                "Use either operation or effects, not both."
            )

        try:
            vfx_filters = build_effect_stack(effects)
        except ValueError as error:
            return unsupported(str(error))

    elif engine or operation:
        if engine != "vfx" or not operation:
            return unsupported(
                "Only a VFX engine operation is supported "
                "on the primary footage layer."
            )

        try:
            vfx_filters = build_vfx_filters(
                operation,
                parameters
            )
        except ValueError as error:
            return unsupported(str(error))

    assets = {
        asset["id"]: asset
        for asset in plan.get("assets", [])
    }

    footage_asset = assets.get(footage.get("asset_id"))

    if not footage_asset or footage_asset["type"] != "video":
        return unsupported(
            "Primary footage must reference a video asset."
        )

    source = resolve_inside_root(root, footage_asset["uri"])

    if not source.is_file():
        return {
            "ready": False,
            "status": "missing_asset",
            "errors": [
                f"Source video does not exist: {footage_asset['uri']}"
            ]
        }

    settings = plan["output"]
    width = settings["width"]
    height = settings["height"]

    filters = (
        f"scale={width}:{height}:"
        "force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:"
        "(ow-iw)/2:(oh-ih)/2"
    )

    if vfx_filters:
        filters += "," + vfx_filters

    command = [
        "ffmpeg",
        "-y",
        "-i", str(source),
    ]

    overlay_source = None
    overlay_settings = None

    if overlay:
        if overlay.get("engine") or overlay.get("operation"):
            return unsupported(
                "VFX operations on overlay layers "
                "are not supported yet."
            )

        if overlay.get("effects") is not None:
            return unsupported(
                "VFX effect stacks on overlay layers "
                "are not supported yet."
            )

        overlay_asset = assets.get(overlay.get("asset_id"))

        if (
            not overlay_asset
            or overlay_asset["type"] != "video"
        ):
            return unsupported(
                "Overlay layer must reference a video asset."
            )

        overlay_source = resolve_inside_root(
            root, overlay_asset["uri"]
        )

        if not overlay_source.is_file():
            return {
                "ready": False,
                "status": "missing_asset",
                "errors": [
                    "Overlay video does not exist: "
                    + overlay_asset["uri"]
                ]
            }

        if overlay_source == source:
            return unsupported(
                "Primary footage and overlay must use "
                "different source files."
            )

        overlay_parameters = overlay.get("parameters", {})

        if not isinstance(overlay_parameters, dict):
            return unsupported(
                "Overlay parameters must be an object."
            )

        x = overlay_parameters.get("x")
        y = overlay_parameters.get("y")
        overlay_width = overlay_parameters.get("width")
        overlay_height = overlay_parameters.get("height")

        for name, value in (
            ("x", x),
            ("y", y),
            ("width", overlay_width),
            ("height", overlay_height),
        ):
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
            ):
                return unsupported(
                    f"Overlay {name} must be an integer."
                )

        if x < 0 or y < 0:
            return unsupported(
                "Overlay x and y must not be negative."
            )

        if overlay_width <= 0 or overlay_height <= 0:
            return unsupported(
                "Overlay width and height must be positive."
            )

        if x + overlay_width > width:
            return unsupported(
                "Overlay exceeds the output width."
            )

        if y + overlay_height > height:
            return unsupported(
                "Overlay exceeds the output height."
            )

        overlay_start = overlay["start_seconds"]
        overlay_duration = overlay["duration_seconds"]
        overlay_end = overlay_start + overlay_duration

        if overlay_end > timeline["duration_seconds"]:
            return unsupported(
                "Overlay extends beyond project duration."
            )

        overlay_settings = {
            "x": x,
            "y": y,
            "width": overlay_width,
            "height": overlay_height,
            "start_seconds": overlay_start,
            "duration_seconds": overlay_duration,
        }

        command.extend(["-i", str(overlay_source)])

        filter_complex = (
            f"[0:v]{filters}[base];"
            f"[1:v]scale={overlay_width}:{overlay_height}"
            "[overlay];"
            f"[base][overlay]overlay="
            f"x={x}:y={y}:"
            f"enable='between(t,{overlay_start},{overlay_end})'"
            "[vout]"
        )

        command.extend([
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "0:a?",
        ])

    else:
        command.extend([
            "-vf", filters,
        ])

    if output == source or (
        overlay_source is not None and output == overlay_source
    ):
        return {
            "ready": False,
            "status": "invalid_output",
            "errors": [
                "Output path cannot overwrite a source video."
            ]
        }

    command.extend([
        "-t", str(timeline["duration_seconds"]),
        "-r", str(settings["fps"]),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(output)
    ])

    return {
        "ready": True,
        "status": "prepared",
        "renderer": "ffmpeg",
        "source": str(source),
        "overlay_source": (
            str(overlay_source) if overlay_source else None
        ),
        "overlay": overlay_settings,
        "output": str(output),
        "duration_seconds": timeline["duration_seconds"],
        "vfx_operation": operation if vfx_filters else None,
        "vfx_effects": (
            [item["operation"] for item in effects]
            if isinstance(effects, list)
            else ([operation] if vfx_filters else [])
        ),
        "command": command,
        "execution_performed": False
    }


def execute_render_job(job):
    """Execute a prepared job only when FFmpeg is available."""
    if not job.get("ready"):
        return {
            "success": False,
            "status": "not_ready",
            "errors": job.get("errors", [])
        }

    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        return {
            "success": False,
            "status": "missing_dependency",
            "errors": ["FFmpeg executable was not found."]
        }

    command = list(job["command"])
    command[0] = ffmpeg_path

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
    except OSError as error:
        return {
            "success": False,
            "status": "execution_error",
            "errors": [str(error)]
        }

    output = Path(job["output"])

    if result.returncode != 0 or not output.is_file():
        return {
            "success": False,
            "status": "render_failed",
            "return_code": result.returncode,
            "errors": [result.stderr[-4000:]]
        }

    return {
        "success": True,
        "status": "rendered",
        "output": str(output),
        "execution_performed": True
    }


def main():
    parser = argparse.ArgumentParser(
        description="Welvox FFmpeg Adapter"
    )
    parser.add_argument(
        "plan",
        help="Path to production-plan JSON"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Root directory for project assets and output"
    )
    parser.add_argument(
        "--output",
        default="output/welvox-render.mp4",
        help="Output path relative to project root"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually run FFmpeg. Default behavior is dry-run."
    )

    args = parser.parse_args()

    try:
        plan = load_plan(args.plan)
        job = prepare_render_job(
            plan,
            args.project_root,
            args.output
        )

        if args.execute and job.get("ready"):
            result = execute_render_job(job)
        else:
            result = job

        print(json.dumps(result, indent=2))

        if not result.get("ready", result.get("success", False)):
            sys.exit(1)

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, indent=2))
        sys.exit(2)


if __name__ == "__main__":
    main()
            
