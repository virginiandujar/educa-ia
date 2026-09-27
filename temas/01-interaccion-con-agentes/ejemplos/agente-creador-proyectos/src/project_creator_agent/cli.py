"""Interfaz de terminal del agente."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import AgentError, ProjectCreatorAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crea una estructura Python a partir de 'Crear el proyecto NOMBRE'."
    )
    parser.add_argument(
        "instruction",
        nargs="+",
        help="Instrucción, por ejemplo: Crear el proyecto inventario-api",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("proyectos-generados"),
        help="Directorio contenedor (por defecto: proyectos-generados).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra el plan sin crear archivos.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    instruction = " ".join(args.instruction)

    try:
        result = ProjectCreatorAgent().run(
            instruction,
            destination_root=args.output,
            dry_run=args.dry_run,
        )
    except AgentError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    action = "Plan preparado" if result.dry_run else "Proyecto creado"
    print(f"{action}: {result.project_path}")
    print("Archivos:")
    for file_path in result.files:
        print(f"  - {file_path}")
    return 0
