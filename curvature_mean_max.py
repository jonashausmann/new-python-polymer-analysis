import pandas as pd 
import numpy as np
import parameters

monomers = parameters.monomers
#nLoop = parameters.nLoop/1000
nLoop = 100

def calculate_curvature(coordinate_csv, measurement_csv,test_data=False):
    df = pd.read_csv(coordinate_csv)
    calculated_data_df = pd.read_csv(measurement_csv)
    frame = 0

    
    result_row = []
    test_curv_data = []
    while frame < (nLoop):
        monomer = 1
        monomer_curvatures = []
        while monomer < int(monomers-1):
            x_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["xcoord"]
            y_1 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer)]["ycoord"]
            x_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["xcoord"]
            y_2 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 1)]["ycoord"]
            x_3 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 2)]["xcoord"]
            y_3 = df[(df["frame"] == frame) & (df["monomernumber"] == monomer + 2)]["ycoord"]

            x = float(x_2.iloc[0]) - float(x_1.iloc[0])
            y = float(y_2.iloc[0]) - float(y_1.iloc[0])
            x_mon_2 = float(x_3.iloc[0]) - float(x_2.iloc[0])
            y_mon_2 = float(y_3.iloc[0]) - float(y_2.iloc[0])

            monomer_1 = np.array((float(x),float(y)))
            monomer_2 = np.array((float(x_mon_2),float(y_mon_2)))

            monomer_1_unit = monomer_1 / np.linalg.norm(monomer_1)
            monomer_2_unit = monomer_2 / np.linalg.norm(monomer_2)

            theta = np.arccos(np.dot(monomer_1_unit,monomer_2_unit))

            theta = (theta*180)/np.pi
            theta = round(theta, 5)

            monomer_curvatures.append(theta)

            if test_data == True:
                test_curv_monomer = [frame,monomer,monomer+1,theta]
                test_curv_data.append(test_curv_monomer)

            
            monomer = monomer + 1
        row = {
                "frames" : frame,
                "mean_curv" : round(np.mean(monomer_curvatures),5),
                "max_curv_monomer" : round(monomer_curvatures.index(np.max(monomer_curvatures)))+1,
                "max_curv" : round(np.max(monomer_curvatures),5),
                "min_curv_monomer" : round(monomer_curvatures.index(np.min(monomer_curvatures)))+1,
                "min_curv" : round(np.min(monomer_curvatures),5),
                }
        result_row.append(row)

        if frame % 10 == 0:
            print(f"{frame}/{nLoop}")
        frame = frame + 1

    if test_data == True:
        test_df = pd.DataFrame(test_curv_data, columns=["frames","monomer1","monomer2","theta"])
        test_df.to_csv("./calculated_data/testing_theta.csv",index=False)
    new_df = pd.DataFrame(result_row)
    calculated_data_df = calculated_data_df.merge(new_df, on="frames",how="left")
    calculated_data_df.to_csv(measurement_csv, index=False)
    #print(calculated_data_df["mean_curv"].mean())

calculate_curvature("./csv_files/F5.0_K0.5_theta0.0.csv", "./calculated_data/real_polymer_test.csv",True)
