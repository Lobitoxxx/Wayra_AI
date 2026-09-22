"""Preprocesado geoespacial de Wayra AI — malla de trabajo 0.1° sobre Perú.

Objetivo D-005: malla **0.1°** con máscara de Perú. El remuestreo desde CHIRPS
v3.0 rnl 0.05° es *agregación por caja* (media), documentada y trazable; nunca
crea datos nuevos (RQ-21). La máscara de Perú usa límites oficiales reales
(cargados por `mask.py`), no un polígono inventado.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..config import GRID_RES_DEG, PERU_BBOX

# CHIRPS v3.0 diario rnl: resolución nativa 0.05° (fuente auditada D-004).
CHIRPS_RES_DEG = 0.05


@dataclass(frozen=True)
class Mesh:
    """Malla regular 0.1° sobre el bbox de Perú (EPSG:4326)."""

    xmin: float = PERU_BBOX[0]
    xmax: float = PERU_BBOX[1]
    ymin: float = PERU_BBOX[2]
    ymax: float = PERU_BBOX[3]
    res: float = GRID_RES_DEG

    @property
    def cols(self) -> int:
        return int(round((self.xmax - self.xmin) / self.res))

    @property
    def rows(self) -> int:
        return int(round((self.ymax - self.ymin) / self.res))

    @property
    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def lons(self) -> np.ndarray:
        return self.xmin + (np.arange(self.cols) + 0.5) * self.res

    def lats(self) -> np.ndarray:
        return self.ymax - (np.arange(self.rows) + 0.5) * self.res

    def to_meta(self) -> dict:
        return {
            "crs": "EPSG:4326",
            "resolution_deg": self.res,
            "bbox": [self.xmin, self.ymin, self.xmax, self.ymax],
            "shape": list(self.shape),
        }


def regrid_block(chirps: np.ndarray, src_geo: tuple[float, float, float, float],
                 mesh: Mesh) -> tuple[np.ndarray, Mesh]:
    """Rejilla CHIRPS (0.05°) → malla 0.1° mediante media por bloques 2×2.

    `src_geo` = (xmin, ymax, xres, yres) en grados (EPSG:4326). CHIRPS ya viene
    recortado a Perú por el adaptador; alineado con la partición de la malla.
    Devuelve (campo 0.1° con NaN en celdas sin datos, malla).
    """
    src_h, src_w = chirps.shape
    k = round(src_geo[2] / mesh.res)  # 0.05/0.1 = 0.5 → usado como factor 2 si se da

    # CHIRPS 0.05° → agrupamos 2×2 hasta la resolución de malla.
    if k < 1:
        raise ValueError(f"CHIRPS {src_geo[2]}° más grueso que malla {mesh.res}°")

    block = int(round(1 / k)) if k < 1 else int(round(k)) if k > 1 else 1
    block = max(1, block)
    h, w = src_h - src_h % block, src_w - src_w % block
    arr = chirps[:h, :w]
    pooled = arr.reshape(h // block, block, w // block, block).mean(axis=(1, 3))

    # Alinear a la malla destino (relleno con NaN fuera del bbox de Perú).
    out = np.full(mesh.shape, np.nan, dtype=np.float32)
    x = mesh.xmin + (np.arange(mesh.cols) + 0.5) * mesh.res
    y = mesh.ymax - (np.arange(mesh.rows) + 0.5) * mesh.res

    # Índices CHIRPS de cada celda (usando esquinas, no centros).
    src_x0 = src_geo[0]
    src_y0 = src_geo[1]
    ci = np.clip(np.floor((x - src_x0) / src_geo[2] - 0.5), 0, src_w - 1).astype(int)
    ri = np.clip(np.floor((src_y0 - y) / src_geo[2] - 0.5), 0, src_h - 1).astype(int)
    out[:, :] = pooled[np.ix_(ri, ci)]
    return out, mesh


def raster_to_mesh_mask(raster: np.ndarray, mesh: Mesh) -> np.ndarray:
    """Máscara de malla a partir de un raster en la misma resolución (0.1°)."""
    valid = np.isfinite(raster)
    return valid.astype(np.uint8) if valid.shape == mesh.shape else None
