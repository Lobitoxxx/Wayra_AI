# Archify en Wayra AI

## Objetivo

Archify se utiliza como complemento de Mermaid para explicar la arquitectura mediante un artefacto interactivo. Mermaid permanece dentro de los archivos Markdown; Archify trabaja a partir de una representación JSON versionable y genera una vista HTML autocontenida.

**Regla:** el diagrama interactivo debe representar el código o la arquitectura objetivo con una etiqueta inequívoca. Un componente planificado no se marca como implementado.

## Artefactos

```text
docs/architecture/diagrams/
├── architecture_wayra.json
├── dataflow_wayra.json
├── lifecycle_wayra.json
├── wayra-current.architecture.json     # estado comprobable del repositorio
└── wayra-propuesta.architecture.json   # arquitectura objetivo
```

Los PNG `visual-check` existentes son evidencias de renders anteriores. Deben regenerarse cuando cambie de forma sustancial el JSON correspondiente.

## Instalación sugerida

Archify se mantiene en `tt-a1i/archify` y publica una skill instalable mediante `skills`.

```bash
npx skills add tt-a1i/archify -g
```

OpenCode puede utilizar skills instaladas globalmente o copiadas al espacio de skills del agente. La ubicación física exacta de la instalación puede variar según la plataforma.

## Flujo recomendado

1. Actualizar el JSON fuente.
2. Ejecutar validación de Archify.
3. Generar HTML con perfil de calidad `showcase`.
4. Ejecutar `visual-check`.
5. Revisar manualmente el resultado.
6. Solo después, versionar el HTML/capturas si aportan valor al repositorio.

Ejemplo cuando `bin/archify.mjs` está disponible desde el directorio de Archify:

```bash
node bin/archify.mjs validate architecture \
  /ruta/Wayra_AI/docs/architecture/diagrams/wayra-current.architecture.json \
  --quality showcase --json

node bin/archify.mjs deliver architecture \
  /ruta/Wayra_AI/docs/architecture/diagrams/wayra-current.architecture.json \
  /ruta/Wayra_AI/docs/architecture/diagrams/wayra-current.architecture.html \
  --quality showcase --json

node bin/archify.mjs visual-check \
  /ruta/Wayra_AI/docs/architecture/diagrams/wayra-current.architecture.html \
  --json
```

En Windows/PowerShell se deben entrecomillar rutas con espacios.

## Dos vistas obligatorias

### 1. `wayra-current.architecture.json`

Debe responder: **¿qué existe realmente en el repositorio?**

Actualmente incluye como núcleo:

- ingesta CHIRPS;
- archivos/manifiestos Bronze locales;
- malla 0.1°;
- máscara PER-ADM0;
- regrid;
- smoke scripts;
- pruebas y CI incorporadas en la rama de mejora;
- documentación.

No debe incluir FastAPI, frontend ni modelos entrenados como componentes activos.

### 2. `wayra-propuesta.architecture.json`

Debe responder: **¿hacia dónde evoluciona Wayra AI?**

Puede mostrar:

- CHIRPS/ERA5-Land/SENAMHI;
- NOAA/IMARPE;
- Bronze/Silver/Gold;
- regresión y clasificación;
- registro de modelos;
- API/web;
- módulo de peligros.

Cada card o etiqueta debe dejar claro que se trata de una arquitectura objetivo.

## Mermaid vs. Archify

| Necesidad | Herramienta |
|---|---|
| Diagrama visible directamente en GitHub | Mermaid |
| Secuencia temporal sencilla | Mermaid |
| Flujo académico/ML | Mermaid |
| Exploración interactiva de muchos componentes | Archify |
| Vista de arquitectura para exposición | Archify + exportación/captura validada |

No se recomienda duplicar exactamente el mismo diagrama en ambas herramientas; cada representación debe responder una pregunta concreta.

## GitHub

GitHub no ejecuta un HTML interactivo dentro del README. El README enlaza al JSON y explica cómo generar/abrir el HTML. Para compartir la vista interactiva en línea, posteriormente puede evaluarse GitHub Pages u otro hosting, pero eso no forma parte del MVP actual.

## Criterio de aceptación

Un artefacto Archify se considera vigente únicamente cuando:

- el JSON pasa validación;
- el HTML se genera sin error;
- `visual-check` termina correctamente;
- una revisión humana comprueba legibilidad;
- los componentes coinciden con el estado real o están explícitamente etiquetados como propuestos.

Hasta ejecutar estas comprobaciones sobre una nueva versión, el documento debe decir **fuente Archify preparada**, no **diagrama validado**.
