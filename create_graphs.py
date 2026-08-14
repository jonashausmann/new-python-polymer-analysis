from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

import visualize_data
from visualize_data import frame_graph

data_directory = "./data/"


def graph_subsubdir(subsubdir):
    """Create all variable-vs-frame graphs for a single RUN_* directory.

    Skips (rather than errors) when the run has already been graphed
    (a "figures" directory already exists), or has no measurements csv yet.
    A leftover "graphs" directory from the old naming is renamed in place
    to "figures" and treated as already processed, rather than deleted
    and regenerated.
    """
    subsubdir = str(subsubdir)

    figures_folder = Path(subsubdir) / "figures"
    if figures_folder.exists():
        return f"Skipping {subsubdir}, figures directory already exists"

    graphs_folder = Path(subsubdir) / "graphs"
    if graphs_folder.exists():
        graphs_folder.rename(figures_folder)
        return f"Renamed graphs to figures for {subsubdir}, skipping reprocessing"

    csv_folder_resolved = (Path(subsubdir) / "csv_files").resolve()
    if not csv_folder_resolved.exists():
        return f"Skipping {subsubdir}, no csv_files directory found"

    csv_file = list(csv_folder_resolved.glob("*_measurements.csv"))
    if len(csv_file) == 0:
        return f"Skipping {subsubdir}, no measurements csv found"

    csv_file_name = str(csv_file[0])
    try:
        frame_graph.run_for_all_columns(csv_file_name)
    except FileNotFoundError as e:
        return f"Skipping {subsubdir}, required file not found: {e}"
    except (KeyError, IndexError, pd.errors.EmptyDataError) as e:
        return f"Skipping {subsubdir}, malformed measurement data: {e}"

    return f"Finished graphing {subsubdir}"


def its_graphing_time():
    resolved_directory = Path(data_directory).resolve()
    subdirs = [p for p in resolved_directory.iterdir() if p.is_dir()]

    subsubdirs = []
    for subdir in subdirs:
        resolved_subdir = Path(subdir).resolve()
        subsubdirs.extend(p for p in resolved_subdir.iterdir() if p.is_dir())

    total_dirs = len(subsubdirs)
    print(f"Start! There are {total_dirs} run directories to graph")

    dir_count = 0
    with ProcessPoolExecutor() as executor:
        for status in executor.map(graph_subsubdir, [str(s) for s in subsubdirs]):
            dir_count += 1
            print(f"{status} ({dir_count}/{total_dirs})")


if __name__ == "__main__":
    its_graphing_time()
