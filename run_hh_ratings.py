#!/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import logging
import sys

MODULE='gen_ratings'

def init_logger(log_file):
    logger=logging.getLogger(MODULE)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)

    formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

# not wrapping it in main as then it becomes impossible to work in ipython
init_logger('comtel.log')
logger = logging.getLogger(MODULE)

# read the SWD file
names_swd=['hh', 'mem', 'channel', 'start_hh', 'start_min', 'start_second', 'end_hh', 'end_min', 'end_second', 'set_number', 'activity', 'platform']
colspecs_swd = [(0,7), (7,9), (9,13), (13,15), (15,17), (17,19), (19,21), (21,23), (23,25), (25,26), (26,27), (27,28)]
df_swd = pd.read_fwf(sys.argv[1], colspecs=colspecs_swd, header=None, names=names_swd)
#df_swd = df_swd[df_swd.activity == '1']
df_swd = df_swd[df_swd.channel != 541]

logger.info('Read the swd file')

df_swd['start_mins'] = (df_swd['start_hh']*60 + df_swd['start_min'] - 120)
df_swd['end_mins'] = (df_swd['end_hh']*60 + df_swd['end_min'] + 1 - 120)

logger.info('Processed the start and end minutes')

#read the DEM file
names_dem = ['hh', 'mem', 'weight' , 'hw']
colspecs_dem = [(0,7), (7,9), (9,17), (26,27)] #hw is character 72
df_dem = pd.read_fwf(sys.argv[2], colspecs=colspecs_dem, header=None, names=names_dem)

logger.info('Read the dem file')


#Get the HW weights
df_hw_weights=df_dem[df_dem.hw == 1]
df_hw_weights = df_hw_weights[['hh', 'weight']]
# Get the universe
universe=df_hw_weights.weight.sum()

merged_df = pd.merge(df_swd, df_hw_weights, on=['hh'])

logger.info('Creating the household weights and the universe figures')

ratings = np.zeros(1440)

logger.info('Creating the ratings')
for home in merged_df.hh.unique():
    indiv_ratings = np.zeros(1440)
    weight = df_hw_weights[df_hw_weights.hh == home].weight.iloc[0]
    for index, row in merged_df[merged_df.hh == home].iterrows():
        indiv_ratings[row['start_mins'] : row['end_mins']] = 1
    ratings = ratings + (indiv_ratings * weight)


logger.info('Finished creating ratings')

ratings = ratings/universe    
ratings = ratings*100

rdate = sys.argv[3] + ' 02:00'
dates = pd.date_range(rdate, periods=1440, freq='1min')
ratings_df=pd.DataFrame(ratings, index=dates, columns=[sys.argv[3]])

logger.info('Finished')

#if __name__ == '__main__':
#    __name__ = 'Main'
#    main()
    

