"""smoke_f5.py: field real de train para D-009 (un día CHIRPS 0.1° + máscara).

RQ-21/22: toma un día CHIRPS REAL (06.15), aplica regrid_block 0.05→0.1,
aplica peru_mask, y salva el field de train. Todo con módulos ya auditados
(mesh.py, mask.py). Nada se inventa.

Uso: uv run python scripts\\smoke_f5.py
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "chirps-rnl" / "daily" / "2024"
OUT = ROOT / "data" / "processed" / "preprocessing" / "F5"

# Día real de train (06.15 ya procesado en F3)
DIA = "2024.06.15"
TIF = RAW / f"chirps-v3.0.rnl.{DIA}.tif"

def main() -> int:
    t0 = time.perf_counter()

    # 1) Día CHIRPS REAL en disco (ya descargado en F2+F4).
    if not TIF.is_file():
        print("ERROR: día CHIRPS real no en disco:", TIF)
        return 2

    # 2) Regrid 0.05→0.1 con módulo auditado (mesh.py).
    import rasterio
    from wayra.preprocessing.mesh import Mesh, regrid_block
    from wayra.preprocessing.mask import peru_mask

    mesh = Mesh()
    with rasterio.open(TIF) as ds:
        arr = ds.read(1).astype(np.float32)
        geo = (ds.bounds.left, ds.bounds.top, ds.res[0], ds.res[1])
    field, _ = regrid_block(arr, geo, mesh)

    # 3) Máscara Perú REAL oficial (mask.py).
    mask = peru_mask(mesh)
    train_field = np.where(mask > 0, field, np.nan).astype(np.float32)

    # 4) Salida + manifiesto (RQ-22).
    OUT.mkdir(parents=True, exist_ok=True)
    np.save(OUT / "train_field.npy", train_field)
    np.save(OUT / "train_mask.npy", mask)

    sha = hashlib.sha256(TIF.read_bytes()).hexdigest()
    man = {
        "fase": "F5",
        "objetivo": "D-009 (train field listo)",
        "dia_real": DIA,
        "field_shape": train_field.shape,
        "mask_celdas_peru": int((mask > 0).sum()),
        "field_sha256": sha,
        "duracion_s": round(time.perf_counter() - t0, 4),
        "tokens_smoke_aprox": train_field.size,
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    (OUT / "manifest_F5.jsonl").write_text(
        json.dumps(man, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("F5_OK", json.dumps(man, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
