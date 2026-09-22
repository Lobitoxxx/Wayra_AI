---
tipo: progreso
estado: vigente
fecha: 2026-09-22
tags: [wayra, progreso, estado]
---

# Progreso — Wayra AI

> Regla: no declarar “validado” sin una ejecución reproducible asociada a la versión de código correspondiente. Un smoke test no equivale a una evaluación científica final.

## Estado ejecutivo

### 🟩 Implementado en el núcleo

- Configuración Python 3.12 + `uv`.
- Adaptador CHIRPS v3 diario RNL.
- Descarga temporal con archivo `.part` y soporte de reanudación cuando el servidor lo permite.
- SHA-256 local y distinción entre hash local y checksum externo verificado.
- Parsing correcto de `observation_time` desde el nombre CHIRPS.
- `published_at` no se infiere desde la fecha observada.
- Malla nacional 0.1° en EPSG:4326.
- Máscara de Perú mediante PER-ADM0 versionado en el repositorio.
- Remuestreo de una fuente fina a malla 0.1° con validación de relación de resoluciones y nodata.
- Scripts smoke históricos F3–F8.
- Documentación Obsidian + Mermaid + fuentes Archify.

### 🟩 Rama `improve/architecture-docs-tests` — CI validada

- corrección de trazabilidad temporal CHIRPS;
- corrección del contrato de regrid 0.05° → 0.1°;
- tests unitarios de ingesta y malla;
- workflow de CI con Python 3.12/pytest;
- README reescrito para distinguir implementado/planificado;
- especificación de arquitectura y catálogo de datasets;
- fuente Archify de arquitectura actual.

**Evidencia CI:** GitHub Actions run `35793090677`, job `Python 3.12 tests`, finalizado con `success`: **9 tests passed** y **76% de cobertura total** sobre el paquete actual. Esto valida los contratos unitarios incluidos en la rama, no la evaluación científica de modelos de ML.

## Evidencia histórica de smokes anteriores

El repositorio documentó una prueba local con tres días CHIRPS reales: 2024-06-15, 2024-06-16 y 2024-06-17. Esa evidencia permitió explorar preprocesamiento, pero **no es un dataset suficiente para evaluación final de Machine Learning**.

### F3 — preprocesamiento geoespacial

Evidencia registrada en la sesión previa:

- raster CHIRPS real;
- malla 0.1°;
- máscara PER-ADM0;
- outputs NPY/manifiesto local.

La implementación de `regrid_block` fue auditada posteriormente y se encontró un defecto en la relación de resoluciones; la rama de mejora lo corrige y sus contratos unitarios ya pasaron CI. Sin embargo, el smoke F3 con el raster real debe reejecutarse con esta versión para renovar la evidencia end-to-end.

### F4 — split temporal histórico

Con solo tres días disponibles se registró:

```text
train = [2024-06-15, 2024-06-16]
validation = [2024-06-17]
test = []
```

Este split demuestra únicamente el mecanismo cronológico. **No existe test final en esa prueba.**

### F5–F8

Se generaron artefactos smoke para explorar features y preparación de modelado, pero no existen en el repositorio:

- un dataset nacional multi-año Gold validado;
- benchmark LazyRegressor;
- benchmark LazyClassifier;
- modelo final persistido;
- RMSE/R² finales;
- matrices de confusión finales.

Por tanto, no se considera que la regresión o clasificación estén completadas.

## Matriz de implementación

| Requisito | Estado real |
|---|---|
| RQ-01 Dataset maestro multi-fuente | No iniciado |
| RQ-02 Regresión precipitación futura | No iniciado |
| RQ-03 Clasificación lluvia extrema | No iniciado |
| RQ-04 LazyPredict | No iniciado |
| RQ-05 Baseline | No iniciado |
| RQ-06 Split cronológico | Implementación conceptual/smoke; dataset final pendiente |
| RQ-07 Trazabilidad temporal | En desarrollo; ingesta CHIRPS mejorada y testeada |
| RQ-08 Modo retrospectivo | En desarrollo |
| RQ-09 Operativo deshabilitado | Decisión vigente |
| RQ-10 API | No iniciado |
| RQ-11 Frontend | No iniciado |
| RQ-12 Disclaimers | Documentado; aplicación pendiente |
| RQ-20 Reproducibilidad | En desarrollo; CI unitario verde |
| RQ-21 No inventar datos/métricas | Regla vigente |
| RQ-22 Registro de modelos fallidos/exitosos | Pendiente de ML |
| RQ-23 DataNote/trazabilidad académica | En desarrollo en `docs/academic/` |
| RQ-24 Entorno OpenCode/Obsidian/Graphify/Archify | Parcialmente implementado |

## Próximos hitos

1. Reejecutar F3 con la versión corregida y guardar evidencia end-to-end.
2. Auditar y ampliar la serie temporal CHIRPS.
3. Formalizar Bronze/Silver/Gold.
4. Integrar al menos una segunda fuente climática.
5. Construir dataset Gold nacional reproducible.
6. Ejecutar EDA y los dos pipelines exigidos por la rúbrica.
7. Solo después desarrollar API/web sobre resultados reales.

## Fuentes de verdad

- requisitos: [[02-requirements]];
- decisiones: [[08-decisions]];
- problemas conocidos: [[09-known-issues]];
- arquitectura: `docs/architecture/wayra-ai-specification.md`;
- datasets: `docs/sources/dataset-catalog.md`;
- rúbrica: `docs/academic/avance-2-mapping.md`.
