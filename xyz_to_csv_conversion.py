import pandas as pd
import numpy as np
import os
# This is just a reminder to myself that this only works for the free polymer case
# particle_type = 2

# Usually like 99% of the time, xyz_filename is just output.xyz
def xyz_to_csv(xyz_filename, parameters_filename):

    bending = activity  = chirality = nLoop = monomers = "N/A"

    with open(parameters_filename, "r") as f:
        for line in f:
            if "bending" in line:
                key,value = line.split(":", 1)
                bending = value.strip()
            if "activity" in line:
                key,value = line.split(":", 1)
                activity = value.strip()
            if "ChiralityAngle" in line:
                key,value = line.split(":",1)
                chirality = value.strip()
            if "nLoop" in line:
                key,value = line.split(":",1)
                nLoop = value.strip()
            if "monomers" in line:
                key,value = line.split(":",1)
                monomers = value.strip()


    name_of_csv_file = "./csv_files/" + "F" + activity + "_K" + bending + "_theta" + chirality + ".csv"
    is_there_already_a_csv_file = os.path.exists(name_of_csv_file)
    runNumber = 0
    while is_there_already_a_csv_file == True:
        runNumber = runNumber + 1
        name_of_csv_file = name_of_csv_file.replace(".csv","")
        name_of_csv_file = name_of_csv_file + "_Run" + str(runNumber) + ".csv"
        is_there_already_a_csv_file = os.path.exists(name_of_csv_file)


    # in the config.xyz file, this line is trying to figure out how many lines constitutes one frame
    frame_line_length = int(monomers)+2
    coord_rows = []
    with open(xyz_filename, "r") as f:
        line_number = 0 
        frame = 0
        for line in f:
            line_number = line_number + 1
            frame = (line_number-2) // frame_line_length
            # This only works for free polymers. Boundary polymers have type 3 I believe
            if line.startswith("2"):
                line = line.strip()
                monomer_number = line_number - frame*frame_line_length -2 
                coordinates = line.split()
                coordinates.insert(0,frame)
                coordinates.insert(1,line_number)
                coordinates.insert(2,monomer_number)
                coord_rows.append(coordinates)
    df = pd.DataFrame(coord_rows, columns=["frame","linenumber","monomernumber","particletype","xcoord","ycoord","zcoord"])
    df["frame"] = df["frame"].astype(int)
    df["linenumber"] = df["linenumber"].astype(int)
    df["monomernumber"] = df["monomernumber"].astype(int)
    df["particletype"] = df["particletype"].astype(int)
    df["xcoord"] = df["xcoord"].astype(float)
    df["ycoord"] = df["ycoord"].astype(float)
    df["zcoord"] = df["zcoord"].astype(float)
    df.drop(['particletype','zcoord'], axis=1,inplace=True)
    df.to_csv(name_of_csv_file, index=False)





xyz_to_csv("config0.xyz", "input_values.txt")







