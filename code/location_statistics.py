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
