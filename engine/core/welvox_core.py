
"""Welvox Studio AI - Core Engine.

Standard-library foundation for capability detection,
production-plan validation, and project inspection.

This module does not render video.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


SCHEMA_VERSION = "1.0.0"

LAYER_TYPES = {
    "footage", "image", "text", "effect",
    "transition", "audio", "overlay", "3d"
}

ENGINE_NAMES = {
    "director", "vfx", "motion", "cinema",
    "captions", "audio", "3d", "reels"
}

OUTPUT_FORMATS = {"mp4", "mov", "webm"}


def detect_capabilities():
    """Detect available external media tools."""
    tools = ["ffmpeg", "ffprobe", "blender"]
    detected = {}

    for tool in tools:
        detected[tool] = shutil.which(tool) is not None

    return {
        "python": sys.version.split()[0],
        "tools": detected,
        "video_rendering_available": detected["ffmpeg"],
        "inspection_available": detected["ffprobe"],
        "3d_tool_available": detected["blender"]
    }


def load_plan(file_path):
    """Load a production plan from a JSON file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Production plan not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_plan(plan):
    """Perform built-in structural and timeline checks."""
    errors = []
    warnings = []

    if not isinstance(plan, dict):
        return {
            "valid": False,
            "validation_level": "basic",
            "errors": ["Plan must be a JSON object."],
            "warnings": []
        }

    required = ["schema_version", "project", "output", "timeline"]

    for field in required:
        if field not in plan:
            errors.append(f"Missing required field: {field}")

    if errors:
        return {
            "valid": False,
            "validation_level": "basic",
            "errors": errors,
            "warnings": warnings
        }

    if plan["schema_version"] != SCHEMA_VERSION:
        errors.append(
            f"Unsupported schema version: {plan['schema_version']}"
        )

    project = plan["project"]
    output = plan["output"]
    timeline = plan["timeline"]

    if not isinstance(project, dict):
        errors.append("project must be an object.")
        project = {}

    if not isinstance(output, dict):
        errors.append("output must be an object.")
        output = {}

    if not isinstance(timeline, dict):
        errors.append("timeline must be an object.")
        timeline = {}

    if not isinstance(project.get("title"), str) or not project.get("title"):
        errors.append("project.title must be a non-empty string.")

    if not isinstance(project.get("creative_brief"), str) or not project.get("creative_brief"):
        errors.append("project.creative_brief must be a non-empty string.")

    for field in ["width", "height"]:
        value = output.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            errors.append(f"output.{field} must be a positive integer.")

    fps = output.get("fps")
    if not isinstance(fps, (int, float)) or isinstance(fps, bool) or not 0 < fps <= 240:
        errors.append("output.fps must be greater than 0 and at most 240.")

    if output.get("format") not in OUTPUT_FORMATS:
        errors.append("output.format must be mp4, mov, or webm.")

    duration = timeline.get("duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append("timeline.duration_seconds must be positive.")
        duration = 0

    assets = plan.get("assets", [])
    if not isinstance(assets, list):
        errors.append("assets must be an array.")
        assets = []

    asset_ids = set()

    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("Each asset must be an object.")
            continue

        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id:
            errors.append("Every asset needs a non-empty id.")
        elif asset_id in asset_ids:
            errors.append(f"Duplicate asset id: {asset_id}")
        else:
            asset_ids.add(asset_id)

        if asset.get("type") not in {
            "video", "image", "audio", "font", "model"
        }:
            errors.append(f"Invalid asset type: {asset.get('type')}")

        if not isinstance(asset.get("uri"), str) or not asset.get("uri"):
            errors.append(f"Asset {asset_id} needs a uri.")

    scenes = timeline.get("scenes")
    if not isinstance(scenes, list):
        errors.append("timeline.scenes must be an array.")
        scenes = []

    scene_ids = set()

    for scene in scenes:
        if not isinstance(scene, dict):
            errors.append("Each scene must be an object.")
            continue

        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id:
            errors.append("Every scene needs a non-empty id.")
        elif scene_id in scene_ids:
            errors.append(f"Duplicate scene id: {scene_id}")
        else:
            scene_ids.add(scene_id)

        start = scene.get("start_seconds")
        length = scene.get("duration_seconds")

        if not isinstance(start, (int, float)) or isinstance(start, bool) or start < 0:
            errors.append(f"Scene {scene_id} has an invalid start time.")
            continue

        if not isinstance(length, (int, float)) or isinstance(length, bool) or length <= 0:
            errors.append(f"Scene {scene_id} has an invalid duration.")
            continue

        if start + length > duration:
            errors.append(f"Scene {scene_id} extends beyond the project duration.")

        layers = scene.get("layers")
        if not isinstance(layers, list):
            errors.append(f"Scene {scene_id} layers must be an array.")
            continue

        layer_ids = set()

        for layer in layers:
            if not isinstance(layer, dict):
                errors.append(f"Scene {scene_id} contains a non-object layer.")
                continue

            layer_id = layer.get("id")
            if not isinstance(layer_id, str) or not layer_id:
                errors.append(f"Scene {scene_id} has a layer without an id.")
            elif layer_id in layer_ids:
                errors.append(f"Duplicate layer id in scene {scene_id}: {layer_id}")
            else:
                layer_ids.add(layer_id)

            if layer.get("type") not in LAYER_TYPES:
                errors.append(f"Layer {layer_id} has an invalid type.")

            engine = layer.get("engine")
            if engine is not None and engine not in ENGINE_NAMES:
                errors.append(f"Layer {layer_id} has an invalid engine.")

            asset_id = layer.get("asset_id")
            if asset_id is not None and asset_id not in asset_ids:
                errors.append(
                    f"Layer {layer_id} references unknown asset: {asset_id}"
                )

            layer_start = layer.get("start_seconds")
            layer_length = layer.get("duration_seconds")

            if (
                not isinstance(layer_start, (int, float))
                or isinstance(layer_start, bool)
                or layer_start < start
            ):
                errors.append(f"Layer {layer_id} has an invalid start time.")
                continue

            if (
                not isinstance(layer_length, (int, float))
                or isinstance(layer_length, bool)
                or layer_length <= 0
            ):
                errors.append(f"Layer {layer_id} has an invalid duration.")
                continue

            if layer_start + layer_length > start + length:
                errors.append(f"Layer {layer_id} extends beyond its scene.")

    if not scenes:
        warnings.append("The timeline contains no scenes.")

    return {
        "valid": len(errors) == 0,
        "validation_level": "basic",
        "errors": errors,
        "warnings": warnings
    }


def inspect_plan(plan):
    """Return a concise project summary."""
    timeline = plan.get("timeline", {})
    scenes = timeline.get("scenes", [])

    return {
        "title": plan.get("project", {}).get("title"),
        "duration_seconds": timeline.get("duration_seconds"),
        "scene_count": len(scenes) if isinstance(scenes, list) else 0,
        "asset_count": len(plan.get("assets", [])),
        "output": plan.get("output", {}),
        "status": "planned"
    }


def main():
    parser = argparse.ArgumentParser(
        description="Welvox Studio AI Core Engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("capabilities")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("plan")

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("plan")

    args = parser.parse_args()

    try:
        if args.command == "capabilities":
            result = detect_capabilities()

        elif args.command == "validate":
            result = validate_plan(load_plan(args.plan))

        else:
            result = inspect_plan(load_plan(args.plan))

        print(json.dumps(result, indent=2))
        if args.command == "validate" and not result["valid"]:
            sys.exit(1)

    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, indent=2))
        sys.exit(2)


if __name__ == "__main__":
    main()
                          
