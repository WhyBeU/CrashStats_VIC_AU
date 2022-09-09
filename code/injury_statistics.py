# %%--  Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import datetime
from pathlib import Path
from matplotlibstyle import *
# %%-

# %%--  Settings
DIR = Path(__file__).parent.parent
DATADIR = str(DIR/'data')
FIGDIR = str(DIR/'figures')
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
    dfs_dic[filename] = pd.read_csv(DATADIR+"\\"+filename+".csv")
# %%-

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#---    A - Injury rate statistics
#///////////////////////////////////////////////////////////////////////////////

# %%--  0-Base statistics
A0_df = dfs_dic["ACCIDENT"]

#   Injury rate
print("Accident mortality rate: %.2F %%"%(A0_df["NO_PERSONS_KILLED"].sum()/A0_df["NO_PERSONS"].sum()*100))
print("Accident serious injury rate: %.2F %%"%(A0_df["NO_PERSONS_INJ_2"].sum()/A0_df["NO_PERSONS"].sum()*100))
print("Accident minor injury rate: %.2F %%"%(A0_df["NO_PERSONS_INJ_3"].sum()/A0_df["NO_PERSONS"].sum()*100))
print("Accident no injury rate: %.2F %%"%(A0_df["NO_PERSONS_NOT_INJ"].sum()/A0_df["NO_PERSONS"].sum()*100))

# %%-

# %%--  1-Mortality and injury over time
#   Reshape dataframe for plot
A1_df = dfs_dic["ACCIDENT"][['ACCIDENTDATE','NO_PERSONS_KILLED','NO_PERSONS_INJ_2','NO_PERSONS_INJ_3','NO_PERSONS_NOT_INJ']].copy(deep=True)
A1_df['ACCIDENTDATE']=pd.to_datetime(A1_df['ACCIDENTDATE'],infer_datetime_format=True)
A1_df = A1_df.groupby([pd.Grouper(key='ACCIDENTDATE',freq='M')]).sum()
A1_df.reset_index(inplace=True)
A1_df = A1_df.melt(id_vars='ACCIDENTDATE',var_name='Injury level',value_name='Number of persons')
A1_df.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury','NO_PERSONS_INJ_3':'Minor injury','NO_PERSONS_NOT_INJ':'No injury'}}, inplace=True)
A1_df=A1_df.loc[A1_df['Injury level']=='Killed']
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
plt.tight_layout()
if SAVE: plt.savefig(FIGDIR+"\\"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
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
    if x == 'Day Week Description':
        sns.barplot(
            x=x,
            y='Number of persons [%]',
            hue='Injury level',
            order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
            data=df,
            ax=ax,
            saturation=0.8,
        )
    else:
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
plt.tight_layout()
if SAVE: plt.savefig(FIGDIR+"\\"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.show()
# %%-

# %%--  3-Mortality and injury ratefrom vehicle type
#   Fatal and serious injury datasets [Severity 1 or 2]
A3_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Convert to injury rate percentage
A3_df['NO_PERSONS_KILLED'] = A3_df['NO_PERSONS_KILLED']/A3_df['NO_PERSONS_KILLED'].sum()*100
A3_df['NO_PERSONS_INJ_2'] = A3_df['NO_PERSONS_INJ_2']/A3_df['NO_PERSONS_INJ_2'].sum()*100

#   Merge to vehcile dataset assuming vehicle 1 is the vehcile responsible for the accident
A3_df_vehic = dfs_dic['VEHICLE'].loc[dfs_dic['VEHICLE']['VEHICLE_ID'] == "A"].copy(deep=True)
A3_df = pd.merge(A3_df, A3_df_vehic,how="left", on="ACCIDENT_NO")

#   Print impact collision statistics
A3_df_coll = A3_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','INITIAL_IMPACT']].groupby("INITIAL_IMPACT").sum()
A3_df_coll.reset_index(inplace=True)
vocab_coll = {
    '0': 'Towed unit',
    '1': 'Right front corner',
    '2': 'Right side forwards',
    '3': 'Right side rearwards',
    '4': 'Right rear corner',
    '5': 'Left front corner',
    '6': 'Left side forwards',
    '7': 'Left side rearwards',
    '8': 'Left rear corner',
    '9': 'Not known/not applicable',
    'F': 'Front',
    'N': 'None',
    'R': 'Rear',
    'S': 'Sidecar',
    'T': 'Top/roof',
    'U': 'Undercarriag',
}
A3_df_coll.replace({'INITIAL_IMPACT': vocab_coll}, inplace=True)
for i, row in A3_df_coll.iterrows():
    print("Killed: %.2F %%; \t"%(row['NO_PERSONS_KILLED']),"Serious injury : %.2F %%; \t"%(row['NO_PERSONS_INJ_2']),"Impact point: ",row["INITIAL_IMPACT"])

#   Reshape data for plot and keep top n categories based on total person killed and inured
n=10
A3_df_maker = A3_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','VEHICLE_MAKE']].groupby("VEHICLE_MAKE").sum()
A3_df_maker.reset_index(inplace=True)
A3_df_maker['Total'] = A3_df_maker['NO_PERSONS_KILLED']+A3_df_maker['NO_PERSONS_INJ_2']
A3_df_maker = A3_df_maker.nlargest(n,'Total')
A3_df_maker = A3_df_maker.melt(id_vars="VEHICLE_MAKE", value_vars=['NO_PERSONS_KILLED','NO_PERSONS_INJ_2'], var_name='Injury level', value_name='Number of persons [%]')
A3_df_maker.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

A3_df_type = A3_df[['NO_PERSONS_KILLED','NO_PERSONS_INJ_2','Vehicle Type Desc']].groupby("Vehicle Type Desc").sum()
A3_df_type.reset_index(inplace=True)
A3_df_type['Total'] = A3_df_type['NO_PERSONS_KILLED']+A3_df_type['NO_PERSONS_INJ_2']
A3_df_type = A3_df_type.nlargest(n,'Total')
A3_df_type = A3_df_type.melt(id_vars="Vehicle Type Desc", value_vars=['NO_PERSONS_KILLED','NO_PERSONS_INJ_2'], var_name='Injury level',value_name='Number of persons [%]')
A3_df_type.replace({'Injury level':{'NO_PERSONS_KILLED':'Killed','NO_PERSONS_INJ_2':'Serious injury'}}, inplace=True)

#   Plot
figname = "Injury rate by vehicle type and maker"
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(17,5))
x_tab = ['Vehicle Type Desc', 'VEHICLE_MAKE']
df_tab = [A3_df_type, A3_df_maker]
xlabel_tab = ['Vehicle type', 'Vehicle maker']
rot_tab = [90, 90]
for x, df, xlabel, rot, ax in zip(x_tab, df_tab, xlabel_tab, rot_tab, axes.flatten()):
    df.sort_values('Number of persons [%]', inplace=True, ascending=False)
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

axes[0].set_title(figname, fontsize=18, y=1.05)
axes[0].legend(ncol=2,bbox_to_anchor=(1.5,1.07), loc='center', borderaxespad=0.,frameon=False)
plt.tight_layout()
if SAVE: plt.savefig(FIGDIR+"\\"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.show()
# %%-

# %%--  4-Mortality and injury rate by car manufacturing year and accident oldness
#   Fatal and serious injury datasets [Severity 1 or 2]
A4_df = dfs_dic["ACCIDENT"].loc[dfs_dic["ACCIDENT"]["SEVERITY"]<3].copy(deep=True)

#   Merge to vehcile dataset assuming vehicle 1 is the vehcile responsible for the accident
A4_df_vehic = dfs_dic['VEHICLE'].loc[dfs_dic['VEHICLE']['VEHICLE_ID'] == "A"].copy(deep=True)
A4_df = pd.merge(A4_df, A4_df_vehic,how="left", on="ACCIDENT_NO")

#   Only keep cars [VEHICLE_TYPE 1]
A4_df = A4_df.loc[A4_df['VEHICLE_TYPE']==1]

#   Keep rows with Valid Manufacturing year and relevant columns
A4_df = A4_df.dropna(subset=['VEHICLE_YEAR_MANUF'])
A4_df = A4_df.loc[A4_df['VEHICLE_YEAR_MANUF']!=0]
A4_df = A4_df[['VEHICLE_YEAR_MANUF','ACCIDENTDATE','NO_PERSONS_KILLED','NO_PERSONS_INJ_2','SEVERITY']]

#   Convert to injury rate percentage
A4_df['NO_PERSONS_KILLED'] = A4_df['NO_PERSONS_KILLED']/A4_df['NO_PERSONS_KILLED'].sum()*100
A4_df['NO_PERSONS_INJ_2'] = A4_df['NO_PERSONS_INJ_2']/A4_df['NO_PERSONS_INJ_2'].sum()*100

#   Calculate car age at accident [Age at accident]
A4_df['ACCIDENTDATE'] = pd.to_datetime(A4_df['ACCIDENTDATE'],infer_datetime_format=True)
A4_df['AGE'] = [date.year-manuf for date,manuf in zip(A4_df['ACCIDENTDATE'],A4_df['VEHICLE_YEAR_MANUF'])]

#   Reshape data for plot
A4_df_killed = A4_df.loc[A4_df['SEVERITY']==1]
A4_df_killed = A4_df_killed[['NO_PERSONS_KILLED','VEHICLE_YEAR_MANUF','AGE']].groupby(['VEHICLE_YEAR_MANUF','AGE']).sum()
A4_df_killed.reset_index(inplace=True)

A4_df_inj = A4_df.loc[A4_df['SEVERITY']==2]
A4_df_inj = A4_df_inj[['NO_PERSONS_INJ_2','VEHICLE_YEAR_MANUF','AGE']].groupby(['VEHICLE_YEAR_MANUF','AGE']).sum()
A4_df_inj.reset_index(inplace=True)
#   Plot
figname = "Vehicle manufacturing date and age injury rate"
alpha = 1
size = 100
vmin = 0
vmax = 0.5
fig = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=2, ncols=2, figure=fig)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1])
ax3 = fig.add_subplot(gs[1,:])

ax1.scatter(A4_df_inj['VEHICLE_YEAR_MANUF'],A4_df_inj['AGE'],marker=".",s=size, c=A4_df_inj['NO_PERSONS_INJ_2'], alpha=alpha, label="Injured", vmin=vmin, vmax=vmax)
sc = ax2.scatter(A4_df_killed['VEHICLE_YEAR_MANUF'],A4_df_killed['AGE'],marker=".",s=size, c=A4_df_killed['NO_PERSONS_KILLED'], alpha=alpha, label="Killed", vmin=vmin, vmax=vmax)
sns.kdeplot(
    data=A4_df,
    ax=ax3,
    x='VEHICLE_YEAR_MANUF',
    fill=True,
    legend=False,
    color="firebrick",
    clip=(1900,2021),
)

ax1.set_title(figname, fontsize=18, y=1.05, x=1.2)
ax1.set_xlim(1970,2020)
ax1.set_ylim(0,50)
ax1.set_xlabel('Manufacturing year')
ax1.set_ylabel('Age at accident')

ax2.set_xlim(1970,2020)
ax2.set_ylim(0,50)
ax2.set_xlabel('Manufacturing year')

ax3.set_xlim(1970,2020)
ax3.set_xlabel('Manufacturing year')
ax3.set_title("Vehicle manufacturing distribution", fontsize=14, y=0.9, x=0.25)

cbar=fig.colorbar(sc, ax=ax3)
cbar.set_label("Injury rate")

if SAVE: plt.savefig(FIGDIR+"\\"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+"_"+figname+".png",transparent=True,bbox_inches='tight')
plt.show()
# %%-
