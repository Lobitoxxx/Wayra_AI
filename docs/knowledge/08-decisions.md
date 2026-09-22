---
tipo: decisiones
estado: vigente
fecha: 2026-09-22
tags: [wayra, adr, decisiones]
---

# Registro de decisiones (ADR + entorno) — Wayra AI

Convención: cada entrada expresa **decisión aprobada** (o propuesta). Se respeta hasta modificación explícita.

## D-001 · Configuración del entorno inteligente (aprobada)
- Instalar skills Obsidian (6), activar/verificar Graphify y Archify; memoria en `docs/knowledge/`; AGENTS.md; README con Mermaid; medición de tokens documentada.
- Alcance: configuración **antes** de desarrollo funcional.

## D-002 · Entorno Python con uv + CPython 3.12 (aprobada)
- Venv en `wayra-ai/.venv`; razones: compatibilidad con lazypredict 0.3.0 (2019) y librerías científicas; respaldo Dockerfile.

## D-003 · Raíz del repositorio `wayra-ai/` (aprobada)
- git init en `D:\Proyects\3. Inteligencia Artificial\Wayra_IA\wayra-ai`, rama `main`.

## D-004 · Fuentes de datos (aprobada)
- Precipitación: **CHIRPS v3.0** diario variante `rnl` (ERA5-downscaled), 0.05°, 2001–2026 completo.
- Temperatura/etc: **ERA5-Land** vía CDS con clave (usuario la tiene/creará).
- Índices: NOAA ERSST5 (mensual+semanal), RONI≈CPC `detrend.nino34.ascii.txt`, ICEN (IGP `ICEN.txt`).
- SENAMHI: sin cuenta → adaptador documentado + subset público.

## D-005 · Malla de trabajo 0.1° (aprobada, del programa)
- Agregar CHIRPS 0.05° → 0.1°; re-grid ERA5-Land 0.1°; máscara Perú + regiones.

## D-006 · Metodología/reglas de datos (aprobada)
- Nunca inventar datos/métricas/resultados; trazas temporales obligatorias; split cronológico (2001–22/2023–24/2025 por ajustar al periodo común real); modo operativo deshabilitado.

## D-007 · Diagramas y documentación (propuesta)
- Archify → HTML interactivo (y PNG/SVG); Mermaid en Markdown; ambos verificados vs código antes de darse por válidos.

Historial completo de fuentes: [[docs/sources/00-fuentes]] · Estado de implementación: [[07-progress]].