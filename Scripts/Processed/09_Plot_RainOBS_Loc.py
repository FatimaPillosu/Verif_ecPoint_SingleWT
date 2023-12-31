import os
from datetime import datetime, timedelta
import metview as mv

########################################################################################
# CODE DESCRIPTION
# 09_Plot_RainOBS_Loc.py plots a map plot with the location of the observations.
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# TheDate (date, in YYYYMMDD format): date to consider for the observations.
# Acc (number, in hours): rainfall accumulation to consider.
# StartPeriod_list (list of integers): list of the accumulation period's starting time.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the raw observations.
# DirOUT (string): relative path of the directory containing the plots of rainfall gauge's locations.

# INPUT PARAMETERS
TheDate = datetime(2021,12,11)
Acc = 12
StartPeriod_list = [0, 6, 12, 18]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Raw/OBS"
DirOUT = "Data/Plot/09_RainOBS_Loc"
########################################################################################


# Plotting the location of the rainfall observations for a specific accumulation period
obs_all = None
for ind_StartPeriod in range(len(StartPeriod_list)):

      StartPeriod = StartPeriod_list[ind_StartPeriod]
      
      # Reading the rainfall observation for a specific date
      TheDateTime = TheDate + timedelta(hours = (StartPeriod+Acc))
      obs = mv.read(Git_repo + "/" + DirIN + "/" + TheDateTime.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDateTime.strftime("%Y%m%d%H") + ".geo")
      obs_all = mv.merge(obs_all, obs)
      print("N. obs for accumulatio period ending at " + str(StartPeriod) + " UTC: " + str(mv.count(obs)))

# Plotting the location of the observations
coastlines = mv.mcoast(
      map_coastline_colour = "grey",
      map_coastline_thickness = 1,
      map_coastline_resolution = "medium",
      map_boundaries = "on",
      map_boundaries_colour = "grey",
      map_boundaries_thickness = 1,
      map_grid_latitude_increment = 30,
      map_grid_longitude_increment = 60,
      map_label_right = "off",
      map_label_top = "off",
      map_label_colour = "charcoal",
      map_grid_thickness = 1,
      map_grid_colour = "grey",
      map_label_height = 0.4
      )

obs_symb = mv.psymb(
      symbol_type = "marker",
      symbol_table_mode = "on",
      legend = "off",
      symbol_quality = "high",
      symbol_min_table = [0],
      symbol_max_table = [10000],
      symbol_marker_table = [15],
      symbol_colour_table = ["blue"],
      symbol_height_table = [0.05]
      )

title = mv.mtext(
      text_line_count = 1,
      text_line_1 = "Rain gauge locations",
      text_colour = "charcoal",
      text_font_size = 0.75
      )

# Saving the map plot
print("Saving the map plot ...")
MainDirOUT = Git_repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/RainOBS_Loc" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(obs_all, coastlines, obs_symb, title)