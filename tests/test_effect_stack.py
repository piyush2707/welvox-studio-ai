
"""Tests for multi-effect stack construction."""

import unittest

from engine.effects.effect_stack import build_effect_stack


class EffectStackTests(unittest.TestCase):

    def test_builds_single_effect_stack(self):
        result = build_effect_stack([
            {"operation": "monochrome"}
        ])

        self.assertEqual(result, "hue=s=0")

    def test_builds_multiple_effects_in_order(self):
        result = build_effect_stack([
            {"operation": "monochrome"},
            {"operation": "vignette"},
            {"operation": "film_grain"}
        ])

        parts = result.split(",")

        self.assertIn("hue=s=0", parts[0])
        self.assertIn("vignette=", parts[1])
        self.assertIn("noise=alls=12", parts[2])

    def test_supports_effect_parameters(self):
        result = build_effect_stack([
            {
                "operation": "film_grain",
                "parameters": {"strength": 25}
            }
        ])

        self.assertIn("noise=alls=25", result)

    def test_rejects_non_list(self):
        with self.assertRaises(ValueError):
            build_effect_stack("monochrome")

    def test_rejects_empty_stack(self):
        with self.assertRaises(ValueError):
            build_effect_stack([])

    def test_rejects_non_object_effect(self):
        with self.assertRaises(ValueError):
            build_effect_stack(["monochrome"])

    def test_rejects_missing_operation(self):
        with self.assertRaises(ValueError):
            build_effect_stack([{}])

    def test_rejects_unknown_operation(self):
        with self.assertRaises(ValueError):
            build_effect_stack([
                {"operation": "unknown_effect"}
            ])

    def test_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            build_effect_stack([
                {
                    "operation": "film_grain",
                    "parameters": {"strength": 500}
                }
            ])


if __name__ == "__main__":
    unittest.main()
  
