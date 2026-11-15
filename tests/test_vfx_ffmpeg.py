"""Real FFmpeg smoke tests for Welvox VFX effects and effect stacks."""

import shutil
import subprocess
import unittest

from engine.effects.vfx_engine import (
    available_effects,
    build_vfx_filters,
)
from engine.effects.effect_stack import build_effect_stack


class VFXFFmpegTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ffmpeg = shutil.which("ffmpeg")

    def test_ffmpeg_is_available(self):
        self.assertIsNotNone(
            self.ffmpeg,
            "FFmpeg must be installed to run render tests."
        )

    def run_filter(self, filter_chain):
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

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

    def test_every_effect_renders(self):
        if not self.ffmpeg:
            self.skipTest("FFmpeg is not installed.")

        failures = []

        for effect in available_effects():
            with self.subTest(effect=effect):
                filter_chain = build_vfx_filters(effect)
                result = self.run_filter(filter_chain)

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

    def test_multi_effect_stack_renders(self):
        if not self.ffmpeg:
            self.skipTest("FFmpeg is not installed.")

        filter_chain = build_effect_stack([
            {"operation": "monochrome"},
            {"operation": "vignette"},
            {"operation": "film_grain"}
        ])

        result = self.run_filter(filter_chain)

        self.assertEqual(
            result.returncode,
            0,
            "Multi-effect stack failed FFmpeg rendering:\n"
            + result.stderr
        )

    def test_parameterized_effect_stack_renders(self):
        if not self.ffmpeg:
            self.skipTest("FFmpeg is not installed.")

        filter_chain = build_effect_stack([
            {
                "operation": "film_grain",
                "parameters": {"strength": 25}
            },
            {
                "operation": "vignette",
                "parameters": {"angle": 0.8}
            }
        ])

        result = self.run_filter(filter_chain)

        self.assertEqual(
            result.returncode,
            0,
            "Parameterized effect stack failed:\n"
            + result.stderr
        )


if __name__ == "__main__":
    unittest.main()
