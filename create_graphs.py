import pandas as pd
import os
import numpy as np
from pathlib import Path

import visualize_data
from visualize_data import frame_graph

def its_graphing_time():
    resolved_directory = Path("/Volumes/project_files/ucmerced/2026/monika_simulations/").resolve()
    subdirs = [p for p in resolved_directory.iterdir() if p.is_dir()]

    for subdir in subdirs:
        resolved_subdir = Path(subdir).resolve()
        subsubdirs = [p for p in resolved_subdir.iterdir() if p.is_dir()]
        for subsubdir in subsubdirs:
            csv_folder = str(subsubdir) + "/csv_files/"
            csv_folder_resolved = Path(csv_folder).resolve()
            csv_file = list(csv_folder_resolved.glob("*_measurements.csv"))
            if len(csv_file) != 0:
                csv_file_name = str(csv_file[0])
                frame_graph.run_for_all_columns(csv_file_name)

its_graphing_time()
