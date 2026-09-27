from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_project_agent import ProjectTools, ToolError


MINIMUM_FILES = [
    {"path": "README.md", "content": "# Demo\n"},
    {"path": "pyproject.toml", "content": "[project]\nname='demo'\n"},
    {"path": "AGENTS.md", "content": "# Reglas\n"},
    {"path": "src/demo/__init__.py", "content": ""},
    {"path": "tests/test_demo.py", "content": "import unittest\n"},
]


class ProjectToolsTest(unittest.TestCase):
    def test_rejects_traversal_and_sensitive_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tools = ProjectTools(Path(temporary_directory))
            with self.assertRaises(ToolError):
                tools.create_project(
                    "demo", MINIMUM_FILES + [{"path": "../escape.py", "content": ""}]
                )
            with self.assertRaises(ToolError):
                tools.create_project(
                    "demo", MINIMUM_FILES + [{"path": ".env", "content": "secret"}]
                )

    def test_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tools = ProjectTools(Path(temporary_directory))
            tools.create_project("demo", MINIMUM_FILES)
            with self.assertRaisesRegex(ToolError, "no se sobrescribirá"):
                tools.create_project("demo", MINIMUM_FILES)

    def test_test_execution_requires_explicit_permission(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tools = ProjectTools(Path(temporary_directory))
            tools.create_project("demo", MINIMUM_FILES)
            result = tools.run_tests("demo")
            self.assertTrue(result["blocked"])
            self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
