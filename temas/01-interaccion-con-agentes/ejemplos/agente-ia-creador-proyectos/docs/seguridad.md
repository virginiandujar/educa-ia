# Límites de seguridad

Este repositorio es un ejemplo didáctico, no un entorno aislado de producción.

## Controles incluidos

- Solo se escribe dentro del directorio indicado mediante `--output`.
- Los nombres se convierten en identificadores seguros.
- Se rechazan rutas absolutas, `..`, barras invertidas y enlaces que salgan del proyecto.
- Se bloquean `.env`, claves privadas y nombres habituales de credenciales.
- Hay límites de archivos, tamaño y pasos del agente.
- Los proyectos existentes nunca se sobrescriben.
- No existe una herramienta de terminal genérica.
- Las pruebas solo ejecutan `python -m unittest discover` y requieren `--allow-test-execution`.

## Riesgo que permanece

Las pruebas son código generado por el modelo. Incluso con un comando fijo, Python puede leer archivos, consumir recursos o acceder a la red con los permisos del proceso. Para una demostración:

1. Revisa la lista de archivos que propone el agente.
2. Usa un directorio temporal y una cuenta sin privilegios.
3. No habilites las pruebas si no confías en el contenido generado.
4. Para uso real, ejecuta el proyecto en un contenedor o sandbox sin secretos ni acceso innecesario a red.

La clave de API debe vivir únicamente en `OPENAI_API_KEY`. Nunca debe escribirse en `.env.example`, código, trazas o Git.
