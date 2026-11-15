
"""Real FFmpeg smoke tests for all Welvox VFX effects."""

import shutil
import subprocess
import unittest

from engine.effects.vfx_engine import (
    available_effects,
    build_vfx_filters,
)


class VFXFFmpegTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ffmpeg = shutil.which("ffmpeg")

    def test_ffmpeg_is_available(self):
        self.assertIsNotNone(
            self.ffmpeg,
            "FFmpeg must be installed to run render tests."
        )

    def test_every_effect_renders(self):
        if not self.ffmpeg:
            self.skipTest("FFmpeg is not installed.")

        failures = []

        for effect in available_effects():
            with self.subTest(effect=effect):
                filter_chain = build_vfx_filters(effect)

                command = [
                    self.ffmpeg,
                    "-hide_banner",
                    "-loglevel", "error",
                    "-f", "lavfi",
                    "-i",
                    "testsrc2=size=160x120:rate=10:duration=1.2",
                    "-vf", filter_chain,
                    "-an",
                    "-frames:v", "5",
                    "-f", "null",
                    "-"
                ]

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    failures.append(
                        f"{effect}: {result.stderr.strip()}"
                    )

        self.assertEqual(
            failures,
            [],
            "Some effects failed real FFmpeg rendering:\n"
            + "\n".join(failures)
        )


if __name__ == "__main__":
    unittest.main()
