# Guion de demostración

## Petición recomendada

```text
Crea un proyecto llamado gestor-tareas. Quiero una aplicación de terminal que permita añadir y listar tareas, guardarlas en JSON y tenga pruebas automáticas.
```

## Qué debería observar el público

1. `record_plan`: el modelo convierte la petición libre en un plan y una lista de archivos.
2. `create_project`: una herramienta limitada crea el proyecto sin sobrescribir nada.
3. `run_tests`: el agente busca evidencia ejecutable.
4. Si una prueba falla, el modelo puede usar `read_file` y `write_file`, y volver a probar.
5. El informe final diferencia hechos comprobados, límites y riesgos.

## Mensaje que conviene remarcar

> El modelo propone y decide; las herramientas validan y ejecutan. Dar acceso directo e ilimitado al sistema no es necesario para construir un agente útil.
