"""End-to-end MP4 rendering test for VFX effect stacks."""

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


@unittest.skipUnless(
    shutil.which("ffmpeg") and shutil.which("ffprobe"),
    "FFmpeg and ffprobe are required."
)
class VFXRenderIntegrationTests(unittest.TestCase):

    def test_renders_mp4_with_ordered_effect_stack(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "assets"
            output_dir = root / "output"

            assets.mkdir()
            output_dir.mkdir()

            source = assets / "source.mp4"
            output = output_dir / "effect-stack.mp4"

            generated = subprocess.run(
                [
                    shutil.which("ffmpeg"),
                    "-y",
                    "-f", "lavfi",
                    "-i", "testsrc2=size=320x240:rate=24:duration=1",
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    str(source),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                generated.returncode,
                0,
                msg=generated.stderr[-3000:],
            )

            plan = {
                "schema_version": "1.0.0",
                "project": {
                    "title": "VFX Stack Integration",
                    "creative_brief": "Verify ordered video effects.",
                },
                "output": {
                    "width": 320,
                    "height": 240,
                    "fps": 24,
                    "format": "mp4",
                },
                "assets": [
                    {
                        "id": "main-footage",
                        "type": "video",
                        "uri": "assets/source.mp4",
                    }
                ],
                "timeline": {
                    "duration_seconds": 1,
                    "scenes": [
                        {
                            "id": "scene-1",
                            "start_seconds": 0,
                            "duration_seconds": 1,
                            "layers": [
                                {
                                    "id": "main-layer",
                                    "type": "footage",
                                    "asset_id": "main-footage",
                                    "engine": "vfx",
                                    "start_seconds": 0,
                                    "duration_seconds": 1,
                                    "effects": [
                                        {"operation": "monochrome"},
                                        {"operation": "vignette"},
                                        {
                                            "operation": "film_grain",
                                            "parameters": {
                                                "strength": 20
                                            },
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                },
            }

            job = prepare_render_job(
                plan,
                root,
                "output/effect-stack.mp4",
            )

            self.assertTrue(job["ready"], msg=json.dumps(job))

            self.assertEqual(
                job["vfx_effects"],
                ["monochrome", "vignette", "film_grain"],
            )

            result = execute_render_job(job)

            self.assertTrue(
                result["success"],
                msg=json.dumps(result),
            )

            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)

            inspected = subprocess.run(
                [
                    shutil.which("ffprobe"),
                    "-v", "error",
                    "-show_entries", "stream=codec_type,width,height",
                    "-of", "json",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                inspected.returncode,
                0,
                msg=inspected.stderr,
            )

            metadata = json.loads(inspected.stdout)
            videos = [
                stream
                for stream in metadata.get("streams", [])
                if stream.get("codec_type") == "video"
            ]

            self.assertTrue(videos)
            self.assertEqual(videos[0]["width"], 320)
            self.assertEqual(videos[0]["height"], 240)


if __name__ == "__main__":
    unittest.main()
