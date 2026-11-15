"""Tests for Claude Code, Codex, and Gemini skill integrations."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKILL_FILES = [
    ROOT / ".agents" / "skills" / "welvox-studio-ai" / "SKILL.md",
    ROOT / ".claude" / "skills" / "welvox-studio-ai" / "SKILL.md",
    ROOT / "skills" / "welvox-studio-ai" / "SKILL.md",
]


class AgentIntegrationTests(unittest.TestCase):

    def test_all_agent_skill_files_exist(self):
        for path in SKILL_FILES:
            with self.subTest(path=str(path)):
                self.assertTrue(
                    path.is_file(),
                    f"Missing agent skill: {path}"
                )

    def test_all_skills_have_valid_frontmatter(self):
        for path in SKILL_FILES:
            with self.subTest(path=str(path)):
                content = path.read_text(encoding="utf-8")

                self.assertTrue(content.startswith("---\n"))
                self.assertIn("\nname: welvox-studio-ai\n", content)
                self.assertIn("\ndescription:", content)
                self.assertIn("\n---\n", content)

    def test_agent_skills_document_renderer_limits(self):
        for path in SKILL_FILES[:2]:
            with self.subTest(path=str(path)):
                content = path.read_text(encoding="utf-8").lower()

                self.assertIn("one scene", content)
                self.assertIn("picture-in-picture", content)
                self.assertIn("effect stack", content)
                self.assertIn("never", content)

    def test_agent_skills_reference_real_project_files(self):
        required_files = [
            "AGENTS.md",
            "schemas/production-plan.schema.json",
            "engine/effects/vfx_engine.py",
            "engine/effects/effect_stack.py",
            "engine/renderer/ffmpeg_adapter.py",
        ]

        for relative_path in required_files:
            with self.subTest(file=relative_path):
                self.assertTrue(
                    (ROOT / relative_path).is_file(),
                    f"Missing project file: {relative_path}"
                )


if __name__ == "__main__":
    unittest.main()
