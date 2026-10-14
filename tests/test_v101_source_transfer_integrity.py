"""Non-network regression for v1.0.1 frozen publisher-source integrity.

Test HTTP source bytes with monkeypatched source and checksum; NEVER download
third-party spectra, no model refitting, and no invalid-source acceptance.
"""
import hashlib
import io
from pathlib import Path

import pytest
from gcei import bootstrap


class _Response(io.BytesIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()


def test_source_fallback_only_accepts_exact_checksum_and_skips_wrong_zenodo_copy(tmp_path, monkeypatch):
    correct = b"synthetic exact frozen test bytes, not real third-party MSP"
    expected = hashlib.sha256(correct).hexdigest()
    monkeypatch.setattr(bootstrap, "EXPECTED_SHA256", expected)
    monkeypatch.setattr(bootstrap.time, "sleep", lambda _: None)
    attempts = []
    def fetch(request, timeout):
        attempts.append(request.full_url)
        if len(attempts) == 1:
            return _Response(b"unexpected alternate publisher file")
        return _Response(correct)
    monkeypatch.setattr(bootstrap.urllib.request, "urlopen", fetch)
    out = tmp_path / "original.msp"
    bootstrap._download_source(out)
    assert out.read_bytes() == correct
    assert len(attempts) == 2
    assert len(set(attempts)) == 2
    assert not list(tmp_path.glob("*.part"))


def test_source_download_rejects_six_wrong_replies_without_overwriting_existing_source(tmp_path, monkeypatch):
    expected = hashlib.sha256(b"protected exact dataset").hexdigest()
    monkeypatch.setattr(bootstrap, "EXPECTED_SHA256", expected)
    monkeypatch.setattr(bootstrap.time, "sleep", lambda _: None)
    count = {"n": 0}
    def fetch(request, timeout):
        count["n"] += 1
        return _Response(f"wrong archive {count['n']}".encode())
    monkeypatch.setattr(bootstrap.urllib.request, "urlopen", fetch)
    original = tmp_path / "original.msp"
    original.write_bytes(b"existing exact dataset")
    with pytest.raises(RuntimeError, match="exact checksum-verified MS-DIAL library"):
        bootstrap._download_source(original)
    assert count["n"] == 6
    assert original.read_bytes() == b"existing exact dataset"
    assert not list(tmp_path.glob("*.part"))


def test_source_download_does_not_skip_sha_verification_on_successful_status(tmp_path, monkeypatch):
    monkeypatch.setattr(bootstrap, "EXPECTED_SHA256", hashlib.sha256(b"exact").hexdigest())
    monkeypatch.setattr(bootstrap.time, "sleep", lambda _: None)
    monkeypatch.setattr(bootstrap.urllib.request, "urlopen",
                        lambda *args, **kwargs: _Response(b"wrong content"))
    with pytest.raises(RuntimeError, match="checksum-verified"):
        bootstrap._download_source(tmp_path / "nonexistent.msp")
    assert not (tmp_path / "nonexistent.msp").exists()
