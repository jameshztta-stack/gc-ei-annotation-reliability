from __future__ import annotations

import hashlib
import os
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .reference_builder import build_reference_assets


ZENODO_RECORD_URL = "https://zenodo.org/records/21910638"
ZENODO_DOWNLOAD_URL = "https://zenodo.org/records/21910638/files/GCMS%20DB-Public-KovatsRI-VS3.msp?download=1"
SOURCE_FILENAME = "GCMS DB-Public-KovatsRI-VS3.msp"
EXPECTED_SHA256 = "6bc2c7dfcf5a2a80227674229e6bd93e0af0880cbc3f87586f36ef9b31fd9132"


@dataclass(frozen=True)
class ReferenceAssets:
    reference_npz: Path
    metadata_csv: Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _verify_source(path: Path) -> None:
    observed = sha256_file(path)
    if observed != EXPECTED_SHA256:
        raise RuntimeError(
            "The MSP source does not match the publication file. "
            f"Expected SHA-256 {EXPECTED_SHA256}, observed {observed}."
        )


def _download_source(destination: Path) -> Path:
    request = urllib.request.Request(
        ZENODO_DOWNLOAD_URL,
        headers={"User-Agent": "GC-EI-Annotation-Reliability-Tool/0.2.0-rc1"},
    )
    with urllib.request.urlopen(request, timeout=180) as response, destination.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
    return destination


def ensure_reference_assets(runtime_dir: Path, source_msp: Path | None = None) -> ReferenceAssets:
    runtime_dir = Path(runtime_dir)
    runtime_dir.mkdir(parents=True, exist_ok=True)
    reference_npz = runtime_dir / "publication_reference.npz"
    metadata_csv = runtime_dir / "publication_reference_metadata.csv"

    if reference_npz.exists() and metadata_csv.exists():
        return ReferenceAssets(reference_npz, metadata_csv)

    if source_msp is not None:
        source_msp = Path(source_msp)
        if not source_msp.exists():
            raise FileNotFoundError(f"MSP file does not exist: {source_msp}")
        _verify_source(source_msp)
        build_reference_assets(source_msp, reference_npz, metadata_csv)
        return ReferenceAssets(reference_npz, metadata_csv)

    env_path = os.environ.get("GCEI_MSP_PATH")
    if env_path:
        candidate = Path(env_path)
        if candidate.exists():
            _verify_source(candidate)
            build_reference_assets(candidate, reference_npz, metadata_csv)
            return ReferenceAssets(reference_npz, metadata_csv)

    with tempfile.TemporaryDirectory(prefix="gcei_msp_") as temp_dir:
        local_msp = Path(temp_dir) / SOURCE_FILENAME
        _download_source(local_msp)
        _verify_source(local_msp)
        build_reference_assets(local_msp, reference_npz, metadata_csv)

    return ReferenceAssets(reference_npz, metadata_csv)
