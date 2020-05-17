import time
import scipy as sc
import numpy as np
import pandas as pd
import sys

from numpy import load
from numpy import asarray
from numpy import savez_compressed


def averaging(list_name, ws=3):
    temp_list = list_name.copy()
    for i in range(len(list_name)):
        s = list_name[i]
        count = int((ws - 1) / 2)
        
        while count > 0:
            if i + count < len(temp_list): 
                s += list_name[i+count]
            if i - 1 >= 0:
                s += list_name[i-count]
            count -= 1
        
        temp_list[i] = s / float(ws)
    return temp_list
    

windows = [int(sys.argv[1])]
times = []
f1_scores = []
for window in windows:
    #averaging_window = int(input('Enter size of window:\n'))
    averaging_window = window
    
    t0 = time.time()
    axises = ['x', 'y', 'z']
    fall_data = list()
    adl_data = list()


    dict_data = load('fall_data.npz')
    #dict_data = load('fall_data10535.npz')
    data = dict_data['arr_0']
    fall_data.append(data)

    x = averaging(fall_data[0][0], averaging_window)
    y = averaging(fall_data[0][1], averaging_window)
    z = averaging(fall_data[0][2], averaging_window)

    fall_data[0][0] = x
    fall_data[0][1] = y
    fall_data[0][2] = z

    data = asarray(fall_data[0])
    savez_compressed('fall_data-denoised-'+str(averaging_window)+'.npz', data)

    # ----------- ADL
    dict_data = load('adl_data.npz')
    #dict_data = load('adl_data10535.npz')
    data = dict_data['arr_0']
    adl_data.append(data)

    x = averaging(adl_data[0][0], averaging_window)
    y = averaging(adl_data[0][1], averaging_window)
    z = averaging(adl_data[0][2], averaging_window)

    adl_data[0][0] = x
    adl_data[0][1] = y
    adl_data[0][2] = z

    data = asarray(adl_data[0])
    savez_compressed('adl_data-denoised-'+str(averaging_window)+'.npz', data)
    

