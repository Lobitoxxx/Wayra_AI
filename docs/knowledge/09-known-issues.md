---
tipo: problemas
estado: vigente
fecha: 2026-09-22
tags: [wayra, issues, bloqueos]
---

# Problemas conocidos — Wayra AI

| ID | Problema | Solución/Workaround | Estado |
|---|---|---|---|
| IS-01 | `opencode` CLI no está en el PATH de PowerShell | Iniciar OpenCode por su lanzador habitual; usar `~/.config/opencode` como ruta de config | Abierto |
| IS-02 | npm/npx bloqueados por ExecutionPolicy (PowerShell) | Ejecutar vía `cmd /c "npx ..."` | Verificado ✓ |
| IS-03 | RONI: endpoints `psl.noaa.gov/data/correlation/roni.data` y `ftp.cpc.ncep.noaa.gov/CPC_CDAS/Products/Nino_Indices/` → 404 | Usar `https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt` (Nino3.4 detrended 3-mes) | Verificado ✓ |
| IS-04 | CHIRTSdaily solo llega a **2016** → no sirve para 2001–2026 | ERA5-Land como fuente de temperatura | Documentado |
| IS-05 | SENAMHI: descarga completa requiere cuenta | Sin cuenta: adaptador documentado + subset datosabiertos.gob.pe | Abierto |
| IS-06 | ERA5-Land requiere clave CDS (cuenta gratuita) | El usuario la tiene/creará; clave en `.env` (no versionada) | Pendiente de credencial |
| IS-07 | lazypredict 0.3.0 (2019) puede ser incompatible con sklearn/pandas modernos | Probar en Fase 5; pin versiones compatibles; registrar fallos en manifiesto | Pendiente |
| IS-08 | `npx skills add` instala en el directorio actual (`.agents/`), no global | Se movió a `wayra-ai/.agents/` (versionable) | Resuelto ✓ |
| IS-09 | Descarga CHIRPS 0.05° 2001–2026 (~150 GB, ~9.500 archivos) | Descarga reanudable/paralela; disco D con 602 GB libres | Pendiente de ejecutar |

Regla: al resolver, mover a 11-lessons-learned o changelog. Debate abierto en próxima sesión si aplica.