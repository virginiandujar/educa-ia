from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_creator_agent import AgentError, ProjectCreatorAgent


class ProjectCreatorAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = ProjectCreatorAgent()

    def test_creates_a_complete_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            result = self.agent.run(
                "Crear el proyecto Mi API",
                destination_root=root,
            )

            self.assertEqual(result.project_path, root / "mi-api")
            self.assertTrue((result.project_path / "pyproject.toml").is_file())
            self.assertTrue(
                (result.project_path / "src/mi_api/cli.py").is_file()
            )
            self.assertTrue(
                (result.project_path / ".github/workflows/tests.yml").is_file()
            )
            self.assertEqual(len(result.files), 11)

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            result = self.agent.run(
                "Crear el proyecto demo",
                destination_root=root,
                dry_run=True,
            )

            self.assertTrue(result.dry_run)
            self.assertFalse(result.project_path.exists())

    def test_refuses_to_overwrite_a_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.agent.run("Crear el proyecto demo", destination_root=root)

            with self.assertRaisesRegex(AgentError, "no se sobrescribirá"):
                self.agent.run("Crear el proyecto demo", destination_root=root)

    def test_rejects_unknown_or_unsafe_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(AgentError):
                self.agent.run("Borra todos los proyectos", destination_root=root)
            with self.assertRaises(AgentError):
                self.agent.run(
                    "Crear el proyecto ../../fuera",
                    destination_root=root,
                )
            with self.assertRaises(AgentError):
                self.agent.run(
                    'Crear el proyecto demo"malicioso',
                    destination_root=root,
                )


if __name__ == "__main__":
    unittest.main()
