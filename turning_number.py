import numpy as np
import pandas as pd
import analysis

#monomers = analysis.parameters.monomers 
#frames = anaylsis.parameters.nLoop/1000
frames = 1 
monomers = 7








def_calculate_turning_number(coordinate_csv, measurement_csv):
    coord_df = pd.read_csv(coordinate_csv)
    measurement_df = pd.read_csv(measurement_csv)
    frame = 0
    turning_number_row = []
    while frame < frames:
        monomer = 0
        frame_phi_angles = []
        for monomer in monomers-1:
            x_1 = df[(df["monomernumber"] == monomer)]["xcoord"]
            y_1 = df[(df["monomernumber"] == monomer)]["ycoord"]
            x_2 = df[(df["monomernumber"] == monomer + 1)]["xcoord"]
            y_2 = df[(df["monomernumber"] == monomer + 1)]["ycoord"]
            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            monomer_vec = np.array(x,y)
            monomer_unit_vec = monomer_vec / np.linalg.norm(monomer_vec)
            phi_angle = np.arctan2(y, x)
            frame_phi_angles.append(phi_angle)
        i = 0
        phi_differences = []
        while i < (len(frame_phi_angles)-1):
            monomer_phi_difference = frame_phi_angles[i+1] - frame_phi_angles[i]
            phi_differences.append(monomer_phi_difference)
            i = i + 1
        sum_of_phi = 0
        for phi_difference in phi_differences:
            sum_of_phi = sum_of_phi + phi_difference
        turning_number = sum_of_phi/(2*np.pi)
        turning_number_degrees = (turning_number*180)/np.pi
        turning_number_row.append(turning_number_degrees)
    measurement_df["turning_number"] = turning_number_row

    measurement_df.to_csv(measurement_csv, index=False)

def_calculate_turning_number("./data/writhe_data_test.csv","./calculated_data/turning_number_test.csv")










