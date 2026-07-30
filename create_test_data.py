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


'''
monomers = 50.0
extension = 20000.0
bending = 0.5
diffusion = 1.0
temperature = 1.0
activity = 5.0
timestep = 1e-05
pInterval = 1000.0
fInterval = 5000000.0
HeadSize = 0.0
HeadStiffness = 1.0
MobilityRatio = 1.0
Opticaltrap = 0.0
Maxrad = 25000.0
wallparticles = 0.0
wallRadius = 0.0
wallOpening = 0.0
arcStartAngle = 0.0
ChiralityAngle = 0.0
ChiralityDirection = -1.0
'''
