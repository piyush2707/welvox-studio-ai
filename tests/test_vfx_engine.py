
"""Tests for the Welvox VFX Engine."""

import unittest

from engine.effects.vfx_engine import build_vfx_filters


class VFXEngineTests(unittest.TestCase):

    def test_cinematic_grade(self):
        result = build_vfx_filters("cinematic_grade")
        self.assertIn("eq=", result)
        self.assertIn("colorbalance=", result)
        self.assertIn("vignette=", result)

    def test_tech_neon_grade(self):
        result = build_vfx_filters("tech_neon_grade")
        self.assertIn("saturation=1.45", result)
        self.assertIn("colorbalance=", result)

    def test_vignette_default(self):
        result = build_vfx_filters("vignette")
        self.assertIn("vignette=", result)

    def test_vignette_custom_angle(self):
        result = build_vfx_filters(
            "vignette",
            {"angle": 0.8}
        )
        self.assertIn("vignette=", result)

    def test_invalid_vignette_angle(self):
        with self.assertRaises(ValueError):
            build_vfx_filters(
                "vignette",
                {"angle": 5}
            )

    def test_film_grain_default(self):
        result = build_vfx_filters("film_grain")
        self.assertEqual(result, "noise=alls=12:allf=t")

    def test_film_grain_custom_strength(self):
        result = build_vfx_filters(
            "film_grain",
            {"strength": 18}
        )
        self.assertEqual(result, "noise=alls=18:allf=t")

    def test_film_grain_minimum_strength(self):
        result = build_vfx_filters(
            "film_grain",
            {"strength": 1}
        )
        self.assertEqual(result, "noise=alls=1:allf=t")

    def test_film_grain_maximum_strength(self):
        result = build_vfx_filters(
            "film_grain",
            {"strength": 100}
        )
        self.assertEqual(result, "noise=alls=100:allf=t")

    def test_invalid_film_grain_strength(self):
        invalid_values = [0, 101, -5, "18", True, 2.5]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    build_vfx_filters(
                        "film_grain",
                        {"strength": value}
                    )

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            build_vfx_filters("unknown_effect")

    def test_invalid_parameters_type(self):
        with self.assertRaises(ValueError):
            build_vfx_filters("cinematic_grade", "invalid")


if __name__ == "__main__":
    unittest.main()
    
