"""Agente determinista que planifica y crea un proyecto Python estándar."""

from __future__ import annotations

import re
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


class AgentError(ValueError):
    """Error comprensible y recuperable producido por el agente."""


@dataclass(frozen=True)
class ProjectSpec:
    display_name: str
    slug: str
    package_name: str


@dataclass(frozen=True)
class AgentResult:
    project_path: Path
    files: tuple[Path, ...]
    dry_run: bool


class ProjectCreatorAgent:
    """Convierte una instrucción acotada en un proyecto verificable."""

    instruction_pattern = re.compile(
        r"^\s*crear\s+el\s+proyecto\s+(.+?)\s*$",
        flags=re.IGNORECASE,
    )

    def run(
        self,
        instruction: str,
        *,
        destination_root: Path,
        dry_run: bool = False,
    ) -> AgentResult:
        spec = self._understand(instruction)
        plan = self._plan(spec)
        project_path = destination_root / spec.slug

        if dry_run:
            return AgentResult(project_path, tuple(plan), dry_run=True)

        destination_root.mkdir(parents=True, exist_ok=True)
        if project_path.exists():
            raise AgentError(
                f"el destino ya existe y no se sobrescribirá: {project_path}"
            )

        # Se prepara todo en un directorio temporal y solo se mueve al final.
        # Así no queda un proyecto a medias si una escritura falla.
        with tempfile.TemporaryDirectory(
            prefix=f".{spec.slug}-", dir=destination_root
        ) as temporary_directory:
            staged_project = Path(temporary_directory) / spec.slug
            for relative_path, content in plan.items():
                target = staged_project / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            staged_project.replace(project_path)

        return AgentResult(project_path, tuple(plan), dry_run=False)

    def _understand(self, instruction: str) -> ProjectSpec:
        match = self.instruction_pattern.fullmatch(instruction)
        if not match:
            raise AgentError(
                "instrucción no reconocida; usa: Crear el proyecto NOMBRE"
            )

        display_name = match.group(1).strip()
        if display_name[:1] in {'"', "'"} and display_name[-1:] == display_name[:1]:
            display_name = display_name[1:-1].strip()

        if (
            len(display_name) > 80
            or not display_name
            or ".." in display_name
            or "/" in display_name
            or "\\" in display_name
            or not re.fullmatch(r"[\w .-]+", display_name)
        ):
            raise AgentError("el nombre del proyecto no es válido")

        ascii_name = (
            unicodedata.normalize("NFKD", display_name)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
        if not slug:
            raise AgentError("el nombre debe contener alguna letra o número")

        package_name = slug.replace("-", "_")
        if package_name[0].isdigit():
            package_name = f"project_{package_name}"

        return ProjectSpec(display_name, slug, package_name)

    def _plan(self, spec: ProjectSpec) -> dict[Path, str]:
        package = spec.package_name
        project = spec.display_name
        slug = spec.slug

        return {
            Path("README.md"): dedent(
                f"""\
                # {project}

                Proyecto Python generado con una estructura mínima, comprobable y preparada para crecer.

                ## Puesta en marcha

                ```bash
                python -m venv .venv
                source .venv/bin/activate
                python -m pip install -e .
                python -m {package}
                ```

                En Windows, activa el entorno con `.venv\\Scripts\\activate`.

                ## Verificación

                ```bash
                python -m unittest discover -s tests
                ```

                ## Estructura

                - `src/{package}/`: código de la aplicación.
                - `tests/`: pruebas automáticas.
                - `docs/`: decisiones y documentación técnica.
                - `AGENTS.md`: contrato de trabajo para agentes de desarrollo.
                - `.github/workflows/tests.yml`: verificación continua.
                """
            ),
            Path("pyproject.toml"): dedent(
                f"""\
                [build-system]
                requires = ["setuptools>=68"]
                build-backend = "setuptools.build_meta"

                [project]
                name = "{slug}"
                version = "0.1.0"
                description = "Proyecto Python {project}"
                readme = "README.md"
                requires-python = ">=3.11"
                dependencies = []

                [project.scripts]
                {slug} = "{package}.cli:main"

                [tool.setuptools.packages.find]
                where = ["src"]
                """
            ),
            Path(".gitignore"): dedent(
                """\
                .venv/
                __pycache__/
                *.py[cod]
                .coverage
                .pytest_cache/
                .mypy_cache/
                .ruff_cache/
                build/
                dist/
                *.egg-info/
                .env
                """
            ),
            Path("AGENTS.md"): dedent(
                f"""\
                # Contrato para agentes

                ## Objetivo

                Mantener y evolucionar `{project}` sin romper su interfaz pública.

                ## Reglas

                - Trabajar únicamente dentro de este repositorio.
                - No añadir dependencias sin explicar la necesidad.
                - No introducir credenciales ni datos sensibles.
                - Mantener compatibilidad con Python 3.11 o posterior.
                - Añadir o actualizar pruebas para cada cambio de comportamiento.
                - Detenerse y pedir contexto si el requisito admite varias interpretaciones.

                ## Verificación obligatoria

                ```bash
                python -m unittest discover -s tests
                ```

                ## Entrega

                Resumir los cambios, las pruebas ejecutadas, los riesgos y las dudas pendientes.
                """
            ),
            Path("docs/architecture.md"): dedent(
                f"""\
                # Arquitectura

                `{project}` comienza como un paquete Python pequeño con arquitectura `src`.
                Las decisiones nuevas deben documentarse aquí antes de añadir complejidad.
                """
            ),
            Path(f"src/{package}/__init__.py"): dedent(
                f'''\
                """Paquete principal de {project}."""

                __version__ = "0.1.0"
                '''
            ),
            Path(f"src/{package}/__main__.py"): dedent(
                """\
                from .cli import main

                raise SystemExit(main())
                """
            ),
            Path(f"src/{package}/cli.py"): dedent(
                f'''\
                """Punto de entrada de la aplicación."""


                def main() -> int:
                    print("{project} está listo.")
                    return 0
                '''
            ),
            Path("tests/__init__.py"): "",
            Path("tests/test_smoke.py"): dedent(
                f"""\
                import unittest

                from {package}.cli import main


                class SmokeTest(unittest.TestCase):
                    def test_main_finishes_successfully(self) -> None:
                        self.assertEqual(main(), 0)


                if __name__ == "__main__":
                    unittest.main()
                """
            ),
            Path(".github/workflows/tests.yml"): dedent(
                """\
                name: Pruebas

                on:
                  push:
                  pull_request:

                jobs:
                  test:
                    runs-on: ubuntu-latest
                    steps:
                      - uses: actions/checkout@v4
                      - uses: actions/setup-python@v5
                        with:
                          python-version: "3.11"
                      - run: python -m pip install -e .
                      - run: python -m unittest discover -s tests
                """
            ),
        }
