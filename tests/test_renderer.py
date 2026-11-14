
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

        self.plan["assets"][0]["uri"] = "assets/source.mp4"

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

    def test_simple_project_prepares_dry_run(self):
        job = prepare_render_job(
            self.plan,
            self.root,
            "output/preview.mp4"
        )

        self.assertTrue(job["ready"])
        self.assertEqual(job["status"], "prepared")
        self.assertFalse(job["execution_performed"])
        self.assertIn("ffmpeg", job["command"])

    def test_missing_source_is_rejected(self):
        self.plan["assets"][0]["uri"] = "assets/missing.mp4"

        job = prepare_render_job(
            self.plan,
            self.root,
            "output/preview.mp4"
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
            self.plan,
            self.root,
            "output/preview.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "unsupported_project")

    def test_invalid_plan_is_rejected(self):
        plan = copy.deepcopy(self.plan)
        del plan["output"]

        job = prepare_render_job(
            plan,
            self.root,
            "output/preview.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_plan")

    def test_path_escape_is_rejected(self):
        self.plan["assets"][0]["uri"] = "../outside.mp4"

        with self.assertRaises(ValueError):
            prepare_render_job(
                self.plan,
                self.root,
                "output/preview.mp4"
            )

    def test_output_cannot_overwrite_source(self):
        job = prepare_render_job(
            self.plan,
            self.root,
            "assets/source.mp4"
        )

        self.assertFalse(job["ready"])
        self.assertEqual(job["status"], "invalid_output")


if __name__ == "__main__":
    unittest.main()
  
