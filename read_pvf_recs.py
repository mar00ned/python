#!/bin/env python

import numpy as np
import sys
import pandas as pd
import copy

viewing_array = []

def split_viewing (df):
    ret_array = []
    for index, row in df.iterrows():
        rest = row[1:13].tolist()
        for i,x in enumerate(list(row['PersonMap'])):
            rest2 = []
            if x == '1':
                rest2 = copy.copy(rest)
                rest2.append(i+1)
                ret_array.append(rest2)
    return ret_array                


def greater(x, y):
    if x > y:
        return y
    else:
        return x

def lesser(x, y):
    if x < y:
        return y
    else:
        return x





PVF_WEIGHTING_REC_TYPE = '05'
pvf_weights_rec =       [ (r'RecordType', '[0-9]', '2', np.int32),
                          (r'HouseholdNumber', '[0-9]', '7', np.int64),
                          (r'PersonNumber', '[0-9]', '2', np.int32),
                          (r'ReportingPanel', '[0-9]', '5', np.int32),
                          (r'DateOfActivity', '[0-9]', '8', np.int64),
                          (r'ResponseCode', '[0-9]', '1', np.int32),
                          (r'ProcessingWeight', '[0-9]', '7', np.int64),
                          (r'AdultsCommTvVwgSt', '[0-9]', '1', np.int32),
                          (r'ABC1AdultsCommTvSt', '[0-9]' , '1', np.int32),
                          (r'AdultsTotalVwgSt', '[0-9]', '1', np.int32),
                          (r'ABC1AdultsTotalVwgSt', '[0-9]', '1', np.int32),
                          (r'AdultsCommTvVwgSt16_34', '[0-9]', '1', np.int32),
                          (r'TotalVwgSt16_34', '[0-9]', '1', np.int32),
                          (r'Padding', '\s', '122', 'S122')
                        ]

PVF_MEMBER_REC_TYPE = '04'
pvf_members_rec =       [ (r'RecordType', '[0-9]', '2', np.int32),
                          (r'HouseholdNumber', '[0-9]', '7', np.int64),
                          (r'DateValidFor', '[0-9]', '8', np.int64),
                          (r'MembershipStatus', '[0-9]', '1', np.int32),
                          (r'PersonNumber', '[0-9]', '2', np.int32),
                          (r'SexCode', '[0-9]', '1', np.int32),
                          (r'DateOfBirth', '[0-9]', '8', np.int64),
                          (r'MaritalStatus', '[0-9]', '1', np.int32),
                          (r'HouseholdStatus', '[0-9]', '1', np.int32),
                          (r'WorkingStatus', '[0-9]', '1', np.int32),
                          (r'TerminalAgeEdu', '[0-9]', '1', np.int32),
                          (r'WelshLangCode', '[0-9]', '1', np.int32),
                          (r'GaelicLangCode', '[0-9]', '1', np.int32),
                          (r'DependencyKids', '[0-9]', '1', np.int32),
                          (r'LifeStage', '[0-9]', '2', np.int32),
                          (r'Ethinicity', '[0-9]', '2', np.int32),
                          (r'Padding', '\s', '120', 'S120')
                         ]

PVF_VWG_REC_TYPE = '06'
pvf_vwg_rec =          [ (r'RecordType', '[0-9]', '2', np.int32),
                          (r'HouseholdNumber', '[0-9]', '7', np.int64),
                          (r'DateValidFor', '[0-9]', '8', np.int64),
                          (r'SetNumber', '[0-9]', '2', np.int64),
                          (r'StartHH', '[0-9]', '2', np.int64),
                          (r'StartMin', '[0-9]', '2', np.int64),
                          (r'Duration', '[0-9]', '4', np.int32),
                          (r'Activity', '[0-9]', '2', np.int32),
                          (r'PlaybackType', '[\s0-9]', '1', 'S1'),
                          (r'DB1StationCode', '[0-9]', '5', np.int32),
                          (r'Platform', '[0-9]', '1', np.int32),
                          (r'DateOfRecording', '[\s0-9]', '8', 'S8'),
                          (r'StartOfRecording', '[\s0-9]', '4', 'S4'),
                          (r'PersonMap','[0-9]', '16', 'S16'),
                          (r'Interactive', '[0-9]', '9', np.int32),
                          (r'VODIndicator', '[0-9]', '1', np.int32),
                          (r'VODProvider', '[\s0-9]', '5', 'S5'),
                          (r'VODService', '[\s0-9]', '5', 'S5'),
                          (r'VODType', '[\s0-9]', '5', 'S5'),
                          (r'DeviceInUse', '[\s0-9]', '4', 'S4'),
                          (r'Padding', '\s', '67', 'S120')
                         ]


BBC_NETWORK_PANEL = 50

def regex_string(record, record_type):
    ret_regex = ''
    for i in range(1,len(record)):
        ret_regex += '(' + record[i][1] + '{' + record[i][2] + '})'
    return r'(' + record_type  + ')' + ret_regex + r'\n'

def data_type_list(record):
    ret_val_list = []
    for i in range(0, len(record)):
        ret_val_list.append((record[i][0], record[i][3]))
    return ret_val_list        

#def main():  Take this out while working in ipython
input_file = sys.argv[1]


regexp = regex_string(pvf_weights_rec, PVF_WEIGHTING_REC_TYPE) 
data_types = data_type_list(pvf_weights_rec) 
weights_df = pd.DataFrame(np.fromregex(input_file, regexp, data_types)) 
del weights_df['Padding']

#Get weights for BBC network panel only.
weights_df = weights_df[weights_df.ReportingPanel == BBC_NETWORK_PANEL]

regexp = regex_string(pvf_members_rec, PVF_MEMBER_REC_TYPE) 
data_types = data_type_list(pvf_members_rec) 
members_df = pd.DataFrame(np.fromregex(input_file, regexp, data_types)) 
del members_df['Padding']

regexp = regex_string(pvf_vwg_rec, PVF_VWG_REC_TYPE) 
data_types = data_type_list(pvf_vwg_rec) 
vwg_df = pd.DataFrame(np.fromregex(input_file, regexp, data_types)) 
del vwg_df['Padding']


# Not very proud of
vwg_df2 = pd.DataFrame(split_viewing(vwg_df), columns=['HouseholdNumber', 'DateValidFor', 'SetNumber', 'StartHH', 'StartMin', 'Duration', 'Activity', 'PlaybackType', 'DB1StationCode', 'Platform', 'DateOfRecording', 'StartOfRecording', 'PersonNumber'])

vwg_df2['start_min'] = vwg_df2.StartHH*60 + vwg_df2.StartMin

vwg_df2['end_min'] = vwg_df2.start_min + vwg_df2.Duration
