import numpy as np
import pandas as pd

from analysis import parameters


def average_filament_neighbors(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating average filament neighbors")

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / parameters.pInterval)

    df = coordinate_df.sort_values(["frame", "monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    xs = coords[:, :, 0]
    ys = coords[:, :, 1]
    squared_distances = (xs[:, :, None] - xs[:, None, :]) ** 2
    squared_distances += (ys[:, :, None] - ys[:, None, :]) ** 2

    within_one = squared_distances <= 1.0
    diagonal = np.arange(monomers)
    within_one[:, diagonal, diagonal] = False

    neighbors_per_bead = within_one.sum(axis=2)

    average_neighbors = neighbors_per_bead.mean(axis=1)
    std_neighbors = neighbors_per_bead.std(axis=1)

    neighbor_avg_df = pd.DataFrame(
        {
            "frames": np.arange(frames),
            "average_neighbors": average_neighbors,
            "std_neighbors": std_neighbors,
        }
    )
    measurement_df = pd.merge(measurement_df, neighbor_avg_df, on="frames", how="right")
    return measurement_df
