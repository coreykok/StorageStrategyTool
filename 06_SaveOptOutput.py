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

# End-of-horizon shortage or excess
S_m_df = pd.DataFrame.from_dict(inst.S_m.extract_values(), orient='index', columns=[str(inst.S_m)])
S_p_df = pd.DataFrame.from_dict(inst.S_p.extract_values(), orient='index', columns=[str(inst.S_p)])
ST_df = pd.DataFrame.from_dict(inst.ST.extract_values(), orient='index', columns=[str(inst.ST)])

# Combines results into single data frame
Horizon_df = pd.concat([S_df, p_ch_df, p_dc_df], axis=1)
Final_df = pd.concat([S_m_df, S_p_df, ST_df], axis=1)

# Prepares output for plotting by appending iteration number, time-step and storage index as columns in data frame
Horizon_df['i'] = pd.Series([i for x in range(len(Horizon_df.index))], index=Horizon_df.index)  # solve iteration
Horizon_df['s'] = pd.Series([x for x, y in Horizon_df.index], index=Horizon_df.index)  # storage index
Horizon_df['t'] = pd.Series([y for x, y in Horizon_df.index], index=Horizon_df.index)  # time step
Horizon_df['Time'] = pd.Series([Time[i] for x in range(len(Horizon_df.index))], index=Horizon_df.index)  # time step

Final_df['s'] = pd.Series([x for x in Final_df.index], index=Final_df.index)  # storage index
Final_df['i'] = pd.Series([i for x in range(len(Final_df.index))], index=Final_df.index)  # solve iteration

Next_df = Horizon_df[Horizon_df['t'] == 1]


# Update next time-step with finalised decisions
for j in Storage.index:
      Initial['S'][j] = inst.S.extract_values()[j, 1]
      Initial['p_dc'][j] = inst.p_dc.extract_values()[j, 1]
      Initial['p_ch'][j] = inst.p_ch.extract_values()[j, 1]


#S1 = Horizon_df[Horizon_df['t'] == 1]['S']
#S1.index = Final_df.index

# Combine data from all runs into a single data frame
if i == 0:
    final_Horizon_df = Horizon_df
    final_Final_df = Final_df
    final_Next_df = Next_df
else:
    final_Horizon_df = pd.concat([final_Horizon_df, Horizon_df])
    final_Final_df = pd.concat([final_Final_df, Final_df])
    final_Next_df = pd.concat([final_Next_df, Next_df])

