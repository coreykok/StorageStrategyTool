# '''
# =========================================================================
# (c) Danmarks Tekniske Universitet 2020
#
# Script         : Plots output
# Author         : Corey Kok
# ========================================================================
# Input          : - .csv files in Output folder
#
# Output         : - Plot of profit, storage state, and charging and discharging solutions
#
# Parameters     : - deltaTime - gap between time-steps in hours,
# =========================================================================
# '''

library(ggplot2)
library(RColorBrewer)
library(scales)

Stor.df = read.csv("Output/StorageNext.csv", header=TRUE)
Gen.df = read.csv("Output/GenerationNext.csv", header=TRUE)
Prices.df = read.csv("Input/Prices.csv", header=TRUE)
StorParam.df = read.csv("Input/Storage.csv", header=TRUE)
GenParam.df = read.csv("Input/Generation.csv", header=TRUE)
Model.df = read.csv("Input/Model.csv", header=TRUE) 

Model.df = read.csv("Input/Model_Barge.csv", header=TRUE) 
Prices.df = read.csv("Input/Prices_Barge.csv", header=TRUE)

deltaTime = Model.df$X_delta_t # 5 Minute timesteps

# Append price and useful storage parameters to Stor.df and calculate profit + cumulative profit
Stor.df = merge(Stor.df, Prices.df, by = "Time", all.x = TRUE)
Stor.df$e_ch = StorParam.df$e_ch[StorParam.df$s %in% Stor.df$s]
Stor.df$e_dc = StorParam.df$e_dc[StorParam.df$s %in% Stor.df$s]
Stor.df$e_st = StorParam.df$e_st[StorParam.df$s %in% Stor.df$s]
Stor.df$e_st = StorParam.df$e_st[StorParam.df$s %in% Stor.df$s]
Stor.df$e_st = StorParam.df$e_st[StorParam.df$s %in% Stor.df$s]
Stor.df$e_st = StorParam.df$e_st[StorParam.df$s %in% Stor.df$s]
Stor.df$Profit = deltaTime * Stor.df$Pi * (Stor.df$e_dc * Stor.df$p_dc - Stor.df$p_ch + Gen.df$p_gen)
Stor.df$Time = as.POSIXct(Stor.df$Time, '%Y-%m-%d %H:%M',tz=Sys.timezone())
Stor.df$CumProfit = ave(Stor.df$Profit, Stor.df$s, FUN = cumsum)

######################################################################

# Net money received on the spot market at each 5 minute time-step
ggplot(Stor.df, aes(x = Time, y = Profit, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Market Profit ($)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') + 
    theme(text=element_text(size=15))
ggsave("Plots/01_Netprofit.pdf")

# Cumulative profit earned on the spot market at current time-step
ggplot(Stor.df, aes(x = Time, y = CumProfit, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Cumulative Profit ($)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    theme(text=element_text(size=15))
ggsave("Plots/02_CumProfit.pdf")

######################################################################

Charge.df = Stor.df[,c("s","Time")]; Charge.df$Type = "Charging"; Charge.df$Power = Stor.df$p_ch
Discha.df = Stor.df[,c("s","Time")]; Discha.df$Type = "Discharging"; Discha.df$Power = Stor.df$p_dc
Energy.df = rbind(Charge.df, Discha.df)
Energy.df$CumEnergy = ave(Energy.df$Power * deltaTime, Energy.df$s, Energy.df$Type, FUN = cumsum)

# Power Charging or Discharging storage device
ggplot(Energy.df, aes(x = Time, y = Power, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Power Transfer (kW)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks = pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    facet_grid(Type~.) + 
    theme(text=element_text(size=15))
ggsave("Plots/03_Power.pdf")

# Cumulative Energy Charged and Discharged from storage devices
ggplot(Energy.df, aes(x = Time, y = CumEnergy, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Cumulative Energy Transfer (kWh)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    facet_grid(Type~.) + 
    theme(text=element_text(size=15))
ggsave("Plots/04_CumEnergy.pdf")

######################################################################

# Energy in storage device at each time-step
ggplot(Stor.df, aes(x = Time, y = S, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Energy in Storage Device (kWh)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    theme(text=element_text(size=15)) +
    geom_hline(data = StorParam.df, aes(yintercept = or_max * S_max, colour = s), linetype ="dashed") +
    geom_hline(data = StorParam.df, aes(yintercept = or_min * S_max, colour = s), linetype ="dashed") +
    geom_hline(data = StorParam.df, aes(yintercept = S_max, colour = s)) + 
    geom_hline(data = StorParam.df, aes(yintercept = 0))
ggsave("Plots/05_EnergyStored.pdf")

######################################################################

# Calculate losses and create Loss.df - which stores each type of storage device losses as well as the total losses
Loss_Cha.df = Stor.df[,c("s","Time")]; Loss_Cha.df$Type = "Charging"; Loss_Cha.df$Loss = Model.df$X_loss[1] * deltaTime * Stor.df$e_ch * Stor.df$p_ch;
Loss_Dch.df = Stor.df[,c("s","Time")]; Loss_Dch.df$Type = "Disharging"; Loss_Dch.df$Loss = Model.df$X_loss[1] * deltaTime * Stor.df$e_dc * Stor.df$p_dc;
Loss_Str.df = Stor.df[,c("s","Time")]; Loss_Str.df$Type = "Storing"; Loss_Str.df$Loss = Model.df$X_loss[1] * deltaTime * Stor.df$e_st * Stor.df$S;
Loss.df = Stor.df[,c("s","Time")]; Loss.df$Type = "Total"; Loss.df$Loss = Loss_Cha.df$Loss + Loss_Dch.df$Loss + Loss_Str.df$Loss
Loss.df = rbind(Loss.df, Loss_Cha.df, Loss_Dch.df, Loss_Str.df)
Loss.df$Type = factor(Loss.df$Type)
Loss.df$CumLoss = ave(Loss.df$Loss, Loss.df$s, Loss.df$Type, FUN = cumsum) 

# Net energy losses at each time-step
ggplot(Loss.df, aes(x = Time, y = Loss, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Net Energy Losses (kWh)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    facet_grid(Type~.) + 
    theme(text=element_text(size=15))
ggsave("Plots/06_Losses.pdf")

# Cumulative energy losses at each time-step
ggplot(Loss.df, aes(x = Time, y = CumLoss, colour = s)) +
    geom_point() +
    geom_line(linetype ="dotted") +
    expand_limits(y = 0) +
    scale_y_continuous("Cumulative Energy Losses (kWh)", breaks = pretty_breaks()) +
    scale_x_datetime("Date", breaks =  pretty_breaks()) +
    scale_colour_brewer('Storage\nDevice', palette = 'Set1') +
    facet_grid(Type~.) + 
    theme(text=element_text(size=15))
ggsave("Plots/07_CumLosses.pdf")


