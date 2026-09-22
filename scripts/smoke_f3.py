"""SMOKE F3 - preprocesado geoespacial sobre datos reales en disco.

Requisitos de entrada:
- un TIFF CHIRPS v3.0 RNL real descargado previamente;
- el límite PER-ADM0 versionado en ``data/external/geoboundaries``;
- rasterio y numpy instalados.

El script no inventa datos ni convierte una ejecución pasada en evidencia actual:
la salida del comando debe conservarse si se quiere afirmar que una versión del
código fue validada.
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

from wayra.config import DATA_PROCESSED, GEO_BOUNDARIES, GRID_RES_DEG, PERU_BBOX  # noqa: E402
from wayra.preprocessing.mask import peru_mask  # noqa: E402
from wayra.preprocessing.mesh import Mesh, regrid_block  # noqa: E402

TIF = (
    ROOT
    / "data"
    / "raw"
    / "chirps-rnl"
    / "daily"
    / "2024"
    / "chirps-v3.0.rnl.2024.06.15.tif"
)


def main() -> int:
    t0 = time.perf_counter()

    if not TIF.is_file():
        print("FALLA: CHIRPS real no está en disco:", TIF)
        return 2
    if not GEO_BOUNDARIES.is_file():
        print("FALLA: límite oficial no está en disco:", GEO_BOUNDARIES)
        return 2

    mesh = Mesh()
    print("Mesh:", mesh.shape, "res", mesh.res)

    try:
        import rasterio
    except ImportError as exc:
        print("SIN_RASTERIO", exc)
        return 1

    with rasterio.open(TIF) as ds:
        chirps = ds.read(1).astype(np.float32)
        geo = (ds.bounds.left, ds.bounds.top, ds.res[0], ds.res[1])
        nodata = ds.nodata
        print(
            "CHIRPS:",
            TIF.name,
            "shape",
            chirps.shape,
            "geo",
            geo,
            "nodata",
            nodata,
        )

    field, mesh_out = regrid_block(chirps, geo, mesh, nodata=nodata)
    print("Regrid ->", field.shape, "mesh_out", mesh_out)

    mask = peru_mask(mesh)
    print(
        "Máscara Perú celdas=",
        int((mask > 0).sum()),
        "shape=",
        mask.shape,
    )

    out_dir = DATA_PROCESSED / "preprocessing" / "F3"
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "field_0p1.npy", field)
    np.save(out_dir / "mask_peru_0p1.npy", mask)

    manifest = {
        "fase": "F3",
        "crs": "EPSG:4326",
        "res_deg": GRID_RES_DEG,
        "bbox": list(PERU_BBOX),
        "mesh_shape": list(mesh.shape),
        "chirps_tif": TIF.name,
        "chirps_sha256": hashlib.sha256(TIF.read_bytes()).hexdigest(),
        "source_nodata": nodata,
        "regrid": "block-mean",
        "mask_src": str(GEO_BOUNDARIES),
        "mask_celdas_peru": int((mask > 0).sum()),
        "finite_cells": int(np.isfinite(field).sum()),
        "duracion_s": round(time.perf_counter() - t0, 3),
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "manifest.jsonl").write_text(
        json.dumps(manifest, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("MANIFEST_OK", json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
