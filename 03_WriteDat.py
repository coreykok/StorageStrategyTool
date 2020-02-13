'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Writes .dat file for optimization problem
Author         : Corey Kok
Project        : -
========================================================================
Input          : - t
                 - s
                 - Pi
                 - DataFrames
                    - Initial (initial state of each storage device_
                    - Storage (fixed storage device parameters)


Output         : - .dat file containing:
                    - t
                    - s
                    - Pi
                    - Initial
                    - Storage


=========================================================================
'''
import numpy as np

# Write .dat file
f = open("04_InDat.dat", 'w')

# SETS
# Time steps
f.write("set t := " + "\n")  # t
f.write(str(np.array(t))[1 : -1] + ";" + "\n" + "\n")

# Final timestep
f.write("set te := " + "\n")  # t
f.write(str(np.array(t)[-1]) + ";" + "\n" + "\n")

# Storage devices
f.write("set s := " + "\n")  # t
for j in range(0, len(s)):
    f.write(s[j] + " ")
f.write(";" + "\n" + "\n")


# PARAMETERS
# Choose active constraints (update choices through /Input/Model.csv)
for col in Model.columns:
    f.write("param " + str(col) + " := " + str(Model[col][0]) + ";" + "\n\n")

# Time-step length
f.write("param delta_t := " + str(delta_t) + ";" + "\n\n")

# Market prices
f.write("param Pi := " + "\n")
for j in range(0, len(t)):
    f.write(str(j+1) + " ")
    f.write(str(Pi[i+j]) + "\n")
f.write(";" + "\n" + "\n")

# Storage parameters
# initial state
for col in Initial.columns:
    temp = Initial[col]
    f.write("param " + str(col) + "0" + " := " + "\n")
    for j in range(0, len(s)):
        f.write(temp.index[j] + " ")
        f.write(str(temp[j]) + "\n")
    f.write(";" + "\n" + "\n")

# fixed storage device properties
for col in Storage.columns:
    temp = Storage[col]
    f.write("param " + str(col) + " := " + "\n")
    for j in range(0, len(s)):
        f.write(temp.index[j] + " ")
        f.write(str(temp[j]) + "\n")
    f.write(";" + "\n" + "\n")


# Close .dat file
f.close()
