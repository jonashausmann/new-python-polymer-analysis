import numpy as np
import pandas as pd

from analysis import parameters


def calculate_max_phi_diff(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating max phi difference")

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

    new_df = pd.DataFrame(
        {
            "frames": np.arange(frames),
            "max_phi_diff": np.round(diffreence_between_bond_angles.max(axis=1), 5),
        }
    )

    measurement_df = measurement_df.merge(new_df, on="frames", how="right")
    return measurement_df
