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
NS = len(Prices) - T_horizon # Times optimisation needs to be solved

# SETS
t = range(1, T_horizon + 1)  # time step array
s = Storage.index  # set of storage devices

# PARAMETERS - cover entire optimisation horizon
Time = Prices['Time']  # Time
Pi = Prices['Pi']  # Market price
