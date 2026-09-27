from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from ai_project_agent import AIProjectAgent, ProjectTools


def function_call(name: str, call_id: str, arguments: dict) -> SimpleNamespace:
    return SimpleNamespace(
        type="function_call",
        name=name,
        call_id=call_id,
        arguments=json.dumps(arguments),
    )


class FakeResponse:
    def __init__(self, output: list, output_text: str = "") -> None:
        self.output = output
        self.output_text = output_text


class FakeResponsesAPI:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.pending = list(responses)
        self.requests: list[dict] = []

    def create(self, **request):
        self.requests.append(request)
        return self.pending.pop(0)


class FakeClient:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = FakeResponsesAPI(responses)


class AIProjectAgentTest(unittest.TestCase):
    def test_model_plans_creates_tests_and_reports(self) -> None:
        files = [
            {"path": "README.md", "content": "# Demo\n"},
            {
                "path": "pyproject.toml",
                "content": '[project]\nname = "demo"\nversion = "0.1.0"\n',
            },
            {"path": "AGENTS.md", "content": "# Reglas\n"},
            {"path": "src/demo/__init__.py", "content": ""},
            {
                "path": "src/demo/cli.py",
                "content": "def answer():\n    return 42\n",
            },
            {
                "path": "tests/test_cli.py",
                "content": (
                    "import unittest\n"
                    "from demo.cli import answer\n\n"
                    "class DemoTest(unittest.TestCase):\n"
                    "    def test_answer(self):\n"
                    "        self.assertEqual(answer(), 42)\n"
                ),
            },
        ]
        responses = [
            FakeResponse(
                [
                    function_call(
                        "record_plan",
                        "plan-1",
                        {
                            "project_name": "Demo",
                            "summary": "CLI pequeña con una prueba.",
                            "files": [file["path"] for file in files],
                            "test_strategy": "Ejecutar unittest.",
                        },
                    )
                ]
            ),
            FakeResponse(
                [
                    function_call(
                        "create_project",
                        "create-1",
                        {"project_name": "Demo", "files": files},
                    )
                ]
            ),
            FakeResponse(
                [
                    function_call(
                        "run_tests",
                        "test-1",
                        {"project_name": "Demo"},
                    )
                ]
            ),
            FakeResponse([], "Proyecto creado y verificado: una prueba superada."),
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            tools = ProjectTools(
                Path(temporary_directory), allow_test_execution=True
            )
            client = FakeClient(responses)
            result = AIProjectAgent(
                client=client,
                model="modelo-de-prueba",
                project_tools=tools,
            ).run("Crea una pequeña aplicación llamada Demo")

            self.assertEqual(
                [event.name for event in result.events],
                ["record_plan", "create_project", "run_tests"],
            )
            self.assertTrue(result.events[-1].result["ok"])
            self.assertTrue(
                (Path(temporary_directory) / "demo/src/demo/cli.py").is_file()
            )
            self.assertIn("verificado", result.message)
            self.assertEqual(len(client.responses.requests), 4)


if __name__ == "__main__":
    unittest.main()
