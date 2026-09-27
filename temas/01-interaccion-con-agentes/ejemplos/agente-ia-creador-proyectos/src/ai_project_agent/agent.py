"""Bucle del agente basado en la Responses API y function calling."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from .tools import ProjectTools, ToolError


INSTRUCTIONS = """
Eres un agente didáctico que crea exactamente un proyecto Python pequeño.

Tu trabajo sigue este orden:
1. Interpreta la petición y llama primero a record_plan.
2. Llama a create_project con una estructura completa y coherente.
3. Llama a run_tests después de crear el proyecto.
4. Si las pruebas fallan, usa read_file y write_file para corregir solo lo
   necesario y vuelve a ejecutar run_tests. Haz como máximo dos intentos de
   reparación.
5. Termina con un informe que incluya archivos, pruebas, límites y riesgos.

Reglas:
- Usa solo las herramientas proporcionadas.
- No pidas ni escribas credenciales.
- Prefiere la biblioteca estándar salvo que el usuario solicite otra cosa.
- Incluye README.md, pyproject.toml, AGENTS.md, paquete src y pruebas unittest.
- No intentes sobrescribir un proyecto existente.
- No inventes que las pruebas se ejecutaron: usa el resultado de run_tests.
- Si run_tests devuelve blocked=true, no repitas la llamada y explica que la
  ejecución necesita autorización explícita.
""".strip()


class AgentError(RuntimeError):
    """Fallo controlado del bucle del agente."""


@dataclass(frozen=True)
class ToolEvent:
    name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class AgentRunResult:
    message: str
    events: tuple[ToolEvent, ...]


class AIProjectAgent:
    """Orquesta al modelo y ejecuta sus llamadas con límites locales."""

    def __init__(
        self,
        *,
        client: Any,
        model: str,
        project_tools: ProjectTools,
        max_steps: int = 10,
        on_event: Callable[[ToolEvent], None] | None = None,
    ) -> None:
        if not model.strip():
            raise ValueError("model no puede estar vacío")
        if not 1 <= max_steps <= 20:
            raise ValueError("max_steps debe estar entre 1 y 20")
        self.client = client
        self.model = model
        self.project_tools = project_tools
        self.max_steps = max_steps
        self.on_event = on_event

    def run(self, request: str) -> AgentRunResult:
        if not request.strip():
            raise AgentError("la petición no puede estar vacía")

        conversation: list[Any] = [{"role": "user", "content": request}]
        events: list[ToolEvent] = []

        for _ in range(self.max_steps):
            try:
                response = self.client.responses.create(
                    model=self.model,
                    instructions=INSTRUCTIONS,
                    tools=self.project_tools.definitions,
                    input=conversation,
                )
            except Exception as error:  # El SDK expone varios tipos de error.
                raise AgentError(
                    f"la llamada al modelo falló: {type(error).__name__}: {error}"
                ) from error

            output_items = list(response.output)
            conversation.extend(output_items)
            function_calls = [
                item for item in output_items if item.type == "function_call"
            ]

            if not function_calls:
                message = response.output_text.strip()
                if not message:
                    raise AgentError("el modelo terminó sin entregar un informe")
                return AgentRunResult(message=message, events=tuple(events))

            for call in function_calls:
                arguments: dict[str, Any] = {"raw": call.arguments}
                try:
                    parsed_arguments = json.loads(call.arguments)
                    if not isinstance(parsed_arguments, dict):
                        raise TypeError("los argumentos de la herramienta deben ser un objeto")
                    arguments = parsed_arguments
                    tool_result = self.project_tools.execute(call.name, arguments)
                except (json.JSONDecodeError, ToolError, TypeError) as error:
                    tool_result = {"ok": False, "error": str(error)}

                event = ToolEvent(call.name, arguments, tool_result)
                events.append(event)
                if self.on_event:
                    self.on_event(event)

                conversation.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(tool_result, ensure_ascii=False),
                    }
                )

        raise AgentError(
            f"el agente alcanzó el límite de {self.max_steps} pasos sin terminar"
        )
