'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Processes data extracted from .csv files
Author         : Corey Kok
Project        : -
========================================================================
Input          : - Prices
                 - Storage

Output         : - Arrays with the values:
                    - t
                    - s
                    - q_ch
                    - q_dc
                    - e_st
                    - e_ch
                    - e_dc
                    - S_max
                    - Pi
=========================================================================
'''
NS = len(Prices) - T_horizon # Times optimisation needs to be solved

# SETS
t = range(0, T_horizon)  # time step array
s = Storage.index  # set of storage devices

# PARAMETERS
q_ch = Storage['q_ch']  # Charging limit
q_dc = Storage['q_dc']  # Discharge limit
e_st = Storage['e_st']  # Energy retention
e_ch = Storage['e_ch']  # Charging efficiency
e_dc = Storage['e_dc']  # Discharge efficiency
S_max = Storage['S_max']  # Storage capacity
S0 = Storage['S0']  # Initial storage state
ST = Storage['ST']  # Ideal or enforced end of horizon storage state
ST_p = Storage['ST_p']  # Maximum end-of-horizon storage state
ST_m = Storage['ST_m']  # Minimum end-of-horizon storage state
c_p = Storage['c_p']  # linear penalty multiplier for exceeding ideal storage state
c_m = Storage['c_m']  # linear penalty multiplier for falling short of ideal storage state

Time = Prices['Time']  # Time
Pi = Prices['Pi']  # Market price


