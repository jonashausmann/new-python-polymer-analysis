import numpy as np
import pandas as pd
from analysis import parameters


def winding_number_around_head(coordinate_df, measurement_df):
    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop/1000)






    df = coordinate_df

    df = df.sort_values(["frame","monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    head_bead = coords[:, 0:1, :]

    vector_from_head_to_bead = coords - head_bead
    vector_from_head_to_bead = vector_from_head_to_bead[:, 1:, :]
    phi = np.degrees(np.arctan2(vector_from_head_to_bead[..., 1], vector_from_head_to_bead[..., 0]))
    difference_between_angles = np.diff(phi, axis=1)
    difference_between_angles = (difference_between_angles + 180) % 360.0 - 180.0

    winding_number = difference_between_angles.sum(axis=1) / 360.0

    measurement_df["winding_number"] = winding_number
    return measurement_df
    '''
    frame = 0
    turning_number_row = []
    while frame < frames:
        monomer = 1
        frame_phi_angles = []
        x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["xcoord"]
        y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["ycoord"]
        while monomer < monomers:
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer+1)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer+1)]["ycoord"]
            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            phi_angle = np.arctan2(y, x)
            frame_phi_angles.append(phi_angle)
            monomer = monomer + 1
        i = 0
        phi_differences = []
        while i < (len(frame_phi_angles)-1):
            monomer_phi_difference = frame_phi_angles[i+1] - frame_phi_angles[i]
            monomer_phi_difference = (monomer_phi_difference*180)/np.pi
            phi_differences.append(monomer_phi_difference)
            i = i + 1
        sum_of_phi = 0
        for phi_difference in phi_differences:
            if phi_difference <= -180:
                phi_difference = phi_difference + 360
            elif phi_difference > 180:
                phi_difference = phi_difference - 360
            sum_of_phi = sum_of_phi + phi_difference
        turning_number = sum_of_phi/(360)
        turning_number_row.append(turning_number)
        frame = frame + 1
    measurement_df["winding_number"] = turning_number_row

    measurement_df.to_csv(measurement_csv, index=False)
'''
