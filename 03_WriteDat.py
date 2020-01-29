'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Writes .dat file for optimization problem
Author         : Corey Kok
Project        : -
========================================================================
Input          : - Arrays with the values:
                 - S_0_Input
                 - t
                 - s
                 - q_ch
                 - q_dc
                 - e_st
                 - e_ch
                 - e_dc
                 - S_max
                 - Pi_Input


Output         : - .dat file containing:
                    - t
                    - s
                    - S_0
                    - q_ch
                    - q_dc
                    - e_st
                    - e_ch
                    - e_dc
                    - S_max
                    - Pi

=========================================================================
'''
import numpy as np

# Write .dat file
f = open("04_InDat.dat", 'w')

# SETS
f.write("set t := " + "\n")  # t
f.write(str(np.array(t))[1 : -1] + ";" + "\n" + "\n")

f.write("set te := " + "\n")  # t
f.write(str(np.array(t)[-1]) + ";" + "\n" + "\n")


f.write("set s := " + "\n")  # t
for j in range(0, len(s)):
    f.write(s[j] + " ")
f.write(";" + "\n" + "\n")


# PARAMETERS

f.write("param delta_t := " + str(delta_t) + ";" + "\n\n")

temp = q_ch
f.write("param q_ch := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = q_dc
f.write("param q_dc := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_st
f.write("param e_st := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_ch
f.write("param e_ch := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_dc
f.write("param e_dc := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = S_max
f.write("param S_max := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = S0_Input
f.write("param S0 := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = ST
f.write("param ST := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = c_p
f.write("param c_p := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = c_m
f.write("param c_m := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = ST_p
f.write("param ST_p := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = ST_m
f.write("param ST_m := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

f.write("param Pi := " + "\n")
for j in range(0, len(t)):
    f.write(str(j+1) + " ")
    f.write(str(Pi[i+j]) + "\n")
f.write(";" + "\n" + "\n")


# Close .dat file
f.close()