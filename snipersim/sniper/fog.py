import sys
import pandas as pd
from decisionTree import *
for window in [int(sys.argv[1])]:
    data = pd.read_pickle("./dataMatrix-"+str(window)+".pkl")
    X = data[['average_x', 'average_y', 'average_z', 'average_A','average_AV', \
            'maximum_x','maximum_y', 'maximum_z', 'maximum_A', 'maximum_AV', \
            'minimum_x', 'minimum_y', 'miminum_z', 'minimum_A', 'minimum_AV', \
            'energy_x', 'energy_y', 'energy_z', 'energy_A', 'energy_AV', \
            'spectral_energy_x', 'spectral_energy_y', 'spectral_energy_z', 'spectral_energy_A', 'spectral_energy_AV', \
            'standard_deviation_x', 'standard_deviation_y', 'standard_deviation_z', 'standard_deviation_A', 'standard_deviation_AV',  \
            'correlation_x_y', 'correlation_y_z', 'correlation_x_z']]
    Y = data['class']
    x_train, x_test, y_train, y_test = custom_train_test_split(X.values, Y.values, len(X), len(Y), test_size=0.2, random_state=42)
    clf = DecisionTreeClassifier(max_depth=100)
    m = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    t=y_test
    p=y_pred
    acc = np.mean(np.equal(t,p))
    right = np.sum(t*p == 1)
    precision = right / float(np.sum(p))
    recall = right / float(np.sum(t))
    f1 = 2* precision*recall/float(precision+recall)
    print('[Window Size: '+str(window)+'] F1: ', f1)
