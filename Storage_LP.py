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
mod.g = Set()  # Set of generation units g
mod.k = Set()  # Set of piecewise cost functions g
mod.sk_map = Set(within=mod.s * mod.k)  # Maps piecewise cost function indices, k, to storage devices, s.

# PARAMETERS
# Binary parameters indicating which constraints are active. Overrides storage device parameters.
mod._loss = Param()  # Indicates whether to use charging/discharging losses
mod._penEOH = Param()  # Indicates whether to use the EOH penalty function
mod._degrade = Param()  # Indicates whether to include the degradation functions
mod._ramp = Param()  # Indicates whether to use ramping constraints
mod._range = Param()  # Indicates whether to enforce an operating range on the storage devices
mod._clearing = Param()  # Indicates whether goal is to maximise profit (0) or minimise cost while balancing load (1)
mod._gen = Param()  # Indicates whether to for generation units

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
mod.A = Param(mod.s, mod.k)  # Gradient of cost function
mod.B = Param(mod.s, mod.k)  # 0 intercept of cost function

# Generation unit
mod.q_gen = Param(mod.g)  # Charging limit (kW)
mod.c_gen = Param(mod.g)  # Discharge limit (kW)

# Demand
mod.dem = Param(mod.t)  # Exogenous demand (kW)


# Market
mod._delta_t = Param()  # Time step length (h)
mod.Pi = Param(mod.t)  # Market price

# Decision variables
mod.S = Var(mod.s, mod.t, within=NonNegativeReals)  # Energy stored in device (kWh)
mod.p_ch = Var(mod.s, mod.t, within=NonNegativeReals)  # Power consumed to charge (kW)
mod.p_dc = Var(mod.s, mod.t, within=NonNegativeReals)  # Power discharged (kW)
mod.S_m = Var(mod.s, within=NonNegativeReals)  # End-of-horizon shortage from ideal storage state (kWh)
mod.S_p = Var(mod.s, within=NonNegativeReals)  # End-of-horizon excess from ideal storage state (kWh)
mod.p_gen = Var(mod.g, mod.t, within=NonNegativeReals)  # Output of generation unit (kW)

# Intermediate variables
mod.f_e_st = Var(mod.s, mod.t)  # Power kept from previous timestep (kWh)
mod.f_e_dc = Var(mod.s, mod.t)  # Power sold to market (kW)
mod.f_e_ch = Var(mod.s, mod.t)  # Power that goes to charging device (kW)
mod.f_c_p = Var(mod.s)  # End of horizon cost for exceeding ideal storage state ($)
mod.f_c_m = Var(mod.s)  # End of horizon cost for falling short of ideal storage state ($)
mod.f_c_dc = Var(mod.s, mod.t)  # Long term degradation cost based on discharging rate ($/h)
mod.f_c_ch = Var(mod.s, mod.t)  # Long term degradation cost based on charging rate ($/h)
mod.f_c_st = Var(mod.s, mod.t)  # Long term degradation cost based on storage state ($/h)
mod.f_c_g = Var(mod.g, mod.t)  # Electricity generation cost ($/h)



# (1) Objective function
def profit_rule(mod):
    if mod._clearing == 0:
        return mod._delta_t * sum(mod.Pi[t] * (
                sum((mod.f_e_dc[s, t] - mod.p_ch[s, t]) for s in mod.s) +
                sum(mod.p_gen[g, t] for g in mod.g)) for t in mod.t) - \
               sum(mod.f_c_p[s] + mod.f_c_m[s] for s in mod.s) - \
               mod._delta_t * sum(
            mod.f_c_dc[s, t] + mod.f_c_ch[s, t] + mod.f_c_st[s, t] for s in mod.s for t in mod.t) - \
               mod._delta_t * sum(mod.f_c_g[g, t] for g in mod.g for t in mod.t)
    else:
        return - mod._delta_t * sum(
            mod.f_c_dc[s, t] + mod.f_c_ch[s, t] + mod.f_c_st[s, t] for s in mod.s for t in mod.t) - \
               mod._delta_t * sum(mod.f_c_g[g, t] for g in mod.g for t in mod.t)


mod.profit = Objective(rule=profit_rule, sense=maximize)

# (1a_i) Defines the amount of storage, mod.f_e_st[s, t], kept from the previous time step
def fun1a_i_rule(mod, s, t):
    if mod._loss == 0:
        if t == 1:
            return mod.f_e_st[s, t] == mod.S0[s]
        else:
            return mod.f_e_st[s, t] == mod.S[s, t - 1]
    else:
        if t == 1:
            return mod.f_e_st[s, t] == mod.e_st[s] * mod.S0[s]
        else:
            return mod.f_e_st[s, t] == mod.e_st[s] * mod.S[s, t - 1]

# (1a_ii) Defines the conversion function, f_e_dc, that converts the energy discharged to the energy sold
def fun1a_ii_rule(mod, s, t):
    if mod._loss == 0:
        return mod.f_e_dc[s, t] == mod.p_dc[s, t]
    else:
        return mod.f_e_dc[s, t] == mod.e_dc[s] * mod.p_dc[s, t]


# (1a_iii) Defines the conversion function, f_e_ch, that converts the purchased energy to the energy charged
def fun1a_iii_rule(mod, s, t):
    if mod._loss == 0:
        return mod.f_e_ch[s, t] == mod.p_ch[s, t]
    else:
        return mod.f_e_ch[s, t] == mod.e_ch[s] * mod.p_ch[s, t]


# (1b_i) Defines the cost function, f_c_p, the penalty function for exceeding the ideal EOH storage state
def fun1b_i_rule(mod, s):
    if mod._penEOH == 0:
        return mod.f_c_p[s] == 0
    else:
        return mod.f_c_p[s] == mod.c_p[s] * mod.S_p[s]


# (1b_ii) Defines the cost function, f_c_m, the penalty function for falling short of the ideal EOH storage state
def fun1b_ii_rule(mod, s):
    if mod._penEOH == 0:
        return mod.f_c_m[s] == 0
    else:
        return mod.f_c_m[s] == mod.c_m[s] * mod.S_m[s]

# (1c_i) Defines the cost function, f_c_st, the long term degradation cost based on the storage state
def fun1c_i_rule(mod, s, k, t):
    if mod._degrade == 0:
        return mod.f_c_st[s, t] == 0
    else:
        return mod.f_c_st[s, t] >= mod.A[s, k] * mod.S[s, t] + mod.B[s, k]

# (1c_ii) Defines the cost function, f_c_dc, the long term degradation cost of discharging the storage unit
def fun1c_ii_rule(mod, s, t):
    if mod._degrade == 0:
        return mod.f_c_dc[s, t] == 0
    else:
        return mod.f_c_dc[s, t] == mod.c_dc[s] * mod.p_dc[s, t]


# (1c_iii) Defines the cost function, f_c_ch, the long term degradation cost of discharging the storage unit
def fun1c_iii_rule(mod, s, t):
    if mod._degrade == 0:
        return mod.f_c_ch[s, t] == 0
    else:
        return mod.f_c_ch[s, t] == mod.c_ch[s] * mod.p_ch[s, t]


# (1d) Defines the cost function, f_c_g, the cost of generation
def fun1d_rule(mod, g, t):
    if mod._gen == 0:
        return mod.f_c_g[g, t] == 0
    else:
        return mod.f_c_g[g, t] == mod.c_gen[g] * mod.p_gen[g, t]


mod.fun1a_i = Constraint(mod.s, mod.t, rule=fun1a_i_rule)
mod.fun1a_ii = Constraint(mod.s, mod.t, rule=fun1a_ii_rule)
mod.fun1a_iii = Constraint(mod.s, mod.t, rule=fun1a_iii_rule)
mod.fun1b_i = Constraint(mod.s, rule=fun1b_i_rule)
mod.fun1b_ii = Constraint(mod.s, rule=fun1b_ii_rule)
mod.fun1c_i = Constraint(mod.sk_map, mod.t, rule=fun1c_i_rule)
mod.fun1c_ii = Constraint(mod.s, mod.t, rule=fun1c_ii_rule)
mod.fun1c_iii = Constraint(mod.s, mod.t, rule=fun1c_iii_rule)
mod.fun1d = Constraint(mod.g, mod.t, rule=fun1d_rule)


# (2a) Storage State:
def con2a_rule(mod, s, t):
    return mod.S[s, t] == mod.f_e_st[s, t] + \
           mod._delta_t * (mod.f_e_ch[s, t] - mod.p_dc[s, t])


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
    if mod._ramp == 0:
        return Constraint.Skip
    else:
        if t == 1:
            return (mod.p_ch[s, t] - mod.p_ch0[s]) - (mod.p_dc[s, t] - mod.p_dc0[s]) <= mod.r_up[s]
        else:
            return (mod.p_ch[s, t] - mod.p_ch[s, t-1]) - (mod.p_dc[s, t] - mod.p_dc[s, t-1]) <= mod.r_up[s]

# (3a) Ramp down
def con3b_rule(mod, s, t):
    if mod._ramp == 0:
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
    if mod._range == 0:
        return Constraint.Skip
    else:
        return mod.S[s, t] <= mod.S_max[s] * mod.or_max[s]


# (4b) Lower limits
def con4b_rule(mod, s, t):
    if mod._range == 0:
        return Constraint.Skip
    else:
        return mod.S[s, t] >= mod.S_max[s] * mod.or_min[s]


mod.con4a = Constraint(mod.s, mod.t, rule=con4a_rule)
mod.con4b = Constraint(mod.s, mod.t, rule=con4b_rule)


# (5) Electricity generation
def con5_rule(mod, g, t):
    if mod._gen == 0:
        return mod.p_gen[g, t] == 0
    else:
        return mod.p_gen[g, t] <= mod.q_gen[g]


# (6) Real-time load balancing
def con6_rule(mod, t):
    if mod._clearing == 0:
        return Constraint.Skip
    else:
        return sum(mod.f_e_dc[s, t] for s in mod.s) - \
               sum(mod.p_ch[s, t] for s in mod.s) + \
               sum(mod.p_gen[g, t] for g in mod.g) == mod.dem[t]


mod.con5 = Constraint(mod.g, mod.t, rule=con5_rule)
mod.con6 = Constraint(mod.t, rule=con6_rule)