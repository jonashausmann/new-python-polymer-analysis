import numpy as np

from analysis import parameters


def calculate_turning_number(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Turning number")

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / 1000)
    df = coordinate_df

    df = df.sort_values(["frame", "monomernumber"])

    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    bead_vectors = np.diff(coords, axis=1)

    phi = np.degrees(np.arctan2(bead_vectors[..., 1], bead_vectors[..., 0]))
    diffreence_between_bond_angles = np.diff(phi, axis=1)
    diffreence_between_bond_angles = (
        diffreence_between_bond_angles + 180.0
    ) % 360 - 180

    turning_number = diffreence_between_bond_angles.sum(axis=1) / 360.0

    measurement_df["turning_number"] = turning_number
    return measurement_df
