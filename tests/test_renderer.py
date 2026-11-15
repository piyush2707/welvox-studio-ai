"""Tests for the Welvox FFmpeg rendering adapter."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from engine.renderer.ffmpeg_adapter import prepare_render_job


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PLAN = ROOT / "examples" / "production-plan.example.json"


class RendererAdapterTests(unittest.TestCase):

    def setUp(self):
        with EXAMPLE_PLAN.open("r", encoding="utf-8") as file:
            self.plan = json.load(file)

        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        source = self.root / "assets" / "source.mp4"
        source.parent.mkdir(parents=True)
        source.write_bytes(b"test video placeholder")

        overlay_source = self.root / "assets" / "overlay.mp4"
        overlay_source.write_bytes(b"overlay video placeholder")

        self.plan["assets"] = [
            {
                "id": "main-footage",
                "type": "video",
                "uri": "assets/source.mp4"
            },
            {
                "id": "overlay-footage",
                "type": "video",
                "uri": "assets/overlay.mp4"
            }
        ]

        scene = self.plan["timeline"]["scenes"][0]
        scene["layers"] = [
            {
                "id": "footage-only",
                "type": "footage",
                "asset_id": "main-footage",
                "start_seconds": 0,
                "duration_seconds": 8
            }
        ]

    def tearDown(self):
        self.temp.cleanup()

    def add_overlay(self):
        self.plan["timeline"]["scenes"][0]["layers"].append({
            "id": "picture-in-picture",
            "type": "overlay",
            "asset_id": "overlay-footage",
            "start_seconds": 2,
            "duration_seconds": 3,
            "parameters": {
                "x": 20,
                "y": 30,
                "width": 120,
                "height": 90
            }
        })

    def test_simple_project_prepares_dry_run(self):
        job = prepare_render_job(
            self.plan, self.root, "output/preview.mp4"
        )

        self.assertTrue(job["ready"])
        self.assertEqual(job["status"], "prepared")
        self.assertFalse(job["execution_performed"])
        self.assertIn("ffmpeg", job["command"])

    def test_cinematic_grade_is_added_to_command(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "cinematic_grade"

        job = prepare_render_job(
            self.plan, self.root, "output/cinematic.mp4"
        )

        self.assertTrue(job["ready"])
        self.assertEqual(job["vfx_operation"], "cinematic_grade")

        filters = job["command"][job["command"].index("-vf") + 1]
        self.assertIn("colorbalance=", filters)
        self.assertIn("vignette=", filters)

    def test_tech_neon_grade_is_added_to_command(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "tech_neon_grade"

        job = prepare_render_job(
            self.plan, self.root, "output/neon.mp4"
        )

        self.assertTrue(job["ready"])
        filters = job["command"][job["command"].index("-vf") + 1]
        self.assertIn("saturation=1.45", filters)

    def test_custom_vignette_is_added_to_command(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "vignette"
        layer["parameters"] = {"angle": 0.8}

        job = prepare_render_job(
            self.plan, self.root, "output/vignette.mp4"
        )

        self.assertTrue(job["ready"])
        filters = job["command"][job["command"].index("-vf") + 1]
        self.assertIn("vignette=", filters)

    def test_unknown_vfx_operation_is_rejected(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "unknown_effect"

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_non_vfx_engine_operation_is_rejected(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "motion"
        layer["operation"] = "unknown_motion"

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_invalid_vignette_parameters_are_rejected(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "vignette"
        layer["parameters"] = {"angle": 5}

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_multi_effect_stack_is_added_to_command(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["effects"] = [
            {"operation": "cinematic_grade"},
            {"operation": "vignette"},
            {"operation": "tech_neon_grade"}
        ]

        job = prepare_render_job(
            self.plan, self.root, "output/effect-stack.mp4"
        )

        self.assertTrue(job["ready"], msg=str(job))
        self.assertEqual(job["status"], "prepared")
        self.assertEqual(
            job["vfx_effects"],
            [
                "cinematic_grade",
                "vignette",
                "tech_neon_grade"
            ]
        )

        filters = job["command"][job["command"].index("-vf") + 1]

        self.assertIn("colorbalance=", filters)
        self.assertIn("vignette=", filters)
        self.assertIn("saturation=1.45", filters)

    def test_multi_effect_stack_preserves_effect_order(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["effects"] = [
            {"operation": "vignette"},
            {"operation": "cinematic_grade"}
        ]

        job = prepare_render_job(
            self.plan, self.root, "output/ordered-stack.mp4"
        )

        self.assertTrue(job["ready"], msg=str(job))

        filters = job["command"][job["command"].index("-vf") + 1]

        self.assertLess(
            filters.index("vignette="),
            filters.index("colorbalance=")
        )

    def test_unknown_effect_in_stack_is_rejected(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["effects"] = [
            {"operation": "cinematic_grade"},
            {"operation": "unknown_effect"}
        ]

        job = prepare_render_job(
            self.plan, self.root, "output/invalid-stack.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_stack_rejects_simultaneous_single_operation(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "vfx"
        layer["operation"] = "vignette"
        layer["effects"] = [
            {"operation": "cinematic_grade"}
        ]

        job = prepare_render_job(
            self.plan, self.root, "output/invalid-stack.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_plan")

    def test_stack_rejects_non_vfx_engine(self):
        layer = self.plan["timeline"]["scenes"][0]["layers"][0]
        layer["engine"] = "motion"
        layer["effects"] = [
            {"operation": "vignette"}
        ]

        job = prepare_render_job(
            self.plan, self.root, "output/invalid-stack.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_plan")

    def test_missing_source_is_rejected(self):
        self.plan["assets"][0]["uri"] = "assets/missing.mp4"

        job = prepare_render_job(
            self.plan, self.root, "output/preview.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "missing_asset")

    def test_multiple_layers_are_not_supported(self):
        self.plan["timeline"]["scenes"][0]["layers"].append({
            "id": "extra-title",
            "type": "text",
            "start_seconds": 1,
            "duration_seconds": 2
        })

        job = prepare_render_job(
            self.plan, self.root, "output/preview.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_prepares_picture_in_picture_command(self):
        self.add_overlay()

        job = prepare_render_job(
            self.plan, self.root, "output/picture-in-picture.mp4"
        )

        self.assertTrue(job["ready"], msg=str(job))
        self.assertEqual(job["status"], "prepared")
        self.assertEqual(
            job["overlay"],
            {
                "x": 20,
                "y": 30,
                "width": 120,
                "height": 90,
                "start_seconds": 2,
                "duration_seconds": 3
            }
        )

        command = job["command"]
        self.assertIn("-filter_complex", command)

        filter_complex = command[
            command.index("-filter_complex") + 1
        ]

        self.assertIn("[vout]", filter_complex)
        self.assertIn("overlay=x=20:y=30", filter_complex)
        self.assertIn("between(t,2,5)", filter_complex)

    def test_overlay_rejects_negative_position(self):
        self.add_overlay()
        overlay = self.plan["timeline"]["scenes"][0]["layers"][1]
        overlay["parameters"]["x"] = -1

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_rejects_size_outside_output(self):
        self.add_overlay()
        overlay = self.plan["timeline"]["scenes"][0]["layers"][1]
        overlay["parameters"]["width"] = 9999

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_rejects_non_integer_dimensions(self):
        self.add_overlay()
        overlay = self.plan["timeline"]["scenes"][0]["layers"][1]
        overlay["parameters"]["width"] = 120.5

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_rejects_boolean_dimensions(self):
        self.add_overlay()
        overlay = self.plan["timeline"]["scenes"][0]["layers"][1]
        overlay["parameters"]["width"] = True

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_rejects_duration_past_timeline(self):
        self.add_overlay()
        overlay = self.plan["timeline"]["scenes"][0]["layers"][1]
        overlay["start_seconds"] = 7
        overlay["duration_seconds"] = 2

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_plan")

    def test_overlay_rejects_missing_video_asset(self):
        self.add_overlay()
        self.plan["assets"][1]["uri"] = "assets/missing-overlay.mp4"

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "missing_asset")

    def test_overlay_rejects_same_source_as_primary(self):
        self.add_overlay()
        self.plan["assets"][1]["uri"] = "assets/source.mp4"

        job = prepare_render_job(
            self.plan, self.root, "output/invalid.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_overlay_cannot_overwrite_overlay_source(self):
        self.add_overlay()

        job = prepare_render_job(
            self.plan, self.root, "assets/overlay.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_output")

    def test_invalid_plan_is_rejected(self):
        plan = copy.deepcopy(self.plan)
        del plan["output"]

        job = prepare_render_job(
            plan, self.root, "output/preview.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_plan")

    def test_path_escape_is_rejected(self):
        self.plan["assets"][0]["uri"] = "../outside.mp4"

        with self.assertRaises(ValueError):
            prepare_render_job(
                self.plan, self.root, "output/preview.mp4"
            )

    def test_output_cannot_overwrite_source(self):
        job = prepare_render_job(
            self.plan, self.root, "assets/source.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_output")


if __name__ == "__main__":
    unittest.main()
