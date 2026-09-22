# AGENTS.md — Wayra AI

Guía operativa para agentes (OpenCode u otros) que trabajen en este repositorio. Lean esto primero; el resto de contexto vive en la memoria Obsidian.

## Prioridad de contexto

1. **Memoria primero:** `docs/knowledge/00-index.md` → recuperar solo las notas pertinentes ([07-progress], [08-decisions], [02-requirements], [10-roadmap]).
2. **Graphify:** si existe `graphify-out/`, consultar el grafo antes de explorar código a mano (`graphify path` / `explain`). Hasta que exista código sustancial, no construir grafo.
3. **Archify:** usar para diagramas interactivos; Mermaid para diagramas en Markdown.
4. **Código:** verificar en el código solo cuando la memoria no alcance.

## Diferenciar implementado vs. propuesto (regla no negociable)

- **Nunca** describir como "implementado" algo sin evidencia en el repositorio.
- Lo plano tiene etiqueta explícita: `🟩 Implementado` / `🟦 Propuesto/Decidido` / `🟨 En desarrollo`.
- **Nunca** declarar pruebas ejecutadas si no lo están. Un "✓" requiere salida real de un comando.
- No inventar datos, métricas ni resultados (regla del programa, RQ-21).

## Entorno y comandos

- PowerShell 5.1 (win32). Rutas con espacios → comillas (`"D:\Proyects\3. Inteligencia Artificial\Wayra_IA\wayra-ai"`).
- Python: `uv` + CPython 3.12, venv en `.venv`. No usar Python 3.14 para el stack científico (D-002).
- npm/npx bloqueados por ExecutionPolicy → ejecutar vía `cmd /c "npx ..."`.
- `~/.local/bin` (uv tools: `graphify`, `opencode`) NO está en PATH.
- `ARCHIFY_CHROME=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` para `visual-check`.
- Credenciales solo en `.env` (gitignored). No versionar ni loguear claves.
- La config global de OpenCode (`C:\Users\D3V1N\.config\opencode\opencode.json`) contiene claves reales: **no tocar, no versionar, no volcar a la conversación**.

## Documentación

- Memoria: `docs/knowledge/` (Obsidian, con frontmatter, wikilinks y fechas).
- Fuentes: `docs/sources/00-fuentes.md` · Arquitectura: `docs/architecture/00-arquitectura.md` · Mediciones: `docs/measurement/`.
- Diagramas Archify: `docs/architecture/diagrams/`. Entregar siempre JSON (fuente) + HTML (visión); validar `--quality showcase` y `visual-check` antes de declarar éxito.
- No generar documentación decorativa; cada artefacto responde una pregunta concreta.

## Commits

- Solo hacer commits cuando el usuario lo solicite explícitamente.
- No configurar identidad git por cuenta propia (aún no definida).