---
tipo: requisitos
estado: vigente
fecha: 2026-09-22
tags: [wayra, requisitos, trazabilidad]
---

# Requisitos — Wayra AI

Lista maestra de requisitos (estado por cubrir; los códigos se usan en la matriz de trazabilidad del README y en Graphify). Estados permitidos: **No iniciado · En desarrollo · Implementado sin validar · Validado · Bloqueado**.

## Funcionales
| ID | Requisito | Estado |
|---|---|---|
| RQ-01 | Dataset maestro con datos reales de múltiples fuentes | No iniciado |
| RQ-02 | Regresión `precipitation_next_day_mm` (malla 0.1° Perú) | No iniciado |
| RQ-03 | Clasificación binaria "lluvia extrema" (percentil) | No iniciado |
| RQ-04 | Comparación de modelos con LazyPredict (LazyRegressor/LazyClassifier) | No iniciado |
| RQ-05 | Baseline ingenuo explícito y comparado | No iniciado |
| RQ-06 | Split cronológico sin fuga temporal/espacial | No iniciado |
| RQ-07 | Trazabilidad `observation_time`/`published_at`/`retrieved_at`/`forecast_issued_at` | No iniciado |
| RQ-08 | Modo retrospectivo funcional | No iniciado |
| RQ-09 | Modo operativo **deshabilitado** (decisión) | No iniciado |
| RQ-10 | API `/api/v1` (salud, predicción punto/región, trazabilidad) | No iniciado |
| RQ-11 | Frontend web responsivo en español con mapa | No iniciado |
| RQ-12 | Disclaimers y no-sustitución de SENAMHI/ENFEN | No iniciado |

## No funcionales
| ID | Requisito | Estado |
|---|---|---|
| RQ-20 | Reproductibilidad (venv pined, Dockerfile de respaldo) | En desarrollo |
| RQ-21 | Sin invención de datos, métricas ni resultados | Vigente |
| RQ-22 | Registro de modelos que aciertan y que fallan | No iniciado |
| RQ-23 | Documentación: DataNote (matriz requisito→implementación) | No iniciado |
| RQ-24 | Entorno inteligente OpenCode (memoria+grafo+archify) | En desarrollo |

## Fuentes (decisión, detalle en [[docs/sources/00-fuentes]])
- CHIRPS **v3.0** diario `rnl` (ERA5-downscaled) 2001–2026 — precipitación.
- ERA5-Land (CDS/Browser API, con clave) — temperatura/viento/presión/humedad.
- NOAA ERSST (mensual+semanal) — índices Niño 1+2, 3, 3.4, 4.
- RONI/ONI: CPC `detrend.nino34.ascii.txt` (Nino3.4 detrended 3-mes).
- ICEN: serie IGP `met.igp.gob.pe/datos/ICEN.txt`.
- SENAMHI: **sin cuenta** → adaptador documentado + subset público datosabiertos.gob.pe.

Analogía de estados completa en [[10-roadmap]] y evidencia en [[07-progress]].