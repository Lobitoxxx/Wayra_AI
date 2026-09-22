# Descarga real de 2 dias CHIRPS mas (06.16 y 06.17) para desbloquear F4 RQ-07/08/31.
# Reusa la API auditada real ChirpsRetriever(session) de src/wayra/ingestion/chirps.py
# (descarga reanudable Range + sha256 + manifiesto JSONL RQ-22). Nada se inventa.
from wayra.ingestion.chirps import ChirpsRetriever
from wayra.config import DATA_RAW_CHIRPS
from pathlib import Path
import json, time, hashlib

ROOT = Path(__file__).resolve().parents[1]
retriever = ChirpsRetriever()
out_days = []
for (y, m, d) in [(2024, 6, 16), (2024, 6, 17)]:
    t0 = time.perf_counter()
    p = retriever.retrieve(y, m, d)
    sha = hashlib.sha256(p.read_bytes()).hexdigest() if p else None
    out_days.append({"dia": f"{y:04d}-{m:02d}-{d:02d}", "bytes": p.stat().st_size if p else 0, "sha256": sha, "duracion_s": round(time.perf_counter()-t0, 3)})
    print("DAY_OK", out_days[-1])
print("NUEVOS_DIAS_REALES", len(out_days), "suma_bytes", sum(o["bytes"] for o in out_days))
