"""CHIRPS v3 diario ``rnl``: descarga, integridad y trazabilidad.

Este módulo descarga un archivo diario del producto CHIRPS v3 final ``rnl`` y
registra metadatos reproducibles. La fecha codificada en el nombre del archivo
es la fecha de observación, no la fecha de publicación. Por esa razón
``published_at`` permanece ``None`` salvo que exista evidencia explícita del
proveedor; ``source_last_modified`` conserva, cuando existe, el encabezado HTTP
``Last-Modified`` como metadato técnico independiente.

Ruta esperada::

    daily/final/rnl/{YYYY}/chirps-v3.0.rnl.YYYY.MM.DD.tif

La descarga usa un archivo temporal ``.part``, admite reanudación cuando el
servidor expone ``Accept-Ranges: bytes`` y siempre calcula SHA-256 local. Si el
proveedor publica un sidecar ``.sha256sum``, el hash local se compara contra él
y el manifiesto lo marca como verificado externamente.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, BinaryIO
from urllib.parse import urlsplit

import requests

CHIRPS_BASE = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0"
CHIRPS_TPL = "daily/final/rnl/{year}/chirps-v3.0.rnl.{year}.{month}.{day}.tif"
CHUNK = 1 << 20
REQUEST_TIMEOUT = 60.0
_OBS_RE = re.compile(r"^chirps-v3\.0\.rnl\.(\d{4})\.(\d{2})\.(\d{2})\.tif$")

ManifestRecord = dict[str, Any]


class ChecksumError(RuntimeError):
    """El contenido descargado no coincide con la integridad esperada."""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _tif_path(year: int, month: int, day: int) -> str:
    return CHIRPS_TPL.format(
        year=year,
        month=f"{month:02d}",
        day=f"{day:02d}",
    )


def chirps_url(year: int, month: int, day: int) -> str:
    """Devuelve la URL oficial esperada para un día del producto final RNL."""
    # datetime valida calendario y evita construir fechas imposibles.
    datetime(year, month, day)
    return f"{CHIRPS_BASE}/{_tif_path(year, month, day)}"


def observation_date_from_url(url: str) -> str:
    """Extrae ``YYYY-MM-DD`` del nombre CHIRPS o levanta ``ValueError``."""
    name = Path(urlsplit(url).path).name
    match = _OBS_RE.match(name)
    if not match:
        raise ValueError(f"Nombre CHIRPS no reconocido: {name}")
    year, month, day = (int(part) for part in match.groups())
    return datetime(year, month, day).date().isoformat()


def _http_datetime_to_iso(value: str | None) -> str | None:
    """Convierte una fecha HTTP a ISO-8601 UTC; devuelve ``None`` si no aplica."""
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds")


class ChirpsRetriever:
    """Descarga reanudable de CHIRPS con manifiesto de procedencia."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = (
            "Wayra-AI/0.1 (climate-research; "
            "+https://github.com/Lobitoxxx/Wayra_AI)"
        )

    @staticmethod
    def _checksum_stream(fh: BinaryIO) -> tuple[str, int]:
        digest = hashlib.sha256()
        size = 0
        while chunk := fh.read(CHUNK):
            digest.update(chunk)
            size += len(chunk)
        return digest.hexdigest(), size

    def retrieve(self, url: str, dest: Path, manifest: Path) -> ManifestRecord:
        """Descarga ``url`` a ``dest`` y añade una entrada JSONL al manifiesto."""
        observation_time = observation_date_from_url(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest_tmp = dest.with_suffix(dest.suffix + ".part")

        expected_len = -1
        source_last_modified: str | None = None

        with self.session.get(url, stream=True, timeout=REQUEST_TIMEOUT) as resp:
            if resp.status_code == 404:
                raise FileNotFoundError(
                    f"CHIRPS: {url} -> 404 (producto no publicado o ruta inválida)"
                )
            resp.raise_for_status()
            expected_len = int(resp.headers.get("Content-Length", "-1"))
            accept_ranges = resp.headers.get("Accept-Ranges", "")
            source_last_modified = _http_datetime_to_iso(
                resp.headers.get("Last-Modified")
            )

            resume_at = dest_tmp.stat().st_size if dest_tmp.is_file() else 0
            if resume_at:
                if accept_ranges.lower() != "bytes":
                    raise RuntimeError(f"Servidor sin soporte de reanudación: {url}")
                if expected_len < 0:
                    raise RuntimeError(
                        "No se puede validar una reanudación sin Content-Length total."
                    )

                resp.close()
                headers = {"Range": f"bytes={resume_at}-"}
                with self.session.get(
                    url,
                    stream=True,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT,
                ) as resumed:
                    resumed.raise_for_status()
                    if resumed.status_code != 206:
                        raise RuntimeError("El servidor ignoró la cabecera Range.")
                    remaining = int(resumed.headers.get("Content-Length", "0"))
                    if resume_at + remaining != expected_len:
                        raise RuntimeError(
                            "Tamaño inconsistente tras reanudar la descarga."
                        )
                    with dest_tmp.open("ab") as fh:
                        for chunk in resumed.iter_content(CHUNK):
                            if chunk:
                                fh.write(chunk)
            else:
                with dest_tmp.open("wb") as fh:
                    for chunk in resp.iter_content(CHUNK):
                        if chunk:
                            fh.write(chunk)

        with dest_tmp.open("rb") as fh:
            sha256, size = self._checksum_stream(fh)

        expected_sha = self._expected_sha(url)
        checksum_verified = expected_sha is not None
        if expected_sha is not None and sha256 != expected_sha:
            dest_tmp.unlink(missing_ok=True)
            raise ChecksumError(f"SHA-256 no coincide para {url}: {sha256}")
        if expected_len != -1 and size != expected_len:
            dest_tmp.unlink(missing_ok=True)
            raise ChecksumError(f"Tamaño {size} != {expected_len} para {url}")

        os.replace(dest_tmp, dest)

        record: ManifestRecord = {
            "source": "CHIRPS",
            "product": "v3.0-daily-final-rnl",
            "url": url,
            # Compatibilidad con manifiestos previos y nombre normalizado nuevo.
            "shasum256": sha256,
            "sha256": sha256,
            "bytes": size,
            "checksum_verified": checksum_verified,
            "checksum_source": (
                "provider_sidecar_sha256sum"
                if checksum_verified
                else "local_sha256_only"
            ),
            "expected_sha256": expected_sha,
            "observation_time": observation_time,
            # No inferir publicación desde la fecha observada.
            "published_at": None,
            "source_last_modified": source_last_modified,
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
    def _append_manifest(manifest: Path, record: ManifestRecord) -> None:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        with manifest.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(
            "uso: python -m wayra.ingestion.chirps "
            "<YYYY-MM-DD> [<ruta-destino>]"
        )
        return 2

    try:
        obs = datetime.strptime(argv[0], "%Y-%m-%d").date()
    except ValueError as exc:
        print(f"fecha inválida: {argv[0]} ({exc})")
        return 2

    target = (
        Path(argv[1])
        if len(argv) > 1
        else Path("data/raw/chirps-rnl/daily")
    )
    dest = (
        target
        / f"{obs.year}"
        / f"chirps-v3.0.rnl.{obs.year}.{obs.month:02d}.{obs.day:02d}.tif"
    )
    manifest = (
        target.parent / "manifiestos" / "chirps-v3.0.rnl.manifest.jsonl"
    )

    rec = ChirpsRetriever().retrieve(
        chirps_url(obs.year, obs.month, obs.day),
        dest,
        manifest,
    )
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
