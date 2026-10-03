from __future__ import annotations

import os
import shutil
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from .reference_builder import EXPECTED_SHA256, build_reference_assets, sha256

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
DEFAULT_RUNTIME = ROOT / ".runtime_assets_v11"
SOURCE_FILENAME = "GCMS DB-Public-KovatsRI-VS3.msp"
SOURCE_RECORD = "https://zenodo.org/records/21910638"
SOURCE_DOWNLOAD = "https://zenodo.org/records/21910638/files/" + urllib.parse.quote(SOURCE_FILENAME) + "?download=1"
REQUIRED_REFERENCE = ("reference_matrix.npz", "reference_metadata.csv", "reference_ri.npy")
REQUIRED_MODELS = ("calibration.json", "model_ei.json", "model_ri.json")


def _complete(asset_dir: Path) -> bool:
    return all((asset_dir / x).exists() for x in REQUIRED_REFERENCE + REQUIRED_MODELS)


def _copy_models(asset_dir: Path):
    for name in REQUIRED_MODELS:
        shutil.copy2(MODELS / name, asset_dir / name)


def _download_source(dest: Path):
    req = urllib.request.Request(
        SOURCE_DOWNLOAD,
        headers={"User-Agent": "GC-EI-Annotation-Reliability-Tool/0.2-v1.1"},
    )
    with urllib.request.urlopen(req, timeout=180) as response, dest.open("wb") as out:
        shutil.copyfileobj(response, out)


def ensure_runtime_assets(asset_dir: str | Path | None = None) -> Path:
    """Create the frozen v1.1 runtime assets without redistributing the upstream MSP."""
    asset_dir = Path(asset_dir or os.environ.get("GCEI_ASSET_DIR", DEFAULT_RUNTIME))
    asset_dir.mkdir(parents=True, exist_ok=True)
    if _complete(asset_dir):
        return asset_dir

    local = os.environ.get("GCEI_MSP_PATH")
    temp_file = None
    try:
        if local:
            msp = Path(local).expanduser().resolve()
            if not msp.exists():
                raise FileNotFoundError(f"GCEI_MSP_PATH does not exist: {msp}")
        else:
            fd, name = tempfile.mkstemp(prefix="gcei_source_", suffix=".msp")
            os.close(fd)
            temp_file = Path(name)
            _download_source(temp_file)
            msp = temp_file

        observed = sha256(msp)
        if observed != EXPECTED_SHA256:
            raise RuntimeError(
                "The downloaded/provided MSP does not match the publication input. "
                f"Expected {EXPECTED_SHA256}; observed {observed}. "
                f"Obtain the exact source from {SOURCE_RECORD}."
            )

        build_reference_assets(msp, asset_dir)
        _copy_models(asset_dir)
        return asset_dir
    finally:
        if temp_file is not None:
            temp_file.unlink(missing_ok=True)
