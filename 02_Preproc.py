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
                    - q_charge
                    - q_disch
                    - e_stor
                    - e_charge
                    - e_disch
                    - S_max
                    - Pi
=========================================================================
'''
NS = len(Prices) - T_horizon # Times optimisation needs to be solved

# SETS
t = range(0, T_horizon)  # time step array
s = Storage.index  # set of storage devices

# PARAMETERS
q_charge = Storage['q_charge']  # Charging limit
q_disch = Storage['q_disch']  # Discharge limit
e_stor = Storage['e_stor']  # Energy retention
e_charge = Storage['e_charge']  # Charging efficiency
e_disch = Storage['e_disch']  # Discharge efficiency
S_max = Storage['S_max']  # Storage capacity
S0 = Storage['S0']  # Initial storage state
ST = Storage['ST']  # Ideal or enforced end of horizon storage state
ST_p = Storage['ST_p']  # Maximum end-of-horizon storage state
ST_m = Storage['ST_m']  # Minimum end-of-horizon storage state
pen_p = Storage['pen_p']  # linear penalty multiplier for exceeding ideal storage state
pen_m = Storage['pen_m']  # linear penalty multiplier for falling short of ideal storage state

Time = Prices['Time']  # Time
Pi = Prices['Pi']  # Market price


