'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Saves optimization output to workspace
Author         : Corey Kok
Project        : -
 ========================================================================
Input          : - results from optimization

Output         : - S1
                 - final_Horizon_df - Storage decisions and states over optimisation horizon
                 - final_Final_df - State of battery at the end of the optimisation horizon
                 - final_Next_df - Storate decisions and states at the next time step

=========================================================================
'''
import pandas as pd

#%% Gettin results into working space

# Objective function value
Profit_Hor = inst.profit.expr

## Load remaining variables
# Storage state, charging, discharging
S_df = pd.DataFrame.from_dict(inst.S.extract_values(), orient='index', columns=[str(inst.S)])
pC_df = pd.DataFrame.from_dict(inst.pC.extract_values(), orient='index', columns=[str(inst.pC)])
pD_df = pd.DataFrame.from_dict(inst.pD.extract_values(), orient='index', columns=[str(inst.pD)])

# End-of-horizon shortage or excess
S_sh_df = pd.DataFrame.from_dict(inst.S_sh.extract_values(), orient='index', columns=[str(inst.S_sh)])
S_ex_df = pd.DataFrame.from_dict(inst.S_ex.extract_values(), orient='index', columns=[str(inst.S_ex)])
ST_df = pd.DataFrame.from_dict(inst.ST.extract_values(), orient='index', columns=[str(inst.ST)])

# Combines results into single data frame
Horizon_df = pd.concat([S_df, pC_df, pD_df], axis=1)
Final_df = pd.concat([S_sh_df, S_ex_df, ST_df], axis=1)

# Prepares output for plotting by appending iteration number, time-step and storage index as columns in data frame
Horizon_df['i'] = pd.Series([i for x in range(len(Horizon_df.index))], index=Horizon_df.index)  # solve iteration
Horizon_df['s'] = pd.Series([x for x, y in Horizon_df.index], index=Horizon_df.index)  # storage index
Horizon_df['t'] = pd.Series([y for x, y in Horizon_df.index], index=Horizon_df.index)  # time step
Horizon_df['Time'] = pd.Series([Time[i] for x in range(len(Horizon_df.index))], index=Horizon_df.index)  # time step

Final_df['s'] = pd.Series([x for x in Final_df.index], index=Final_df.index)  # storage index
Final_df['i'] = pd.Series([i for x in range(len(Final_df.index))], index=Final_df.index)  # solve iteration

Next_df = Horizon_df[Horizon_df['t'] == 0]

# Update next time-step with finalised decisions
S1 = Horizon_df[Horizon_df['t'] == 0]['S']
S1.index = Final_df.index

# Combine data from all runs into a single data frame
if i == 0:
    final_Horizon_df = Horizon_df
    final_Final_df = Final_df
    final_Next_df = Next_df
else:
    final_Horizon_df = pd.concat([final_Horizon_df, Horizon_df])
    final_Final_df = pd.concat([final_Final_df, Final_df])
    final_Next_df = pd.concat([final_Next_df, Next_df])

