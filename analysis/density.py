import numpy as np
import pandas as pd
from analysis import parameters


def compute_density(measurement_df):
    monomers = parameters.monomers
    frames = parameters.nLoop/1000
    df = measurement_df
    frame = 0
    


    frame_density_row = []
    while frame < frames:
        Rg = df[(df["frames"] == frame)]["Rg"]
        density = monomers/(np.pi * Rg.iloc[0] * Rg.iloc[0])
        frame_density_row.append(density)
        frame = frame + 1
    df["density"] = frame_density_row
    return df

