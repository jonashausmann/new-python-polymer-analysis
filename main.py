import pandas as pd
import os
import numpy as np
from pathlib import Path

import analysis
from analysis import parameters

def main(simulation_directory):
    simulation_directory = str(simulation_directory)

    frames = parameters.nLoop / 1000
    coordinate_csv_name = analysis.xyz_to_csv_conversion.xyz_to_csv(simulation_directory)

    


    measurement_csv_name = coordinate_csv_name.replace(".csv","") + "_measurements" + ".csv"
    measurement_df = pd.DataFrame({'frames' : np.arange(frames)})
    measurement_df.to_csv(measurement_csv_name, index=False)
    print(f"CSV created: {coordinate_csv_name}")

    analysis.rg_calculation.calculate_radius_of_gyration(coordinate_csv_name, measurement_csv_name)
    print("Rg Calculated")
    analysis.direction_of_head_bead.find_direction_of_head(coordinate_csv_name, measurement_csv_name)
    print("Direction of Head Bead Calculated")
    analysis.curvature_mean_max.calculate_curvature(coordinate_csv_name, measurement_csv_name)
    print("Curvature Calculated")
    analysis.turning_number.calculate_turning_number(coordinate_csv_name, measurement_csv_name)
    print("Turning Number Calculated")
    analysis.winding_number.winding_number_around_head(coordinate_csv_name, measurement_csv_name)
    print("Winding Number Calculated")
    analysis.density.compute_density(measurement_csv_name)
    print("Density Calculated")

def find_directories_and_run_for_all():
    resolved_directory = Path("./data/").resolve()
    subdirs = [p for p in resolved_directory.iterdir() if p.is_dir()]

    for subdir in subdirs:
        resolved_subdir = Path(subdir).resolve()
        subsubdirs = [p for p in resolved_subdir.iterdir() if p.is_dir()]
        subsubdirs = [p for p in subsubdirs if "RUN" in p.name]
        for subsubdir in subsubdirs:
            print(f"Starting Initial Calculations for {subsubdir}")
            main(subsubdir)
            print(f"Finished initial Calculation for {subsubdir}")
        sort_subsubdirs = sorted(subsubdirs, key=lambda x: int(x.name.split('_')[1]))

#        average_df = pd.DataFrame({"run" : np.arange(len(subsubdirs))})
#        average_csv_name = str(run_avg_resolved) + "/average.csv"
        #average_df.to_csv(average_csv_name, index=False)

        run_number = 1
        variables_to_average_min_max = ["Rg","turning_number",
                                        "winding_number","density"]
        variable_dict = {}
        for subsubdir in sort_subsubdirs:
            print(f"Starting average calculations for run {run_number}")
            csv_folder = str(subsubdir) + "/csv_files/"
            csv_folder_resolved = Path(csv_folder).resolve()
            csv_file = list(csv_folder_resolved.glob("*_measurements.csv"))
            csv_file_name = str(csv_file[0])
            measurement_df = pd.read_csv(csv_file_name)

            variable_dict.setdefault("run", []).append(run_number)

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

        average_df = pd.DataFrame(variable_dict)
        run_average_directory = str(subdir) + "/Averaged_Runs/"
        os.mkdir(run_average_directory)
        run_avg_resolved = Path(run_average_directory).resolve()
        average_csv_name = str(run_avg_resolved) + "/average.csv"
        average_df.to_csv(average_csv_name, index=False)
        print(f"Calculations Complete for {run_number}")



'''
            average_rg = np.mean(measurement_df["Rg"])
            average_df["average_rg"] = average_rg
            min_rg = np.min(measurement_df["Rg"])
            average_df["min_rg"] = min_rg
            max_rg = np.max(measurement_df["Rg"])
            average_df["max_rg"] = max_rg

            average_direct = np.mean(measurement_df["degrees"])
            average_df["average_direction_of_head"] = average_direct

            average_curv = np.mean(measurement_df["mean_curv"])
            average_df["average_curv"] = average_curv
            min_curv = np.min(measurement_df["min_curv"])
            average_df["min_curv"] = min_curv
            max_curv = np.max(measurement_df["max_curv"])
            average_df["max_curv"] = max_curv

            average_turn = np.mean(measurement_df["turning_number"])
            average_df["average_turn_number"] = average_turn
            min_turn = np.min(measurement_df["turning_number"])
            average_df["min_turn_number"] = min_turn
            max_turn = np.max(measurement_df["turning_number"])
            average_df["max_turn_number"] = max_turn

            average_wind = np.mean(measurement_df["winding_number"])
            average_df["average_winding"] = average_wind
            min_wind = np.min(measurement_df["winding_number"])
            average_df["min_winding"] = min_wind
            max_wind = np.max(measurement_df["winding_number"])
            average_df["max_winding"] = max_wind

            average_density = np.mean(measurement_df["density"])
            average_df["average_density"] = average_density
            min_density = np.min(measurement_df["density"])
            average_df["min_density"] = min_density
            max_density = np.max(measurement_df["density"])
            average_df["max_density"] = max_density

            average_df["nLoop"] = parameters.nLoop/1000
            average_df["bending"] = parameters.bending
            average_df["activity"] = parameters.activity
            average_df["theta"] = parameters.ChiralityAngle
'''





        
        


find_directories_and_run_for_all()
