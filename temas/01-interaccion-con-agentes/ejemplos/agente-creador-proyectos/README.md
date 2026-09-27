# Generador determinista de proyectos Python

Ejemplo didáctico de una automatización que transforma una instrucción concreta en una acción verificable:

```text
Crear el proyecto inventario-api
```

No es un agente de IA porque no usa un modelo para razonar ni elegir herramientas. Para una orden tan acotada, un intérprete determinista es más barato, rápido y predecible. El diseño deja visibles varias piezas que también utilizaría un agente:

1. **Entender:** reconoce la intención y extrae el nombre.
2. **Validar:** rechaza rutas, nombres peligrosos e instrucciones desconocidas.
3. **Planificar:** prepara todos los archivos antes de escribir.
4. **Actuar:** crea el proyecto en un directorio temporal.
5. **Verificar:** no sobrescribe destinos y realiza una entrega atómica.
6. **Informar:** enumera el proyecto y los archivos creados.

## Probarlo sin instalar

Desde este directorio:

```bash
PYTHONPATH=src python -m project_creator_agent \
  "Crear el proyecto inventario-api" \
  --output proyectos-generados
```

Para ver el plan sin escribir nada:

```bash
PYTHONPATH=src python -m project_creator_agent \
  "Crear el proyecto inventario-api" \
  --output proyectos-generados \
  --dry-run
```

## Instalar el comando

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
crear-proyecto "Crear el proyecto inventario-api"
```

## Estructura generada

```text
inventario-api/
├── .github/workflows/tests.yml
├── src/inventario_api/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_smoke.py
├── docs/architecture.md
├── .gitignore
├── AGENTS.md
├── README.md
└── pyproject.toml
```

El agente nunca reemplaza un proyecto existente. Tampoco acepta `/`, `\\` ni `..` en el nombre.

## Ejecutar sus pruebas

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Qué añadiría un modelo de lenguaje

Un modelo sería útil si quisiéramos aceptar peticiones menos estructuradas, por ejemplo:

> Crea una API de inventario con FastAPI, PostgreSQL, Docker y pruebas.

En ese caso, el modelo podría convertir la petición en un plan estructurado. La herramienta que escribe archivos debería seguir siendo determinista, limitada y verificable como en este ejemplo.
