# Educa IA

Material abierto y reutilizable para compartir conceptos de inteligencia artificial con equipos de trabajo. Cada tema vive en su propio directorio y tiene dos formatos:

- **Markdown**, para leer, revisar y mejorar directamente desde GitHub.
- **Presentación web**, para exponer en una reunión o compartir mediante GitHub Pages.

## Temas

| N.º | Tema | Contenido |
|---:|---|---|
| 01 | [Interacción con agentes](temas/01-interaccion-con-agentes/README.md) | Qué es un agente, cómo se trabaja con él y qué conviene construir o contratar. |

## Ver la presentación

La presentación permite navegar con los botones, las flechas del teclado, `Re Pág` / `Av Pág` o la barra espaciadora. También incluye modo de pantalla completa y salida a PDF.

Para ejecutarla en local:

```bash
pnpm install
pnpm dev
```

Después, abre `http://localhost:3000`.

## Publicar con GitHub Pages

El repositorio incluye el flujo [`.github/workflows/pages.yml`](.github/workflows/pages.yml). En GitHub:

1. Abre **Settings → Pages**.
2. En **Build and deployment**, selecciona **GitHub Actions**.
3. Envía los cambios a la rama `main`.

GitHub construirá y publicará el sitio. La ruta se ajusta automáticamente al nombre del repositorio.

## Estructura

```text
.
├── app/                         # Presentación web
├── temas/
│   └── 01-interaccion-con-agentes/
│       ├── README.md            # Documento principal
│       └── notas-presentador.md # Guion breve
└── .github/workflows/pages.yml  # Publicación automática
```

## Criterios editoriales

- Una idea principal por diapositiva.
- El detalle y los matices viven en Markdown.
- Los ejemplos deben ser concretos y verificables.
- Se distingue siempre entre modelo, agente, integración y plataforma.
- No se incluyen datos internos, credenciales ni capturas de sistemas corporativos.

Antes de hacerlo público, conviene acordar una licencia para el código y otra para el contenido (por ejemplo, MIT y CC BY 4.0, respectivamente).
