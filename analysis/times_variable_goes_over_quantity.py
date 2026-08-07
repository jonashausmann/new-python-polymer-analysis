import pandas as pd
import numpy as np
import parameters

def count_surpass_critical_value(value, critical_point, measurements_csv, run_averages_csv):
    measurement_df = pd.read_csv(measurements_csv)
    run_avg_df = pd.read_csv(run_averages_csv)
    frame = 0






    if measurement_df[(measurement_df["frames"] == 0)][value] > critical_point:  
        amount_of_times = (measurement_df[value] >= critical_point).sum()
        value_count_string = value + "_times_over_" + str(critical_point)
    else:
        amount_of_times = (measurement_df[value] <= critical_point).sum()
        value_count_string = value + "_times_over_" + str(critical_point)

    

    print(amount_of_times)

'''
    run_avg_df[value_count_string] = amount_of_times
    run_avg_df.to_csv(run_averages_csv, index=False)
'''
def count_multiple_variables(measurements_csv_path, run_averages_csv):
    variables = {
            "Rg" : 10.0,
            "mean_curv" : 100,
            }
    for variable, critical_value in variables.items():
        count_surpass_critical_value(variable, critical_value, measurements_csv_path, run_averages_csv)

count_multiple_variables("../data/F10_K5_theta0.0/RUN_0001/csv_files/F10.0_K5.0_theta0.0_measurements.csv", "../data/F10_K5_theta0.0/Averaged_Runs/average.csv")
