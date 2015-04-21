import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

research_date = os.path.basename(sys.argv[3]).split('.')[0]

names = ['card', 'box_type', 'free', 'max_space', 'used_percent', 'research_date']
df_card_data = pd.read_csv(sys.argv[1], delimiter=',', index_col=False, names=names)

names = ['home', 'set', 'card']
df_home_map = pd.read_csv(sys.argv[2], delimiter=',', index_col=False, names=names)

df_merged = pd.merge(df_card_data, df_home_map, on=['card'])
df_merged['viewing_date'] = df_merged.research_date.str.split('-').apply(lambda x : int(x[0]+x[1]+x[2]))





#names=['home', 'set', 'viewing_date', 'viewing_hh', 'viewing_mm', 'viewing_sec', 'broadcast_date', 'broadcast_time', 'duration', 'comtel_station', 'activity', 'network_id',
#       'transport_id', 'service_id', 'station_type', 'video_track', 'audio_track', 'data_track', 'application_id', 'producer_id', 'playback_speed',
#       'piv_genre', 'capping_genre', 'service_key', 'original_duration']
#colspecs = [(4,11), (11,13), (13,21), (21,23), (23,25), (25,27), (27, 35), (35,41), (41,46), (46,51), (51, 53), (53, 58), (58, 63), (63, 68), (68, 71), (71, 74),
#            (74, 77), (77, 80), (80, 86), (86, 92), (92, 96), (96, 101), (101, 106), (106, 112), (112, 118)]
#df = pd.read_fwf(sys.argv[3], colspecs=colspecs, header=None, names=names)
#df = df[(df.activity != 52) & (df.activity >= 30)]
#df = df[['home', 'set', 'viewing_date', 'viewing_hh', 'viewing_mm', 'viewing_sec', 'broadcast_date', 'duration', 'activity', 'capping_genre', 'duration']]
#file_name = research_date + '.tuning.dat'
#df.to_csv(file_name, index = False, header = False)

#df_m = pd.merge(df, df_merged, on=['home', 'set', 'viewing_date'])

names=['home', 'set', 'viewing_date', 'viewing_hh', 'viewing_mm', 'viewing_sec', 'broadcast_date', 'duration', 'activity', 'capping_genre', 'duration']
df = pd.read_csv(sys.argv[3], delimiter=',', index_col = False, names = names)
df_m = pd.merge(df, df_merged, on=['home', 'set', 'viewing_date'])



