import pandas as pd

# This creates a straight filament for testing data
nLoops = 5000
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
df.to_csv("./straight_filament_test.csv", index=False)


'''
monomers:50
extension:20000
bending:5
diffusion:1
temperature:1
activity:10
timestep:1e-05
nLoop:5000000
pInterval:1000
fInterval:5000000
HeadSize:0
HeadStiffness:1
MobilityRatio:1
Opticaltrap:0
Maxrad:25000
wallparticles:0
wallRadius:0
wallOpening:0
arcStartAngle:0
ChiralityAngle:0
ChiralityDirection:-1
'''
