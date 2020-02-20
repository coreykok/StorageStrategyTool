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
p_ch_df = pd.DataFrame.from_dict(inst.p_ch.extract_values(), orient='index', columns=[str(inst.p_ch)])
p_dc_df = pd.DataFrame.from_dict(inst.p_dc.extract_values(), orient='index', columns=[str(inst.p_dc)])
p_gen_df = pd.DataFrame.from_dict(inst.p_gen.extract_values(), orient='index', columns=[str(inst.p_gen)])

# End-of-horizon shortage or excess
S_m_df = pd.DataFrame.from_dict(inst.S_m.extract_values(), orient='index', columns=[str(inst.S_m)])
S_p_df = pd.DataFrame.from_dict(inst.S_p.extract_values(), orient='index', columns=[str(inst.S_p)])
ST_df = pd.DataFrame.from_dict(inst.ST.extract_values(), orient='index', columns=[str(inst.ST)])

# Combines results into single data frame
Storage_Horizon_df = pd.concat([S_df, p_ch_df, p_dc_df], axis=1, sort=True)
Generation_Horizon_df = p_gen_df
Final_df = pd.concat([S_m_df, S_p_df, ST_df], axis=1)

# Prepares output for plotting by appending iteration number, time-step and storage index as columns in data frame
Storage_Horizon_df['i'] = pd.Series([i for x in range(len(Storage_Horizon_df.index))],
                                    index=Storage_Horizon_df.index)  # solve iteration
Storage_Horizon_df['s'] = pd.Series([x for x, y in Storage_Horizon_df.index],
                                    index=Storage_Horizon_df.index)  # storage index
Storage_Horizon_df['t'] = pd.Series([y for x, y in Storage_Horizon_df.index],
                                    index=Storage_Horizon_df.index)  # time index
Storage_Horizon_df['Time'] = pd.Series([Time[i] for x in range(len(Storage_Horizon_df.index))],
                                       index=Storage_Horizon_df.index)  # time step

Generation_Horizon_df['i'] = pd.Series([i for x in range(len(Generation_Horizon_df.index))],
                                    index=Generation_Horizon_df.index)  # solve iteration
Generation_Horizon_df['g'] = pd.Series([x for x, y in Generation_Horizon_df.index],
                                    index=Generation_Horizon_df.index)  # storage index
Generation_Horizon_df['t'] = pd.Series([y for x, y in Generation_Horizon_df.index],
                                    index=Generation_Horizon_df.index)  # time index
Generation_Horizon_df['Time'] = pd.Series([Time[i] for x in range(len(Generation_Horizon_df.index))],
                                       index=Generation_Horizon_df.index)  # time step

Final_df['s'] = pd.Series([x for x in Final_df.index], index=Final_df.index)  # storage index
Final_df['i'] = pd.Series([i for x in range(len(Final_df.index))], index=Final_df.index)  # solve iteration

Storage_Next_df = Storage_Horizon_df[Storage_Horizon_df['t'] == 1]
Generation_Next_df = Generation_Horizon_df[Generation_Horizon_df['t'] == 1]

# Update next time-step with finalised decisions
for j in Storage.index:
    Initial['S'][j] = inst.S.extract_values()[j, 1]
    Initial['p_dc'][j] = inst.p_dc.extract_values()[j, 1]
    Initial['p_ch'][j] = inst.p_ch.extract_values()[j, 1]

# Combine data from all runs into a single data frame
if i == 0:
    final_Storage_Horizon_df = Storage_Horizon_df
    final_Generation_Horizon_df = Generation_Horizon_df
    final_Final_df = Final_df
    final_Storage_Next_df = Storage_Next_df
    final_Generation_Next_df = Generation_Next_df
else:
    final_Storage_Horizon_df = pd.concat([final_Storage_Horizon_df, Storage_Horizon_df])
    final_Generation_Horizon_df = pd.concat([final_Generation_Horizon_df, Generation_Horizon_df])
    final_Final_df = pd.concat([final_Final_df, Final_df])
    final_Storage_Next_df = pd.concat([final_Storage_Next_df, Storage_Next_df])
    final_Generation_Next_df = pd.concat([final_Generation_Next_df, Generation_Next_df])
