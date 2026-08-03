import numpy as np
import pandas as pd
import analysis

# YOU CANT MEASURE WRITHE FOR 2D system

# take in data via the coordinate csv data


# create a function 
# Find out what the i and js of the system are
# Create a list of nonconsecutive, nonequal i and js
# for each index in this list, set points 1, 2, 3 and 4
# calculate r13, r14, r24, and r23
# Find the cross product of 




# r13 cross r14, r14 cross r24, r24 cross r23, r23 cross r13
# divide by magnitude for unit vector

# find the dot product of
# n1 dot n2, n2 dot n3, n3 dot n4, n4 dot n1

# Take the inverse sign of all vectors to find angle
# find the sum of all angles

# find r12 and r34
# take the cross of r34 cross r12
# take dot of this n5 dot r13

# multiply sum by n5 dot r13 
# divide sum by 4pi
# have an overall sum of all of the i and j pairs that produce angles. Multiply by 2
