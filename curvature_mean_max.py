import pandas as pd 
import numpy as np
import parameters

monomers = parameters.monomers
nLoop = parameters.nLoop

def calculate_curvature(coordinate_csv, measurement_csv):
    df = pd.read_csv(coordinate_csv)
    calculated_data_df = pd.read_csv(measurement_csv)
    frame = 0

    

    monomer_curvatures = []
    mean_curv_rows = []
    max_curv_rows = []
    max_monomer_rows = []
    min_curv_rows = []
    min_monomer_rows = []
    
    while frame < nLoop:
        monomer = 1
        while monomer < monomers-1:
            x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["xcoord"]
            y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["ycoord"]
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["ycoord"]
            if frame == nLoop -1:
                print(f"Monomer: {Monomer}, Frame: {frame}, x: {x_2.iloc[0]}")
            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            theta = np.arctan2(x,y)
            monomer_curvatures.append(theta)
            monomer = monomer + 1
        frame_mean = [frame, np.mean(monomer_curvatures)]
        mean_curv_rows.append(frame_mean)

        frame_max = [frame, monomer_curvatures.index(np.max(monomer_curvatures)), np.max(monomer_curvatures)]
        max_curv_rows.append(frame_max)

        frame_min = [frame, monomer_curvatures.index(np.min(monomer_curvatures)),np.min(monomer_curvatures)]
        min_curv_rows.append(frame_min)

        frame = frame + 1

    df["frame","mean_curvature"] = mean_curv_rows
    df["frame","max_curv_bead_index","max_curv"] = max_curv_rows
    df["frame", "min_curv_bead_index", "min_curv"] = min_curv_rows
    print(np.mean(df["mean_curvature"]))

calculate_curvature("./csv_files/F5.0_K0.5_theta0.0.csv", "./calculated_data/real_polymer_test.csv")
