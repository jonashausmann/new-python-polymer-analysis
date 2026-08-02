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

    
    result_row = []
    while frame < nLoop:
        monomer = 1
        monomer_curvatures = []
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

calculate_curvature("./csv_files/F5.0_K0.5_theta0.0.csv", "./calculated_data/real_polymer_test.csv")
