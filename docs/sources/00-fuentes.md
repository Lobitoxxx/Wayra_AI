---
tipo: fuentes
estado: auditar_en_2026-09-22
fecha: 2026-09-22
---

# Registro de fuentes de datos — Wayra AI

> Regla: indicar versión, cobertura, licencia, latencia de publicación, estado de acceso y `retrieved_at` de cada verificación.

## Precipitación
| Campo | Valor |
|---|---|
| Fuente | **CHIRPS v3.0** diario, variante **`rnl`** (downscaled con ERA5) |
| URLs | `https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/rnl/{year}/chirps-v3.0.rnl.YYYY.MM.DD.tif` (+ `prelim/`) |
| Cobertura | 60N–60S, 0.05°, **1981→NRT**; diario final disponible ~3ª semana del mes siguiente |
| Tamaño | ~13–18 MiB/archivo (global) |
| Verificado | ✓ 2026-09-22 (estructura y nombres; existe `p25` y `cogs`) |

## Temperatura / viento / presión / humedad
| Campo | Valor |
|---|---|
| Fuente | **ERA5-Land** (CDS/Browser API) |
| URL | `https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land` |
| Acceso | Cuenta gratuita + API key (en `.env`, `cdsapirc`) |
| Variables | t2m, d2m, sp, u10, v10, tp (conversiones: K→°C, m→mm) |
| Estado | **Requiere credencial** — pendiente (IS-06) |

## Índices oceánicos (NOAA)
| Campo | Valor |
|---|---|
| Mensual | `https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii` (yr mon NINO1+2/3/3.4/4 ANOM; base 1991–2020) |
| Semanal | `https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for` (SST/SSTA 1981→) |
| Verificado | ✓ 2026-09-22 |

## RONI / ONI
| Campo | Valor |
|---|---|
| URL | `https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt` (YR MON TOTAL ClimAdjust ANOM) |
| Anotación | RONI = variante Nino3.4 detrended 3-mes; fuentes `roni.data` estaban 404 (IS-03) |
| Verificado | ✓ 2026-09-22 (archivo descargado y revisado) |

## ICEN (ENFEN/IMARPE)
| Campo | Valor |
|---|---|
| Serie | `http://met.igp.gob.pe/datos/ICEN.txt` (IGP: yy mm ICEN) |
| Oficial | `https://siofen.imarpe.gob.pe/nivel2/indice-costero-el-nino-icen` |
| Nota | Metodología ENFEN 2012; Nota Técnica ENFEN 01-2024 la actualiza |
| Estado | Verificado en auditoría; formato de archivo a confirmar en F2 |

## SENAMHI
| Campo | Valor |
|---|---|
| Portal | `https://www.datosabiertos.gob.pe/dataset/datos-hidrometeorol%C3%B3gicos-de-libre-acceso` |
| Acceso | Descarga completa requiere **registro/contraseña** → sin cuenta ahora (IS-05) |
| Alternativa | Subset público de estaciones de intercambio (CSV) |

## Límites geográficos
| Campo | Valor |
|---|---|
| Límite nacional | Natural Earth (Geopandas) / GeoBoundaries; departamentos SIGRID |
| Estado | Para hacer en F3 (geospatial) |

Registrar cada descarga real en manifiestos con checksum (`data/raw/manifiestos/`).