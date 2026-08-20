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

    phi = np.arctan2(bead_vectors[..., 1], bead_vectors[..., 0])
    diffreence_between_bond_angles = np.diff(phi, axis=1)
    diffreence_between_bond_angles = (diffreence_between_bond_angles + np.pi) % (
        2 * np.pi
    ) - np.pi

    # total turning angle in radians, and the same quantity as a dimensionless
    # number of turns (unchanged from when this was computed in degrees)
    turning_radians = diffreence_between_bond_angles.sum(axis=1)
    turning_number = turning_radians / (2 * np.pi)

    measurement_df["turning_number"] = turning_number
    measurement_df["turning_radians"] = turning_radians
    return measurement_df
