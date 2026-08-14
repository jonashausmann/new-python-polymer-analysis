"""
Collects and moves CSV files, figures, and averaged run data from simulation
output directories into a single dated archive directory.

Destination layout:
  csv_data_YYYY-MM-DD_{N}/
    {param}_csv/
      RUN_000*/          <- csv_files/* contents + figures/ (if present)
      Averaged_Runs/     <- average.csv (if present)
    heat_map_data/
      figures/           <- heat_map/figures/ (if present)
      parameter_averages.csv (if present)
"""

import os
import shutil
from datetime import date
from glob import glob

# ── Configuration ──────────────────────────────────────────────────────────────
DEST_ROOT   = "/Volumes/project_files/ucmerced/csv_dumps"           
# Parent directory where csv_data_DATE_N/ is created

SOURCE_ROOT = "./data"      # Directory containing F*_K*_theta* parameter folders
HEAT_MAP_DIR = "./heat_map" # Directory containing heat_map figures/averages
# ───────────────────────────────────────────────────────────────────────────────


def make_dest_dir(root: str) -> str:
    """Return a new dated destination path, appending _2, _3, etc. if needed."""
    today = date.today().isoformat()
    base = os.path.join(root, f"csv_data_{today}")
    if not os.path.exists(base):
        os.makedirs(base)
        return base
    n = 2
    while True:
        candidate = f"{base}_{n}"
        if not os.path.exists(candidate):
            os.makedirs(candidate)
            return candidate
        n += 1


def move_item(src: str, dst: str) -> None:
    """Move src to dst, creating parent dirs as needed. No-op if src missing."""
    if not os.path.exists(src):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"  moved: {src} -> {dst}")


def move_dir_contents(src_dir: str, dst_dir: str) -> None:
    """Move every item inside src_dir into dst_dir. Skips if src_dir missing."""
    if not os.path.isdir(src_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    for name in os.listdir(src_dir):
        move_item(os.path.join(src_dir, name), os.path.join(dst_dir, name))


def collect_parameter_folder(param_dir: str, dest_param_dir: str) -> None:
    """
    Move CSV files, figures, and averaged runs out of one F*_K*_theta* folder.
    """
    # ── Per-run data ────────────────────────────────────────────────────────────
    for run_name in sorted(os.listdir(param_dir)):
        run_path = os.path.join(param_dir, run_name)
        if not (os.path.isdir(run_path) and run_name.startswith("RUN_")):
            continue

        dest_run = os.path.join(dest_param_dir, run_name)

        # Move contents of csv_files/ flat into dest_run/
        csv_files_dir = os.path.join(run_path, "csv_files")
        move_dir_contents(csv_files_dir, dest_run)

        # Move figures/ directory if present
        figures_dir = os.path.join(run_path, "figures")
        if os.path.isdir(figures_dir):
            move_item(figures_dir, os.path.join(dest_run, "figures"))

        # Remove now-empty csv_files dir if it exists and is empty
        if os.path.isdir(csv_files_dir) and not os.listdir(csv_files_dir):
            os.rmdir(csv_files_dir)

    # ── Averaged_Runs ───────────────────────────────────────────────────────────
    avg_src = os.path.join(param_dir, "Averaged_Runs")
    avg_dst = os.path.join(dest_param_dir, "Averaged_Runs")
    if os.path.isdir(avg_src):
        move_dir_contents(avg_src, avg_dst)
        if not os.listdir(avg_src):
            os.rmdir(avg_src)


def collect_heat_map(heat_map_dir: str, dest_heat_map: str) -> None:
    """Move figures/ and parameter_averages.csv out of heat_map/."""
    figures_src = os.path.join(heat_map_dir, "figures")
    if os.path.isdir(figures_src):
        move_item(figures_src, os.path.join(dest_heat_map, "figures"))

    csv_src = os.path.join(heat_map_dir, "parameter_averages.csv")
    if os.path.isfile(csv_src):
        move_item(csv_src, os.path.join(dest_heat_map, "parameter_averages.csv"))


def main() -> None:
    if not os.path.isdir(SOURCE_ROOT):
        raise SystemExit(f"Source directory not found: {SOURCE_ROOT}")

    dest_dir = make_dest_dir(DEST_ROOT)
    print(f"Destination: {dest_dir}\n")

    # ── Parameter folders ───────────────────────────────────────────────────────
    param_dirs = sorted(glob(os.path.join(SOURCE_ROOT, "F*_K*_theta*")))
    if not param_dirs:
        print("Warning: no F*_K*_theta* directories found in source root.")

    for param_dir in param_dirs:
        if not os.path.isdir(param_dir):
            continue
        param_name = os.path.basename(param_dir)
        dest_param = os.path.join(dest_dir, f"{param_name}_csv")
        print(f"Processing {param_name} ...")
        try:
            collect_parameter_folder(param_dir, dest_param)
        except Exception as exc:
            print(f"  ERROR processing {param_name}: {exc}")

    # ── Heat map ────────────────────────────────────────────────────────────────
    if os.path.isdir(HEAT_MAP_DIR):
        print("\nProcessing heat_map ...")
        try:
            collect_heat_map(HEAT_MAP_DIR, os.path.join(dest_dir, "heat_map_data"))
        except Exception as exc:
            print(f"  ERROR processing heat_map: {exc}")
    else:
        print(f"\nheat_map directory not found ({HEAT_MAP_DIR}), skipping.")

    print(f"\nDone. Data collected into: {dest_dir}")


if __name__ == "__main__":
    main()
