import pandas as pd
import numpy as np
import parameters

# Improve performance
def count_nearest_neighbors(coordinate_df, measurements_df):
    interm_measurements_df = pd.read_csv(measurements_df)
    df = pd.read_csv(coordinate_df)
    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop/parameters.pInterval)
    frame = 0

    




    
    frames_neighbor_list = []
    while frame < frames:
        nearest_neighbors = 0

        monomer = 2 
        # head bead coordinates
        x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["xcoord"]
        y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == 1)]["ycoord"]
        while monomer < monomers + 1:
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["ycoord"]
            x = float(x_2.iloc[0]) -float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            diff_vec = np.array([x,y])
            if np.linalg.norm(diff_vec) <= 1:
                nearest_neighbors = nearest_neighbors + 1
            monomer = monomer + 1
        frames_neighbor_list.append([int(frame), int(nearest_neighbors)])
        if frame%100 == 0:
            print(f"{frame}/{frames}")
        frame = frame + 1
    neighbor_df = pd.DataFrame(frames_neighbor_list, columns=["frames", "neighbor_count"])
    interm_measurements_df = pd.merge(interm_measurements_df, neighbor_df, on="frames", how="right")
    interm_measurements_df.to_csv(measurements_df, index=False)

count_nearest_neighbors("../data/F10_K5_theta0.0/RUN_0001/csv_files/F10.0_K5.0_theta0.0.csv", "../data/F10_K5_theta0.0/RUN_0001/csv_files/F10.0_K5.0_theta0.0_measurements.csv")
