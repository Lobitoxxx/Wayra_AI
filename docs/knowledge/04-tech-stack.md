---
tipo: tech-stack
estado: vigente
fecha: 2026-09-22
tags: [wayra, stack, tecnologias]
---

# Stack tecnológico — Wayra AI

Se distingue **decidido** (aprobado), **propuesto** (pendiente de confirmación) e **implementado** (verificado con evidencia).

## Entorno de desarrollo (decidido)
| Elemento | Decisión | Evidencia |
|---|---|---|
| Gestor de entorno | **uv** + CPython **3.12** (venv en `wayra-ai/.venv`) | Decisión D-002 → [[08-decisions]] |
| Python | 3.12 (vía uv); local también hay 3.14 y 3.11 | `uv python` |
| Control de versiones | Git, rama `main` | `wayra-ai/.git` |

## Stack del pipeline (propuesto / por confirmar)
- **Ciencia/geo**: pandas 3.x, numpy, xarray, rioxarray, rasterio 1.5.1, geopandas 1.1.x, shapely 2.x, scipy, dask o duckdb, netCDF4, pyarrow.
- **ML**: scikit-learn 1.9.x, **lazypredict 0.3.0** (riesgo: fecha 2019; pendiente de probar en F5), joblib, imbalanced-learn.
- **API**: FastAPI 0.141.x, uvicorn, pydantic 2.x.
- **Web**: frontend vanilla/JS (a decidir), HTML/CSS, librería de mapas (a decidir).
- **Infra**: Docker + docker-compose (respaldo).

## Stack del entorno inteligente (implementado ✓)
| Herramienta | Version | Ubicación | Estado |
|---|---|---|---|
| Skills Obsidian (6) | — | `wayra-ai/.agents/skills/` | ✓ instaladas |
| Graphify skill | — | `~/.config/opencode/skills/graphify` | ✓ skill; **CLI pendiente** |
| Archify | v2.17.0-dev.1 | `~/.config/opencode/skills/archify` | ✓ instalado |

## No usar
- Python 3.14 para el stack científico (riesgo de ruedas/lazypredict) salvo necesidad.
- CDS sin clave: se documenta como limitación.

Verificar versiones reales antes de reportar como implementado. Fuente viva de decisiones: [[08-decisions]].