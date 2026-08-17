import numpy as np
import pandas as pd

from . import parameters

# nLoop = 1000


def find_direction_of_head(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Finding direction of head")

    nLoop = parameters.nLoop / 1000
    df = coordinate_df
    calculated_data_df = measurement_df
    frame = 0

    my_weird_calculated_direction_rows = []
    direction_rows = []
    x_unit_vector = np.array([1, 0])
    while frame < nLoop:
        x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["xcoord"]
        y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["ycoord"]
        x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["xcoord"]
        y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["ycoord"]
        x = float(x_2.iloc[0]) - float(x_1.iloc[0])
        y = float(y_2.iloc[0]) - float(y_1.iloc[0])
        theta = np.arctan2(y, x)
        """
        head_bead_vector = np.array([x, y])

        head_bead_vector_magnitude = np.sqrt(head_bead_vector[0]**2 + head_bead_vector[1]**2)
        head_bead_vector_unit = head_bead_vector / head_bead_vector_magnitude
"""
        # based on cos^2 + sin^2 = 1, if doing cos = sqrt(1-sin^2)
        radians = theta
        """
        if radians < 0:
            if radians >= -np.pi and radians <= -np.pi/2:
                radians = (radians + np.pi/2)*-1
            elif radians > -np.pi/2 and radians < 0:
                radians = radians - np.pi/2
        elif radians > 0:
            if radians > 0 and radians <= np.pi/2:
                radians = -np.pi/2 + radians
            elif radians <= np.pi and radians > np.pi/2:
                radians = 3*np.pi/2 - radians
        elif radians == 0:
            radians = -np.pi/2
           """

        my_weird_calculated_direction_rows.append(radians)
        direction_rows.append(theta)
        frame = frame + 1

    # calculated_data_df["radians"] = direction_rows
    calculated_data_df["radians"] = my_weird_calculated_direction_rows

    return calculated_data_df


# find_direction_of_head("./csv_files/F5.0_K0.5_theta0.0.csv","./calculated_data/real_polymer_test.csv")
