"""CHIRPS v3.0 diario `rnl` — adaptador de ingesta con descarga reanudable.

Verificado contra `https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/rnl/`
(200, image/tiff, ~17.3 MB por día en malla global 0.05°). La malla de trabajo de
Wayra será 0.1° (D-005): el re-muestreo ocurre en [src/wayra/preprocess].

Ruta de archivo: f"chirps-v3.0.rnl.{Y}.{m}.{d}.tif" bajo daily/final/rnl/{Y}/.
Manifiesto de salida: JSONL con trazabilidad temporal D-006 / RQ-07.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

import requests

try:
    import tomllib
except ModuleNotFoundError:  # CPython < 3.11
    tomllib = None  # type: ignore[assignment]

CHIRPS_BASE = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0"
CHIRPS_TPL = "daily/final/rnl/{year}/chirps-v3.0.rnl.{year}.{month}.{day}.tif"
CHUNK = 1 << 20
REQUEST_TIMEOUT = 60.0

ManifestRecord: dict[str, Any]


class ChecksumError(RuntimeError):
    """Firma SHA-256 de un archivo no coincide con la esperada."""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _tif_path(year: int, month: int, day: int) -> str:
    m = f"{month:02d}"
    d = f"{day:02d}"
    return CHIRPS_TPL.format(year=year, month=m, day=d)


def chirps_url(year: int, month: int, day: int) -> str:
    return f"{CHIRPS_BASE}/{_tif_path(year, month, day)}"


class ChirpsRetriever:
    """Descarga reanudable de un día de CHIRPS con verificación SHA-256."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = "Wayra-AI/0.1 (ingestion;+https://github.com/#wayra)"

    def _existing_shasum(self, dest: Path) -> str | None:
        if not dest.is_file():
            return None
        digest = hashlib.sha256()
        with dest.open("rb") as fh:
            while chunk := fh.read(CHUNK):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _checksum_stream(fh: BinaryIO) -> tuple[str, int]:
        digest = hashlib.sha256()
        size = 0
        while chunk := fh.read(CHUNK):
            digest.update(chunk)
            size += len(chunk)
        return digest.hexdigest(), size

    def retrieve(self, url: str, dest: Path, manifest: Path) -> ManifestRecord:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest_tmp = dest.with_suffix(dest.suffix + ".part")
        expected_sha: str
        expected_len: int

        with self.session.get(url, stream=True, timeout=REQUEST_TIMEOUT) as resp:
            if resp.status_code == 404:
                raise FileNotFoundError(f"CHIRPS: {url} -> 404 (producto no publicado)")
            resp.raise_for_status()
            expected_len = int(resp.headers.get("Content-Length", "-1"))
            accept_ranges = resp.headers.get("Accept-Ranges", "")
            resume_at = dest_tmp.stat().st_size if dest_tmp.is_file() else 0
            if resume_at:
                if accept_ranges.lower() != "bytes":
                    raise RuntimeError(f"Servidor sin soporte de reanudación: {url}")
                resp.close()
                headers = {"Range": f"bytes={resume_at}-"}
                with self.session.get(url, stream=True, headers=headers,
                                      timeout=REQUEST_TIMEOUT) as r2:
                    r2.raise_for_status()
                    if r2.status_code != 206:
                        raise RuntimeError("El servidor ignoró la cabecera Range.")
                    length = int(r2.headers.get("Content-Length", "0"))
                    if resume_at + length != expected_len:
                        raise RuntimeError("Tamaño inconsistente tras la reanudación.")
                    with dest_tmp.open("ab") as fh:
                        for chunk in r2.iter_content(CHUNK):
                            if chunk:
                                fh.write(chunk)
            else:
                with dest_tmp.open("wb") as fh:
                    for chunk in resp.iter_content(CHUNK):
                        if chunk:
                            fh.write(chunk)

        sha, size = self._checksum_stream(dest_tmp.open("rb"))
        expected_sha = self._expected_sha(url)
        if expected_sha is not None and sha != expected_sha:
            dest_tmp.unlink(missing_ok=True)
            raise ChecksumError(f"SHA-256 no coincide para {url}: {sha}")
        if expected_len != -1 and size != expected_len:
            dest_tmp.unlink(missing_ok=True)
            raise ChecksumError(f"Tamaño {size} != {expected_len} para {url}")

        os.replace(dest_tmp, dest)
        record: ManifestRecord = {
            "url": url,
            "shasum256": sha,
            "bytes": size,
            "published_at": self._published_at(url),
            "observation_time": self._observation_time(url),
            "retrieved_at": _utcnow(),
        }
        self._append_manifest(manifest, record)
        return record

    def _expected_sha(self, url: str) -> str | None:
        sidecar = url + ".sha256sum"
        try:
            with self.session.get(sidecar, timeout=REQUEST_TIMEOUT) as resp:
                resp.raise_for_status()
            line = resp.text.strip().splitlines()[0]
            return line.split()[0].strip().lower()
        except (requests.RequestException, IndexError, UnicodeDecodeError):
            return None

    @staticmethod
    def _published_at(url: str) -> str:
        stem = Path(url).stem
        try:
            date = stem.rsplit(".", 1)[-1]
            return datetime.strptime(date, "%Y.%m.%d").strftime("%Y-%m-%d")
        except ValueError:
            return ""

    @staticmethod
    def _observation_time(url: str) -> str:
        return ChirpsRetriever._published_at(url)

    def _append_manifest(self, manifest: Path, record: ManifestRecord) -> None:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        with manifest.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("uso: python -m wayra.ingestion.chirps <YYYY-MM-DD> [<malla|ruta-destino>]")
        return 2
    date = argv[0]
    target = Path(argv[1]) if len(argv) > 1 else Path("data/raw/chirps-rnl/daily")
    year, month, day = (int(part) for part in date.split("-"))
    dest = target / f"{year}" / f"chirps-v3.0.rnl.{year}.{month:02d}.{day:02d}.tif"
    manifest = target.parent / "manifiestos" / "chirps-v3.0.rnl.manifest.jsonl"
    rec = ChirpsRetriever().retrieve(chirps_url(year, month, day), dest, manifest)
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
