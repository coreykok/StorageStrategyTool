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
f.write(str(np.array(t))[1: -1] + ";" + "\n" + "\n")

# Final timestep
f.write("set te := " + "\n")  # t
f.write(str(np.array(t)[-1]) + ";" + "\n" + "\n")

# Storage devices
f.write("set s := " + "\n")  # t
for j in range(0, len(s)):
    f.write(s[j] + " ")
f.write(";" + "\n" + "\n")

# Generation units
f.write("set g := " + "\n")  # t
for j in range(0, len(g)):
    f.write(g[j] + " ")
f.write(";" + "\n" + "\n")

# Storage Penalty Function indices
f.write("set k := " + "\n")  # t
f.write(str(np.array(k))[1: -1] + ";" + "\n" + "\n")

# map piecewise penalty functions to storage devices
f.write("set sk_map := " + "\n")  # sk_map
for j in k:
    f.write(str(sk[j]) + " " + str(j) + "\n")
f.write(";" + "\n" + "\n")


# PARAMETERS
# Choose active constraints (update choices through /Input/Model.csv) columns within /Input/Model.csv that are used as
# parameters begin with '_'
for col in Model.columns:
    if str(col).startswith('_'):
        f.write("param " + str(col) + " := " + str(Model[col][0]) + ";" + "\n\n")

# Market prices and demand
f.write("param Pi := " + "\n")
for j in range(0, len(t)):
    f.write(str(j+1) + " ")
    f.write(str(Pi[i+j]) + "\n")
f.write(";" + "\n" + "\n")

f.write("param dem := " + "\n")
for j in range(0, len(t)):
    f.write(str(j+1) + " ")
    f.write(str(dem[i+j]) + "\n")
f.write(";" + "\n" + "\n")


# Cost function parameters
temp = StorPenFun['A']
f.write("param A := " + "\n")
for j in k:
    f.write(str(sk[j]) + " " + str(j) + " " + str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = StorPenFun['B']
f.write("param B := " + "\n")
for j in k:
    f.write(str(sk[j]) + " " + str(j) + " " + str(temp[j]) + "\n")
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

# Generation parameters
for col in Generation.columns:
    temp = Generation[col]
    f.write("param " + str(col) + " := " + "\n")
    for j in range(0, len(g)):
        f.write(temp.index[j] + " ")
        f.write(str(temp[j]) + "\n")
    f.write(";" + "\n" + "\n")

# Close .dat file
f.close()
