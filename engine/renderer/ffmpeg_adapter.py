
"""Welvox Studio AI - FFmpeg Rendering Adapter.

Initial adapter for preparing and optionally executing
simple single-clip video render jobs.

Complex multi-layer projects are not supported yet.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from engine.core.welvox_core import load_plan, validate_plan


def resolve_inside_root(root, value):
    """Resolve a project path without allowing directory escape."""
    root = Path(root).resolve()
    candidate = (root / value).resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError(f"Path is outside project root: {value}")

    return candidate


def prepare_render_job(plan, project_root, output_path):
    """Prepare an FFmpeg command for a supported simple project."""
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
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["Initial adapter supports exactly one scene."]
        }

    scene = scenes[0]

    if scene["start_seconds"] != 0:
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["The first scene must start at zero."]
        }

    if scene["duration_seconds"] != timeline["duration_seconds"]:
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["Scene duration must match project duration."]
        }

    layers = scene["layers"]

    if len(layers) != 1:
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": [
                "Initial adapter supports exactly one layer. "
                "Effects, titles, overlays, and separate audio layers "
                "are not implemented yet."
            ]
        }

    layer = layers[0]

    if layer["type"] != "footage":
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["The only supported layer type is footage."]
        }

    if layer.get("engine") or layer.get("operation"):
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["Engine operations are not supported by this adapter yet."]
        }

    if layer["start_seconds"] != 0:
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["The footage layer must start at zero."]
        }

    if layer["duration_seconds"] != timeline["duration_seconds"]:
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["Footage duration must match project duration."]
        }

    asset_id = layer.get("asset_id")
    assets = {
        asset["id"]: asset
        for asset in plan.get("assets", [])
    }

    asset = assets.get(asset_id)

    if not asset or asset["type"] != "video":
        return {
            "ready": False,
            "status": "unsupported_project",
            "errors": ["Footage layer must reference a video asset."]
        }

    source = resolve_inside_root(root, asset["uri"])

    if not source.is_file():
        return {
            "ready": False,
            "status": "missing_asset",
            "errors": [f"Source video does not exist: {asset['uri']}"]
        }

    if source == output:
        return {
            "ready": False,
            "status": "invalid_output",
            "errors": ["Output path cannot overwrite the source video."]
        }

    settings = plan["output"]

    command = [
        "ffmpeg",
        "-y",
        "-i", str(source),
        "-t", str(timeline["duration_seconds"]),
        "-vf",
        (
            f"scale={settings['width']}:{settings['height']}:"
            "force_original_aspect_ratio=decrease,"
            f"pad={settings['width']}:{settings['height']}:"
            "(ow-iw)/2:(oh-ih)/2"
        ),
        "-r", str(settings["fps"]),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(output)
    ]

    return {
        "ready": True,
        "status": "prepared",
        "renderer": "ffmpeg",
        "source": str(source),
        "output": str(output),
        "duration_seconds": timeline["duration_seconds"],
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
    parser.add_argument("plan", help="Path to production-plan JSON")
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
      
