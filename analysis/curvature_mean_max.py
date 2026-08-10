import numpy as np
import pandas as pd

from analysis import parameters


def calculate_curvature(coordinate_df, measurement_df, debug=False):
    if debug:
        print("Calculating curvature")

    monomers = int(parameters.monomers)
    frames = int(parameters.nLoop / 1000)
    df = coordinate_df
    calculated_data_df = measurement_df

    df = df.sort_values(["frame", "monomernumber"])
    coords = df[["xcoord", "ycoord"]].to_numpy().reshape(frames, monomers, 2)

    bead_pairs = np.diff(coords, axis=1)

    bond_1 = bead_pairs[:, :-1, :]
    bond_2 = bead_pairs[:, 1:, :]

    bond_1_unit = bond_1 / np.linalg.norm(bond_1, axis=2, keepdims=True)
    bond_2_unit = bond_2 / np.linalg.norm(bond_2, axis=2, keepdims=True)

    dot_product = np.clip(np.sum(bond_1_unit * bond_2_unit, axis=2), -1.0, 1.0)

    theta = np.degrees(np.arccos(dot_product))

    new_df = pd.DataFrame(
        {
            "frames": np.arange(frames),
            "mean_curv": np.round(theta.mean(axis=1), 5),
            "max_curv": np.round(theta.max(axis=1), 5),
            "max_curv_monomer": theta.argmax(axis=1) + 1,
            "min_curv": np.round(theta.min(axis=1), 5),
            "min_curv_monomer": theta.argmin(axis=1) + 1,
        }
    )

    calculated_data_df = calculated_data_df.merge(new_df, on="frames", how="left")
    return calculated_data_df


"""
    frame = 0
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
                test_curv_monomer = [frame,monomer,monomer+2,theta]
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

        if frame % 1000 == 0:
            print(f"{frame}/{nLoop}")
        frame = frame + 1

    if test_data == True:
        test_df = pd.DataFrame(test_curv_data, columns=["frames","monomer1","monomer2","theta"])
        test_df.to_csv("./calculated_data/testing_theta.csv",index=False)
"""
