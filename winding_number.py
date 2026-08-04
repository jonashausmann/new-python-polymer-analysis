import numpy as np
import pandas as pd
monomers = 7
frames = 1



def winding_number_around_head(coordinate_csv, measurement_csv):
    df = pd.read_csv(coordinate_csv)
    measurement_df = pd.read_csv(measurement_csv)
    frame = 0
    turning_number_row = []
    while frame < frames:
        monomer = 1
        frame_phi_angles = []
        x_1 = df[(df["monomernumber"] == 1)]["xcoord"]
        y_1 = df[(df["monomernumber"] == 1)]["ycoord"]
        while monomer < monomers:
            x_2 = df[(df["monomernumber"] == monomer+1)]["xcoord"]
            y_2 = df[(df["monomernumber"] == monomer+1)]["ycoord"]
            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            phi_angle = np.arctan2(y, x)
            frame_phi_angles.append(phi_angle)
            monomer = monomer + 1
            print(f"Monomer:{monomer} Phi Angle:{phi_angle}")
        i = 0
        phi_differences = []
        while i < (len(frame_phi_angles)-1):
            monomer_phi_difference = frame_phi_angles[i+1] - frame_phi_angles[i]
            monomer_phi_difference = (monomer_phi_difference*180)/np.pi
            phi_differences.append(monomer_phi_difference)
            print(f"Angle difference {(monomer_phi_difference*180)/np.pi}")
            i = i + 1
        sum_of_phi = 0
        for phi_difference in phi_differences:
            print(phi_difference)
            if phi_difference <= -180:
                phi_difference = phi_difference + 360
                print(f"I'm a changed phi_difference! {phi_difference}")
            elif phi_difference > 180:
                phi_difference = phi_difference - 360
            sum_of_phi = sum_of_phi + phi_difference
        turning_number = sum_of_phi/(360)
        turning_number_row.append(turning_number)
        frame = frame + 1
    measurement_df["winding_number"] = turning_number_row

    measurement_df.to_csv(measurement_csv, index=False)

winding_number_around_head("./data/writhe_data_test.csv", "./calculated_data/turning_number_test.csv")
