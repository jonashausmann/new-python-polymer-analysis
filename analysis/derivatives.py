import numpy as np
import pandas as pd

from . import parameters


def calculate_derivatives(list_of_variables, measurement_df, debug=False):

    if debug:
        print("Calculating variable differences")

    df = measurement_df

    frames = int(parameters.nLoop / parameters.pInterval)
    for variable in list_of_variables:
        frame = 1
        difference_list = [0.0]
        while frame < frames:
            value_one = df[(df["frames"] == frame - 1)][variable]
            value_two = df[(df["frames"] == frame)][variable]
            difference = float(value_two.iloc[0]) - float(value_one.iloc[0])
            difference_list.append(float(difference))
            frame = frame + 1
        variable_diff_name = str(variable) + "_frame_difference"
        df[variable_diff_name] = difference_list
    return df
