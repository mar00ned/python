#!/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import logging
import sys

MODULE='gen_home_channel_reach'
REACH_DURAION = 3 # minutes


# read the SWD file
names_swd=['hh', 'mem', 'channel', 'start_hh', 'start_min', 'start_second', 'end_hh', 'end_min', 'end_second', 'set_number', 'activity', 'platform']
colspecs_swd = [(0,7), (7,9), (9,13), (13,15), (15,17), (17,19), (19,21), (21,23), (23,25), (25,26), (26,27), (27,28)]
df_swd = pd.read_fwf(sys.argv[1], colspecs=colspecs_swd, header=None, names=names_swd)
df_swd['start_mins'] = (df_swd['start_hh']*60 + df_swd['start_min'] - 120)
df_swd['end_mins'] = (df_swd['end_hh']*60 + df_swd['end_min'] + 1 - 120)

df_swd['duration'] = (df_swd.end_mins - df_swd.start_mins) 

#Eliminate the guests / Do it for BBC1-SD only / Duration > REACH_DURATION
df_swd = df_swd[(df_swd.channel == 100) & (df_swd.duration >= REACH_DURAION) & (df_swd.mem < 50)]

#read the DEM file
names_dem = ['hh', 'mem', 'weight' , 'hw']
colspecs_dem = [(0,7), (7,9), (9,17), (26,27)] #hw is character 27
df_dem = pd.read_fwf(sys.argv[2], colspecs=colspecs_dem, header=None, names=names_dem)

# Get the HW weights
df_hw_weights=df_dem[df_dem.hw == 1]
df_hw_weights = df_hw_weights[['hh', 'weight']]
# Get the household universe
universe=df_hw_weights.weight.sum()

hh_durations = df_swd.groupby('hh').duration.sum().reset_index()
merged_df = pd.merge(hh_durations, df_hw_weights, on=['hh'])
av_reach_thousands = merged_df.weight.sum()
av_reach_percentage = av_reach_thousands/universe*100.0
