import re
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("/Volumes/project_files/ucmerced/2026/monika_simulations").resolve()
#Path(__file__).resolve().parent.parent / "data"
OUTPUT_CSV = Path(__file__).resolve().parent / "parameter_averages.csv"

DIR_NAME_PATTERN = re.compile(r"^F(?P<F>[0-9.]+)_K(?P<K>[0-9.]+)_theta(?P<theta>[0-9.]+)$")

TRUSTED_FROM_DIRNAME = ["F", "K", "theta"]
COLUMNS_TO_DROP = ["run", "nLoop", "bending", "activity", "theta"]


def parse_directory_name(name):
    match = DIR_NAME_PATTERN.match(name)
    if match is None:
        return None
    return {
        "F": float(match.group("F")),
        "K": float(match.group("K")),
        "theta": float(match.group("theta")),
    }


def average_one_directory(average_csv_path, params):
    runs_df = pd.read_csv(average_csv_path)

    measurement_columns = [c for c in runs_df.columns if c not in COLUMNS_TO_DROP]
    numeric_runs = runs_df[measurement_columns].apply(pd.to_numeric, errors="coerce")

    averaged_row = numeric_runs.mean(axis=0, skipna=True).to_dict()

    averaged_row["F"] = params["F"]
    averaged_row["K"] = params["K"]
    averaged_row["theta"] = params["theta"]
    averaged_row["n_runs"] = int(len(runs_df))
    return averaged_row


def build():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"data directory not found: {DATA_DIR}")

    rows = []
    skipped = []
    for average_csv_path in sorted(DATA_DIR.glob("*/Averaged_Runs/average.csv")):
        sim_dir_name = average_csv_path.parents[1].name
        params = parse_directory_name(sim_dir_name)
        if params is None:
            skipped.append((sim_dir_name, "unrecognized directory name"))
            continue
        try:
            rows.append(average_one_directory(average_csv_path, params))
        except (pd.errors.EmptyDataError, ValueError) as error:
            skipped.append((sim_dir_name, str(error)))

    if len(rows) == 0:
        raise RuntimeError("no average.csv files could be read")

    result_df = pd.DataFrame(rows)

    leading = TRUSTED_FROM_DIRNAME + ["n_runs"]
    ordered_columns = leading + [c for c in result_df.columns if c not in leading]
    result_df = result_df[ordered_columns]
    result_df = result_df.sort_values(TRUSTED_FROM_DIRNAME).reset_index(drop=True)

    result_df.to_csv(OUTPUT_CSV, index=False)

    print(f"Wrote {len(result_df)} parameter rows to {OUTPUT_CSV}")
    print(f"Unique F (activity): {sorted(result_df['F'].unique())}")
    print(f"Unique K (bending):  {sorted(result_df['K'].unique())}")
    print(f"Unique theta:        {sorted(result_df['theta'].unique())}")
    if skipped:
        print(f"Skipped {len(skipped)} directories:")
        for name, reason in skipped:
            print(f"  {name}: {reason}")


if __name__ == "__main__":
    build()
