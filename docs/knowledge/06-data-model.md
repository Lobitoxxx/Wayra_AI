---
tipo: datos
estado: propuesta
fecha: 2026-09-22
tags: [wayra, datos, schema]
---

# Modelo de datos — Wayra AI

> Estado: **PROPUESTA**. Esquema objetivo del dataset maestro, a validar con datos reales en fase de ingesta.

## Trazabilidad temporal (obligatoria en toda fila)
| Campo | Significado |
|---|---|
| `forecast_issued_at` | Cuándo se emitió la predicción (solo inferencia) |
| `observation_time` | Fecha del fenómeno observado (día calendario) |
| `published_at` | Fecha de disponibilidad de la fuente (política de lag) |
| `retrieved_at` | Fecha de descarga por nuestro pipeline |

## Registro maestro (por celda ~0.1°, por día)
- `cell_id` (o `lat`,`lon`), `region` (costa/sierra/selva u otra), `date`.
- **Chips de grilla**: `precipitation_mm` (CHIRPS v3.0 rnl), `t2m_mean_k/_c`, `dewpoint_temperature`, `surface_pressure`, `u10/v10` (ERA5-Land si hay clave), conversión velocidad del viento.
- **Features derivadas**: acumulados/medias móviles de precipitación, anomalías, para la ventana previa.
- **Índices (match por `published_at`)**: Niño1+2, Niño3, Niño3.4, Niño4 (ERSST5), RONI (CPC detrended), ICEN (IGP).
- **Targets**: `precipitation_next_day_mm` (regresión); `extreme_next_day` (clasificación, umbral por percentil a investigar).

## Particionado físico (propuesto)
`data/processed/{year}/{month}/part-*.parquet` + catálogo DuckDB/índice para consultas.

## Almacenamiento
- `data/raw` (descargas originales), `data/interim` (limpieza intermedia), `data/processed` (modelado). No versionar volumen; sí los manifiestos.

Limitación conocida: sin clave CDS no hay variables ERA5-Land (se documenta, ver [[09-known-issues]]).