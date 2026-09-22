"""smoke_f7.py: modelado D-009 preparado (train_field + features listos).

RQ-21/22: verifica que train_field REAL de F5 y features de F6 estén
listos para modelado con LazyPredict u otros modelos. Nada se inventa.

Uso: uv run python scripts\\smoke_f7.py
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "preprocessing" / "F7"

def main() -> int:
    t0 = time.perf_counter()

    # 1) Carga train_field REAL de F5 y features de F6.
    train_field = np.load(ROOT / "data" / "processed" / "preprocessing" / "F5" / "train_field.npy")
    features = np.load(ROOT / "data" / "processed" / "preprocessing" / "F6" / "features.npy")
    feature_names = np.load(ROOT / "data" / "processed" / "preprocessing" / "F6" / "feature_names.npy")
    print("F7 train_field real shape:", train_field.shape, "n_features:", len(features))

    # 2) Modelado baseline (D-009) preparado.
    # En la realidad, aquí usarías LazyPredict u otros modelos con los features reales.
    # Por ahora, verificamos que los datos estén listos para modelado.
    print("F7 Datos listos para modelado: train_field y features disponibles")
    print("   - Forma del campo:", train_field.shape)
    print("   - Número de features:", len(features))
    print("   - Lista de features:", feature_names.tolist())

    # 3) Salida + manifiesto (RQ-22).
    OUT.mkdir(parents=True, exist_ok=True)
    np.save(OUT / "train_field.npy", train_field)
    np.save(OUT / "features.npy", features)
    np.save(OUT / "feature_names.npy", feature_names)

    sha = hashlib.sha256(train_field.tobytes()).hexdigest()
    man = {
        "fase": "F7",
        "objetivo": "D-009 (modelado preparado)",
        "train_field_shape": train_field.shape,
        "n_features": len(features),
        "features": feature_names.tolist(),
        "field_sha256": sha,
        "duracion_s": round(time.perf_counter() - t0, 4),
        "tokens_smoke_aprox": train_field.size + len(features) * 10,
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    (OUT / "manifest_F7.jsonl").write_text(
        json.dumps(man, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("F7_OK", json.dumps(man, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())