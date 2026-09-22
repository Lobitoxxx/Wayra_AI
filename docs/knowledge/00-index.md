---
tipo: índice
estado: vigente
fecha: 2026-09-22
tags: [memory, wayra, indice]
---

# Índice de memoria — Wayra AI

Memoria persistente del proyecto **Wayra AI**. Objetivo: retomar cualquier sesión sin reconstruir todo el contexto.

## Protocolo de recuperación (resumen)
1. Identificar la tarea solicitada.
2. Consultar este índice.
3. Recuperar **solo** las notas pertinentes.
4. Usar [[../architecture/../sources/00-fuentes]] y Graphify (cuando exista grafo) para relaciones de código.
5. Verificar en código solo si la memoria no alcanza.

> Reglas: hechos ≠ decisiones ≠ propuestas ≠ hipótesis. Registrar fecha y estado en cada nota.

## Navegación por responsabilidad
| Nota | Responsabilidad |
|---|---|
| [[01-project-vision]] | Qué es y para qué (visión, objetivos, alcance) |
| [[02-requirements]] | Requisitos funcionales y no funcionales con estado |
| [[03-architecture]] | Arquitectura (propuesta/implementada), decisiones clave de diseño |
| [[04-tech-stack]] | Tecnologías: implementadas, decididas y propuestas |
| [[05-modules]] | Módulos, paquetes y responsabilidades |
| [[06-data-model]] | Esquema del dataset maestro y trazabilidad temporal |
| [[07-progress]] | Progreso por fase, estado actual |
| [[08-decisions]] | Registro de decisiones aprobadas (ADR) |
| [[09-known-issues]] | Problemas conocidos, bloqueos y workarounds |
| [[10-roadmap]] | Hoja de ruta y siguientes pasos |
| [[11-lessons-learned]] | Lecciones de entornos OpenCode/herramientas |

Documentos de referencia (no memoria):
- [[../README]] — punto de entrada del repositorio.
- [[../sources/00-fuentes]] — registro de fuentes de datos.
- [[../architecture/00-arquitectura]] — diagramas y notas de arquitectura.
- [[../measurement/2026-09-22-token-metodologia]] — medición de tokens.

Sesiones terminadas: ver [[sessions/]].