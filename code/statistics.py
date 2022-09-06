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
# %%--  Base statistics
A_df = dfs_dic["ACCIDENT"]

#   Injury rate
print("Accident mortality rate: %.2F %%"%(A_df["NO_PERSONS_KILLED"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident serious injury rate: %.2F %%"%(A_df["NO_PERSONS_INJ_2"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident minor injury rate: %.2F %%"%(A_df["NO_PERSONS_INJ_3"].sum()/A_df["NO_PERSONS"].sum()*100))
print("Accident no injury rate: %.2F %%"%(A_df["NO_PERSONS_NOT_INJ"].sum()/A_df["NO_PERSONS"].sum()*100))

# %%-
# %%--  1-Mortality and injury over time
#   Reshape dataframe for plot
A1_df = A_df[['ACCIDENTDATE','NO_PERSONS_KILLED','NO_PERSONS_INJ_2','NO_PERSONS_INJ_3','NO_PERSONS_NOT_INJ']].copy(deep=True)
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
# %%--
#   Serious injury rate at speed/age/vehicle type/location over time?
# %%-
