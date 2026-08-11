import numpy as np
import pandas as pd

from analysis import parameters


def count_nearest_neighbors(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating nearest neighbors")

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / parameters.pInterval)

    df = coordinate_df.sort_values(["frame", "monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    head_bead = coords[:, 0:1, :]
    vector_from_head_to_bead = coords[:, 1:, :] - head_bead
    distances = np.linalg.norm(vector_from_head_to_bead, axis=2)
    within_one = distances <= 1

    neighbor_count = within_one.sum(axis=1)

    monomer_numbers = np.arange(2, monomers + 1)
    neighbor_lists = []
    max_neighbor = []
    frame = 0
    while frame < frames:
        neighbor_indices = np.nonzero(within_one[frame])[0]
        max_neighbor.append(int(max(neighbor_indices, default=0) + 2))
        nearest_neighbor_list = []
        for index in neighbor_indices:
            nearest_neighbor_list.append(int(monomer_numbers[index]))
            nearest_neighbor_list.append(float(distances[frame, index]))
        neighbor_lists.append(nearest_neighbor_list)
        frame = frame + 1

    neighbor_df = pd.DataFrame(
        {
            "frames": np.arange(frames),
            "neighbor_count": neighbor_count.astype(int),
            "neighbor_monomor_neighbor_distance": neighbor_lists,
            "max_neighbor_monomer": max_neighbor,
        }
    )

    measurement_df = pd.merge(measurement_df, neighbor_df, on="frames", how="right")
    return measurement_df
