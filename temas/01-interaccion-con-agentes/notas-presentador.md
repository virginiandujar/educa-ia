# Notas para presentar · Interacción con agentes

Duración orientativa: **15–20 minutos**, más conversación.

## Apertura

Preguntar: “Cuando oís *agente*, ¿pensáis en un modelo distinto, en un chatbot o en algo que actúa sobre sistemas?”. La variedad de respuestas sirve para introducir que el término agrupa varias piezas.

## Mensajes que conviene subrayar

1. **Un agente no es magia.** La diferencia la crean el contexto, las herramientas, las reglas y la validación.
2. **Delegar no elimina la responsabilidad.** La persona decide el objetivo, los permisos y el criterio de aceptación.
3. **No mezclar niveles.** Un agente de repositorio y una plataforma corporativa tienen costes, plazos y riesgos muy distintos.
4. **El conocimiento interno es el activo.** La configuración del agente captura decisiones y restricciones del sistema.
5. **Un proveedor puede acelerar.** Debe dejar capacidad, código y conocimiento, no una dependencia permanente.

## Ejemplo rápido: consultar el tiempo

Usar la pregunta “¿Qué tiempo hace en Madrid?” para recorrer el flujo completo:

1. La aplicación entrega al modelo la petición, las instrucciones y las herramientas disponibles.
2. El modelo solicita una llamada estructurada a `get_weather`.
3. La aplicación comprueba los permisos y ejecuta la herramienta.
4. El servicio devuelve datos y la aplicación se los pasa al modelo.
5. El modelo interpreta el resultado y redacta la respuesta final.

Frase para resumirlo: **el modelo decide el siguiente paso; la aplicación lo valida y lo ejecuta; la herramienta aporta los datos**.

Conviene aclarar que el modelo no ejecuta la función directamente. También puede haber varias vueltas si necesita más datos. Si no interviene un modelo y todos los pasos están prefijados, es más preciso hablar de automatización, aunque en informática el término *agente* también pueda usarse en un sentido más amplio.

## Pausas para conversación

- Tras el ciclo de interacción: pedir un ejemplo de tarea que requiera aprobación humana.
- Tras los niveles de dificultad: identificar qué capacidades existen ya en la organización.
- Antes del cierre: elegir entre todos un candidato para piloto.

## Cierre sugerido

“La pregunta no es si podemos comprar un agente. La pregunta es qué capacidad queremos conservar, qué riesgo estamos dispuestos a delegar y qué evidencia exigiremos para confiar en el resultado.”
