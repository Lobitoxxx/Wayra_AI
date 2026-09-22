"""Configuración central Wayra AI (D-005, D-006).

Única fuente de verdad para la resolución de malla, bbox de Perú y rutas.
Nada aquí se "declara" sin evidencia: cada constante refiere a D-005/D-006 o a
un límite oficial real cargado por `mask.py` (RQ-21/22).
"""

from __future__ import annotations

from pathlib import Path

# Ruta raíz del proyecto (wayra-ai/). Este archivo vive en src/wayra/
# → parents[0]=wayra, [1]=src, [2]=wayra-ai.
ROOT = Path(__file__).resolve().parents[2]

# Resolución de trabajo de Wayra (D-005): malla 0.1°.
GRID_RES_DEG = 0.1

# CHIRPS v3.0 rnl nativo (fuente auditada, D-004 → 0.05°).
CHIRPS_RES_DEG = 0.05

# Bbox continental de trabajo sobre Perú (EPSG:4326), (xmin, xmax, ymin, ymax).
# Marco de referencia: da cobertura de todo Perú incluyendo la Amazonía llanura
# y el altiplano. El límite *preciso* es el oficial de geoBoundaries (mask.py).
PERU_BBOX = (-81.5, -68.0, -18.7, -0.5)

# Datos.
DATA_RAW = ROOT / "data" / "raw"
DATA_EXTERNAL = ROOT / "data" / "external"
DATA_PROCESSED = ROOT / "data" / "processed"
GEO_BOUNDARIES = DATA_EXTERNAL / "geoboundaries" / "PER-ADM0" / "geoBoundaries-PER-ADM0.geojson"
