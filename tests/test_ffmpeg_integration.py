
"""Integration tests for real FFmpeg rendering."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from engine.renderer.ffmpeg_adapter import (
    execute_render_job,
    prepare_render_job,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PLAN = ROOT / "examples" / "production-plan.example.json"


@unittest.skipUnless(
    shutil.which("ffmpeg") and shutil.which("ffprobe"),
    "FFmpeg and ffprobe are required."
)
class FFmpegRenderIntegrationTests(unittest.TestCase):

    def create_source_and_plan(self, root):
        (root / "assets").mkdir()
        (root / "output").mkdir()

        source = root / "assets" / "source.mp4"

        generated = subprocess.run(
            [
                shutil.which("ffmpeg"),
                "-y",
                "-f", "lavfi",
                "-i", "color=c=0x24334a:s=320x240:r=24:d=1",
                "-f", "lavfi",
                "-i", "sine=frequency=440:duration=1",
                "-shortest",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                str(source),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            generated.returncode, 0,
            msg=generated.stderr[-3000:]
        )

        with EXAMPLE_PLAN.open("r", encoding="utf-8") as file:
            plan = json.load(file)

        plan["output"].update({
            "width": 320,
            "height": 240,
            "fps": 24,
            "format": "mp4",
        })
        plan["assets"][0]["uri"] = "assets/source.mp4"
        plan["timeline"]["duration_seconds"] = 1

        scene = plan["timeline"]["scenes"][0]
        scene["start_seconds"] = 0
        scene["duration_seconds"] = 1
        scene["layers"] = [{
            "id": "integration-footage",
            "type": "footage",
            "asset_id": "main-footage",
            "start_seconds": 0,
            "duration_seconds": 1,
        }]

        return plan

    def assert_valid_mp4(self, output):
        self.assertTrue(output.is_file())
        self.assertGreater(output.stat().st_size, 0)

        inspected = subprocess.run(
            [
                shutil.which("ffprobe"),
                "-v", "error",
                "-show_entries",
                "format=duration:stream=codec_type,codec_name,width,height",
                "-of", "json",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            inspected.returncode, 0,
            msg=inspected.stderr[-3000:]
        )

        metadata = json.loads(inspected.stdout)
        videos = [
            stream for stream in metadata.get("streams", [])
            if stream.get("codec_type") == "video"
        ]

        self.assertTrue(videos, msg=metadata)
        self.assertEqual(videos[0]["codec_name"], "h264")
        self.assertEqual(videos[0]["width"], 320)
        self.assertEqual(videos[0]["height"], 240)

    def test_renders_and_inspects_a_real_mp4(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self.create_source_and_plan(root)

            output = root / "output" / "rendered.mp4"

            job = prepare_render_job(
                plan, root, "output/rendered.mp4"
            )
            self.assertTrue(job["ready"], msg=str(job))

            result = execute_render_job(job)
            self.assertTrue(result["success"], msg=str(result))

            self.assert_valid_mp4(output)

    def test_renders_real_mp4_with_cinematic_vfx(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self.create_source_and_plan(root)

            layer = plan["timeline"]["scenes"][0]["layers"][0]
            layer["engine"] = "vfx"
            layer["operation"] = "cinematic_grade"

            output = root / "output" / "cinematic.mp4"

            job = prepare_render_job(
                plan, root, "output/cinematic.mp4"
            )
            self.assertTrue(job["ready"], msg=str(job))
            self.assertEqual(
                job["vfx_operation"], "cinematic_grade"
            )

            result = execute_render_job(job)
            self.assertTrue(result["success"], msg=str(result))

            self.assert_valid_mp4(output)

    def test_renders_real_mp4_with_film_grain(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self.create_source_and_plan(root)

            layer = plan["timeline"]["scenes"][0]["layers"][0]
            layer["engine"] = "vfx"
            layer["operation"] = "film_grain"
            layer["parameters"] = {"strength": 18}

            output = root / "output" / "film-grain.mp4"

            job = prepare_render_job(
                plan, root, "output/film-grain.mp4"
            )
            self.assertTrue(job["ready"], msg=str(job))
            self.assertEqual(
                job["vfx_operation"], "film_grain"
            )

            result = execute_render_job(job)
            self.assertTrue(result["success"], msg=str(result))

            self.assert_valid_mp4(output)

    def test_renders_real_mp4_with_tech_neon_vfx(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self.create_source_and_plan(root)

            layer = plan["timeline"]["scenes"][0]["layers"][0]
            layer["engine"] = "vfx"
            layer["operation"] = "tech_neon_grade"

            output = root / "output" / "tech-neon.mp4"

            job = prepare_render_job(
                plan, root, "output/tech-neon.mp4"
            )
            self.assertTrue(job["ready"], msg=str(job))
            self.assertEqual(
                job["vfx_operation"], "tech_neon_grade"
            )

            result = execute_render_job(job)
            self.assertTrue(result["success"], msg=str(result))

            self.assert_valid_mp4(output)

    def test_renders_real_mp4_with_custom_vignette(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = self.create_source_and_plan(root)

            layer = plan["timeline"]["scenes"][0]["layers"][0]
            layer["engine"] = "vfx"
            layer["operation"] = "vignette"
            layer["parameters"] = {"angle": 0.65}

            output = root / "output" / "vignette.mp4"

            job = prepare_render_job(
                plan, root, "output/vignette.mp4"
            )
            self.assertTrue(job["ready"], msg=str(job))
            self.assertEqual(
                job["vfx_operation"], "vignette"
            )

            result = execute_render_job(job)
            self.assertTrue(result["success"], msg=str(result))

            self.assert_valid_mp4(output)


if __name__ == "__main__":
    unittest.main()
    
