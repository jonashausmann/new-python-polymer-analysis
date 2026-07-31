import parameters
import pandas as pd
import numpy as np

nLoop = parameters.nLoop/1000
#nLoop = 1000

def find_direction_of_head(coordinate_csv,measurement_csv):
    df = pd.read_csv(coordinate_csv)
    calculated_data_df = pd.read_csv(measurement_csv)
    frame = 0





    direction_rows = []
    x_unit_vector = np.array([1,0])
    while frame < nLoop:
        x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["xcoord"]
        y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["ycoord"]
        x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["xcoord"]
        y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == 2)]["ycoord"]
        x = float(x_2.iloc[0]) -float(x_1.iloc[0])
        y = float(y_2.iloc[0]) - float(y_1.iloc[0])
        head_bead_vector = np.array([x, y])
        head_bead_vector_magnitude = np.sqrt(head_bead_vector[0]**2 + head_bead_vector[1]**2)
        head_bead_vector_unit = head_bead_vector / head_bead_vector_magnitude
        cos_theta = np.dot(head_bead_vector_unit, x_unit_vector)
        threed_x_unit_vector = np.array([1,0,0])
        threed_head_bead_unit_vector = np.array([head_bead_vector_unit[0], head_bead_vector_unit[1], 0])
        orthogonal_vec = np.cross(threed_head_bead_unit_vector, threed_x_unit_vector)
        sin_theta = np.sqrt(orthogonal_vec[0]**2 + orthogonal_vec[1]**2 + orthogonal_vec[2]**2)
        # based on cos^2 + sin^2 = 1, if doing cos = sqrt(1-sin^2)
        using_arccos_equation = np.sqrt(1-(sin_theta**2))
        theta = np.arccos(using_arccos_equation)
        degrees = (theta*180)/np.pi
        direction_rows.append(degrees)
        frame = frame + 1

    calculated_data_df["degrees"] = direction_rows
    print(np.mean(calculated_data_df["degrees"]))

    calculated_data_df.to_csv(measurement_csv, index=False)
        





find_direction_of_head("./csv_files/F5.0_K0.5_theta0.0.csv","./calculated_data/real_polymer_test.csv")




