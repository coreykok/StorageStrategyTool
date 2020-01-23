'''
=========================================================================
(c) Danmarks Tekniske Universitet 2020

Script         : Linear Programming Problem
Author         : Corey Kok
Project        : -
========================================================================
Input          : - .dat file

Output         : - optimal offers
=========================================================================
'''

import pyomo.environ as pe

# %%
# Creation of an abstract model
mod = pe.AbstractModel("Battery Optimisation")

# Sets
mod.t = pe.Set(within=pe.NonNegativeIntegers, ordered=True)  # Set of time steps t
mod.te = pe.Set(within=pe.NonNegativeIntegers, ordered=True, doc='Index of last step')  # Set of time steps t
mod.s = pe.Set()  # Set of storage devices s

# PARAMETERS
# Storage device
mod.delta_t = pe.Param()  # Time step length
mod.q_ch = pe.Param(mod.s)  # Charging limit
mod.q_dc = pe.Param(mod.s)  # Discharge limit
mod.e_st = pe.Param(mod.s)  # Energy retention
mod.e_ch = pe.Param(mod.s)  # Charging efficiency
mod.e_dc = pe.Param(mod.s)  # Discharge efficiency
mod.S_max = pe.Param(mod.s)  # Storage capacity
mod.S0 = pe.Param(mod.s)  # Initial storage state
mod.ST = pe.Param(mod.s)  # Ideal or enforced end of horizon storage state
mod.ST_p = pe.Param(mod.s)  # Maximum end-of-horizon storage state
mod.ST_m = pe.Param(mod.s)  # Minimum end-of-horizon storage state
mod.c_p = pe.Param(mod.s)  # linear penalty multiplier for exceeding ideal storage state
mod.c_m = pe.Param(mod.s)  # linear penalty multiplier for falling short of ideal storage state
# Market
mod.Pi = pe.Param(mod.t)  # Market price

# Decision variables
mod.S = pe.Var(mod.s, mod.t, within=pe.NonNegativeReals)  # Energy stored in device
mod.p_ch = pe.Var(mod.s, mod.t, within=pe.NonNegativeReals)  # Power consumed to charge
mod.p_dc = pe.Var(mod.s, mod.t, within=pe.NonNegativeReals)  # Power discharged
mod.S_m = pe.Var(mod.s, within=pe.NonNegativeReals)  # End-of-horizon shortage from ideal storage state
mod.S_p = pe.Var(mod.s, within=pe.NonNegativeReals)  # End-of-horizon excess from ideal storage state


# (1) Objective function:
def profit_rule(mod):
    return mod.delta_t * sum(mod.Pi[t] * (mod.e_dc[s] * mod.p_dc[s, t] - mod.p_ch[s, t])
                             for s in mod.s for t in mod.t) - \
           mod.delta_t * sum(mod.c_p[s] * mod.S_p[s] + mod.c_m[s] * mod.S_m[s] for s in mod.s)


mod.profit = pe.Objective(rule=profit_rule, sense=pe.maximize)


# (2a) Storage State:
def con2a_rule(mod, s, t):
    if t == 0:
        return mod.S[s, t] == (mod.e_st[s] ** mod.delta_t) * mod.S0[s] + \
               mod.delta_t * (mod.e_ch[s] * mod.p_ch[s, t] - mod.p_dc[s, t])
    else:
        return mod.S[s, t] == (mod.e_st[s] ** mod.delta_t) * mod.S[s, t - 1] + \
               mod.delta_t * (mod.e_ch[s] * mod.p_ch[s, t] - mod.p_dc[s, t])


mod.con2a = pe.Constraint(mod.s, mod.t, rule=con2a_rule)


# (2b) End-of-horizon condition:
# (2bi) Defines end-of-horizon storage excess or shortage (constraint only applied to final time-step):
def con2bi_rule(mod, s, t):
    return mod.ST[s] == mod.S[s, t] - mod.S_p[s] + mod.S_m[s]


# (2bii) Limit on end-of-horizon excess:
def con2bii_rule(mod, s):
    return mod.S_p[s] <= mod.ST_p[s] - mod.ST[s]


# (2biii) Limit on end-of-horizon shortage:
def con2biii_rule(mod, s):
    return mod.S_m[s] <= mod.ST[s] - mod.ST_m[s]


mod.con2bi = pe.Constraint(mod.s, mod.te, rule=con2bi_rule)
mod.con2bii = pe.Constraint(mod.s, rule=con2bii_rule)
mod.con2biii = pe.Constraint(mod.s, rule=con2biii_rule)


# (2c) Limits on charging and discharging
# (2ci) Charging
def con2ci_rule(mod, s, t):
    return mod.p_ch[s, t] <= mod.q_ch[s]

# (2ci) Disharging
def con2cii_rule(mod, s, t):
    return mod.p_dc[s, t] <= mod.q_dc[s]


mod.con2ci = pe.Constraint(mod.s, mod.t, rule=con2ci_rule)
mod.con2cii = pe.Constraint(mod.s, mod.t, rule=con2cii_rule)
