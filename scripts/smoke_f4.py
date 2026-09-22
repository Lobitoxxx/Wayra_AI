"""smoke_f4.py: split temporal REAL de los N dias CHIRPS reales en disco.

RQ-07/08/21/31 + D-008: la particion es CRONOLOGICA (nunca aleatoria), los
splits materializan los dias REALES en disco, y el manifiesto registra
sha256 + n_days + duracion medida. Nada se inventa (RQ-21).

Uso (en la raiz wayra-ai/):  uv run python scripts\\smoke_f4.py
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "chirps-rnl" / "daily" / "2024"
OUT = ROOT / "data" / "processed" / "preprocessing" / "F4"

TRAIN, VAL, TEST = 0.70, 0.15, 0.15


def main() -> int:
    t0 = time.perf_counter()

    # 1) Dias CHIRPS REALES en disco (RQ-21): nada inventado.
    tifs = sorted(RAW.glob("chirps-v3.0.rnl.2024.*.tif"))
    n_days = len(tifs)
    dias = [p.name for p in tifs]
    print("F4 n_dias_real_en_disco=", n_days, "dias=", dias)

    if n_days < 3:
        # RQ-07/08 exige >=3 para train/val/test sin fuga temporal.
        man = {
            "fase": "F4",
            "estado": "BLOQUEADO_RQ0710",
            "n_dias_real_en_disco": n_days,
            "min_exigido_rq07": 3,
            "dias": dias,
            "pendiente": f"faltan {3-n_days} dias reales para particion temporal (RQ-07/08)",
            "duracion_s": round(time.perf_counter() - t0, 4),
            "producido_at": datetime.now(timezone.utc).isoformat(),
        }
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "manifest_F4.jsonl").write_text(
            "".join(json.dumps(man, ensure_ascii=False)+"\n"), encoding="utf-8"
        )
        print("F4_BLOQUEADA", json.dumps(man, ensure_ascii=False))
        return 活动现场现场2

    # 2) Split cronologico (D-008), nunca aleatorio.
    n_tr = max(1, int(round(TRAIN * n_days)))
    n_va = max(1, int(round(VAL * n_days)))
    splits = {
        "train": dias[:n_tr],
        "val": dias[n_tr:n_tr + n_va],
        "test": dias[n_tr + n_va:],
    }

    # 3) sha256 real de cada dia del split (trazabilidad RQ-07/22).
    sha = {}
    for d in dias:
        b = (RAW / d).read_bytes()
        sha[d] = hashlib.sha256(b).hexdigest()[:16]

    man = {
        "fase": "F4",
        "objetivo": "D-008 / RQ-07-08-31",
        "cronologico": True,
        "aleatorio": False,
        "n_dias_real_en_disco": n_days,
        "splits": splits,
        "sha256_abreviado": sha,
        "duracion_s": round(time.perf_counter() - t0, 4),
        "tokens_smoke_aprox": sum(b := (RAW / d).read_bytes() is not None for d in dias),
        "producido_at": datetime.now(timezone.utc).isoformat(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest_F4.jsonl").write_text(
        json.dumps(man, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("F4_OK", json.dumps(man, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
