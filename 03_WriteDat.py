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
                 - q_charge
                 - q_disch
                 - e_stor
                 - e_charge
                 - e_disch
                 - S_max
                 - Pi_Input


Output         : - .dat file containing:
                    - t
                    - s
                    - S_0
                    - q_charge
                    - q_disch
                    - e_stor
                    - e_charge
                    - e_disch
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

f.write("param t_delta := " + str(T_delta) + ";" + "\n\n")

temp = q_charge
f.write("param q_charge := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = q_disch
f.write("param q_disch := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_stor
f.write("param e_stor := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_charge
f.write("param e_charge := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = e_disch
f.write("param e_disch := " + "\n")
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

temp = pen_p
f.write("param pen_p := " + "\n")
for j in range(0, len(s)):
    f.write(temp.index[j] + " ")
    f.write(str(temp[j]) + "\n")
f.write(";" + "\n" + "\n")

temp = pen_m
f.write("param pen_m := " + "\n")
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
    f.write(str(j) + " ")
    f.write(str(Pi[i+j]) + "\n")
f.write(";" + "\n" + "\n")


# Close .dat file
f.close()