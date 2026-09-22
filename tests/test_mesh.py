from __future__ import annotations

import numpy as np
import pytest

from wayra.preprocessing.mesh import Mesh, raster_to_mesh_mask, regrid_block


def test_regrid_005_to_01_uses_2x2_mean() -> None:
    mesh = Mesh(xmin=0.0, xmax=0.2, ymin=0.0, ymax=0.2, res=0.1)
    source = np.arange(16, dtype=np.float32).reshape(4, 4)

    out, returned_mesh = regrid_block(
        source,
        (0.0, 0.2, 0.05, 0.05),
        mesh,
    )

    expected = np.array([[2.5, 4.5], [10.5, 12.5]], dtype=np.float32)
    np.testing.assert_allclose(out, expected)
    assert returned_mesh == mesh


def test_regrid_ignores_declared_nodata_inside_block() -> None:
    mesh = Mesh(xmin=0.0, xmax=0.1, ymin=0.0, ymax=0.1, res=0.1)
    source = np.array([[1.0, -9999.0], [3.0, 5.0]], dtype=np.float32)

    out, _ = regrid_block(
        source,
        (0.0, 0.1, 0.05, 0.05),
        mesh,
        nodata=-9999.0,
    )

    np.testing.assert_allclose(out, np.array([[3.0]], dtype=np.float32))


def test_regrid_rejects_non_integer_resolution_ratio() -> None:
    mesh = Mesh(xmin=0.0, xmax=0.2, ymin=0.0, ymax=0.2, res=0.1)
    source = np.ones((4, 4), dtype=np.float32)

    with pytest.raises(ValueError, match="múltiplo entero"):
        regrid_block(source, (0.0, 0.24, 0.06, 0.06), mesh)


def test_regrid_rejects_destination_outside_source_coverage() -> None:
    mesh = Mesh(xmin=0.0, xmax=0.3, ymin=0.0, ymax=0.3, res=0.1)
    source = np.ones((4, 4), dtype=np.float32)

    with pytest.raises(ValueError, match="fuera de la cobertura"):
        regrid_block(source, (0.0, 0.2, 0.05, 0.05), mesh)


def test_raster_to_mesh_mask_requires_matching_shape() -> None:
    mesh = Mesh(xmin=0.0, xmax=0.2, ymin=0.0, ymax=0.2, res=0.1)
    raster = np.array([[1.0, np.nan], [4.0, 5.0]], dtype=np.float32)

    mask = raster_to_mesh_mask(raster, mesh)
    np.testing.assert_array_equal(mask, np.array([[1, 0], [1, 1]], dtype=np.uint8))

    with pytest.raises(ValueError, match="no coincide"):
        raster_to_mesh_mask(np.ones((1, 1), dtype=np.float32), mesh)
