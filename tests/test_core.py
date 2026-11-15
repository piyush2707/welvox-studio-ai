"""Automated tests for the Welvox Studio AI Core Engine."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from engine.core.welvox_core import (
    detect_capabilities,
    inspect_plan,
    load_plan,
    validate_plan,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PLAN = ROOT / "examples" / "production-plan.example.json"


class WelvoxCoreTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with EXAMPLE_PLAN.open("r", encoding="utf-8") as file:
            cls.example = json.load(file)

    def make_plan(self):
        return copy.deepcopy(self.example)

    def make_effect_stack_plan(self):
        plan = self.make_plan()
        layer = plan["timeline"]["scenes"][0]["layers"][0]

        layer["engine"] = "vfx"
        layer.pop("operation", None)
        layer["effects"] = [
            {"operation": "brightness"},
            {
                "operation": "contrast",
                "parameters": {"amount": 1.2}
            }
        ]

        return plan

    def test_example_plan_is_valid(self):
        result = validate_plan(self.make_plan())
        self.assertTrue(result["valid"], result["errors"])

    def test_missing_required_field_is_invalid(self):
        plan = self.make_plan()
        del plan["timeline"]

        result = validate_plan(plan)

        self.assertFalse(result["valid"])
        self.assertTrue(
            any("timeline" in error for error in result["errors"])
        )

    def test_wrong_schema_version_is_invalid(self):
        plan = self.make_plan()
        plan["schema_version"] = "9.0.0"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_invalid_output_width_is_rejected(self):
        plan = self.make_plan()
        plan["output"]["width"] = 0

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_invalid_output_format_is_rejected(self):
        plan = self.make_plan()
        plan["output"]["format"] = "unknown"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_unknown_asset_reference_is_rejected(self):
        plan = self.make_plan()
        layer = plan["timeline"]["scenes"][0]["layers"][0]
        layer["asset_id"] = "missing-asset"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])
        self.assertTrue(
            any("unknown asset" in error for error in result["errors"])
        )

    def test_scene_cannot_exceed_project_duration(self):
        plan = self.make_plan()
        plan["timeline"]["scenes"][0]["duration_seconds"] = 20

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_layer_cannot_exceed_scene_duration(self):
        plan = self.make_plan()
        layer = plan["timeline"]["scenes"][0]["layers"][0]
        layer["duration_seconds"] = 20

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_invalid_non_object_plan_is_rejected(self):
        result = validate_plan(["not", "a", "plan"])

        self.assertFalse(result["valid"])

    def test_inspection_returns_project_summary(self):
        summary = inspect_plan(self.make_plan())

        self.assertEqual(summary["title"], "Midnight Vision")
        self.assertEqual(summary["scene_count"], 1)
        self.assertEqual(summary["asset_count"], 1)
        self.assertEqual(summary["status"], "planned")

    def test_capability_report_has_expected_fields(self):
        result = detect_capabilities()

        self.assertIn("python", result)
        self.assertIn("tools", result)
        self.assertIn("ffmpeg", result["tools"])
        self.assertIn("ffprobe", result["tools"])
        self.assertIn("blender", result["tools"])

    def test_load_plan_reads_json_file(self):
        plan = self.make_plan()

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            encoding="utf-8",
            delete=False
        ) as file:
            json.dump(plan, file)
            temp_path = file.name

        try:
            loaded = load_plan(temp_path)
            self.assertEqual(
                loaded["project"]["title"],
                "Midnight Vision"
            )
        finally:
            Path(temp_path).unlink(missing_ok=True)

    # Effect stack validation tests

    def test_valid_effect_stack_is_accepted(self):
        plan = self.make_effect_stack_plan()

        result = validate_plan(plan)

        self.assertTrue(result["valid"], result["errors"])

    def test_empty_effect_stack_is_rejected(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = []

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_non_list_effect_stack_is_rejected(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = "brightness"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_effect_item_must_be_an_object(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = [
            "brightness"
        ]

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_effect_requires_operation(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = [
            {"parameters": {"amount": 1.2}}
        ]

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_empty_effect_operation_is_rejected(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = [
            {"operation": " "}
        ]

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_effect_parameters_must_be_an_object(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["effects"] = [
            {
                "operation": "brightness",
                "parameters": "invalid"
            }
        ]

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_operation_and_effect_stack_cannot_coexist(self):
        plan = self.make_effect_stack_plan()
        layer = plan["timeline"]["scenes"][0]["layers"][0]
        layer["operation"] = "brightness"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_effect_stack_requires_vfx_engine(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0]["engine"] = "motion"

        result = validate_plan(plan)

        self.assertFalse(result["valid"])

    def test_effect_stack_rejects_missing_engine(self):
        plan = self.make_effect_stack_plan()
        plan["timeline"]["scenes"][0]["layers"][0].pop("engine")

        result = validate_plan(plan)

        self.assertFalse(result["valid"])


if __name__ == "__main__":
    unittest.main()
