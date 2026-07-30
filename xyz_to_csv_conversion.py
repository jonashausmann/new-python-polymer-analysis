
# Usually like 99% of the time, xyz_filename is just output.xyz
def xyz_to_csv(xyz_filename, parameters_filename):
    xyz_file = open(xyz_filename, "r")
    parameters_file = open(parameters_filename, "r")

    bending, activity, chirality, nLoop, monomers = "N/A"

    with open(parameters_filename, "r") as f:
        for line in f:
            if "bending" in line:
                key,value = line.strip(":", 1)
                bending = value.strip()
            if "activity" in line:
                key,value = line.strip(":", 1)
                activity = value.strip()
            if "ChiralityAngle" in line:
                key,value = line.strip(":",1)
                chirality = value.strip()
            if "nLoop" in line:
                key,value = line.strip(":",1)
                nLoop = value.strip()
            if "monomers" in line:
                key,value = line.strip(":",1)
                monomers = value.strip()


    name_of_csv_file = "F" + activity + "_K" + bending + "_theta" + chirality

    with open(xyz_filename, "r") as f:
        for line in f:





    
