import pandas as pd

# This creates a straight filament for testing data
nLoops = 1000
monomers = 50










coord_rows = []
i = 0
while i < nLoops:
    monomer = 1
    while monomer < monomers+1:
        row = [i,monomer,0,monomer-1]
        coord_rows.append(row)
        monomer = monomer+1
    i = i + 1
df = pd.DataFrame(coord_rows, columns=["frame","monomernumber","xcoord","ycoord"])
df.to_csv("./csv_files/straight_filament_test.csv", index=False)
