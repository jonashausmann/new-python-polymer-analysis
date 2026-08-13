import numpy as np
import pandas as pd

from . import parameters


def calculate_inverse_average_spacing(coordinate_df, measurement_df):

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / parameters.pInterval)
    df = coordinate_df.sort_values(["frame", "monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)
    xs = coords[:, :, 0]
    ys = coords[:, :, 1]
    squared_distances = (xs[:, :, None] - xs[:, None, :]) ** 2
    squared_distances += (ys[:, :, None] - ys[:, None, :]) ** 2

    row = np.arange(monomers - 1)
    column = np.arange(1, monomers)

    interm_matrix = squared_distances
    interm_matrix[:, row, column] = 0
    test_matrix = (xs[:, :, None] - xs[:, None, :]) ** 2
    test_matrix += (ys[:, :, None] - ys[:, None, :]) ** 2
    squared_distances = test_matrix - interm_matrix

    distances_we_want_matrix = squared_distances.sum(axis=2)
    sum_of_all_distances = distances_we_want_matrix.sum(axis=1)
    print(sum_of_all_distances)
    inv_average_of_all_distances = 1 / (sum_of_all_distances / monomers)

    inv_avg_df = pd.DataFrame(
        {"frames": np.arange(frames), "inv_avg_df": inv_average_of_all_distances}
    )
    measurement_df = pd.merge(measurement_df, inv_avg_df, on="frames", how="right")

    return measurement_df
