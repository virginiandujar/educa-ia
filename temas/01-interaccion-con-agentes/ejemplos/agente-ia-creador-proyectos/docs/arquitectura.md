# Arquitectura del ejemplo

## Componentes

```text
Petición en lenguaje natural
          │
          ▼
   Modelo de IA (Responses API)
          │ solicita herramientas
          ▼
     Bucle AIProjectAgent
          │
          ├── record_plan
          ├── create_project
          ├── read_file
          ├── write_file
          └── run_tests
          │
          ▼
  Directorio proyectos-generados/
```

El modelo interpreta la petición y decide la siguiente herramienta. `AIProjectAgent` conserva la conversación, ejecuta las llamadas y devuelve cada resultado al modelo. `ProjectTools` aplica los límites y realiza las operaciones locales.

## Bucle

1. La aplicación envía la petición, las instrucciones y los esquemas de herramientas.
2. El modelo devuelve una llamada de función.
3. Python valida los argumentos y ejecuta la herramienta.
4. La aplicación añade un `function_call_output` asociado al `call_id`.
5. El modelo recibe la observación y decide si llama otra herramienta o termina.

Este patrón sigue el flujo descrito en la [documentación oficial de function calling](https://developers.openai.com/api/docs/guides/function-calling).

## Por qué es un agente

- Usa un modelo de IA para interpretar requisitos abiertos.
- El modelo elige herramientas y argumentos.
- Observa el resultado de cada acción.
- Puede leer y corregir archivos cuando una prueba falla.
- Decide cuándo dispone de evidencia suficiente para finalizar.

La escritura y las pruebas siguen siendo herramientas deterministas: el modelo solicita acciones, pero no recibe acceso directo al sistema operativo.
