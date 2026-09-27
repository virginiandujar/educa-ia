"""Herramientas locales, deterministas y limitadas del agente."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any


class ToolError(ValueError):
    """Una herramienta rechazó una operación no válida o insegura."""


class ProjectTools:
    MAX_FILES = 30
    MAX_FILE_BYTES = 100_000
    MAX_TOTAL_BYTES = 500_000
    BLOCKED_NAMES = {".env", "credentials.json", "secrets.json"}
    BLOCKED_SUFFIXES = {".key", ".pem", ".p12"}

    def __init__(self, workspace: Path, *, allow_test_execution: bool = False):
        self.workspace = workspace
        self.allow_test_execution = allow_test_execution

    @property
    def definitions(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": "record_plan",
                "description": "Registra el plan antes de crear el proyecto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "summary": {"type": "string"},
                        "files": {"type": "array", "items": {"type": "string"}},
                        "test_strategy": {"type": "string"},
                    },
                    "required": [
                        "project_name",
                        "summary",
                        "files",
                        "test_strategy",
                    ],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "create_project",
                "description": (
                    "Crea atómicamente un proyecto nuevo. Nunca sobrescribe uno existente."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "files": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "content": {"type": "string"},
                                },
                                "required": ["path", "content"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["project_name", "files"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "read_file",
                "description": "Lee un archivo de texto dentro del proyecto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "path": {"type": "string"},
                    },
                    "required": ["project_name", "path"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "write_file",
                "description": "Crea o corrige un archivo dentro del proyecto existente.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["project_name", "path", "content"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "run_tests",
                "description": (
                    "Ejecuta únicamente unittest dentro del proyecto. Puede estar bloqueada."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"project_name": {"type": "string"}},
                    "required": ["project_name"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        ]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        handlers = {
            "record_plan": self.record_plan,
            "create_project": self.create_project,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_tests": self.run_tests,
        }
        if name not in handlers:
            raise ToolError(f"herramienta desconocida: {name}")
        return handlers[name](**arguments)

    def record_plan(
        self,
        project_name: str,
        summary: str,
        files: list[str],
        test_strategy: str,
    ) -> dict[str, Any]:
        slug = self._project_slug(project_name)
        if not files or len(files) > self.MAX_FILES:
            raise ToolError("el plan debe contener entre 1 y 30 archivos")
        for path in files:
            self._safe_relative_path(path)
        return {
            "ok": True,
            "project": slug,
            "summary": summary,
            "files": files,
            "test_strategy": test_strategy,
        }

    def create_project(
        self, project_name: str, files: list[dict[str, str]]
    ) -> dict[str, Any]:
        slug = self._project_slug(project_name)
        if not files or len(files) > self.MAX_FILES:
            raise ToolError("se requieren entre 1 y 30 archivos")

        normalized_files: list[tuple[PurePosixPath, str]] = []
        seen_paths: set[PurePosixPath] = set()
        total_bytes = 0
        for file in files:
            path = self._safe_relative_path(file["path"])
            content = file["content"]
            size = len(content.encode("utf-8"))
            if size > self.MAX_FILE_BYTES:
                raise ToolError(f"archivo demasiado grande: {path}")
            if path in seen_paths:
                raise ToolError(f"ruta duplicada: {path}")
            seen_paths.add(path)
            total_bytes += size
            normalized_files.append((path, content))

        if total_bytes > self.MAX_TOTAL_BYTES:
            raise ToolError("el proyecto supera el tamaño máximo permitido")
        self._validate_minimum_structure(seen_paths)

        self.workspace.mkdir(parents=True, exist_ok=True)
        project_path = self.workspace / slug
        if project_path.exists():
            raise ToolError(f"el proyecto ya existe y no se sobrescribirá: {slug}")

        with tempfile.TemporaryDirectory(
            prefix=f".{slug}-", dir=self.workspace
        ) as temporary_directory:
            staged_project = Path(temporary_directory) / slug
            for relative_path, content in normalized_files:
                target = staged_project.joinpath(*relative_path.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            staged_project.replace(project_path)

        return {
            "ok": True,
            "project": slug,
            "path": str(project_path),
            "files_created": [str(path) for path, _ in normalized_files],
        }

    def read_file(self, project_name: str, path: str) -> dict[str, Any]:
        project_path = self._existing_project(project_name)
        relative_path = self._safe_relative_path(path)
        target = self._contained_target(project_path, relative_path)
        if not target.is_file():
            raise ToolError(f"el archivo no existe: {relative_path}")
        content = target.read_text(encoding="utf-8")
        return {"ok": True, "path": str(relative_path), "content": content}

    def write_file(
        self, project_name: str, path: str, content: str
    ) -> dict[str, Any]:
        project_path = self._existing_project(project_name)
        relative_path = self._safe_relative_path(path)
        if len(content.encode("utf-8")) > self.MAX_FILE_BYTES:
            raise ToolError("el contenido supera el tamaño máximo permitido")
        target = self._contained_target(project_path, relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"ok": True, "path": str(relative_path)}

    def run_tests(self, project_name: str) -> dict[str, Any]:
        project_path = self._existing_project(project_name)
        if not self.allow_test_execution:
            return {
                "ok": False,
                "blocked": True,
                "reason": (
                    "La ejecución de código generado requiere --allow-test-execution."
                ),
            }

        environment = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": str(project_path / "src"),
            "PYTHONUNBUFFERED": "1",
        }
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests",
                    "-v",
                ],
                cwd=project_path,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "timed_out": True, "output": "Tiempo agotado."}

        output = (completed.stdout + completed.stderr)[-8_000:]
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "output": output,
        }

    def _project_slug(self, project_name: str) -> str:
        if not project_name.strip() or len(project_name) > 80:
            raise ToolError("nombre de proyecto no válido")
        ascii_name = (
            unicodedata.normalize("NFKD", project_name)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
        if not slug:
            raise ToolError("el nombre debe contener alguna letra o número")
        return slug

    def _safe_relative_path(self, raw_path: str) -> PurePosixPath:
        if not raw_path or "\\" in raw_path:
            raise ToolError("ruta de archivo no válida")
        path = PurePosixPath(raw_path)
        if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
            raise ToolError(f"la ruta debe ser relativa y segura: {raw_path}")
        if (
            path.name.lower() in self.BLOCKED_NAMES
            or path.suffix.lower() in self.BLOCKED_SUFFIXES
        ):
            raise ToolError(f"no se permiten archivos sensibles: {raw_path}")
        return path

    def _existing_project(self, project_name: str) -> Path:
        project_path = self.workspace / self._project_slug(project_name)
        if not project_path.is_dir():
            raise ToolError(f"el proyecto no existe: {project_path.name}")
        return project_path

    def _contained_target(
        self, project_path: Path, relative_path: PurePosixPath
    ) -> Path:
        project_root = project_path.resolve()
        target = project_path.joinpath(*relative_path.parts)
        resolved_target = target.resolve()
        if project_root != resolved_target and project_root not in resolved_target.parents:
            raise ToolError("la ruta sale del proyecto")
        return target

    def _validate_minimum_structure(self, paths: set[PurePosixPath]) -> None:
        required = {
            PurePosixPath("README.md"),
            PurePosixPath("pyproject.toml"),
            PurePosixPath("AGENTS.md"),
        }
        missing = required - paths
        has_source = any(
            len(path.parts) >= 3 and path.parts[0] == "src" and path.suffix == ".py"
            for path in paths
        )
        has_test = any(
            path.parts[0] == "tests"
            and path.name.startswith("test_")
            and path.suffix == ".py"
            for path in paths
        )
        if missing or not has_source or not has_test:
            details = [str(path) for path in sorted(missing)]
            if not has_source:
                details.append("src/<paquete>/*.py")
            if not has_test:
                details.append("tests/test_*.py")
            raise ToolError("faltan elementos obligatorios: " + ", ".join(details))
