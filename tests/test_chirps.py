from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from wayra.ingestion.chirps import (
    ChirpsRetriever,
    chirps_url,
    observation_date_from_url,
)


class FakeResponse:
    def __init__(
        self,
        *,
        body: bytes = b"",
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        text: str = "",
    ) -> None:
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def iter_content(self, _chunk_size: int):
        if self.body:
            yield self.body

    def close(self) -> None:
        return None


class FakeSession:
    def __init__(self, body: bytes) -> None:
        self.headers: dict[str, str] = {}
        self.body = body
        self.sha = hashlib.sha256(body).hexdigest()

    def get(self, url: str, **_kwargs: object) -> FakeResponse:
        if url.endswith(".sha256sum"):
            return FakeResponse(text=f"{self.sha}  sample.tif\n")
        return FakeResponse(
            body=self.body,
            headers={
                "Content-Length": str(len(self.body)),
                "Accept-Ranges": "bytes",
                "Last-Modified": "Mon, 17 Jun 2024 18:30:00 GMT",
            },
        )


def test_chirps_url_and_observation_date() -> None:
    url = chirps_url(2024, 6, 15)
    assert url.endswith("/2024/chirps-v3.0.rnl.2024.06.15.tif")
    assert observation_date_from_url(url) == "2024-06-15"


def test_observation_date_rejects_unknown_filename() -> None:
    with pytest.raises(ValueError):
        observation_date_from_url("https://example.org/not-chirps.tif")


def test_chirps_url_validates_calendar_date() -> None:
    with pytest.raises(ValueError):
        chirps_url(2024, 2, 31)


def test_retrieve_records_temporal_provenance_and_verified_checksum(
    tmp_path: Path,
) -> None:
    payload = b"real-file-bytes-for-test"
    session = FakeSession(payload)
    retriever = ChirpsRetriever(session=session)  # type: ignore[arg-type]

    url = chirps_url(2024, 6, 15)
    dest = tmp_path / "chirps.tif"
    manifest = tmp_path / "manifest.jsonl"

    record = retriever.retrieve(url, dest, manifest)

    assert dest.read_bytes() == payload
    assert record["observation_time"] == "2024-06-15"
    assert record["published_at"] is None
    assert record["source_last_modified"] == "2024-06-17T18:30:00+00:00"
    assert record["checksum_verified"] is True
    assert record["checksum_source"] == "provider_sidecar_sha256sum"
    assert record["sha256"] == session.sha

    stored = json.loads(manifest.read_text(encoding="utf-8").strip())
    assert stored["sha256"] == session.sha
    assert stored["observation_time"] == "2024-06-15"
