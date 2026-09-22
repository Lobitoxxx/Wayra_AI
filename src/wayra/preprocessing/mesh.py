"""Malla climática nacional y remuestreo reproducible para Wayra AI.

La malla de trabajo es 0.1° en EPSG:4326. CHIRPS v3 diario se distribuye a
0.05°, por lo que el caso esperado es una agregación 2x2. Este módulo valida la
relación de resoluciones y evita inferencias silenciosas cuando las rejillas no
son compatibles.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..config import GRID_RES_DEG, PERU_BBOX

CHIRPS_RES_DEG = 0.05


@dataclass(frozen=True)
class Mesh:
    """Malla regular sobre el bbox de Perú en EPSG:4326."""

    xmin: float = PERU_BBOX[0]
    xmax: float = PERU_BBOX[1]
    ymin: float = PERU_BBOX[2]
    ymax: float = PERU_BBOX[3]
    res: float = GRID_RES_DEG

    def __post_init__(self) -> None:
        if self.res <= 0:
            raise ValueError("La resolución de malla debe ser positiva.")
        if self.xmax <= self.xmin or self.ymax <= self.ymin:
            raise ValueError("BBox de malla inválido.")

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

    def to_meta(self) -> dict[str, object]:
        return {
            "crs": "EPSG:4326",
            "resolution_deg": self.res,
            "bbox": [self.xmin, self.ymin, self.xmax, self.ymax],
            "shape": list(self.shape),
        }


def regrid_block(
    chirps: np.ndarray,
    src_geo: tuple[float, float, float, float],
    mesh: Mesh,
    *,
    nodata: float | None = None,
) -> tuple[np.ndarray, Mesh]:
    """Agrega una rejilla regular más fina a la malla de Wayra.

    Parameters
    ----------
    chirps:
        Matriz 2-D ordenada de norte a sur y oeste a este.
    src_geo:
        ``(xmin, ymax, xres, yres)`` en grados, EPSG:4326. Las resoluciones
        deben ser positivas.
    mesh:
        Malla destino.
    nodata:
        Valor nodata opcional. Si se proporciona, se convierte a ``NaN`` antes
        de calcular medias de bloque.

    Notes
    -----
    La relación ``mesh.res / src_res`` debe ser un entero. Para CHIRPS 0.05° y
    Wayra 0.1° el factor es 2. Las medias ignoran ``NaN``; si todo un bloque es
    ``NaN``, el resultado también será ``NaN``.
    """
    if chirps.ndim != 2:
        raise ValueError("La rejilla fuente debe ser una matriz 2-D.")

    src_xmin, src_ymax, src_xres, src_yres = src_geo
    if src_xres <= 0 or src_yres <= 0:
        raise ValueError("Las resoluciones fuente deben ser positivas.")
    if not np.isclose(src_xres, src_yres, rtol=0, atol=1e-9):
        raise ValueError("Wayra requiere píxeles fuente cuadrados para block-mean.")

    ratio = mesh.res / src_xres
    block = int(round(ratio))
    if block < 1 or not np.isclose(ratio, block, rtol=0, atol=1e-9):
        raise ValueError(
            "La resolución destino debe ser un múltiplo entero de la fuente: "
            f"fuente={src_xres}°, destino={mesh.res}°."
        )

    src_h, src_w = chirps.shape
    h = src_h - (src_h % block)
    w = src_w - (src_w % block)
    if h == 0 or w == 0:
        raise ValueError("La rejilla fuente es demasiado pequeña para agregarla.")

    arr = np.asarray(chirps[:h, :w], dtype=np.float32)
    if nodata is not None:
        arr = np.where(np.isclose(arr, nodata), np.nan, arr)

    blocks = arr.reshape(h // block, block, w // block, block)
    with np.errstate(invalid="ignore"):
        pooled = np.nanmean(blocks, axis=(1, 3)).astype(np.float32)

    pooled_res = src_xres * block
    if not np.isclose(pooled_res, mesh.res, rtol=0, atol=1e-9):
        raise AssertionError("Resolución agregada inconsistente con la malla destino.")

    x = mesh.lons()
    y = mesh.lats()
    ci = np.floor((x - src_xmin) / pooled_res).astype(int)
    ri = np.floor((src_ymax - y) / pooled_res).astype(int)

    if (
        ci.min(initial=0) < 0
        or ri.min(initial=0) < 0
        or ci.max(initial=-1) >= pooled.shape[1]
        or ri.max(initial=-1) >= pooled.shape[0]
    ):
        raise ValueError(
            "La malla destino cae fuera de la cobertura de la rejilla fuente."
        )

    out = pooled[np.ix_(ri, ci)].astype(np.float32, copy=False)
    if out.shape != mesh.shape:
        raise AssertionError(
            f"Salida {out.shape} no coincide con malla destino {mesh.shape}."
        )
    return out, mesh


def raster_to_mesh_mask(raster: np.ndarray, mesh: Mesh) -> np.ndarray:
    """Convierte un ráster de la misma forma en una máscara ``uint8``."""
    if raster.shape != mesh.shape:
        raise ValueError(
            f"Ráster {raster.shape} no coincide con malla {mesh.shape}."
        )
    return np.isfinite(raster).astype(np.uint8)
