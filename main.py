import ast
import os
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

import analysis
from analysis import parameters

debug = False
neighbors = True
tail = True
density = False

data_directory = "./data/"
# /Volumes/project_files/ucmerced/2026/monika_simulations/

DIR_NAME_PATTERN = re.compile(
    r"^F(?P<F>[0-9.]+)_K(?P<K>[0-9.]+)_theta(?P<theta>[0-9.]+)$"
)

# Shared critical-value config, used both when writing each run's per-frame
# streak columns (in main, run in parallel) and when averaging the runs.
variables_to_count_over_critical = {
    # curvature is now measured in radians, so these are the radian equivalents
    # of the old 27 and 119 degree cutoffs
    "mean_curv": np.radians(27),
    "max_curv": np.radians(119),
    # turning/winding numbers stay dimensionless (number of turns)
    "turning_number": 3,
    "winding_number": 2.9,
}
"""
    "density": 2,
"""
variables_to_count_under_critical = {
    "Rg": 3.1,
    "winding_number": -3,
    "turning_number": -3,
}
values_for_crit_quant = [
    "Rg",
    "radians",
    "mean_curv",
    "max_curv",
    "min_curv",
    "max_curv_monomer",
    "min_curv_monomer",
    "turning_number",
    "winding_number",
]
"""
    "density",
    "neighbor_count",
    "max_neighbor_monomer",
    "tail_direction",
    "head_and_tail_angle_diff",
"""
variables_to_average_min_max = [
    "Rg",
    "turning_number",
    "winding_number",
    "Rg_frame_difference",
    "turning_number_frame_difference",
    "winding_number_frame_difference",
]
"""
    "density",
    "average_neighbors",
    "std_neighbors",
    "density_frame_difference",
    "average_neighbors_frame_difference",
    "std_neighbors_frame_difference",

"""
derivative_variables = [
    "Rg",
    "turning_number",
    "winding_number",
    "average_neighbors",
    "std_neighbors",
]
"""
    "max_phi_diff",
    "density",
"""


def main(simulation_directory):
    simulation_directory = str(simulation_directory)

    frames = parameters.nLoop / 1000
    coordinate_csv_name = analysis.xyz_to_csv_conversion.xyz_to_csv(
        simulation_directory
    )

    measurement_csv_name = (
        coordinate_csv_name.replace(".csv", "") + "_measurements" + ".csv"
    )
    coordinate_df = pd.read_csv(coordinate_csv_name)
    measurement_df = pd.DataFrame({"frames": np.arange(frames)})

    coordinate_csv_path = Path(coordinate_csv_name).resolve()
    print(f"CSV created in: {coordinate_csv_path.parent.name}")

    measurement_df = analysis.rg_calculation.calculate_radius_of_gyration(
        coordinate_df, measurement_df, debug
    )
    measurement_df = analysis.direction_of_head_bead.find_direction_of_head(
        coordinate_df, measurement_df, debug
    )
    measurement_df = analysis.curvature_mean_max.calculate_curvature(
        coordinate_df, measurement_df, debug
    )
    measurement_df = analysis.turning_number.calculate_turning_number(
        coordinate_df, measurement_df, debug
    )
    measurement_df = analysis.winding_number.winding_number_around_head(
        coordinate_df, measurement_df, debug
    )
    if density:
        measurement_df = analysis.density.compute_density(measurement_df, debug)
    if neighbors:
        measurement_df = analysis.head_nearest_neighbors.count_nearest_neighbors(
            coordinate_df, measurement_df, debug
        )
        measurement_df = analysis.all_neighbors.average_filament_neighbors(
            coordinate_df, measurement_df, debug
        )

    for variable, critical_value in variables_to_count_over_critical.items():
        measurement_df, discard = (
            analysis.critical_streaks.count_critical_value_streak_greater_than(
                measurement_df, variable, critical_value, debug
            )
        )
    for variable, critical_value in variables_to_count_under_critical.items():
        measurement_df, discard = (
            analysis.critical_streaks.count_critical_value_streak_less_than(
                measurement_df, variable, critical_value, debug
            )
        )
    if tail:
        measurement_df = (
            analysis.angle_between_head_and_tail_neighbor.find_angle_between(
                measurement_df, coordinate_df, 2, debug
            )
        )

    measurement_df = analysis.derivatives.calculate_derivatives(
        derivative_variables, measurement_df, debug
    )

    measurement_df = analysis.max_phi_diff.calculate_max_phi_diff(
        coordinate_df, measurement_df
    )

    measurement_df = analysis.inverse_average_space_between_monomers.calculate_inverse_average_spacing(
        coordinate_df, measurement_df
    )

    measurement_df.to_csv(measurement_csv_name, index=False)


def run_initial_calculation(subsubdir):
    subsubdir = str(subsubdir)
    if Path(subsubdir + "/csv_files/").exists():
        return f"Skipping {subsubdir}, csv_files already exists"
    print(f"Starting Initial Calculations for {subsubdir}")
    try:
        main(subsubdir)
    except FileNotFoundError as e:
        return f"Skipping {subsubdir}, required file not found: {e}"
    except IndexError as e:
        return f"Skipping {subsubdir}, malformed frame data: {e}"
    return f"Finished initial Calculation for {subsubdir}"


def find_directories_and_run_for_all(data_directory):
    resolved_directory = Path(data_directory).resolve()
    subdirs = [p for p in resolved_directory.iterdir() if p.is_dir()]

    finished_parameter_directories = 0
    total_dirs = sum(1 for _ in resolved_directory.iterdir() if _.is_dir())
    print(f"Start! There are {total_dirs} directories")

    for subdir in subdirs:
        resolved_subdir = Path(subdir).resolve()
        subsubdirs = [p for p in resolved_subdir.iterdir() if p.is_dir()]
        subsubdirs = [p for p in subsubdirs if "RUN" in p.name]
        with ProcessPoolExecutor() as executor:
            for status in executor.map(
                run_initial_calculation, [str(s) for s in subsubdirs]
            ):
                print(status)
        sort_subsubdirs = sorted(subsubdirs, key=lambda x: int(x.name.split("_")[1]))

        #        average_df = pd.DataFrame({"run" : np.arange(len(subsubdirs))})
        #        average_csv_name = str(run_avg_resolved) + "/average.csv"
        # average_df.to_csv(average_csv_name, index=False)

        run_number = 1
        dir_name_match = DIR_NAME_PATTERN.match(Path(subdir).name)
        variable_dict = {}
        total_counts_over_critical = {}
        total_counts_under_critical = {}
        unique_under_streak_dict = {}
        unique_over_streak_dict = {}

        rg_crit_dict = {}
        for subsubdir in sort_subsubdirs:
            print(f"Starting average calculations for run {run_number}")
            csv_folder = str(subsubdir) + "/csv_files/"
            csv_folder_resolved = Path(csv_folder).resolve()
            csv_file = list(csv_folder_resolved.glob("*_measurements.csv"))
            if len(csv_file) == 0:
                print(f"Skipping average for {subsubdir}, no measurements csv found")
                continue
            csv_file_name = str(csv_file[0])
            measurement_df = pd.read_csv(csv_file_name)

            variable_dict.setdefault("run", []).append(run_number)
            total_counts_over_critical.setdefault("run", []).append(run_number)
            total_counts_under_critical.setdefault("run", []).append(run_number)
            unique_over_streak_dict.setdefault("run", []).append(run_number)
            unique_under_streak_dict.setdefault("run", []).append(run_number)
            rg_crit_dict.setdefault("run", []).append(run_number)

            # Counting how frames a variable is over a critical value
            for variable, critical_value in variables_to_count_over_critical.items():
                new_variable, count = (
                    analysis.times_variable_goes_over_quantity.count_surpass_critical_value(
                        variable, critical_value, measurement_df
                    )
                )
                total_counts_over_critical.setdefault(new_variable, []).append(
                    int(count)
                )

                measurement_df, unique_over_streak = (
                    analysis.critical_streaks.count_critical_value_streak_greater_than(
                        measurement_df, variable, critical_value
                    )
                )
                unique_over_streak_name = (
                    variable + "_over_" + str(critical_value) + "_unique_streaks"
                )
                unique_over_streak_dict.setdefault(unique_over_streak_name, []).append(
                    unique_over_streak
                )

            # Counting how frames a variable is under a critical value
            for variable, critical in variables_to_count_under_critical.items():
                new_variable, count = (
                    analysis.times_variable_goes_over_quantity.count_under_critical_value(
                        variable, critical, measurement_df
                    )
                )
                total_counts_under_critical.setdefault(new_variable, []).append(
                    int(count)
                )
                measurement_df, unique_under_streak = (
                    analysis.critical_streaks.count_critical_value_streak_less_than(
                        measurement_df, variable, critical
                    )
                )
                unique_under_streak_name = (
                    variable + "_under_" + str(critical_value) + "_unique_streaks"
                )
                unique_under_streak_dict.setdefault(
                    unique_under_streak_name, []
                ).append(unique_under_streak)

            # for a given critical value, what quantifications are within it?
            rg_crit_dict = analysis.rows_for_crit_csv.create_crit_under_row(
                measurement_df,
                "Rg",
                variables_to_count_under_critical["Rg"],
                values_for_crit_quant,
                rg_crit_dict,
            )

            # the average streak and the longest streak
            for variable, critical_value in variables_to_count_over_critical.items():
                streak_column = variable + "_over_" + str(critical_value) + "_streak"
                variable_mean = streak_column + "_mean"
                variable_max = streak_column + "_max"
                variable_dict.setdefault(variable_mean, []).append(
                    np.mean(measurement_df[streak_column])
                )
                variable_dict.setdefault(variable_max, []).append(
                    np.max(measurement_df[streak_column])
                )

            # the average streak and the longest streak
            for variable, critical_value in variables_to_count_under_critical.items():
                streak_column = variable + "_under_" + str(critical_value) + "_streak"
                variable_mean = streak_column + "_mean"
                variable_max = streak_column + "_max"
                variable_dict.setdefault(variable_mean, []).append(
                    np.mean(measurement_df[streak_column])
                )
                variable_dict.setdefault(variable_max, []).append(
                    np.max(measurement_df[streak_column])
                )

            # nearest neighbor max and mean count

            # Creating mean, max and min data
            for variable in variables_to_average_min_max:
                variable_mean = variable + "_mean"
                variable_max = variable + "_max"
                variable_min = variable + "_min"
                variable_std = variable + "_std"

                variable_dict.setdefault(variable_mean, []).append(
                    np.mean(measurement_df[variable])
                )
                variable_dict.setdefault(variable_max, []).append(
                    np.max(measurement_df[variable])
                )
                variable_dict.setdefault(variable_min, []).append(
                    np.min(measurement_df[variable])
                )
                variable_dict.setdefault(variable_std, []).append(
                    np.std(measurement_df[variable])
                )

            variable_dict.setdefault("direction_mean", []).append(
                np.mean(measurement_df["radians"])
            )
            variable_dict.setdefault("mean_curv_mean", []).append(
                np.mean(measurement_df["mean_curv"])
            )
            variable_dict.setdefault("max_curv_max", []).append(
                np.max(measurement_df["max_curv"])
            )
            variable_dict.setdefault("min_curv_min", []).append(
                np.min(measurement_df["min_curv"])
            )

            if neighbors:
                variable_dict.setdefault("mean_neighbor_count", []).append(
                    np.mean(measurement_df["neighbor_count"])
                )
                variable_dict.setdefault("max_neighbor_count", []).append(
                    np.max(measurement_df["neighbor_count"])
                )

                def split_monomer_and_distance(string_list):
                    if string_list == "[]":
                        return [], []
                    lst = ast.literal_eval(string_list)
                    monomers = lst[0::2]
                    distances = lst[1::3]
                    return monomers, distances

                (
                    measurement_df["nearest_monomers"],
                    measurement_df["monomer_distances"],
                ) = zip(
                    *measurement_df["neighbor_monomor_neighbor_distance"].apply(
                        split_monomer_and_distance
                    )
                )

                all_nearest_monomers = [
                    x for sublist in measurement_df["nearest_monomers"] for x in sublist
                ]
                all_monomer_distances = [
                    x
                    for sublist in measurement_df["monomer_distances"]
                    for x in sublist
                ]

                # mean_monomer = np.mean(all_nearest_monomers) if all_nearest_monomers else np.nan
                mean_distance = (
                    np.mean(all_monomer_distances) if all_monomer_distances else np.nan
                )
                max_monomer = (
                    np.max(all_nearest_monomers) if all_nearest_monomers else np.nan
                )
                min_distance = (
                    np.min(all_monomer_distances) if all_monomer_distances else np.nan
                )

                variable_dict.setdefault("max_neighbor_monomer", []).append(max_monomer)
                variable_dict.setdefault("mean_neighbor_distance", []).append(
                    mean_distance
                )
                variable_dict.setdefault("min_neighbor_distance", []).append(
                    min_distance
                )

            variable_dict.setdefault("nLoop", []).append(parameters.nLoop / 1000)
            variable_dict.setdefault("bending", []).append(
                float(dir_name_match.group("K"))
                if dir_name_match
                else parameters.bending
            )
            variable_dict.setdefault("activity", []).append(
                float(dir_name_match.group("F"))
                if dir_name_match
                else parameters.activity
            )
            variable_dict.setdefault("theta", []).append(
                float(dir_name_match.group("theta"))
                if dir_name_match
                else np.degrees(parameters.ChiralityAngle)
            )

            run_number = run_number + 1
        if debug:
            print(total_counts_over_critical)
            print(total_counts_under_critical)

        if len(variable_dict) == 0:
            print(f"Skipping average for {subdir}, no runs produced measurements")
            continue

        unique_under_streaks_df = pd.DataFrame(unique_under_streak_dict)
        unique_over_streaks_df = pd.DataFrame(unique_over_streak_dict)
        counts_over_df = pd.DataFrame(total_counts_over_critical)
        counts_under_df = pd.DataFrame(total_counts_under_critical)
        crit_rg_average_df = pd.DataFrame(rg_crit_dict)
        average_df = pd.DataFrame(variable_dict)
        average_df = pd.merge(average_df, counts_over_df, on="run", how="right")
        average_df = pd.merge(average_df, counts_under_df, on="run", how="right")
        average_df = pd.merge(
            average_df, unique_under_streaks_df, on="run", how="right"
        )
        average_df = pd.merge(average_df, unique_over_streaks_df, on="run", how="right")
        average_df = pd.merge(average_df, crit_rg_average_df, on="run", how="right")
        run_average_directory = str(subdir) + "/Averaged_Runs/"
        os.makedirs(run_average_directory, exist_ok=True)
        run_avg_resolved = Path(run_average_directory).resolve()
        average_csv_name = str(run_avg_resolved) + "/average.csv"
        average_df.to_csv(average_csv_name, index=False)

        finished_parameter_directories = finished_parameter_directories + 1
        print(f"Progress :{finished_parameter_directories}/{total_dirs}")


if __name__ == "__main__":
    find_directories_and_run_for_all(data_directory)
