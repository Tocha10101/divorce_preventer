"""
    Created by:             Jan Dzięgiel
    Date of creation:       29.05.2020
    Github:                 https://github.com/Vedir18
"""

import random

from specimen import Specimen
from treeNode import TreeNode

class TreeCreator():

    def __init__(self, max_feat_select=2):
        """
            An initializer for the Tree Creator

            :param max_feat_select:  a maximum number of features a tree can be build on
        """
        self.max_feat_select = max_feat_select


    
    def calculateGini(self, selectedFeature, threshold, specimenList):

        """
            A method to calculate the gini index for a given
            feature and threshold

            :param selectedFeature:     A given feature number
            :param threshold:           A given threshold for this feature
            :param specimenList:        A list of training examples in the given node

            :return:                    Returns a:  - Calculated GINI index for a specific feature and threshold
                                                    - Examples that has lower value Sfor the feature than threshold
                                                    - Examples that has lower value for the feature than threshold
            :rtype:                     tuple
            
        """

        leftTrues, rightTrues, leftFalse, rightFalse = 0, 0, 0, 0
        leftGini, rightGini = 1, 1
        for spec in specimenList:
            if spec.data[selectedFeature] <= threshold:
                if spec.outCome:
                    leftTrues += 1
                else:
                    leftFalse += 1
            else:
                if spec.outCome:
                    rightTrues += 1
                else:
                    rightFalse += 1

        if (leftTrues+leftFalse == 0) | (rightTrues + rightFalse == 0):
            nodeGini = 1
        else:
            leftGini = 1 - (leftTrues/(leftTrues+leftFalse))**2 - (leftFalse/(leftTrues+leftFalse))**2
            rightGini = 1 - (rightTrues/(rightTrues+rightFalse))**2 - (rightFalse/(rightTrues+rightFalse))**2

            nodeGini = ((rightFalse + rightTrues) * rightGini + (leftTrues + leftFalse) * leftGini) / (rightTrues + rightFalse + leftTrues + leftFalse)

        return nodeGini, leftTrues > leftFalse, rightTrues > rightFalse



    def chooseDescreteThreshold(self, selectedFeature, trainingList):

        """
            A function that chooses a threshold for the given feature
            by calculating the GINI index for each of them and chooses
            the one with the smallest index

            :param selectedFeature:     A selected feature for possible split
            :param trainingList:        A training list for the given node

            :return:                    A tuple of: - Best threshold for the given feature
                                                    - GINI index for the given feature and threshold
                                                    - The most possible assignment of the class for the examples in left child
                                                    - The most possible assignment of the class for the examples in right child
                                                    - The list of examples that go to the left child of current node
                                                    - The list of examples that go to the right child of current node

            :rtype:                     tuple
        """
        bestThreshold = -1
        bestGini = 1
        left_is_more_trues, right_is_more_trues = False, False
        trainingList.sort(key=lambda spec: spec.data[selectedFeature])

        values = set([el.data[selectedFeature] for el in trainingList])
        for item in values:
            if item != 4:
                tempThreshold = item
                tempGini, temp_left_more_trues, temp_right_more_trues = self.calculateGini(selectedFeature, tempThreshold, trainingList)
                if tempGini < bestGini:
                    bestThreshold = tempThreshold
                    bestGini = tempGini
                    left_is_more_trues, right_is_more_trues = temp_left_more_trues, temp_right_more_trues

        left_specimen, right_specimen = [], []
        for el in trainingList:
            if el.data[selectedFeature] <= bestThreshold:
                left_specimen.append(el)
            elif el.data[selectedFeature] > bestThreshold:
                right_specimen.append(el)

        return bestThreshold, bestGini, left_is_more_trues, right_is_more_trues, left_specimen, right_specimen


    def makeNode(self, training_list, unused_features, parent_gini, parent_ans):


        """

            Creates a leaf node of the tree or 
            runs recursively in order to creating a subtree

            :param training_list:       A list of training examples for the given node
            :param unused_features:     A list of unused features for this tree
            :param parant_gini:         A GINI index of the parent node
            :param parent_ans:          A class that is most likely to be assigned by the parent node


            :return:                    A new node
            :rtype:                     TreeNode

        """
    
        chosen_features = []
        for i in range(self.max_feat_select):
            choice = random.choice(unused_features)
            chosen_features.append(choice)
            unused_features.remove(choice)
        
        min_gini = parent_gini
        min_gini_elem = {}  
        for feature in chosen_features:
            element = {}
            element["feature"] = feature
            element['threshold'], element['gini'], element['is_left_more_trues'], \
            element['is_right_more_trues'], element['left_specimen'], \
                element['right_specimen'] = self.chooseDescreteThreshold(feature, training_list)
            if element['gini'] <= min_gini:
                min_gini = element['gini']
                min_gini_elem = element


        if 'feature' in min_gini_elem.keys():
            chosen_features.remove(min_gini_elem['feature'])
                
        for feature in chosen_features:
            unused_features.append(feature)

        if min_gini < parent_gini:
            left_child = self.makeNode(min_gini_elem['left_specimen'], unused_features.copy(), min_gini, min_gini_elem['is_left_more_trues'])
            right_child = self.makeNode(min_gini_elem['right_specimen'], unused_features.copy(), min_gini, min_gini_elem['is_right_more_trues'])
            return TreeNode(min_gini_elem['feature'], min_gini_elem['threshold'], False, parent_ans, left_child, right_child)
        else:
            return TreeNode(None, None, True, parent_ans, None, None)
    
