import numpy as np

from . import parameters


def calculate_radius_of_gyration(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating Rg")

    nLoop = parameters.nLoop / 1000
    monomers = parameters.monomers
    calculated_rows = []
    frame = 0
    calculated_df = measurement_df
    df = coordinate_df
    while frame < nLoop:
        sum = 0
        xcoords = df[df["frame"] == frame]["xcoord"]
        ycoords = df[df["frame"] == frame]["ycoord"]
        x_mean = np.mean(xcoords)
        y_mean = np.mean(ycoords)
        for xcoord, ycoord in zip(xcoords, ycoords):
            x_diff = xcoord - x_mean
            x_sqr = x_diff * x_diff
            y_diff = ycoord - y_mean
            y_sqr = y_diff * y_diff
            sum = sum + y_sqr + x_sqr
        Rg_sqrd = sum / monomers
        Rg = np.sqrt(Rg_sqrd)
        calculated_rows.append(Rg)
        frame = frame + 1
    calculated_df["Rg"] = calculated_rows
    return calculated_df
