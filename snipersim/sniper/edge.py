import time
import scipy as sc
import numpy as np
import pandas as pd
from scipy.fftpack import fft
import sys

from numpy import load

def average(data):
    return np.mean(data)

def maximum(data):
    return max(data)

def minimum(data):
    return min(data)

def energy(data):
    return sum(np.square(np.abs(data[:])))

def spectral_energy(data):
    return sum(np.square(abs(fft(data))))

def power_spectral_entropy(data):
    return 

def standard_deviation(data):
    return np.std(data)

def correlation(data1, data2):
    return np.corrcoef(data1, data2)

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
    
        
def createA(data_x, data_y, data_z):
    A = list()
    min_length = min(len(data_x), len(data_y), len(data_z))
    for i in range(min_length):
        temp = np.square(data_x[i]) + np.square(data_y[i]) + np.square(data_z[i])
        A.append(temp)
    return np.sqrt(A)

def createAV(data_x, data_y, data_z):
    AV = list()
    min_length = min(len(data_x), len(data_y), len(data_z))
    for i in range(min_length - 1):
        Y1, Y2 = [data_x[i], data_y[i], data_z[i]], [data_x[i+1], data_y[i+1], data_z[i+1]]
        #length of Y1 and Y2
        l_Y1, l_Y2 = np.linalg.norm(Y1), np.linalg.norm(Y2)
        temp = np.cosh(np.dot(Y1, Y1) / (l_Y1 * l_Y2)) * (180 / np.pi)
        AV.append(temp)
    AV.append(AV[-1])
    return AV

def createVector(data, A_data, AV_data, person_num, i, _type):
    try:
        x = data[person_num][0][i: i + 100].copy()
        y = data[person_num][1][i: i + 100].copy()
        z = data[person_num][2][i: i + 100].copy()
        A = A_data[person_num][i: i+100].copy()
        AV = AV_data[person_num][i: i+100].copy()
    except:
        x = data[person_num][0][i:].copy()
        y = data[person_num][1][i:].copy()
        z = data[person_num][2][i:].copy() 
        A = A_data[person_num][i:].copy()
        AV = AV_data[person_num][i:].copy()
    min_length = min(len(x), len(y), len(z), len(A), len(AV))
    x, y, z, A, Av = x[:min_length], y[:min_length], z[:min_length], A[:min_length], AV[:min_length]
    
    lst = [x, y, z, A, AV]
    result = list()
    for l in lst:
        result.append(average(l))
        result.append(maximum(l))
        result.append(minimum(l))
        result.append(energy(l))
        result.append(spectral_energy(l))
        result.append(standard_deviation(l))
    
    result.append(correlation(x, y)[0][1])
    result.append(correlation(x, z)[0][1])
    result.append(correlation(y, z)[0][1])
    
    if _type == 'Fall':
        result.append(1)
    elif _type == 'Adl':
        result.append(0)
    result.append(person_num)
    return result

feature_lst = ['average', 'maximum', 'minimum', 'energy', 'spectral_energy', 'standard_deviation']
column_names = ['average_x', 'average_y', 'average_z', 'average_A','average_AV', \
                'maximum_x','maximum_y', 'maximum_z', 'maximum_A', 'maximum_AV', \
                'minimum_x', 'minimum_y', 'miminum_z', 'minimum_A', 'minimum_AV', \
                'energy_x', 'energy_y', 'energy_z', 'energy_A', 'energy_AV', \
                'spectral_energy_x', 'spectral_energy_y', 'spectral_energy_z', 'spectral_energy_A', 'spectral_energy_AV', \
                'standard_deviation_x', 'standard_deviation_y', 'standard_deviation_z', 'standard_deviation_A', 'standard_deviation_AV',  \
                'correlation_x_y', 'correlation_y_z', 'correlation_x_z', \
                'class', 'person_num']

windows = range(1, 52, 2)
times = []
f1_scores = []
for window in [int(sys.argv[1])]:
    #averaging_window = int(input('Enter size of window:\n'))
    averaging_window = window
    
    t0 = time.time()
    axises = ['x', 'y', 'z']
    fall_data = list()
    adl_data = list()


    dict_data = load('fall_data.npz')
    data = dict_data['arr_0']
    fall_data.append(data)

    x = averaging(fall_data[0][0], averaging_window)
    y = averaging(fall_data[0][1], averaging_window)
    z = averaging(fall_data[0][2], averaging_window)

    allA = list()
    allA.append(createA(x, y, z))
    allAV = list()
    allAV.append(createAV(x, y, z))

    # ----------- ADL
    dict_data = load('adl_data.npz')
    data = dict_data['arr_0']
    adl_data.append(data)

    x = averaging(adl_data[0][0], averaging_window)
    y = averaging(adl_data[0][1], averaging_window)
    z = averaging(adl_data[0][2], averaging_window)

    allA_adl = list()
    allA_adl.append(createA(x, y, z))
    allAV_adl = list()
    allAV_adl.append(createAV(x, y, z))

    samples_per_window = 100
    
    fall_result = list()
    for i in range(1):
        min_length = min(len(fall_data[i][0]), len(fall_data[i][1]), len(fall_data[i][2]))
        #print(min_length)
        for j in range(1, min_length, samples_per_window):
            try: 
                fall_result.append(createVector(fall_data, allA, allAV, i, j, 'Fall'))
            except:
                pass

    adl_result = list()
    for i in range(1):
        min_length = min(len(adl_data[i][0]), len(adl_data[i][1]), len(adl_data[i][2]))
        #print(min_length)
        for j in range(1, min_length, samples_per_window):
            adl_result.append(createVector(adl_data, allA_adl, allAV_adl, i, j, 'Adl'))

    fall = pd.DataFrame(fall_result, columns=column_names)
    adl = pd.DataFrame(adl_result, columns=column_names)
    data = pd.concat([fall, adl])
    
    t1 = time.time()
    print('[Window Size: '+str(averaging_window)+'] time:', t1-t0)

    data.to_pickle("./dataMatrix-"+str(averaging_window)+".pkl")
    
