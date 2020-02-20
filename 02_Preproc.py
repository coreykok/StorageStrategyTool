'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Processes data extracted from .csv files
Author         : Corey Kok
Project        : -
========================================================================
Input          : - NS
                 - Prices
                 - Storage

Output         : - Arrays with the values:
                    - NS (Number of times LP will be solved in simulation)
                    - t
                    - s
                    - Time
                    - Pi
=========================================================================
'''
if Model['i_fulltraj'][0] == 1:
    NS = len(Prices) - Model['t_horizon'][0] # Times optimisation needs to be solved
else:
    NS = 1

# SETS
t = range(1, Model['t_horizon'][0] + 1)  # time step array
s = Storage.index  # set of storage devices
g = Generation.index  # set of storage devices
k = StorPenFun.index  # set of piecewise cost functions
sk = StorPenFun['s']

# PARAMETERS - cover entire optimisation horizon
Time = Prices['Time']  # Time
Pi = Prices['Pi']  # Market price
dem = Prices['dem']  # Market price
