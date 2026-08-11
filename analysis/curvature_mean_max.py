import numpy as np
import pandas as pd

from analysis import parameters


def calculate_curvature(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating curvature")

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / 1000)
    df = coordinate_df
    calculated_data_df = measurement_df

    df = df.sort_values(["frame", "monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    bead_pairs = np.diff(coords, axis=1)

    bond_1 = bead_pairs[:, :-1, :]
    bond_2 = bead_pairs[:, 1:, :]

    bond_1_unit = bond_1 / np.linalg.norm(bond_1, axis=2, keepdims=True)
    bond_2_unit = bond_2 / np.linalg.norm(bond_2, axis=2, keepdims=True)

    dot_product = np.clip(np.sum(bond_1_unit * bond_2_unit, axis=2), -1.0, 1.0)

    theta = np.degrees(np.arccos(dot_product))

    new_df = pd.DataFrame(
        {
            "frames": np.arange(frames),
            "mean_curv": np.round(theta.mean(axis=1), 5),
            "max_curv": np.round(theta.max(axis=1), 5),
            "max_curv_monomer": theta.argmax(axis=1) + 1,
            "min_curv": np.round(theta.min(axis=1), 5),
            "min_curv_monomer": theta.argmin(axis=1) + 1,
        }
    )

    calculated_data_df = calculated_data_df.merge(new_df, on="frames", how="left")
    return calculated_data_df
