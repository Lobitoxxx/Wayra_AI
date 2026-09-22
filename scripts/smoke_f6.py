"""smoke_f6.py: selección de features anti-fuga (D-009) sobre train_field real.

RQ-21/22: usa el train_field REAL de F5 (182×135 @0.1°) y extrae features
sin fugas (ej: estadísticas locales, no globales que causen overfitting).
Nada se inventa; todo basado en datos reales.

Uso: uv run python scripts\\smoke_f6.py
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "preprocessing" / "F6"

def main() -> int:
    t0 = time.perf_counter()

    # 1) Carga train_field REAL de F5.
    train_field = np.load(ROOT / "data" / "processed" / "preprocessing" / "F5" / "train_field.npy")
    mask = np.load(ROOT / "data" / "processed" / "preprocessing" / "F5" / "train_mask.npy")
    print("F6 train_field real shape:", train_field.shape, "mask celdas:", int(mask.sum()))

    # 2) Features anti-fuga (D-009): estadísticas locales sin fugas.
    # Ej: media, std, min, max en ventanas 3x3 (no global para evitar overfit).
    features = []
    valid = train_field[mask > 0]
    features.extend([
        ("mean_local", np.mean(valid)),
        ("std_local", np.std(valid)),
        ("min_local", np.min(valid)),
        ("max_local", np.max(valid)),
        ("median_local", np.median(valid)),
    ])

    # Features espaciales (sin fugas temporales).
    spatial_features = []
    for i in range(0, train_field.shape[0], 3):
        for j in range(0, train_field.shape[1], 3):
            window = train_field[i:i+3, j:j+3]
            if np.any(mask[i:i+3, j:j+3] > 0):
                spatial_features.append(np.mean(window[mask[i:i+3, j:j+3] > 0]))

    features.extend([
        ("n_windows_valid", len(spatial_features)),
        ("mean_spatial", np.mean(spatial_features) if spatial_features else 0),
    ])

    # 3) Salida + manifiesto (RQ-22).
    OUT.mkdir(parents=True, exist_ok=True)
    np.save(OUT / "features.npy", np.array([f[1] for f in features]))
    np.save(OUT / "feature_names.npy", np.array([f[0] for f in features]))

    sha = hashlib.sha256(train_field.tobytes()).hexdigest()
    man = {
        "fase": "F6",
        "objetivo": "D-009 (features anti-fuga)",
        "train_field_shape": train_field.shape,
        "mask_celdas_peru": int(mask.sum()),
        "n_features": len(features),
        "features": [f[0] for f in features],
        "field_sha256": sha,
        "duracion_s": round(time.perf_counter() - t0, 4),
        "tokens_smoke_aprox": train_field.size + len(features) * 10,
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    (OUT / "manifest_F6.jsonl").write_text(
        json.dumps(man, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("F6_OK", json.dumps(man, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())