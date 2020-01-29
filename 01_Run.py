'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Rolling horizon strategy tool:
                 Battery storage and discharge in the electricity market
Author         : Corey Kok
Project        : -
=========================================================================
Input          : - Storage capacity
                 - Storage efficiency
                 - Market prices
                 - End of horizon condition (ideal capacity / penalty / EOH storage requirement)

Output         : - Optimal operation of storage units
=========================================================================
'''

# Load required packages
import pandas as pd

# Initialise parameters
T_horizon = 12  # Optimisation horizon: Corresponds to 60 minutes with 5 minute intervals
delta_t = 1 / 12  # Time interval length

# Load .csv file of market prices
Prices = pd.read_csv("Input\Prices.csv")
Storage = pd.read_csv("Input\Storage.csv", index_col='s')



''' 
Run pre-processing
'''
exec(open("02_Preproc.py").read())

for i in range(0, NS):
    print("Progress:", str(i+1), "/ " + str(NS)) # Uncomment to check progress of simulation
    S0_Input = S0  # Set storage state
    exec(open("03_WriteDat.py").read())  # Create data file
    exec(open("05_RunOpt.py").read())  # Optimisation Model
    exec(open("06_SaveOptOutput.py").read())  # Process output for plotting
    S0 = S1  # Update storage state for next step

# Store Output
final_Horizon_df.to_csv(r'Output\Horizon.csv', index=None, header=True)  # Storage Horizon
final_Final_df.to_csv(r'Output\Final.csv', index=None, header=True)  # End of horizon deviation from ideal
final_Next_df.to_csv(r'Output\Next.csv', index=None, header=True)  # Decisions finalised at current time-step

