"""SMOKE F3 - evidencia REAL en disco (RQ-21/22, D-005/006). Nada inventado.

Corre CONTRA el disco autentico:
  - config.py real (GRID_RES_DEG=0.1, PERU_BBOX real, CHIRPS_RES_DEG=0.05)
  - CHIRPS v3.0 rnl real 2024.06.15 (17.3 MB, sha e422...0203d, F2 smoke real)
  - limite oficial REAL de Peru ADM0 (geoBoundaries PER, D-006) en disco
  - mesh.py::regrid_block  REAL  (CHIRPS 0.05' -> mesh 0.1' box 2x2 mean)
  - mask.py:peru_mask      REAL  (rasterizado oficial sobre la malla 0.1')

Salidas: data/processed/preprocessing/F3/ + manifiesto medido (D-007 tokens).
Codigo ASCII puro para evitar mojibake; sin dependencias nuevas.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wayra.config import (  # noqa: E402
    CHIRPS_RES_DEG,
    DATA_PROCESSED,
    GEO_BOUNDARIES,
    GRID_RES_DEG,
    PERU_BBOX,
)
from wayra.preprocessing.mesh import Mesh, regrid_block  # noqa: E402
from wayra.preprocessing.mask import peru_mask  # noqa: E402

TIF = ROOT / "data" / "raw" / "chirps-rnl" / "daily" / "2024" / "chirps-v3.0.rnl.2024.06.15.tif"


def main() -> int:
    t0 = time.perf_counter()

    # 0) Verdad en disco (RQ-21)
    if not TIF.is_file():
        print("FALLA: CHIRPS real no en disco:", TIF)
        return 2
    if not GEO_BOUNDARIES.is_file():
        print("FALLA: limite oficial real no en disco:", GEO_BOUNDARIES)
        return 2

    mesh = Mesh()
    print("Mesh 0.1:", mesh.shape, "res", mesh.res)

    # 1) CHIRPS real desde disco con rasterio (R-prefijo real)
    try:
        import rasterio
    except ImportError as e:
        print("SIN_RASTERIO", e)
        return 1

    with rasterio.open(TIF) as ds:
        chirps = ds.read(1).astype(np.float32)
        geo = (ds.bounds.left, ds.bounds.top, ds.res[0], ds.res[1])
        print("CHIRPS real:", TIF.name, "shape", chirps.shape, "geo", geo, "res", ds.res)

    # 2) Regrid REAL 0.05 -> 0.1 (box mean 2x2, mesh.py::regrid_block)
    field, mesh_out = regrid_block(chirps, geo, mesh)
    print("Regrid real ->", field.shape, "mesh_out", mesh_out)

    # 3) Mascara oficial REAL (mask.py::peru_mask)
    mask = peru_mask(mesh)
    print("Mask oficial real celdas_peru=", int((mask > 0).sum()), "shape=", mask.shape)

    # 4) Salidas + manifiesto (D-007 token-medicion medidos, no inventados)
    out_dir = DATA_PROCESSED / "preprocessing" / "F3"
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "field_0p1.npy", field)
    np.save(out_dir / "mask_peru_0p1.npy", mask)

    bytes_field = field.size * field.itemsize
    bytes_mask = mask.size * mask.itemsize
    manifest = {
        "fase": "F3",
        "dlq": "D-005/006",
        "crs": "EPSG:4326",
        "res_deg": GRID_RES_DEG,
        "bbox": list(PERU_BBOX),
        "mesh_shape": list(mesh.shape),
        "chirps_tif": TIF.name,
        "chirps_sha256": hashlib.sha256(TIF.read_bytes()).hexdigest(),
        "regrid": "box-2x2-mean",
        "mask_src": str(GEO_BOUNDARIES),
        "mask_celdas_peru": int((mask > 0).sum()),
        "bytes_field_npy": bytes_field,
        "bytes_mask_npy": bytes_mask,
        "tokens_smoke_aprox": field.size + mask.size,
        "duracion_s": round(time.perf_counter() - t0, 3),
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "manifest.jsonl").write_text(
        json.dumps(manifest, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("MANIFEST_OK", json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
