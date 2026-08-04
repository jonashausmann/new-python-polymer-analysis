import numpy as np
import pandas as pd
from analysis import parameters

monomers = parameters.monomers
frames = parameters.nLoop/1000
frames = 100

def compute_density(measurement_csv):
    df = pd.read_csv(measurement_csv)
    frame = 0
    


    frame_density_row = []
    while frame < frames:
        Rg = df[(df["frames"] == frame)]["Rg"]
        density = monomers/(np.pi * Rg * Rg)
        frame_density_row.append(density)
        frame = frame + 1
    df["density"] = frame_density_row
    df.to_csv(measurement_csv, index=False)

compute_density("./calculated_data/real_polymer_test.csv")
