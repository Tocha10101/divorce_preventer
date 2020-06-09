"""
    Created by:                     Jan Dzięgiel, Anton Masiukevich
    Date of creation:               29.05.2020
    Date of the last modification:  08.06.2020
    Github:                         https://github.com/Vedir18, https://github.com/amasiuke
"""

import random

from treeCreator import TreeCreator
from specimen import Specimen

class Forest():

    """
        A class to represent a forest
    """

    def __init__(self, numOfTrees, trainingList, max_feat_select=2):

        """
            A forest initializer

            :param numOfTrees:      A number of trees in forest
            :param trainingList:    A list of training examples
            :param max_feat_select: A maximum number of features a single tree can use
        
        """

        self.trees = []
        self.TreeCreator = TreeCreator(max_feat_select)
        self.trainingList = trainingList
        self.n_estimators = numOfTrees
        features = [i for i in range(len(self.trainingList[0].data))]
        bagged = self.bagging()

        for i in range(len(bagged)):
            self.trees.append(self.TreeCreator.makeNode(bagged[i], features.copy(), 1, None))
    
    
    def predict(self, testing_specimen_list):

        """
            A method returns a prediction foe a whole list
            of testing examples

            :param testing_specimen_list:   A list of examples to predict

            :return:                        A list of predicted examples
            :rtype:                         list
        """
        values = []
        for spec in testing_specimen_list:
            values.append(self.predict_one(spec))
        return values

    def predict_one(self, spec):

        """
            A utility function to performs a prediction
            for a single specimen

            :param spec:    A single training example for which we make the prediction

            :return:        Same example with modified (when predicting) class
            :rtype:         Specimen
         """
        numOfTrue = 0
        numOfFalse = 0
        for tree in self.trees:
            if tree.decide(spec):
                numOfTrue += 1
            else:
                numOfFalse += 1
        predicted_spec = Specimen(spec.data, numOfTrue > numOfFalse)
        return predicted_spec


    def bagging(self):

        """
            Bags the data to be used for creating trees
        
            :return:    list of lists of training examples
            :rtype:     list
        """
        bagged_samples = []
        for i in range(self.n_estimators):
            sample = []
            for j in range(len(self.trainingList)):
                sample.append(random.choice(self.trainingList))
            bagged_samples.append(sample)
        return bagged_samples