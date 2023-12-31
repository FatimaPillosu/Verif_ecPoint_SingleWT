import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

########################################################################################
# CODE DESCRIPTION
# 03_Plot_BSrel_CI.py plots Brier Score - Reliability component (BSrel), and their correspondent confidence 
# intervals (CI).
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# VRT_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRT).
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the BSrel values for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped BSrel values.
# DirOUT (string): relative path of the directory containing the plots of the real and boostrapped BSrel values.

# INPUT PARAMETERS
Acc = 12
VRT_list = [0.2, 10, 50]
CL = 99
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "orangered", "dimgray"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/02_BSrel_BS"
DirOUT = "Data/Plot/03_BSrel_CI"
########################################################################################


# Defining the way to plot the y-axis in the BSrel plots
class ScalarFormatterClass(ScalarFormatter):
   def _set_format(self):
      self.format = "%1.1f"

# Plotting the BSrel values for a specific VRT
for VRT in VRT_list:

      # Setting the figure
      fig, ax = plt.subplots(figsize=(17, 13))
      
      # Plotting the BSrel values for a specific forecasting system
      for indSystemFC in range(len(SystemFC_list)):
            
            # Selecting the forecasting system to plot, and its correspondent colour in the plot
            SystemFC = SystemFC_list[indSystemFC]
            Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

            # Reading the steps computed, and the original and bootstrapped BSrel values
            DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/BSrel"
            FileNameIN_temp = "BSrel_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT) + ".npy"
            StepF = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,0].astype(int)
            bsrel_real = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1]
            bsrel_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2:]

            # Computing the confidence intervals from the bootstrapped BSrel values
            alpha = 100 - CL # significance level (in %) 
            CI_lower = np.nanpercentile(bsrel_BS, alpha/2, axis=1)
            CI_upper = np.nanpercentile(bsrel_BS, 100 - (alpha/2), axis=1)

            # Plotting the BSrel values
            ax.plot(StepF, bsrel_real, "o-", color=Colour_SystemFC, label=SystemFC, linewidth=4)
            ax.fill_between(StepF, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")

      # Setting the BSrel plot metadata
      DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
      ax.set_title("Brier Score - Reliability Component (BSrel)\n VRT>=" + str(VRT) + "mm/" + str(Acc) + "h, CL=" + str(CL) + "%\n ", fontsize=24, pad=20, weight="bold")
      ax.set_xlabel("Steps ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=24, labelpad=20)
      ax.set_ylabel("BSrel [-]", fontsize=24, labelpad=10)
      yScalarFormatter = ScalarFormatterClass(useMathText=True)
      yScalarFormatter.set_powerlimits((0,0))
      ax.yaxis.set_major_formatter(yScalarFormatter)
      ax.set_xlim([StepF[0]-1, StepF[-1]+1])
      ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
      ax.xaxis.set_tick_params(labelsize=24, rotation=90)
      ax.yaxis.set_tick_params(labelsize=24)
      ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.06), ncol=3, fontsize=20, frameon=False)
      ax.grid(linewidth=0.5)

      # Saving the BSrel plot
      DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "BSrel_" + f"{Acc:02d}" + "h_" + str(VRT) + ".jpeg"
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
      plt.close() 