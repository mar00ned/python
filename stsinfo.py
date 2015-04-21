import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


names=['home', 'set', 'viewing_date', 'viewing_hh', 'viewing_mm', 'viewing_sec', 'broadcast_date', 'broadcast_time', 'duration', 'comtel_station', 'activity', 'network_id',
       'transport_id', 'service_id', 'station_type', 'video_track', 'audio_track', 'data_track', 'application_id', 'producer_id', 'playback_speed',
       'piv_genre', 'capping_genre', 'service_key', 'original_duration']

colspecs = [(4,11), (11,13), (13,21), (21,23), (23,25), (25,27), (27, 35), (35,41), (41,46), (46,51), (51, 53), (53, 58), (58, 63), (63, 68), (68, 71), (71, 74),
            (74, 77), (77, 80), (80, 86), (86, 92), (92, 96), (96, 101), (101, 106), (106, 112), (112, 118)]

chunksize = 20000
j = 0
index_start = 1
total_df = 0


ratings = np.zeros(1440)
for df in pd.read_fwf(sys.argv[1], colspecs=colspecs, header=None, names=names, chunksize=chunksize, iterator=True):
    df = df[['viewing_hh', 'viewing_mm', 'viewing_sec', 'comtel_station', 'activity', 'duration']]
    df['start_min'] = (df.viewing_hh*60 + df.viewing_mm) - 120
    df['end_min'] = (df.start_min + (df.duration / 60))
    df['end_min'] = df.end_min.astype(int)
    if index_start == 1:
        total_df = df
    else:
        total_df = total_df.append(df)
    df.index += index_start
    index_start = df.index[-1] + 1

    for index, row in df.iterrows():
        ratings[row['start_min'] : row['end_min']] += 1

rdate = '2014-06-06 02:00'
dates = pd.date_range(rdate, periods=1440, freq='1min')
ratings_df=pd.DataFrame(ratings, index=dates, columns=['2014-06-06'])


