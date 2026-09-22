---
tipo: módulos
estado: propuesta
fecha: 2026-09-22
tags: [wayra, modulos]
---

# Módulos — Wayra AI

> Estado: **PROPUESTA**. Sin código funcional todavía (excepto entornos/config de esta configuración).

## Módulos del pipeline (propuestos)
| Módulo | Responsabilidad | Entregable clave |
|---|---|---|
| `src.ingestion` | Descargar y validar fuentes (CHIRPS v3.0/NOAA/RONI/ICEN/ERA5-Land/SENAMHI opcional) | Manifiestos con checksum, `retrieved_at` |
| `src.preprocessing` | QC, limpieza, regrid, malla 0.1° Perú | Particiones parquet `processed` |
| `src.geospatial` | Máscara, regiones, vecindades | Layer de celdas/regiones |
| `src.features` | Ventanas de lluvia, anomalías, índices (por `published_at`), estacionalidad | Feature store |
| `src.models` | LazyPredict (reg/class), baseline, splits | Modelo(s) pined + registro fallos |
| `src.evaluation` | Métricas por split/región, matrices | Tablas + diagramas |
| `src.inference` | Predicción con `forecast_issued_at`; modo retrospectivo | Servicio interno |
| `apps.api` | API REST de predicción y trazabilidad | OpenAPI |
| `apps.web` | UI en español (mapa Perú, retrospectiva) | Página estática |

## Módulos del entorno (implementados ✓)
| Módulo | Ubicación |
|---|---|
| Memoria (Obsidian md) | `docs/knowledge/` + `sessions/` |
| Skills Obsidian | `wayra-ai/.agents/skills/` |
| Diagramas Archify | `docs/architecture/diagrams/` |
| Fuentes de datos | `docs/sources/` |

Enlaces: arquitectura [[03-architecture]], datos [[06-data-model]].