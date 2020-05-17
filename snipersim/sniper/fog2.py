import time
import numpy as np
import pandas as pd
import sys
from scipy.fftpack import fft

from decisionTree import *

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

for window in [int(sys.argv[1])]:
    fall_data = list()
    adl_data = list()


    dict_data = load('fall_data-denoised-'+str(window)+'.npz')
    data = dict_data['arr_0']
    fall_data.append(data)

    x = fall_data[0][0]
    y = fall_data[0][1]
    z = fall_data[0][2]

    allA = list()
    allA.append(createA(x, y, z))
    allAV = list()
    allAV.append(createAV(x, y, z))

    #### ADL
    dict_data = load('adl_data-denoised-'+str(window)+'.npz')
    data = dict_data['arr_0']
    adl_data.append(data)

    x = adl_data[0][0]
    y = adl_data[0][1]
    z = adl_data[0][2]

    allA_adl = list()
    allA_adl.append(createA(x, y, z))
    allAV_adl = list()
    allAV_adl.append(createAV(x, y, z))

    # feature extraction

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

    X = data[['average_x', 'average_y', 'average_z', 'average_A','average_AV', \
            'maximum_x','maximum_y', 'maximum_z', 'maximum_A', 'maximum_AV', \
            'minimum_x', 'minimum_y', 'miminum_z', 'minimum_A', 'minimum_AV', \
            'energy_x', 'energy_y', 'energy_z', 'energy_A', 'energy_AV', \
            'spectral_energy_x', 'spectral_energy_y', 'spectral_energy_z', 'spectral_energy_A', 'spectral_energy_AV', \
            'standard_deviation_x', 'standard_deviation_y', 'standard_deviation_z', 'standard_deviation_A', 'standard_deviation_AV',  \
            'correlation_x_y', 'correlation_y_z', 'correlation_x_z']]

    Y = data['class']

    # test the ML performance
    m = {'col': 0, 'index_col': 0, 'cutoff': 11.048341762258147, 'val': 1.0, 'left': {'col': 2, 'index_col': 2, 'cutoff': 9.0643857917409232, 'val': 0.0, 'left': {'col': 4, 'index_col': 4, 'cutoff': 951672.69105738285, 'val': 0.0, 'left': {'val': 0}, 'right': {'col': 1, 'index_col': 1, 'cutoff': 13.1013455777057, 'val': 0.0, 'left': {'col': 20, 'index_col': 20, 'cutoff': 15.554957925055682, 'val': 1.0, 'left': {'col': 8, 'index_col': 8, 'cutoff': 9.5575089703950837, 'val': 1.0, 'left': {'val': 1}, 'right': {'val': 0}}, 'right': {'col': 31, 'index_col': 31, 'cutoff': -0.17871646257296922, 'val': 0.0, 'left': {'val': 1}, 'right': {'val': 0}}}, 'right': {'col': 13, 'index_col': 13, 'cutoff': 26.444013343471664, 'val': 0.0, 'left': {'col': 1, 'index_col': 1, 'cutoff': 22.191074762018577, 'val': 0.0, 'left': {'col': 14, 'index_col': 14, 'cutoff': 3.2918757255105504, 'val': 0.0, 'left': {'val': 1}, 'right': {'col': 17, 'index_col': 17, 'cutoff': 0.30646039944166226, 'val': 0.0, 'left': {'val': 1}, 'right': {'col': 20, 'index_col': 20, 'cutoff': 14.917935009232263, 'val': 0.0, 'left': {'col': 24, 'index_col': 24, 'cutoff': 88.553457980561745, 'val': 0.0, 'left': {'col': 24, 'index_col': 24, 'cutoff': 88.478191676633202, 'val': 1.0, 'left': {'val': 0}, 'right': {'val': 1}}, 'right': {'col': 22, 'index_col': 22, 'cutoff': 3851883.3904822837, 'val': 0.0, 'left': {'col': 13, 'index_col': 13, 'cutoff': 21.931202470605601, 'val': 0.0, 'left': {'col': 6, 'index_col': 6, 'cutoff': 10.033256478579409, 'val': 0.0, 'left': {'col': 22, 'index_col': 22, 'cutoff': 3003665.5342299356, 'val': 0.0, 'left': {'col': 6, 'index_col': 6, 'cutoff': 9.6170531929453151, 'val': 1.0, 'left': {'val': 1}, 'right': {'val': 0}}, 'right': {'val': 0}}, 'right': {'col': 31, 'index_col': 31, 'cutoff': -0.025479427267783065, 'val': 1.0, 'left': {'val': 0}, 'right': {'col': 17, 'index_col': 17, 'cutoff': 1.7350989582257961, 'val': 1.0, 'left': {'col': 0, 'index_col': 0, 'cutoff': 10.321569909993546, 'val': 0.0, 'left': {'val': 1}, 'right': {'val': 0}}, 'right': {'val': 1}}}}, 'right': {'val': 0}}, 'right': {'val': 1}}}, 'right': {'col': 0, 'index_col': 0, 'cutoff': 9.842614390162467, 'val': 0.0, 'left': {'val': 1}, 'right': {'val': 0}}}}}, 'right': {'col': 5, 'index_col': 5, 'cutoff': 5.3560110411437609, 'val': 0.0, 'left': {'val': 0}, 'right': {'col': 0, 'index_col': 0, 'cutoff': 11.021520849531123, 'val': 0.0, 'left': {'val': 1}, 'right': {'val': 0}}}}, 'right': {'col': 20, 'index_col': 20, 'cutoff': 12.161316610020712, 'val': 1.0, 'left': {'val': 1}, 'right': {'col': 6, 'index_col': 6, 'cutoff': 11.945842139046167, 'val': 0.0, 'left': {'val': 0}, 'right': {'val': 1}}}}}}, 'right': {'col': 2, 'index_col': 2, 'cutoff': 9.5974464813153482, 'val': 1.0, 'left': {'col': 31, 'index_col': 31, 'cutoff': 0.23692746399936709, 'val': 1.0, 'left': {'col': 10, 'index_col': 10, 'cutoff': 949064.22228738351, 'val': 1.0, 'left': {'col': 0, 'index_col': 0, 'cutoff': 10.056415465491019, 'val': 0.0, 'left': {'val': 1}, 'right': {'val': 0}}, 'right': {'val': 1}}, 'right': {'col': 2, 'index_col': 2, 'cutoff': 9.4227323664635616, 'val': 0.0, 'left': {'val': 0}, 'right': {'val': 1}}}, 'right': {'val': 0}}}, 'right': {'col': 31, 'index_col': 31, 'cutoff': -0.34750862492373569, 'val': 1.0, 'left': {'val': 0}, 'right': {'val': 1}}}
    x_train, x_test, y_train, y_test = custom_train_test_split(X.values, Y.values, len(X), len(Y), test_size=0.2, random_state=42)
    clf = DecisionTreeClassifier(max_depth=100)
    clf.set_tree(m)

    y_pred = clf.predict(x_test)
    t=y_test
    p=y_pred
    acc = np.mean(np.equal(t,p))
    right = np.sum(t*p == 1)
    precision = right / float(np.sum(p))
    recall = right / float(np.sum(t))
    f1 = 2* precision*recall/float(precision+recall)
    print('[Window Size: '+str(window)+'] F1: ', f1)


