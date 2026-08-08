import pandas as pd
import os
import numpy as np
from pathlib import Path

import analysis
from analysis import parameters

data_directory = "./data/"
#/Volumes/project_files/ucmerced/2026/monika_simulations/

def main(simulation_directory):
    simulation_directory = str(simulation_directory)

    frames = parameters.nLoop / 1000
    coordinate_csv_name = analysis.xyz_to_csv_conversion.xyz_to_csv(simulation_directory)

    


    measurement_csv_name = coordinate_csv_name.replace(".csv","") + "_measurements" + ".csv"
    coordinate_df = pd.read_csv(coordinate_csv_name)
    measurement_df = pd.DataFrame({'frames' : np.arange(frames)})
    print(f"CSV created in: {coordinate_csv_name.parent.name}")

    measurement_df = analysis.rg_calculation.calculate_radius_of_gyration(coordinate_df, measurement_df)
    measurement_df = analysis.direction_of_head_bead.find_direction_of_head(coordinate_df, measurement_df)
    measurement_df = analysis.curvature_mean_max.calculate_curvature(coordinate_df, measurement_df)
    measurement_df = analysis.turning_number.calculate_turning_number(coordinate_df, measurement_df)
    measurement_df = analysis.winding_number.winding_number_around_head(coordinate_df, measurement_df)
    measurement_df = analysis.density.compute_density(measurement_df)
    measurement_df.to_csv(measurement_csv_name, index=False)


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
        for subsubdir in subsubdirs:
            if Path(str(subsubdir) + "/csv_files/").exists():
                print(f"Skipping {subsubdir}, csv_files already exists")
                continue
            print(f"Starting Initial Calculations for {subsubdir}")
            try:
                main(subsubdir)
            except FileNotFoundError as e:
                print(f"Skipping {subsubdir}, required file not found: {e}")
                continue
            except IndexError as e:
                print(f"Skipping {subsubdir}, malformed frame data: {e}")
                continue
            print(f"Finished initial Calculation for {subsubdir}")
        sort_subsubdirs = sorted(subsubdirs, key=lambda x: int(x.name.split('_')[1]))

#        average_df = pd.DataFrame({"run" : np.arange(len(subsubdirs))})
#        average_csv_name = str(run_avg_resolved) + "/average.csv"
        #average_df.to_csv(average_csv_name, index=False)

        run_number = 1
        variables_to_average_min_max = ["Rg","turning_number",
                                        "winding_number","density"]
        variables_to_count_over_critical = {
                "mean_curv" : 27,
                "max_curv" : 119,
                "turning_number" : 3.7,
                "winding_number" : 3.4,
                "density" : 2,
                }
        variables_to_count_under_critical = {
                "Rg" : 2.7,
                "winding_number" : -3.4,
                "turning_number" : -3.7,
                }
        variable_dict = {}
        total_counts_over_critical = {} 
        total_counts_under_critical = {}
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

        
            # Counting how many times a variable goes over a critical value
            for variable, critical_value in variables_to_count_over_critical.items():
                new_variable, count = analysis.times_variable_goes_over_quantity.count_surpass_critical_value(variable, critical_value, measurement_df)
                total_counts_over_critical.setdefault(new_variable, []).append(int(count))

                measurement_df = analysis.critical_streaks.count_critical_value_streak_greater_than(measurement_df, variable, critical_value)
            # Counting how many times a variable goes under a critical value
            for variable, critical in variables_to_count_under_critical.items():
                new_variable, count = analysis.times_variable_goes_over_quantity.count_under_critical_value(variable, critical, measurement_df)
                total_counts_under_critical.setdefault(new_variable, []).append(int(count))
                measurement_df = analysis.critical_streaks.count_critical_value_streak_less_than(measurement_df, variable, critical)

                


            # the average streak and the longest streak
            for variable, critical_value in variables_to_count_over_critical.items():
                variable_mean = variable + "_over_" + str(critical_value) + "_streak" + "_mean"
                variable_max = variable + "_over_" + str(critical_value) + "_streak" + "_max"
                variable_dict.setdefault(variable_mean,[]).append(np.mean(measurement_df[variable]))
                variable_dict.setdefault(variable_max,[]).append(np.max(measurement_df[variable]))

            # the average streak and the longest streak
            for variable, critical_value in variables_to_count_under_critical.items():
                variable_mean = variable + "_under_" + str(critical_value) + "_streak" + "_mean"
                variable_max = variable + "_under_" + str(critical_value) + "_streak" + "_max"
                variable_dict.setdefault(variable_mean,[]).append(np.mean(measurement_df[variable]))
                variable_dict.setdefault(variable_max,[]).append(np.max(measurement_df[variable]))

            

            # Creating mean, max and min data
            for variable in variables_to_average_min_max:
                variable_mean = variable + "_mean"
                variable_max = variable + "_max"
                variable_min = variable + "_min"

                variable_dict.setdefault(variable_mean,[]).append(np.mean(measurement_df[variable]))
                variable_dict.setdefault(variable_max,[]).append(np.max(measurement_df[variable]))
                variable_dict.setdefault(variable_min,[]).append(np.min(measurement_df[variable]))

            variable_dict.setdefault("direction_mean",[]).append(np.mean(measurement_df["degrees"]))
            variable_dict.setdefault("mean_curv_mean",[]).append(np.mean(measurement_df["mean_curv"]))
            variable_dict.setdefault("max_curv_max",[]).append(np.max(measurement_df["max_curv"]))
            variable_dict.setdefault("min_curv_min",[]).append(np.min(measurement_df["min_curv"]))

            variable_dict.setdefault("nLoop",[]).append(parameters.nLoop/1000)
            variable_dict.setdefault("bending",[]).append(parameters.bending)
            variable_dict.setdefault("activity",[]).append(parameters.activity)
            variable_dict.setdefault("theta",[]).append(parameters.ChiralityAngle)
            run_number = run_number + 1
        print(total_counts_over_critical)
        print(total_counts_under_critical)


        counts_over_df = pd.DataFrame(total_counts_over_critical)
        counts_under_df = pd.DataFrame(total_counts_under_critical)
        average_df = pd.DataFrame(variable_dict)
        average_df = pd.merge(average_df, counts_over_df, on="run",how="right")
        average_df = pd.merge(average_df, counts_under_df, on="run",how="right")
        run_average_directory = str(subdir) + "/Averaged_Runs/"
        os.makedirs(run_average_directory, exist_ok=True)
        run_avg_resolved = Path(run_average_directory).resolve()
        average_csv_name = str(run_avg_resolved) + "/average.csv"
        average_df.to_csv(average_csv_name, index=False)
        finished_parameter_directories = finished_parameter_directories + 1
        print(f"Progress :{finished_parameter_directories}/{total_dirs}")

find_directories_and_run_for_all(data_directory)

