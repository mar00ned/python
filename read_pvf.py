#!/bin/env python

import numpy as np
import sys
import pandas as pd

weight_rec_col_specs = [0,7,9,14,22,23,30]
weight_rec_col_names = ['hh', 'person', 'panel', 'date_of_activity', 'response_code', 'weight']

def chunk_splitter(string, col_specs):
    return (string[0 + col_specs[i] : col_specs[i+1]] for i in range(0, len(col_specs) - 1))


def main():
    input_file = sys.argv[1]
    header_names = ['rec_type', 'rec_data']
    header_col_specs = [(0,2), (2,161)]


    df_pvf = pd.read_fwf(input_file, colspecs = header_col_specs, header=None, names = header_names)

    df_weights = df_pvf[df_pvf.rec_type == 5]
    #del df_weights.rec_data
    s = df_weights.rec_data
    df_weights = df_weights.join(s.apply(lambda x: pd.Series(chunk_splitter(x, weight_rec_col_specs), index=weight_rec_col_names)))

if __name__ == '__main__':
    __name__ = 'Main'
    main()
