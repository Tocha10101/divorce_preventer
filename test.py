"""
    Created by:         Anton Masiukevich
    Date of creation:   01.06.2020
    Github:             https://github.com/amasiukevich
"""

import random
import pandas as pd
import numpy as np
import argparse

from forest import Forest
from specimen import Specimen

"""
    Parsing command line arguments part
"""
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Random Forest algorithm
------------------------------------------------------------------------''')

parser.add_argument('-nT', '--num_Trees', nargs='*', type=int,  default=[1, 2, 3, 5, 10, 20, 35, 50, 100],
                    help="defines how many trees will be in a forest \
                        accepts a list of arguments, for example -nT 10 10 10 50 50 \
                         will create 3 forests with 10 trees and 2 forests with 50 trees")

parser.add_argument('-mF', '--max_Feat', action='store', type=int, default=[2, 4, 6, 8, 10],
                    help="defines how many features will be taken into \
                         consideration at each step while creating a tree node")
parser.add_argument('-nC', '--num_Chunks', action='store', type=int, default=[2, 3, 5, 8, 10, 15, 20, 35, 50],
                    help='defines number chunk for cross validation')
args = parser.parse_args()



def accuracy(testing_specimen, predicted_specimen):
    
    """
        A simple function to calculate the accuracy of the model
        :param testing_specimen:        a list of examples for test
        :param predicted_specimen:      a list of predicted by the model examples

        :return:    the accuracy of the model
        :rtype:     int 
    """

    good_choices = [1 for i in range(len(testing_specimen)) if testing_specimen[i].outCome == predicted_specimen[i].outCome]
    return sum(good_choices) / len(predicted_specimen)



def cross_valid_values(list_of_specimen, num_chunks, n_estimators, max_features_select):
    """
        A function to perform cross validation of the model

        :param list_of_specimen:        a list of training examples
        :param num_chunks:              a K number in K-fold cross validation
        :param n_estimators:            a number of trees in RF
        :param max_features_select:     a number of features per tree

        :return:                    an mean accuracy of the model
        :rtype:                     int
    """


    if (num_chunks <= 1):
        print("number of chunks has to be greater than 1")
        return -1
    scores = np.array([])
    loss = [0 for i in range(num_chunks)]   
    list_of_specimen = list(np.random.permutation(list_of_specimen))
    
    for i in range(num_chunks):
        
        begin, end = int(i * len(list_of_specimen) / num_chunks), int((i + 1) * len(list_of_specimen) / num_chunks)
        list_of_testing_specimen = list_of_specimen[begin:end].copy()
    
        testing_predictions = list_of_testing_specimen

        list_of_training_specimen = list_of_specimen.copy()[:begin] + list_of_specimen.copy()[end:]
        
        classifier = Forest(n_estimators, list_of_training_specimen, max_feat_select=max_features_select)
        testing_predictions = classifier.predict(testing_predictions)

        acc = accuracy(list_of_testing_specimen, testing_predictions)
        loss[i] = 1 - acc
        
        scores = np.append(scores, acc)
        avg_acc = sum(scores) / len(scores)
    return avg_acc


def read_data(csv_filename):

    """
        A utility function to read the data and return a list of training examples

        :param csv_filename:    a path to the data
        
        :return:                list of training examples
        :rtype:                 list
    """
    data = pd.read_csv(csv_filename)
    features, labels = data.loc[:, data.columns != 'Class'], data.loc[:, 'Class']

    list_of_specimen = []
    
    for index, row_val_series in features.iterrows():
        values = list(row_val_series)
        speciman = Specimen(values, bool(labels[index]))
        list_of_specimen.append(speciman)

    return list_of_specimen



list_of_specimen = read_data('true_divorce_data.csv')


def test_estimators(list_of_estimators):

    """
        A testing function to check the change of accuracy
        while changing the number of estimators

        :param list_of_estimators:      a list of quantities of trees
     
    """

    for el in list_of_estimators:
        cross_val = cross_valid_values(list_of_specimen, num_chunks=10, n_estimators=el, max_features_select=2)
        print(f"Trees: {el} Accuracy: {cross_val}")


def test_chunks(list_of_chunks):

    """
        A testing functions to check the change of accuracy
        while changing the K number in K-fold cross validation

        :param list_of_chunks:          a list of K numbers for K-fold cross validation
    """
    for el in list_of_chunks:
        cross_val = cross_valid_values(list_of_specimen, num_chunks=el, n_estimators=10, max_features_select=2)
        print(f"N_chunks: {el} Accuracy: {cross_val}")



def test_max_features(list_of_mf):

    """
        A testing function to checkt the change of accuracy
        while changing the maximum number of features to select

        :param list_of_mf:              a list of numbers of features to select

    """

    for el in list_of_mf:
        cross_val = cross_valid_values(list_of_specimen, num_chunks=10, n_estimators=10, max_features_select=2)
        print(f"Selected_features: {el} Accuracy: {cross_val}")



if __name__ == '__main__':

    inits = {
        'num_trees': args.num_Trees,
        'max_features': args.max_Feat,
        'num_chunks': args.num_Chunks,
    }

    test_estimators(inits['num_trees'])
    test_chunks(inits['num_chunks'])
    test_max_features(inits['max_features'])