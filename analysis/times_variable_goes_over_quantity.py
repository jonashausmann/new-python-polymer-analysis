import pandas as pd
import numpy as np
import parameters

def count_surpass_critical_value(value, critical_point, measurements_csv):
    measurement_df = measurements_csv#pd.read_csv(measurements_csv)







    
    if measurement_df[(measurement_df["frames"] == 0)][value].iloc[0] > critical_point:  
        amount_of_times = (measurement_df[value] >= critical_point).sum()
        value_count_string = value + "_times_over_" + str(critical_point)
    else:
        amount_of_times = (measurement_df[value] <= critical_point).sum()
        value_count_string = value + "_times_under_" + str(critical_point)

    
    return value_count_string, amount_of_times



def count_multiple_variables(measurements_csv_path):
    variables = {
            "Rg" : 10.0,
            "mean_curv" : 6,
            }
    counts_over_critical = {}
    for variable, critical_value in variables.items():
        new_variable, count = count_surpass_critical_value(variable, critical_value, measurements_csv_path)
        counts_over_critical[new_variable] = int(count)
    return counts_over_critical


#print(count_multiple_variables("../data/F10_K5_theta0.0/RUN_0001/csv_files/F10.0_K5.0_theta0.0_measurements.csv"))
