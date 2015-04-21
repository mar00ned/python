#!/bin/env python

import pandas as pd
import numpy as np
from pylab import *
import logging
import sys

REACH_DURAION = 3 # minutes


#Read the wgt file
names_wgt = ['hh', 'type', 'comp', 'panel', 'weight']
colspecs_wgt = [(0,7), (7,8), (8,10), (10,13), (13,21)]
df_wgt = pd.read_fwf('a.wgt', colspecs=colspecs_wgt, header=None, names=names_wgt)

names_vwg = ['hh', 'comp', 'channel', 'st_time', 'duration']
colspecs_vwg = [(0,7), (7,9), (9,14), (14,18), (18,22)]
df_vwg = pd.read_fwf('blah.vwg', colspecs=colspecs_vwg, header=None, names=names_vwg)

df_wgt = df_wgt[ df_wgt.comp > 0 ]
universe = df_wgt.weight.sum()

df_vwg = df_vwg [ (df_vwg.channel == 148) & (df_vwg.comp > 0)]

hh_durations = df_vwg.groupby(['hh', 'comp']).duration.sum().reset_index()
hh_durations = hh_durations[hh_durations.duration >= 3]

merged_df = pd.merge(hh_durations, df_wgt, on=['hh', 'comp'])
av_reach_thousands = merged_df.weight.sum()
av_reach_percentage = av_reach_thousands/universe*100.0




# read the SWD file
# Get the HW weights
#df_hw_weights=df_dem[df_dem.hw == 1]
#df_hw_weights = df_hw_weights[['hh', 'weight']]
# Get the household universe
#universe=df_hw_weights.weight.sum()

#hh_durations = df_swd.groupby('hh').duration.sum().reset_index()
#merged_df = pd.merge(hh_durations, df_hw_weights, on=['hh'])
#av_reach_thousands = merged_df.weight.sum()
#av_reach_percentage = av_reach_thousands/universe*100.0
