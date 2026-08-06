import pandas as pd
import numpy as np
import parameters

def count_surpass_critical_value(value, critical_point, measurements_csv, run_averages_csv):
    measurement_df = pd.read_csv(measurements_csv)
    run_avg_df = pd.read_csv(run_averages_csv)
    frames = int(parameters.nLoop / parameters.pInterval)
    frame = 0

    amount_of_times = (measurement_df[value] >= critical_point).sum()
    value_count_string = value + "_times_over_" + str(critical_point)
    



    run_avg_df[value_count_string] = amount_of_times

def count_multiple_variables(measurements_csv, run_averages_csv):
    variables = {
            "Rg" : 15,
            }
    for variable, critical_value in variables.items():
        count_surpass_critical_value(variable, critical_value, measurements_csv, run_averages_csv)


