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

from pyomo.environ import *

# %%
# Creation of an abstract model
mod = AbstractModel("Battery Optimisation")

# Sets
mod.t = Set(within=NonNegativeIntegers, ordered=True)  # Set of time steps t
mod.te = Set(within=NonNegativeIntegers, ordered=True, doc='Index of last step')  # Set of time steps t
mod.s = Set()  # Set of storage devices s

# PARAMETERS
# Binary parameters indicating which constraints are active. Overrides storage device parameters.
mod.b_loss = Param()  # Indicates whether to use charging/discharging losses
mod.b_penEOH = Param()  # Indicates whether to use the EOH penalty function
mod.b_degrade = Param()  # Indicates whether to include the degradation functions
mod.b_ramp = Param()  # Indicates whether to use ramping constraints
mod.b_range = Param()  # Indicates whether to enforce an operating range on the storage devices


# Storage device
# Initial
mod.S0 = Param(mod.s)  # Initial storage state (kWh)
mod.p_dc0 = Param(mod.s)  # Initial discharging of device (kW)
mod.p_ch0 = Param(mod.s)  # Initial charging rate of device (kW)

# Fixed
mod.q_ch = Param(mod.s)  # Charging limit (kW)
mod.q_dc = Param(mod.s)  # Discharge limit (kW)
mod.e_st = Param(mod.s)  # Energy retention (1/t)
mod.e_ch = Param(mod.s)  # Charging efficiency
mod.e_dc = Param(mod.s)  # Discharge efficiency
mod.S_max = Param(mod.s)  # Storage capacity (kWh)
mod.ST = Param(mod.s)  # Ideal or enforced end of horizon storage state (kWh)
mod.ST_p = Param(mod.s)  # Maximum end-of-horizon storage state (kWh)
mod.ST_m = Param(mod.s)  # Minimum end-of-horizon storage state (kWh)
mod.c_p = Param(mod.s)  # linear penalty multiplier for exceeding ideal storage state ($/kWh)
mod.c_m = Param(mod.s)  # linear penalty multiplier for falling short of ideal storage state ($/kWh)
mod.c_dc = Param(mod.s)  # Long term degradation cost multiplier for discharging the storage device ($/kWh)
mod.c_ch = Param(mod.s)  # Long term degradation cost multiplier for charging the storage device ($/kWh)
mod.c_st = Param(mod.s)  # Long term degradation cost for storing charge within each device ($/kWh)
mod.r_up = Param(mod.s)  # Ramp up limit (kW/t)
mod.r_dn = Param(mod.s)  # Ramp down limit (kW/t)
mod.or_max = Param(mod.s)  # storage must be kept lower than this proportion of the maximum capacity
mod.or_min = Param(mod.s)  # storage must be kept higher than this proportion of the maximum capacity

# Market
mod.delta_t = Param()  # Time step length (h)
mod.Pi = Param(mod.t)  # Market price

# Decision variables
mod.S = Var(mod.s, mod.t, within=NonNegativeReals)  # Energy stored in device (kWh)
mod.p_ch = Var(mod.s, mod.t, within=NonNegativeReals)  # Power consumed to charge (kW)
mod.p_dc = Var(mod.s, mod.t, within=NonNegativeReals)  # Power discharged (kW)
mod.S_m = Var(mod.s, within=NonNegativeReals)  # End-of-horizon shortage from ideal storage state (kWh)
mod.S_p = Var(mod.s, within=NonNegativeReals)  # End-of-horizon excess from ideal storage state (kWh)

# Intermediate variables
mod.f_e_st = Var(mod.s, mod.t)  # Power kept from previous timestep (kWh)
mod.f_e_dc = Var(mod.s, mod.t)  # Power sold to market (kW)
mod.f_e_ch = Var(mod.s, mod.t)  # Power that goes to charging device (kW)
mod.f_c_p = Var(mod.s)  # End of horizon cost for exceeding ideal storage state ($)
mod.f_c_m = Var(mod.s)  # End of horizon cost for falling short of ideal storage state ($)
mod.f_c_dc = Var(mod.s, mod.t)  # Long term degradation cost based on discharging rate ($/h)
mod.f_c_ch = Var(mod.s, mod.t)  # Long term degradation cost based on charging rate ($/h)
mod.f_c_st = Var(mod.s, mod.t)  # Long term degradation cost based on storage state ($/h)



# (1) Objective function:
def profit_rule(mod):
    return mod.delta_t * sum(mod.Pi[t] * (mod.f_e_dc[s, t] - mod.p_ch[s, t])
                             for s in mod.s for t in mod.t) - \
        sum(mod.f_c_p[s] + mod.f_c_m[s] for s in mod.s) - \
           mod.delta_t * sum(mod.f_c_dc[s, t] + mod.f_c_ch[s, t] + mod.f_c_st[s, t] for s in mod.s for t in mod.t)


mod.profit = Objective(rule=profit_rule, sense=maximize)

#
def fun1a_rule(mod, s, t):
    if mod.b_loss == 0:
        if t == 1:
            return mod.f_e_st[s, t] == mod.S0[s]
        else:
            return mod.f_e_st[s, t] == mod.S[s, t - 1]
    else:
        if t == 1:
            return mod.f_e_st[s, t] == mod.e_st[s] * mod.S0[s]
        else:
            return mod.f_e_st[s, t] == mod.e_st[s] * mod.S[s, t - 1]

# (1b) Defines the conversion function, e_dc, that converts the energy discharged to the energy sold
def fun1b_rule(mod, s, t):
    if mod.b_loss == 0:
        return mod.f_e_dc[s, t] == mod.p_dc[s, t]
    else:
        return mod.f_e_dc[s, t] == mod.e_dc[s] * mod.p_dc[s, t]


# (1c) Defines the conversion function, e_ch, that converts the purchased energy to the energy charged
def fun1c_rule(mod, s, t):
    if mod.b_loss == 0:
        return mod.f_e_ch[s, t] == mod.p_ch[s, t]
    else:
        return mod.f_e_ch[s, t] == mod.e_ch[s] * mod.p_ch[s, t]


# (1d) Defines the cost function, c_p, the penalty function for exceeding the ideal EOH storage state
def fun1d_rule(mod, s):
    if mod.b_penEOH == 0:
        return mod.f_c_p[s] == 0
    else:
        return mod.f_c_p[s] == mod.c_p[s] * mod.S_p[s]


# (1e) Defines the cost function, c_m, the penalty function for falling short of the ideal EOH storage state
def fun1e_rule(mod, s):
    if mod.b_penEOH == 0:
        return mod.f_c_m[s] == 0
    else:
        return mod.f_c_m[s] == mod.c_m[s] * mod.S_m[s]


# (1f) Defines the cost function, c_dc, the long term degradation cost of discharging the storage unit
def fun1f_rule(mod, s, t):
    if mod.b_degrade == 0:
        return mod.f_c_dc[s, t] == 0
    else:
        return mod.f_c_dc[s, t] == mod.c_dc[s] * mod.p_dc[s, t]


# (1g) Defines the cost function, c_ch, the long term degradation cost of discharging the storage unit
def fun1g_rule(mod, s, t):
    if mod.b_degrade == 0:
        return mod.f_c_ch[s, t] == 0
    else:
        return mod.f_c_ch[s, t] == mod.c_ch[s] * mod.p_ch[s, t]


# (1h) Defines the cost function, c_st, the long term degradation cost based on the storage state
def fun1h_rule(mod, s, t):
    if mod.b_degrade == 0:
        return mod.f_c_st[s, t] == 0
    else:
        return mod.f_c_st[s, t] == mod.c_st[s] * mod.S[s, t]


mod.fun1a = Constraint(mod.s, mod.t, rule=fun1a_rule)
mod.fun1b = Constraint(mod.s, mod.t, rule=fun1b_rule)
mod.fun1c = Constraint(mod.s, mod.t, rule=fun1c_rule)
mod.fun1d = Constraint(mod.s, rule=fun1d_rule)
mod.fun1e = Constraint(mod.s, rule=fun1e_rule)
mod.fun1f = Constraint(mod.s, mod.t, rule=fun1f_rule)
mod.fun1g = Constraint(mod.s, mod.t, rule=fun1g_rule)
mod.fun1h = Constraint(mod.s, mod.t, rule=fun1h_rule)


# (2a) Storage State:
def con2a_rule(mod, s, t):
    return mod.S[s, t] == mod.f_e_st[s, t] + \
           mod.delta_t * (mod.f_e_ch[s, t] - mod.p_dc[s, t])


mod.con2a = Constraint(mod.s, mod.t, rule=con2a_rule)


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


mod.con2bi = Constraint(mod.s, mod.te, rule=con2bi_rule)
mod.con2bii = Constraint(mod.s, rule=con2bii_rule)
mod.con2biii = Constraint(mod.s, rule=con2biii_rule)


# (2c) Limits on charging and discharging
# (2ci) Charging
def con2ci_rule(mod, s, t):
    return mod.p_ch[s, t] <= mod.q_ch[s]

# (2ci) Disharging
def con2cii_rule(mod, s, t):
    return mod.p_dc[s, t] <= mod.q_dc[s]


mod.con2ci = Constraint(mod.s, mod.t, rule=con2ci_rule)
mod.con2cii = Constraint(mod.s, mod.t, rule=con2cii_rule)

# (3) Ramping constraints
# (3a) Ramp up
def con3a_rule(mod, s, t):
    if mod.b_ramp == 0:
        return Constraint.Skip
    else:
        if t == 1:
            return (mod.p_ch[s, t] - mod.p_ch0[s]) - (mod.p_dc[s, t] - mod.p_dc0[s]) <= mod.r_up[s]
        else:
            return (mod.p_ch[s, t] - mod.p_ch[s, t-1]) - (mod.p_dc[s, t] - mod.p_dc[s, t-1]) <= mod.r_up[s]

# (3a) Ramp down
def con3b_rule(mod, s, t):
    if mod.b_ramp == 0:
        return Constraint.Skip
    else:
        if t == 1:
            return (mod.p_dc[s, t] - mod.p_dc0[s]) - (mod.p_ch[s, t] - mod.p_ch0[s]) <= mod.r_up[s]
        else:
            return (mod.p_dc[s, t] - mod.p_dc[s, t - 1]) - (mod.p_ch[s, t] - mod.p_ch[s, t - 1]) <= mod.r_up[s]


mod.con3a = Constraint(mod.s, mod.t, rule=con3a_rule)
mod.con3b = Constraint(mod.s, mod.t, rule=con3b_rule)

# (4) Storage operating range
# (4a) Upper limits
def con4a_rule(mod, s, t):
    if mod.b_range == 0:
        return Constraint.Skip
    else:
        return mod.S[s, t] <= mod.S_max[s] * mod.or_max[s]


# (4b) Lower limits
def con4b_rule(mod, s, t):
    if mod.b_range == 0:
        return Constraint.Skip
    else:
        return mod.S[s, t] >= mod.S_max[s] * mod.or_min[s]


mod.con4a = Constraint(mod.s, mod.t, rule=con4a_rule)
mod.con4b = Constraint(mod.s, mod.t, rule=con4b_rule)
