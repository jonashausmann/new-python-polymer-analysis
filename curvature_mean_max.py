import pandas as pd 
import numpy as np
import parameters

monomers = parameters.monomers
#nLoop = parameters.nLoop/1000
nLoop = 100

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

    result_row = []
    
    while frame < nLoop:
        monomer = 1
        while monomer < int(monomers):
            x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["xcoord"]
            y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["ycoord"]
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["ycoord"]
            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            theta = np.arctan2(x,y)
            theta = (theta*180)/np.pi
            if theta < 0:
                theta = theta * -1
            theta = round(theta, 5)
            monomer_curvatures.append(theta)
            monomer = monomer + 1
        frame_mean = [frame, round(np.mean(monomer_curvatures),5)]
        mean_curv_rows.append(frame_mean)

        frame_max = [frame, monomer_curvatures.index(np.max(monomer_curvatures))-frame*monomers,
                     round(np.max(monomer_curvatures),5)]
        max_curv_rows.append(frame_max)

        frame_min = [frame, monomer_curvatures.index(np.min(monomer_curvatures))-frame*monomers,
                     round(np.min(monomer_curvatures),5)]
        min_curv_rows.append(frame_min)

        row = {
                "frames" : frame,
                "mean_curv" : round(np.mean(monomer_curvatures),5),
                "max_curv" : round(np.max(monomer_curvatures),5),
                "min_curv" : round(np.min(monomer_curvatures),5),
                }
        result_row.append(row)



        if frame % 10 == 0:
            print(f"{frame}/{nLoop}")

        frame = frame + 1
    new_df = pd.DataFrame(result_row)
    calculated_data_df = calculated_data_df.merge(new_df, on="frames",how="left")
    calculated_data_df.to_csv(measurement_csv, index=False)
    print(calculated_data_df["mean_curv"].mean())
'''
    calculated_data_df["frame","mean_curvature"] = mean_curv_rows
    calculated_data_df["frame","max_curv_bead_index","max_curv"] = max_curv_rows
    calculated_data_df["frame", "min_curv_bead_index", "min_curv"] = min_curv_rows
    #print(calculated_data_df["mean_curvature"].mean())
    calculated_data_df.to_csv(measurement_csv, index=False)
'''

calculate_curvature("./csv_files/F5.0_K0.5_theta0.0.csv", "./calculated_data/real_polymer_test.csv")
