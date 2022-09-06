# %%--  Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

from matplotlibstyle import *
# %%-

# %%--  Settings
DATADIR = "data/"
FIGDIR = "figures/"
SAVE = True
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
#---    A - Injury rate statistics
#///////////////////////////////////////////////////////////////////////////////
# %%--  0-Base statistics
A0_df = dfs_dic["ACCIDENT"]

#   Injury rate
print("Accident mortality rate: %.2F %%"%(A_df["NO_PERSONS_KILLED"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident serious injury rate: %.2F %%"%(A_df["NO_PERSONS_INJ_2"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident minor injury rate: %.2F %%"%(A_df["NO_PERSONS_INJ_3"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident no injury rate: %.2F %%"%(A_df["NO_PERSONS_NOT_INJ"].sum()/A_df["NO_PERSONS"].sum()*100))

# %%-
# %%--  1-Mortality and injury over time
#   Reshape dataframe for plot
A1_df = dfs_dic["ACCIDENT"][['ACCIDENTDATE','NO_PERSONS_KILLED','NO_PERSONS_INJ_2','NO_PERSONS_INJ_3','NO_PERSONS_NOT_INJ']].copy(deep=True)
A1_df['ACCIDENTDATE']=pd.to_datetime(A1_df['ACCIDENTDATE'],infer_datetime_format=True)
A1_df = A1_df.groupby([pd.Grouper(key='ACCIDENTDATE',freq='M')]).sum()
A1_df.reset_index(inplace=True)
A1_df = A1_df.melt(id_vars='ACCIDENTDATE',var_name='Injury level',value_name='Number of persons')
A1_df.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury','NO_PERSONS_INJ_3':'Minor injury','NO_PERSONS_NOT_INJ':'No injury'}}, inplace=True)

#   Plot
figname = "Injury over time"
fig = plt.figure(figsize=(10,6))
ax = plt.gca()
sns.lineplot(
    x='ACCIDENTDATE',
    y='Number of persons',
    hue='Injury level',
    style='Injury level',
    data=A1_df,
    estimator='mean',
    ci=95,
    ax=ax,
    err_style='band',
    markers=True,
    dashes=False,
    legend=True,
)
ax.set_xlabel('Date')
ax.set_title(figname, fontsize=18, y=1.1)
ax.tick_params(axis='x',labelrotation=45)
ax.legend(ncol=4,bbox_to_anchor=(0.5,1.05), loc='center', borderaxespad=0.,frameon=False)
if SAVE: plt.savefig(FIGDIR+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.tight_layout()
plt.show()
# %%-
# %%--  2-Mortality and injury vs speed, age, vehicle type, accident type, person type and location
#   Fatal and serious injury datasets [Severity 1 or 2]
A2_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Merge to events dataset keep only first sequend of events to asses initial impact data
A2_df_events = dfs_dic['ACCIDENT_EVENT'].loc[dfs_dic['ACCIDENT_EVENT']['EVENT_SEQ_NO'] == 1].copy(deep=True)
A2_df = pd.merge(A2_df_fatal, A2_df_events,how="left", on="ACCIDENT_NO")

#   Reshape data for plot
A2_df_speed=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','SPEED_ZONE']].groupby("SPEED_ZONE").sum()
A2_df_speed.reset_index(inplace=True)
A2_df_speed = A2_df_speed.melt(id_vars="SPEED_ZONE",var_name='Injury level',value_name='Number of persons')
A2_df_speed.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_day=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Day Week Description']].groupby("Day Week Description").sum()
A2_df_day.reset_index(inplace=True)
A2_df_day = A2_df_day.melt(id_vars="Day Week Description",var_name='Injury level',value_name='Number of persons')
A2_df_day.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_type=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Accident Type Desc']].groupby("Accident Type Desc").sum()
A2_df_type.reset_index(inplace=True)
A2_df_type = A2_df_type.melt(id_vars="Accident Type Desc",var_name='Injury level',value_name='Number of persons')
A2_df_type.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_light=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Light Condition Desc']].groupby("Light Condition Desc").sum()
A2_df_light.reset_index(inplace=True)
A2_df_light = A2_df_light.melt(id_vars="Light Condition Desc",var_name='Injury level',value_name='Number of persons')
A2_df_light.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_road=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Object Type Desc']].groupby("Road Geometry Desc").sum()
A2_df_road.reset_index(inplace=True)
A2_df_road = A2_df_road.melt(id_vars="Road Geometry Desc",var_name='Injury level',value_name='Number of persons')
A2_df_road.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_obj=A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Object Type Desc']].groupby("Object Type Desc").sum()
A2_df_obj.reset_index(inplace=True)
A2_df_obj = A2_df_obj.melt(id_vars="Object Type Desc",var_name='Injury level',value_name='Number of persons')
A2_df_obj.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)
A2_df_obj=A2_df_obj.loc[A2_df_obj["Object Type Desc"]!="Not Applicable"]

# %%-
# %%--
#   Serious injury rate at speed/age/vehicle type/location over time?
# %%-
