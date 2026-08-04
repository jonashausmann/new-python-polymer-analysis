import pandas as pd
import numpy as np

import analysis
from analysis import parameters

def main(simulation_directory):

    frames = parameters.nLoop / 1000
    coordinate_csv_name = analysis.xyz_to_csv_conversion.xyz_to_csv(simulation_directory)





    measurement_csv_name = coordinate_csv_name.replace(".csv","") + "_measurements" + ".csv"


    measurement_df = pd.DataFrame({'frames' : np.arange(frames)})
    measurement_df.to_csv(measurement_csv_name, index=False)

    analysis.rg_calculation.calculate_radius_of_gyration(coordinate_csv_name, measurement_csv_name)
    analysis.direction_of_head_bead.find_direction_of_head(coordinate_csv_name, measurement_csv_name)
    analysis.curvature_mean_max.calculate_curvature(coordinate_csv_name, measurement_csv_name)
    analysis.turning_number.caclulate_turning_number(coordinate_csv_name, measurement_csv_name)
    analysis.winding_number.winding_number_around_head(coordinate_csv_name, measurement_csv_name)
    analysis.density.compute_density(measurement_csv_name)



main("../data/F05_K0.5_theta0.0/RUN_0001/")





