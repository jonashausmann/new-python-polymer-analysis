"""
Copies the per-run "graphs" folders out of a data directory into a dated
output directory, without touching the originals.

Destination layout:
  {output_dir}/{M}_{D}_{YY}_frame_graphs/
    F*_K*_theta*/
      RUN_000*/
        graphs/          <- copy of RUN_000*/graphs from the source

Usage:
  python copy_frame_graphs.py --data-dir ./data --output-dir ./output
"""

import argparse
import shutil
from datetime import date
from pathlib import Path


def make_dest_dir(output_dir: Path) -> Path:
    """Return a new dated destination path, appending _2, _3, etc. if needed."""
    today = date.today()
    stamp = f"{today.month}_{today.day}_{today.strftime('%y')}"
    base = output_dir / f"{stamp}_frame_graphs"
    if not base.exists():
        base.mkdir(parents=True)
        return base
    n = 2
    while True:
        candidate = output_dir / f"{stamp}_frame_graphs_{n}"
        if not candidate.exists():
            candidate.mkdir(parents=True)
            return candidate
        n += 1


def copy_frame_graphs(data_dir: Path, dest_dir: Path) -> None:
    param_dirs = sorted(p for p in data_dir.iterdir() if p.is_dir())
    if not param_dirs:
        print(f"Warning: no subdirectories found in {data_dir}")

    for param_dir in param_dirs:
        run_dirs = sorted(
            p for p in param_dir.iterdir() if p.is_dir() and p.name.startswith("RUN_")
        )
        for run_dir in run_dirs:
            graphs_src = run_dir / "figures"
            if not graphs_src.is_dir():
                continue
            graphs_dst = dest_dir / param_dir.name / run_dir.name / "graphs"
            shutil.copytree(graphs_src, graphs_dst)
            print(f"  copied: {graphs_src} -> {graphs_dst}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy per-run graphs folders into a dated output directory."
    )
    parser.add_argument(
        "--data-dir", default="./data", help="Directory containing F*_K*_theta* parameter folders (default: ./data)"
    )
    parser.add_argument(
        "--output-dir", default="./output", help="Directory in which to create the dated output folder (default: ./output)"
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not data_dir.is_dir():
        raise SystemExit(f"Data directory not found: {data_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    dest_dir = make_dest_dir(output_dir)
    print(f"Destination: {dest_dir}\n")

    copy_frame_graphs(data_dir, dest_dir)

    print(f"\nDone. Graphs copied into: {dest_dir}")


if __name__ == "__main__":
    main()
