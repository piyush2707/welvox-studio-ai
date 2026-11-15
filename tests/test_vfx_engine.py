
"""Automated tests for the Welvox VFX engine."""

import unittest

from engine.effects.vfx_engine import (
    available_effects,
    build_vfx_filters,
)


class VFXEngineTests(unittest.TestCase):

    def test_effect_catalog_has_at_least_50_effects(self):
        effects = available_effects()
        self.assertGreaterEqual(len(effects), 50)

    def test_effect_names_are_unique(self):
        effects = available_effects()
        self.assertEqual(len(effects), len(set(effects)))

    def test_every_effect_has_a_filter_or_parameter_handler(self):
        for effect in available_effects():
            with self.subTest(effect=effect):
                result = build_vfx_filters(effect)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    def test_existing_cinematic_grade(self):
        result = build_vfx_filters("cinematic_grade")
        self.assertIn("colorbalance", result)
        self.assertIn("vignette", result)

    def test_existing_tech_neon_grade(self):
        result = build_vfx_filters("tech_neon_grade")
        self.assertIn("saturation=1.45", result)

    def test_vignette_default(self):
        result = build_vfx_filters("vignette")
        self.assertIn("vignette=", result)

    def test_vignette_custom_angle(self):
        result = build_vfx_filters(
            "vignette",
            {"angle": 0.8}
        )
        self.assertIn("vignette=", result)

    def test_vignette_rejects_invalid_angle(self):
        for angle in (0, 2, -1, True, "wide", float("nan")):
            with self.subTest(angle=angle):
                with self.assertRaises(ValueError):
                    build_vfx_filters(
                        "vignette",
                        {"angle": angle}
                    )

    def test_film_grain_default(self):
        result = build_vfx_filters("film_grain")
        self.assertIn("noise=alls=12", result)

    def test_film_grain_custom_strength(self):
        result = build_vfx_filters(
            "film_grain",
            {"strength": 30}
        )
        self.assertIn("noise=alls=30", result)

    def test_film_grain_rejects_invalid_strength(self):
        for strength in (0, 101, -5, 2.5, True, "strong"):
            with self.subTest(strength=strength):
                with self.assertRaises(ValueError):
                    build_vfx_filters(
                        "film_grain",
                        {"strength": strength}
                    )

    def test_unknown_effect_is_rejected(self):
        with self.assertRaises(ValueError):
            build_vfx_filters("not_a_real_effect")

    def test_parameters_must_be_an_object(self):
        with self.assertRaises(ValueError):
            build_vfx_filters("cinematic_grade", "invalid")

    def test_unexpected_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            build_vfx_filters(
                "cinematic_grade",
                {"raw_filter": "some text"}
            )

    def test_expected_visual_effect_categories_exist(self):
        effects = available_effects()

        expected = {
            "monochrome",
            "sepia",
            "rgb_glitch",
            "pixelate",
            "gaussian_blur",
            "edge_detect",
            "fisheye",
            "scanlines",
            "letterbox",
            "golden_hour",
            "noir",
            "sharpen",
        }

        self.assertTrue(expected.issubset(set(effects)))


if __name__ == "__main__":
    unittest.main()
    
