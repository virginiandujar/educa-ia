"""Interfaz de terminal para la demostración del agente de IA."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .agent import AIProjectAgent, AgentError, ToolEvent
from .tools import ProjectTools


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crea un proyecto Python mediante un agente de IA."
    )
    parser.add_argument("request", nargs="+", help="Descripción libre del proyecto.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("proyectos-generados"),
        help="Directorio contenedor permitido.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL"),
        help="Modelo disponible en la cuenta; también admite OPENAI_MODEL.",
    )
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument(
        "--allow-test-execution",
        action="store_true",
        help="Autoriza ejecutar unittest generado por el modelo.",
    )
    return parser


def print_event(event: ToolEvent) -> None:
    status = "OK" if event.result.get("ok") else "ATENCIÓN"
    print(f"[{status}] {event.name}")
    if not event.result.get("ok"):
        detail = event.result.get("error", event.result.get("reason", ""))
        if detail:
            print(f"  {detail}")
        return
    if event.name == "record_plan":
        print(f"  {event.result.get('summary', '')}")
    elif event.name == "create_project":
        print(f"  {event.result.get('path', event.result.get('error', ''))}")
    elif event.name == "run_tests":
        print(f"  {event.result.get('output', event.result.get('reason', ''))}".rstrip())
    elif event.result.get("error"):
        print(f"  {event.result['error']}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: define OPENAI_API_KEY antes de ejecutar el agente.", file=sys.stderr)
        return 2
    if not args.model:
        print("Error: indica --model o define OPENAI_MODEL.", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print(
            "Error: instala las dependencias con 'python -m pip install -e .'.",
            file=sys.stderr,
        )
        return 2

    tools = ProjectTools(
        args.output,
        allow_test_execution=args.allow_test_execution,
    )
    agent = AIProjectAgent(
        client=OpenAI(),
        model=args.model,
        project_tools=tools,
        max_steps=args.max_steps,
        on_event=print_event,
    )
    try:
        result = agent.run(" ".join(args.request))
    except (AgentError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("\nInforme final del agente:\n")
    print(result.message)
    return 0
