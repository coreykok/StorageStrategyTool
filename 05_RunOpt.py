'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Runs LP
Author         : Corey Kok
========================================================================
Input          : - .dat file

Output         : - Optimization results

Parameters     : - Solver, e.g., glpk, gurobi,
=========================================================================
'''

# Import model
from Storage_LP import mod
from pyomo.opt import SolverFactory

# Create model instance
inst = mod.create_instance('04_InDat.dat')

# Setup the optimizer, e.g., glpk, gurobi,...
opt = SolverFactory('glpk')

# Optimize
res = opt.solve(inst)

# Write the output
#res.write(num=1)
print(i)
inst.solutions.load_from(res)