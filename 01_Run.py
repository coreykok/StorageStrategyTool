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

# Load .csv file of market prices
Initial = pd.read_csv("Input\Initial.csv", index_col='s')  # Initial state of storage devices
Storage = pd.read_csv("Input\Storage.csv", index_col='s')  # Current state of storage devices
StorPenFun = pd.read_csv("Input\StorPenFun.csv", index_col='k')  # Parameters that define a piecewise linear cost func.
Generation = pd.read_csv("Input\Generation.csv", index_col='g')  # Generation cost and limit

# Uncomment to switch to market participation model
#Model = pd.read_csv("Input\Model.csv")  # Load choices for which constraints are active
#Prices = pd.read_csv("Input\Prices.csv")  # Market prices for buying/selling electricity

# Uncomment to switch to barge model
Model = pd.read_csv("Input\Model_Barge.csv")  # Load choices for which constraints are active
Prices = pd.read_csv("Input\Prices_Barge.csv")  # Market prices for buying/selling electricity

exec(open("02_Preproc.py").read())  # Run pre-processing
for i in range(0, NS):
    exec(open("03_WriteDat.py").read())  # Creates data file in optimisation model
    exec(open("05_RunOpt.py").read())  # Optimisation Model (included user options from Model.csv)
    exec(open("06_SaveOptOutput.py").read())  # Process output for plotting and updates initial next timestep

# Store Output
final_Storage_Horizon_df.to_csv(r'Output\StorageHorizon.csv', index=None, header=True)  # Storage over opt. Horizon
final_Generation_Horizon_df.to_csv(r'Output\GenerationHorizon.csv', index=None, header=True)  # Generation over Horizon
final_Final_df.to_csv(r'Output\Final.csv', index=None, header=True)  # End of horizon deviation from ideal
final_Storage_Next_df.to_csv(r'Output\StorageNext.csv', index=None, header=True)  # Storage decisions finalised at current time-step
final_Generation_Next_df.to_csv(r'Output\GenerationNext.csv', index=None, header=True)  # Decisions finalised at current time-step
