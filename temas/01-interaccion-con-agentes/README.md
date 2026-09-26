# Interacción con agentes

> **Objetivo de aprendizaje:** entender qué es un agente de IA, cómo delegarle trabajo de forma segura y qué capacidades interesa desarrollar dentro de la empresa.

## La idea central

Un agente no suele ser un modelo de IA creado específicamente para una empresa. Normalmente es una configuración especializada construida sobre un modelo existente.

Podemos resumirlo así:

> **Agente = modelo + instrucciones + contexto + herramientas + validación**

El modelo aporta capacidad general. El resto de los componentes convierte esa capacidad en una forma de trabajo concreta, limitada y revisable.

## Del chat a la delegación

En una conversación sencilla pedimos información y recibimos una respuesta. En una interacción con un agente delegamos un objetivo que puede requerir varios pasos y el uso de herramientas.

El ciclo recomendable es:

1. **Definir el objetivo.** Qué resultado debe producir y para quién.
2. **Aportar contexto.** Repositorio, documentación, restricciones y decisiones previas.
3. **Acordar un plan.** Qué pasos seguirá y qué no hará.
4. **Autorizar herramientas.** Solo las necesarias y con el menor permiso posible.
5. **Verificar.** Pruebas, revisiones y controles automáticos.
6. **Recibir evidencia.** Cambios realizados, pruebas ejecutadas, riesgos y dudas.

La persona no desaparece del proceso. Conserva el criterio, decide los límites y asume la responsabilidad del resultado.

## Qué se construye realmente

Cuando una empresa ofrece “agentes”, normalmente combina cinco piezas.

### 1. Instrucciones especializadas

Definen:

- La tarea y el resultado esperado.
- Las normas de programación o de negocio.
- Los archivos y sistemas permitidos.
- Las acciones prohibidas.
- Las pruebas obligatorias.
- Las condiciones para detenerse y pedir ayuda.

### 2. Conectores e integraciones

Permiten trabajar con GitLab o GitHub, integración continua, sistemas de incidencias, documentación, analizadores de código, bases de datos o inventarios técnicos.

### 3. Flujos de trabajo

Un flujo puede leer una incidencia, analizar el repositorio, proponer un plan, modificar una rama, ejecutar pruebas, preparar una solicitud de cambio y entregar un informe para revisión.

### 4. Plataforma de ejecución

Puede proporcionar entornos aislados, permisos, registro de acciones, administración centralizada, cuadros de mando y control de costes o modelos.

### 5. Conocimiento y consultoría

Incluye comprender las aplicaciones, recuperar conocimiento de los equipos, redactar instrucciones, preparar herramientas y diseñar evaluaciones.

## Ejemplo de contrato para un agente

```text
Rol:
Especialista en mantenimiento de esta aplicación Java heredada.

Objetivo:
Resolver defectos acotados y crear pruebas de regresión.

Reglas:
- No cambiar interfaces públicas.
- No añadir dependencias sin autorización.
- No modificar esquemas de base de datos.
- Mantener compatibilidad con Java 8.
- Trabajar únicamente en una rama.
- Ejecutar compilación, pruebas y análisis estático.
- Detenerse si falta información funcional.

Herramientas:
- Lectura y edición del repositorio.
- Maven, pruebas unitarias, analizador estático y Git.

Resultado:
Cambio propuesto, pruebas ejecutadas, riesgos y dudas pendientes.
```

Esto ya constituye la base de un agente especializado. No exige entrenar un modelo ni construir una plataforma corporativa completa.

## Tres niveles de dificultad

| Resultado | Orden de magnitud | Dificultad | Participantes |
|---|---|---:|---|
| Agente configurado para un repositorio | Días | Baja o media | Equipo de desarrollo |
| Integración con GitLab, CI y herramientas internas | Semanas | Media | Desarrollo y plataforma |
| Plataforma corporativa segura y auditada | Meses | Alta | Desarrollo, plataforma, ciberseguridad y, quizá, un proveedor |

La dificultad principal no está en “crear la IA”. Está en recuperar conocimiento, automatizar compilaciones, disponer de pruebas, definir permisos, integrar herramientas, proteger el código y demostrar que los cambios son correctos.

## Por qué el equipo interno tiene ventaja

Quien mantiene una aplicación conoce:

- El comportamiento que debe conservarse.
- Las decisiones históricas y sus motivos.
- Las interfaces que no pueden romperse.
- Los cambios que parecen simples, pero son peligrosos.
- La evidencia necesaria para aceptar un resultado.

Ese conocimiento es precisamente lo que especializa al agente. Delegarlo por completo crea una dependencia difícil de revertir.

## Cuándo tiene sentido un proveedor

Puede aportar valor si ofrece una capacidad que hoy no existe internamente:

- Experiencia en redes restringidas.
- Integración con GitLab y herramientas internas.
- Plataforma aislada, segura y auditable.
- Modelos desplegados en infraestructura autorizada.
- Conocimiento de lenguajes o plataformas antiguas.
- Aceleración temporal.
- Transferencia efectiva de conocimiento.

No basta con afirmar que dispone de “agentes propios”. La expresión es demasiado ambigua.

## Preguntas para evaluar una propuesta

1. ¿Qué modelo utiliza y quién lo opera?
2. ¿Qué parte ha desarrollado realmente el proveedor?
3. ¿Qué datos salen de la red?
4. ¿Cómo se integra con GitLab, CI y las herramientas internas?
5. ¿Entrega instrucciones, conectores, evaluaciones y documentación?
6. ¿La empresa recibe el código fuente?
7. ¿El equipo interno puede modificar el agente?
8. ¿Qué componentes seguirán funcionando al terminar el contrato?
9. ¿Por qué no podría construirlo el equipo interno?

## Decisión recomendable

La alternativa no es “hacerlo todo dentro” o “comprarlo todo fuera”. Una estrategia más sólida es:

1. Crear internamente uno o dos agentes sencillos sobre proyectos controlados.
2. Medir calidad, tiempo, seguridad, coste y esfuerzo de supervisión.
3. Usar esos agentes como referencia para evaluar ofertas.
4. Contratar solo las capacidades que no puedan desarrollarse en un plazo razonable.
5. Exigir que instrucciones, integraciones, pruebas y documentación queden bajo control de la empresa.
6. Exigir transferencia de conocimiento.
7. Evitar que cada modificación futura dependa del proveedor.

## Conclusión

> Proponemos desarrollar internamente la capacidad de crear y mantener agentes para nuestras aplicaciones. Los proveedores pueden complementar esa capacidad con plataforma, integración o conocimientos especializados, pero los agentes, sus instrucciones, sus pruebas y el conocimiento de los proyectos deben permanecer bajo control de la empresa.

## Preguntas para conversar con el equipo

- ¿Qué tarea repetitiva y acotada sería un buen primer piloto?
- ¿Qué conocimiento solo existe hoy en la cabeza de algunas personas?
- ¿Qué permisos nunca debería tener un agente sin aprobación humana?
- ¿Qué pruebas demostrarían que el piloto aporta valor?
