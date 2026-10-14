from __future__ import annotations

import os
import shutil
import tempfile
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
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
    """Retrieve EXACT frozen MS-DIAL source bytes from publisher endpoints.

    Known publisher historical archive URLs are transport alternatives only.
    Every response is SHA-256 verified before an atomic replace of the
    destination. A mismatching source cannot become application data.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    source_urls = (
        "https://zenodo.org/api/records/10951913/files/"
        + urllib.parse.quote(SOURCE_FILENAME) + "/content",
        "https://zenodo.org/records/10951913/files/"
        + urllib.parse.quote(SOURCE_FILENAME) + "?download=1",
        SOURCE_DOWNLOAD,
    )
    last_failure = None
    for attempt in range(6):
        endpoint = source_urls[attempt % len(source_urls)]
        temporary = None
        try:
            fd, name = tempfile.mkstemp(prefix=".gcei_msp_", suffix=".part", dir=dest.parent)
            os.close(fd)
            temporary = Path(name)
            request = urllib.request.Request(
                endpoint, headers={"User-Agent": "GC-EI-Annotation-Reliability-Tool/1.0.1"}
            )
            with urllib.request.urlopen(request, timeout=180) as stream, temporary.open("wb") as output:
                shutil.copyfileobj(stream, output)
            actual = sha256(temporary)
            if actual != EXPECTED_SHA256:
                # Publisher URLs sometimes return a different generation of
                # bytes. Never accept these, but safely try another endpoint.
                last_failure = RuntimeError(
                    "Publisher MSP SHA-256 mismatch; received " + actual
                )
                continue
            temporary.replace(dest)
            return
        except HTTPError as exc:
            last_failure = exc
        except (URLError, TimeoutError, ConnectionError, OSError) as exc:
            last_failure = exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        if attempt < 5:
            time.sleep(min(1 + attempt, 3))
    raise RuntimeError(
        "Could not obtain the exact checksum-verified MS-DIAL library. "
        "No substituted spectra were accepted."
    ) from last_failure


def ensure_runtime_assets(asset_dir: str | Path | None = None) -> Path:
    """Build v1 study-frozen reference assets without redistributing the source MSP."""
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
                "The downloaded or supplied MSP does not match the validated source file. "
                f"Expected {EXPECTED_SHA256}; observed {observed}. "
                f"Obtain the exact source from {SOURCE_RECORD}."
            )

        build_reference_assets(msp, asset_dir)
        _copy_models(asset_dir)
        return asset_dir
    finally:
        if temp_file is not None:
            temp_file.unlink(missing_ok=True)
