#!/bin/env python

import numpy as np
import sys
import pandas as pd
import re


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
                          (r'TotalVwgSt16_34', '[0-9]', '1', np.int32)
                        ]

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
                          (r'Ethinicity', '[0-9]', '2', np.int32)
                         ]

def regex_string(record, record_type):
    ret_regex = ''
    for i in range(1,len(record)):
        ret_regex += '(' + record[i][1] + '{' + record[i][2] + '})'
    return r'(\^' + record_type  + ')' + ret_regex + r'\s*\n'

def data_type_list(record):
    ret_val_list = []
    for i in range(0, len(record)):
#        ret_val_list.append((record[i][0], 'S' + record[i][2]))
        ret_val_list.append((record[i][0], record[i][3]))
    return ret_val_list        

#def main():
#    print pvf_weights_rec
input_file = sys.argv[1]

regexp = regex_string(pvf_weights_rec, '05')
print regexp
data_types = data_type_list(pvf_weights_rec)
weights_df = pd.DataFrame(np.fromregex(input_file, regexp, data_types))

regexp = regex_string(pvf_members_rec, '04')
print regexp
data_types = data_type_list(pvf_members_rec)
members_df = pd.DataFrame(np.fromregex(input_file, regexp, data_types))


#if __name__ == '__main__':
#    __name__ = 'Main'
#    main()
