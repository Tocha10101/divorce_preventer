from forest import Forest
from specimen import Specimen
import random


import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import argparse



parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Random Forest algorithm
------------------------------------------------------------------------''')

parser.add_argument('-nT', '--num_Trees', nargs='*', type=int,  default=[1, 1, 1, 2, 2, 2, 10, 10, 10, 50, 50, 50, 100],
                    help="defines how many trees will be in a forest \
                        accepts a list of arguments, for example -nT 10 10 10 50 50 \
                         will create 3 forests with 10 trees and 2 forests with 50 trees")

parser.add_argument('-mF', '--max_Feat', action='store', type=int, default=2,
                    help="defines how many features will be taken into \
                         consideration at each step while creating a tree node")
parser.add_argument('-nC', '--num_Chunks', action='store', type=int, default=5,
                    help='defines number chunk for cross validation')
args = parser.parse_args()

if __name__ == '__main__':
    inits = {
        'num_trees': args.num_Trees,
        'max_feat': args.max_Feat,
        'num_chunks': args.num_Chunks,
    }

""" Calculates forrest accuracy for a list of specimen"""
def accuracy(testing_specimen, predicted_specimen):
    good_choices = [1 for i in range(len(testing_specimen)) if testing_specimen[i].outCome == predicted_specimen[i].outCome]
    return sum(good_choices) / len(predicted_specimen)

"""Clears outcome values for a testing specimen list"""
def set_nulls(list_of_specimen):
    new_list = []
    for el in list_of_specimen:
        new_spec = Specimen(el.data, None)
        new_list.append(new_spec)
    return new_list

"""Creates a list of outcomes"""
def get_labels(specimen):
    lst = []
    for spec in specimen:
        lst.append(spec.outCome)
    return lst
"""Creates a labeled data set"""
def info_of_specimen(list_of_specimen, list_of_trains, list_of_tests, predicted_list):
    data = {}
    data['all_labels'] = get_labels(list_of_specimen)
    data['train_labels'] = get_labels(list_of_trains)
    data['test_labels'] = get_labels(list_of_trains)
    data['predicted_labels'] = get_labels(predicted_list)

    return data

"""Cross validation"""
def cross_valid_values(list_of_specimen, num_chunks, n_estimators):
    if (num_chunks <= 1):
        print("number of chunks has to be greater than 1")
        return -1
    scores = np.array([])
    loss = [0 for i in range(num_chunks)]   
    list_of_specimen = list(np.random.permutation(list_of_specimen))
    
    for i in range(num_chunks):
        
        # print(f"\nTest number {i}")
        begin, end = int(i * len(list_of_specimen) / num_chunks), int((i + 1) * len(list_of_specimen) / num_chunks)
        list_of_testing_specimen = list_of_specimen[begin:end].copy()
    

        testing_predictions = set_nulls(list_of_testing_specimen)
        list_of_training_specimen = list_of_specimen.copy()[:begin] + list_of_specimen.copy()[end:]
        
        classifier = Forest(n_estimators, list_of_training_specimen, max_feat_select=inits['max_feat'])
        testing_predictions = classifier.predict(testing_predictions)


        data = info_of_specimen(list_of_specimen, list_of_training_specimen, list_of_testing_specimen, testing_predictions)
        acc = accuracy(list_of_testing_specimen, testing_predictions)
        loss[i] = 1 - acc
        
        scores = np.append(scores, acc)
        avg_acc = sum(scores) / len(scores)
    return scores, avg_acc

"""Reads data"""
data = pd.read_csv('true_divorce_data.csv', index_col=0)
features, labels = data.loc[:, data.columns != 'Class'], data.loc[:, 'Class']

list_of_specimen = []
for index, row_val_series in features.iterrows():
    values = list(row_val_series)
    speciman = Specimen(values, bool(labels[index]))
    list_of_specimen.append(speciman)
"""Splits list into testing and training lists"""
train_X, test_X, train_y, test_y = train_test_split(features, labels, test_size=0.33)

"""Number of trees in a forest per test run"""
estimators = inits['num_trees']
"""Conduct tests"""
for el in estimators:
    cross_val = cross_valid_values(list_of_specimen, num_chunks=inits['num_chunks'], n_estimators=el)
    print(f"{el}: {cross_val}")
