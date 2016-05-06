import os
import sys
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

view = pd.read_csv('expedia_tv3.sql', delimiter = '\t')
view['view_start'] = pd.to_datetime(view.view_start)
view['view_end'] = pd.to_datetime(view.view_end)
view['r_date'] = view.view_start.apply(lambda x : x.date())
view['r_date'] = pd.to_datetime(view.r_date)



adplay = pd.read_excel('tv3_expedia.xlsx')
adplay['r_date'] = pd.to_datetime(adplay.Date, format = '%d-%m-%Y')

#fucking 26 hrs in a day crap
adplay['start_sec'] = adplay['Start Time'].apply(lambda x : int(x.split(':')[0])*3600 + int(x.split(':')[1])*60)
adplay['start_time'] = adplay.r_date + adplay.start_sec.values.astype("timedelta64[s]")
adplay['end_time'] = adplay.start_time + adplay.Duration.values.astype("timedelta64[s]")

#quartiles
adplay['fq_end_time'] = adplay.start_time + (adplay.Duration.values / 4).astype("timedelta64[s]")
adplay['sq_end_time'] = adplay.start_time + (2*(adplay.Duration.values/4)).astype("timedelta64[s]")
adplay['tq_end_time'] = adplay.start_time + (3*(adplay.Duration.values/4)).astype("timedelta64[s]")


adplay['creative'] = 'expedia_ie_march_2016_' + adplay.Duration.apply(str)
adplay = adplay[['r_date', 'start_time', 'end_time', 'creative', 'Break-Name', 'fq_end_time', 'sq_end_time', 'tq_end_time']]

merged = pd.merge(view, adplay, on='r_date')
merged_copy = merged.copy()

#Any exposure
merged = merged[(merged.view_start <= merged.end_time) & (merged.view_end >= merged.start_time)]
result = merged.groupby(['start_time', 'end_time', 'Break-Name', 'creative']).cpe_wid.unique().apply(np.size).reset_index()
result = result.sort(['cpe_wid'], ascending = [0])

#FQ watched
merged_fq = merged_copy[(merged_copy.view_start <= merged_copy.start_time) & (merged_copy.view_end >= merged_copy.fq_end_time)]
result_fq = merged_fq.groupby(['start_time', 'end_time', 'Break-Name', 'creative']).cpe_wid.unique().apply(np.size).reset_index().sort(['cpe_wid'], ascending = [0])
final_result = result.merge(result_fq, on=['start_time', 'end_time', 'Break-Name', 'creative'])

#SQ watched
merged_sq = merged_copy[(merged_copy.view_start <= merged_copy.start_time) & (merged_copy.view_end >= merged_copy.sq_end_time)]
result_sq = merged_sq.groupby(['start_time', 'end_time', 'Break-Name', 'creative']).cpe_wid.unique().apply(np.size).reset_index().sort(['cpe_wid'], ascending = [0])
final_result = final_result.merge(result_sq, on=['start_time', 'end_time', 'Break-Name', 'creative'])

#TQ watched
merged_tq = merged_copy[(merged_copy.view_start <= merged_copy.start_time) & (merged_copy.view_end >= merged_copy.tq_end_time)]
result_tq = merged_tq.groupby(['start_time', 'end_time', 'Break-Name', 'creative']).cpe_wid.unique().apply(np.size).reset_index().sort(['cpe_wid'], ascending = [0])
final_result = final_result.merge(result_tq, on=['start_time', 'end_time', 'Break-Name', 'creative'])

#Complete Watched
merged_com = merged_copy[(merged_copy.view_start <= merged_copy.start_time) & (merged_copy.view_end >= merged_copy.end_time)]
result_com = merged_com.groupby(['start_time', 'end_time', 'Break-Name', 'creative']).cpe_wid.unique().apply(np.size).reset_index().sort(['cpe_wid'], ascending = [0])
final_result = final_result.merge(result_com, on=['start_time', 'end_time', 'Break-Name', 'creative'])


final_result.columns=['start_time', 'end_time', 'Break-Name', 'creative', 'any', 'fq', 'sq', 'tq', 'complete']

