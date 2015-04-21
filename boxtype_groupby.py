#!/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


names = ['box', 'space_free']

df_fs = pd.read_csv(sys.argv[1], names=names,delimiter=',', index_col=False, skiprows=0 )

research_date = os.path.basename(sys.argv[1]).split('.')[0]

names = ['box', 'box_type']
df_box =  pd.read_csv(sys.argv[2], names=names,delimiter=',', index_col=False, skiprows=0 )

df_merged = df_box.merge(df_fs, on=['box'])

df_merged = df_merged[df_merged.box_type.str.contains('^.*MYSKY.*')]

df_merged = df_merged.groupby(['box', 'box_type'])['space_free'].mean().reset_index()

df_merged['max_space'] = np.nan
df_merged['max_space'][df_merged.box_type == 'PACE TDS850NNZ      (0850 - MYSKY HDI)'] = 167772160
df_merged['max_space'][df_merged.box_type == 'PACE TDS850NNZ2     (1850 - MYSKY PLUS)'] = 692060159
df_merged['max_space'][df_merged.box_type == 'PACE TDS460NNZ      (5514 - MYSKY)'] = 83886080

df_merged['used'] = (df_merged.max_space - df_merged.space_free) / df_merged.max_space * 100
df_merged['rdate'] = research_date

file_name  = research_date + '.' + 'usage.dat'
df_merged.to_csv(file_name, index = False, header = False)
