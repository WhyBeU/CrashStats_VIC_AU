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
# %%--  2-Mortality and injury rate category statistics
#   Fatal and serious injury datasets [Severity 1 or 2]
A2_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Merge to atmospheric condition dataset keep only first sequend of events to asses initial impact data
A2_df_atms = dfs_dic['ATMOSPHERIC_COND'].loc[dfs_dic['ATMOSPHERIC_COND']['ATMOSPH_COND_SEQ'] == 1].copy(deep=True)
A2_df = pd.merge(A2_df, A2_df_atms,how="left", on="ACCIDENT_NO")

#   Convert to injury rate percentage
A2_df['NO_PERSONS_KILLED'] = A2_df['NO_PERSONS_KILLED']/A2_df['NO_PERSONS_KILLED'].sum()*100
A2_df['NO_PERSONS_INJ_2'] = A2_df['NO_PERSONS_INJ_2']/A2_df['NO_PERSONS_INJ_2'].sum()*100

#   Reshape data for plot
A2_df_speed = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','SPEED_ZONE']].groupby("SPEED_ZONE").sum()
A2_df_speed.reset_index(inplace=True)
A2_df_speed = A2_df_speed.melt(id_vars="SPEED_ZONE",var_name='Injury level',value_name='Number of persons [%]')
A2_df_speed.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_day = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Day Week Description']].groupby("Day Week Description").sum()
A2_df_day.reset_index(inplace=True)
A2_df_day = A2_df_day.melt(id_vars="Day Week Description",var_name='Injury level',value_name='Number of persons [%]')
A2_df_day.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_type = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Accident Type Desc']].groupby("Accident Type Desc").sum()
A2_df_type.reset_index(inplace=True)
A2_df_type = A2_df_type.melt(id_vars="Accident Type Desc",var_name='Injury level',value_name='Number of persons [%]')
A2_df_type.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_light = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Light Condition Desc']].groupby("Light Condition Desc").sum()
A2_df_light.reset_index(inplace=True)
A2_df_light = A2_df_light.melt(id_vars="Light Condition Desc",var_name='Injury level',value_name='Number of persons [%]')
A2_df_light.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_road = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Road Geometry Desc']].groupby("Road Geometry Desc").sum()
A2_df_road.reset_index(inplace=True)
A2_df_road = A2_df_road.melt(id_vars="Road Geometry Desc",var_name='Injury level',value_name='Number of persons [%]')
A2_df_road.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A2_df_atm = A2_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Atmosph Cond Desc']].groupby("Atmosph Cond Desc").sum()
A2_df_atm.reset_index(inplace=True)
A2_df_atm = A2_df_atm.melt(id_vars="Atmosph Cond Desc",var_name='Injury level',value_name='Number of persons [%]')
A2_df_atm.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)
A2_df_atm = A2_df_atm.loc[A2_df_atm["Atmosph Cond Desc"]!="Not Applicable"]

#   Plot
figname = "Injury rate by category"
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20,15))
x_tab = ['SPEED_ZONE', 'Day Week Description', 'Accident Type Desc', 'Light Condition Desc', 'Road Geometry Desc', 'Atmosph Cond Desc']
df_tab = [A2_df_speed, A2_df_day, A2_df_type, A2_df_light, A2_df_road, A2_df_atm]
xlabel_tab = ['Speed zone', 'Day of the week', 'Accident type', 'Light condition', 'Road type', 'Atmospheric condition']
rot_tab = [0, 0, 90, 90, 90, 90]
asc_tab = [False, False, True, True, True, True]
for x, df, xlabel, rot, ax, asc in zip(x_tab, df_tab, xlabel_tab, rot_tab, axes.flatten(),asc_tab):
    if asc: df.sort_values('Number of persons [%]', inplace=True, ascending=False)
    sns.barplot(
        x=x,
        y='Number of persons [%]',
        hue='Injury level',
        data=df,
        ax=ax,
        saturation=0.8,
    )
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x',labelrotation=rot)
    ax.legend_.remove()

axes[0][1].set_title(figname, fontsize=18, y=1.1)
axes[0][1].legend(ncol=2,bbox_to_anchor=(0.5,1.05), loc='center', borderaxespad=0.,frameon=False)
if SAVE: plt.savefig(FIGDIR+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.tight_layout()
plt.show()
# %%-
# %%--
#   Serious injury rate at speed/age/vehicle type/location over time?
# %%-
