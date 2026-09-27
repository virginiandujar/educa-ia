# Agente de IA creador de proyectos Python

Ejemplo didáctico de un agente real: un modelo interpreta una petición abierta, prepara un plan, elige herramientas, observa sus resultados, ejecuta pruebas y puede corregir archivos antes de entregar un informe.

## Ejemplo de petición

```text
Crea un proyecto llamado gestor-tareas. Quiero una aplicación de terminal
que permita añadir y listar tareas, guardarlas en JSON y tenga pruebas.
```

El agente dispone únicamente de cinco herramientas:

- `record_plan`: hace visible el plan antes de escribir.
- `create_project`: crea el proyecto de forma atómica.
- `read_file`: inspecciona un archivo cuando necesita diagnosticar.
- `write_file`: corrige un archivo dentro del proyecto.
- `run_tests`: ejecuta exclusivamente `unittest` con autorización explícita.

Consulta [la arquitectura](docs/arquitectura.md), [los límites de seguridad](docs/seguridad.md) y [el guion de demostración](docs/demo.md).

## Preparación

Requiere Python 3.11 o posterior y una clave de la API de OpenAI.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

export OPENAI_API_KEY="tu-clave"
export OPENAI_MODEL="un-modelo-disponible-en-tu-cuenta"
```

El SDK oficial lee `OPENAI_API_KEY` desde el entorno, como muestra el [quickstart oficial](https://developers.openai.com/api/docs/quickstart). No guardes la clave en el repositorio.

## Ejecutar la demostración

```bash
agente-ia-proyectos \
  "Crea un proyecto llamado gestor-tareas. Quiero una aplicación de terminal que permita añadir y listar tareas, guardarlas en JSON y tenga pruebas." \
  --output proyectos-generados \
  --allow-test-execution
```

También se puede ejecutar sin instalar el comando:

```bash
PYTHONPATH=src python -m ai_project_agent \
  "Crea un gestor de tareas en Python con persistencia JSON y pruebas." \
  --model "$OPENAI_MODEL" \
  --output proyectos-generados
```

Sin `--allow-test-execution`, el agente puede crear el proyecto, pero la herramienta de pruebas devuelve `blocked=true`. Esto hace visible que ejecutar código generado necesita una autorización distinta de escribir archivos.

## Flujo esperado

```text
Usuario
  ↓
Modelo interpreta la petición
  ↓
record_plan
  ↓
create_project
  ↓
run_tests ── fallo ──→ read_file / write_file ──→ run_tests
  ↓ éxito
Informe final
```

## Ejecutar pruebas del ejemplo

Las pruebas no llaman a la API. Utilizan un cliente simulado y directorios temporales:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Automatización frente a agente

El ejemplo vecino [`agente-creador-proyectos`](../agente-creador-proyectos/README.md) reconoce una orden fija y aplica una plantilla. Este ejemplo sí utiliza IA: el modelo interpreta requisitos variables y decide qué herramientas usar y cuándo terminar.

## Alcance

Es material de formación. Para producción harían falta sandbox de ejecución, observabilidad, aprobaciones, gestión de costes, evaluaciones y políticas corporativas de datos y modelos.
