from __future__ import annotations

import argparse
from pathlib import Path

from gcei.bootstrap import ensure_reference_assets


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the frozen publication reference assets.")
    parser.add_argument("--msp", type=Path, default=None, help="Exact local publication MSP; otherwise fetched from original Zenodo record.")
    parser.add_argument("--output", type=Path, default=Path("runtime_assets"))
    args = parser.parse_args()

    assets = ensure_reference_assets(args.output, source_msp=args.msp)
    print(assets.reference_npz)
    print(assets.metadata_csv)


if __name__ == "__main__":
    main()
