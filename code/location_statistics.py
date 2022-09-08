# %%--  Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import datetime

from matplotlibstyle import *
# %%-

# %%--  Settings
DATADIR = "data/"
FIGDIR = "figures/"
SAVE = False
# %%-

# %%--  Data loading
filenames = [
    "ACCIDENT_CHAINAGE",
    "ACCIDENT_EVENT",
    "ACCIDENT_LOCATION",
    "ACCIDENT",
    "ATMOSPHERIC_COND",
    "NODE_ID_COMPLEX_INT_ID",
    "NODE",
    "PERSON",
    "SUBDCA",
    "VEHICLE"
]
dfs_dic = {}
for filename in filenames:
    dfs_dic[filename] = pd.read_csv(DATADIR+filename+".csv")
# %%-


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#---    B - Location based accident awareness
#///////////////////////////////////////////////////////////////////////////////

# %%--  0-Map road of all Serious and fatal accident
#   Fatal and serious injury datasets [Severity 1 or 2]
B0_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Merge to NODE dataset to access location. Remove ACCIDENT_NO duplicates
B0_df_node = dfs_dic['NODE'].copy(deep=True)
B0_df_node.drop_duplicates(subset=['ACCIDENT_NO'], inplace=True)
B0_df = pd.merge(B0_df, B0_df_node,how="left", on="ACCIDENT_NO")
B0_df['TOTAL_INJURY'] = B0_df['NO_PERSONS_KILLED'] + B0_df['NO_PERSONS_INJ_2']

#   Convert to injury rate percentage
B0_df['TOTAL_INJURY'] = B0_df['TOTAL_INJURY']/B0_df['TOTAL_INJURY'].sum()*100
B0_df['NO_PERSONS_KILLED'] = B0_df['NO_PERSONS_KILLED']/B0_df['NO_PERSONS_KILLED'].sum()*100
B0_df['NO_PERSONS_INJ_2'] = B0_df['NO_PERSONS_INJ_2']/B0_df['NO_PERSONS_INJ_2'].sum()*100

#   Reshape data for plot
B0_df_killed = B0_df.loc[B0_df['SEVERITY']==1]
B0_df_inj = B0_df.loc[B0_df['SEVERITY']==2]

#   Plot map of all serious accidents
figname = "Injury and fatality map"
alpha = 0.3
size = 1

fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
ax1.scatter(B0_df_inj["VICGRID94_X"],B0_df_inj["VICGRID94_Y"], marker=".", s=size, alpha=alpha, c="orchid")
ax2.scatter(B0_df_killed["VICGRID94_X"],B0_df_killed["VICGRID94_Y"], marker=".", s=size, alpha=alpha, c="k")

ax1.set_aspect("equal")
ax1.axis("off")

ax2.set_aspect("equal")
ax2.axis("off")

if SAVE: plt.savefig(FIGDIR+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.tight_layout()
plt.show()
# %%-
# %%--  1-Map of Bendigo
#   Fatal and serious injury datasets [Severity 1 or 2]
B1_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Merge to NODE dataset to access location. Remove ACCIDENT_NO duplicates
B1_df_node = dfs_dic['NODE'].copy(deep=True)
B1_df_node.drop_duplicates(subset=['ACCIDENT_NO'], inplace=True)
B1_df = pd.merge(B1_df, B1_df_node,how="left", on="ACCIDENT_NO")
B1_df['TOTAL_INJURY'] = B1_df['NO_PERSONS_KILLED'] + B1_df['NO_PERSONS_INJ_2']

#   Convert to injury rate percentage
B1_df['TOTAL_INJURY'] = B1_df['TOTAL_INJURY']/B1_df['TOTAL_INJURY'].sum()*100

#   Plot map of all serious accidents
figname = "Bendigo injury and fatality map"
alpha = 0.5
size = 5
xmin = 2.41e6
ymin = 2.505e6
window = 0.045e6

fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
ax1.scatter(B1_df["VICGRID94_X"],B1_df["VICGRID94_Y"], marker=".", s=size, alpha=alpha, c="orchid")

ax1.set_xlim(xmin, xmin+window)
ax1.set_ylim(ymin, ymin + window)
ax1.set_aspect("equal")
ax1.axis("off")

if SAVE: plt.savefig(FIGDIR+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.tight_layout()
plt.show()
# %%-
