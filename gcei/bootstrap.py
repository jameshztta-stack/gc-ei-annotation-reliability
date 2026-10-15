"""Retrieval of the original MS-DIAL EI spectral library."""
from __future__ import annotations
import os
import shutil
import tempfile
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path
from .reference_builder import EXPECTED_SHA256, sha256

SOURCE_FILENAME = "GCMS DB-Public-KovatsRI-VS3.msp"
SOURCE_RECORD = "https://zenodo.org/records/21910638"
SOURCE_DOWNLOAD = SOURCE_RECORD + "/files/" + urllib.parse.quote(SOURCE_FILENAME) + "?download=1"

def _download_source(dest: Path):
    """Obtain the original MS-DIAL spectral data and verify its SHA-256 checksum.

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
                endpoint, headers={"User-Agent": "GC-EI-MS-Annotation-Tool/2.0.2"}
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

