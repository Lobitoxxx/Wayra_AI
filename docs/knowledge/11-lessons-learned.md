---
tipo: lecciones
estado: vigente
fecha: 2026-09-22
tags: [wayra, lecciones]
---

# Lecciones aprendidas — Wayra AI

## OpenCode / herramientas (verificadas 2026-09-22)
1. **`npx skills add` instala en el directorio de ejecución** (`.agents/skills/`), no global. Ejecutar con `workdir` en la raíz del repo o mover el resultado. (→ IS-08)
2. **PowerShell bloquea npm/npx** por ExecutionPolicy: usar `cmd /c "npx ..."`. (→ IS-02)
3. **`opencode` CLI no está en PATH**; la configuración vive en `~/.config/opencode/` (opencode.json/opencode.jsonc con claves → no tocar).
4. **`git branch -m main`** al iniciar repo con git que aún usa `master` por defecto.
5. Los directorios con `.gitkeep` permiten versionar estructura vacía respetando `.gitignore` de datos.

## Datos (verificadas)
1. **CHIRPS v3.0 existe** (release 2025-01-01) con diario `rnl`/`sat` bajo `daily/final/`; global 0.05° (~13–18 MiB/archivo).
2. **CHIRTSdaily solo llega a 2016** → no es fuente de temperatura actual.
3. **RONI 404 en varios endpoints CDC/PSL**; el archivo `detrend.nino34.ascii.txt` sigue funcionando.

Regla: mover problemas resueltos aquí desde [[09-known-issues]] con fecha.