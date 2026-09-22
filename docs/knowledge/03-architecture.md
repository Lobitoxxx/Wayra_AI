---
tipo: arquitectura
estado: propuesta
fecha: 2026-09-22
tags: [wayra, arquitectura]
---

# Arquitectura — Wayra AI

> Estado: **PROPUESTA** (no hay código funcional todavía). Lo confirmado se marcará "implementado" cuando exista evidencia.

## Descomposición propuesta
- `src/ingestion` — adaptadores de datos (CHIRPS, ERA5-Land, NOAA, RONI, ICEN, SENAMHI), descarga reanudable, manifiestos con checksum.
- `src/preprocessing` — control de calidad, limpieza, regrid a malla 0.1°, particionado (parquet año-mes).
- `src/geospatial` — máscara de Perú, regionalización (costa/sierra/selva), vecindades.
- `src/features` — ingeniería de características, ventanas, índices con `published_at`, anti-fuga.
- `src/models` — LazyPredict (regresión+clasificación), baseline, splits cronológicos.
- `src/evaluation` — métricas, matrices, análisis por región/estación.
- `src/inference` — servicio de predicción con `forecast_issued_at`.
- `apps/api` — FastAPI `/api/v1/`.
- `apps/web` — frontend responsivo en español.

## Límites
- Datos externos: Servidor CHC (CHIRPS), CDS Copernicus (ERA5-Land), NOAA CPC, IMARPE/IGP (ICEN), SENAMHI (opcional).
- El modo operativo se representará con `status: no_habilitado` hasta autorización.

## Relación con la visualización
- Diagramas verificados: [[docs/architecture/diagrams/archify-proyecto]] y Mermaid en [[../README]].
- Cuando exista código, Graphify construirá el grafo (`graphify-out/`) como primera fuente de consulta estructural.

Decisiones que afectan arquitectura: [[08-decisions]]. Datos: [[06-data-model]].