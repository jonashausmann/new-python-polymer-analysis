import pandas as pd
import numpy as np
from . import parameters

nLoop = parameters.nLoop/1000
#nLoop = 1000

def find_direction_of_head(coordinate_csv,measurement_csv):
    df = pd.read_csv(coordinate_csv)
    calculated_data_df = pd.read_csv(measurement_csv)
    frame = 0





    my_weird_calculated_direction_rows = []
    direction_rows = []
    x_unit_vector = np.array([1,0])
    while frame < nLoop:
        x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["xcoord"]
        y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["ycoord"]
        x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["xcoord"]
        y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["ycoord"]
        x = float(x_2.iloc[0]) -float(x_1.iloc[0])
        y = float(y_2.iloc[0]) - float(y_1.iloc[0])
        theta = np.arctan2(x,y)
        head_bead_vector = np.array([x, y])

        head_bead_vector_magnitude = np.sqrt(head_bead_vector[0]**2 + head_bead_vector[1]**2)
        head_bead_vector_unit = head_bead_vector / head_bead_vector_magnitude
        # based on cos^2 + sin^2 = 1, if doing cos = sqrt(1-sin^2)
        degrees = (theta*180)/np.pi 
        if degrees < 0:
            if degrees >= -180 and degrees <= -90:
                degrees = (degrees + 90)*-1
            elif degrees > -90 and degrees < 0:
                degrees = degrees - 90
        elif degrees > 0:
            if degrees > 0 and degrees <= 90:
                degrees = -90 + degrees
            elif degrees <= 180 and degrees > 90:
                degrees = 270 - degrees
        elif degrees == 0:
            degrees = -90
                


        my_weird_calculated_direction_rows.append(degrees)
        direction_rows.append((theta*180)/np.pi)
        frame = frame + 1

    # calculated_data_df["degrees"] = direction_rows
    calculated_data_df["degrees"] = my_weird_calculated_direction_rows
    print(np.mean(calculated_data_df["new_degrees"]))

    calculated_data_df.to_csv(measurement_csv, index=False)
        





#find_direction_of_head("./csv_files/F5.0_K0.5_theta0.0.csv","./calculated_data/real_polymer_test.csv")




