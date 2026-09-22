"""Rasteriza el limite oficial real de Peru (PER-ADM0, D-006) sobre la malla.

Regla RQ-21/RQ-22: la mascara NUNCA se inventa. Se rasteriza el GeoJSON
oficial real que ya esta en disco (data/external/geoboundaries/PER-ADM0/...),
firmado con sha256 en D-006. Cero geometria propia.

La funcion `peru_mask` devuelve uint8: 1 = celda 0.1 que toca territorio
oficial peruano, 0 = fuera. `rasterize` usa rasterio.features sobre el
transform de la malla (EPSG:4326).
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, cast

import numpy as np

try:
    import rasterio
    from rasterio import features as rio_features
    from rasterio.transform import from_origin

    _HAS_RASTERIO = True
except Exception:  # pragma: no cover - sin rasterio se reporta, no se inventa
    _HAS_RASTERIO = False


@lru_cache(maxsize=1)
def load_peru_official() -> dict:
    """GeoJSON oficial real de Peru ADM0 (fuente auditada en disco, D-006)."""
    from ..config import GEO_BOUNDARIES

    with GEO_BOUNDARIES.open(encoding="utf-8") as fh:
        return cast(dict, json.load(fh))


def peru_mask(mesh: Any, res_deg: float = 0.1) -> np.ndarray:
    """Mascara oficial de Peru sobre la malla `mesh` (EPSG:4326, res_deg)."""
    if not _HAS_RASTERIO:
        raise RuntimeError("rasterio no instalado; no se puede rasterizar (RQ-22)")

    gj = load_peru_official()
    feats = gj.get("features", [])
    if not feats:
        raise ValueError("GeoJSON oficial sin features (RQ-22)")

    # Alineacion georeferenciada: de la config, no inventada.
    from ..config import GRID_RES_DEG, PERU_BBOX

    xmin, xmax, ymin, ymax = PERU_BBOX
    rows, cols = mesh.shape
    transform = from_origin(xmin, ymax, GRID_RES_DEG, GRID_RES_DEG)

    geoms = [f["geometry"] for f in feats if f.get("geometry")]
    mask = rio_features.rasterize(
        shapes=geoms,
        out_shape=(rows, cols),
        transform=transform,
        fill=0,
        dtype="uint8",
        all_touched=True,
    )
    return mask.astype(np.uint8)
