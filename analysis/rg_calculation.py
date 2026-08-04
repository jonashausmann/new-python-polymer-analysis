from . import parameters
import pandas as pd
import numpy as np

#nLoop = 100









def calculate_radius_of_gyration(csv_file_path,new_csv_name):
    nLoop = parameters.nLoop/1000
    monomers = parameters.monomers
    calculated_rows = []
    frame = 0
    calculated_df = pd.read_csv(new_csv_name)
    df = pd.read_csv(csv_file_path)
    while frame < nLoop:
        sum = 0
        monomer = 0
        xcoords = df[df["frame"] == frame]["xcoord"]
        ycoords = df[df["frame"] == frame]["ycoord"]
        x_mean = np.mean(xcoords)
        y_mean = np.mean(ycoords)
        for xcoord, ycoord in zip(xcoords,ycoords):
            x_diff = xcoord-x_mean
            x_sqr = x_diff*x_diff
            y_diff = ycoord-y_mean
            y_sqr = y_diff*y_diff
            sum = sum + y_sqr+x_sqr
        Rg_sqrd = sum/monomers
        Rg = np.sqrt(Rg_sqrd)
        calculated_rows.append(Rg)
        frame = frame + 1
    calculated_df["Rg"] = calculated_rows
    calculated_df.to_csv(new_csv_name, index=False)
    '''
    I'm leaving this here in case I need it for later
    Rg_mean = np.mean(calculated_df["Rg"])
'''


#calculate_radius_of_gyration("./csv_files/F5.0_K0.5_theta0.0.csv", "./calculated_data/real_polymer_test.csv")
