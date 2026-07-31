import pandas as pd 
import numpy as np
import parameters

monomers = parameters.monomers
nLoop = parameters.nLoop

def calculate_curvature(coordinate_csv, measurement_csv):
    df = pd.read_csv(coordinate_csv)
    calculated_data_df = pd.read_csv(measurement_csv)
    frame = 0

    

    mean_curv_rows = []
    max_curv_rows = []
    while frame < nLoop:
        monomer = 1
        while monomer < monomers-1:
            x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["xcoord"]
            y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["ycoord"]
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["ycoord"]
            x = float(x_2.iloc[0]) -float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            theta = np.arctan2(x,y)


