from specimen import Specimen
from treeNode import TreeNode
import random
from operator import itemgetter
from collections import Counter


class TreeCreator:

    def __init__(self, n_features, max_feat_select=2):
        self.max_feat_select = max_feat_select
        self.n_features = n_features

    def calculateGini(self, selectedFeature, threshold, specimenList, wanna_print=False):
        leftTrues, rightTrues, leftFalse, rightFalse = 0, 0, 0, 0
        leftGini, rightGini = 1, 1
        for spec in specimenList:
            if spec.data[selectedFeature] < threshold:
                if spec.outCome:
                    leftTrues += 1
                else:
                    leftFalse += 1
            else:
                if spec.outCome:
                    rightTrues += 1
                else:
                    rightFalse += 1

        if wanna_print:
            self.print_division(leftTrues, leftFalse, rightTrues, rightFalse)
        

        try:
            leftGini = 1 - (leftTrues/(leftTrues+leftFalse))**2 - (leftFalse/(leftTrues+leftFalse))**2
        except:
            pass
            #print(f"leftGini LF {leftFalse} LT {leftTrues} RF {rightFalse} RT {rightTrues} Threshold = {threshold}")
        try:
            rightGini = 1 - (rightTrues/(rightTrues+rightFalse))**2 - (rightFalse/(rightTrues+rightFalse))**2
        except:
            pass
            # print(f"rightGini LF {leftFalse} LT {leftTrues} RF {rightFalse} RT {rightTrues} Threshold= {threshold}")
        nodeGini = ((rightFalse + rightTrues) * rightGini + (leftTrues + leftFalse) * leftGini) / (rightTrues + rightFalse + leftTrues + leftFalse)
        return nodeGini, leftTrues > leftFalse, rightTrues > rightFalse

    def print_division(self, left_t, left_f, right_t, right_f):
        print(f"LT: {left_t}, LF: {left_f}, RT: {right_t}, RF: {right_f}")


    def chooseDescreteThreshold(self, selectedFeature, trainingList, omen=False):
        bestThreshold = -1
        bestGini = 1
        left_is_more_trues, right_is_more_trues = False, False
        trainingList.sort(key=lambda spec: spec.data[selectedFeature])

        values = dict(Counter(el.data[selectedFeature] for el in trainingList))
        # gets the frequency of values in particular column
        # for number, freq in values.items():
        #     tempThreshold = number
        #     tempGini, temp_left_more_values, temp_right_more_values = self.calculateGini(selectedFeature, tempThreshold, trainingList)
        #     if tempGini < bestGini
        # values = set([el.data[selectedFeature] for el in trainingList])
        for item in values.keys():
            tempThreshold = item
            tempGini, temp_left_more_trues, temp_right_more_trues = self.calculateGini(selectedFeature, tempThreshold, trainingList)
            if tempGini < bestGini:
                bestThreshold = tempThreshold
                bestGini = tempGini
                left_is_more_trues, right_is_more_trues = temp_left_more_trues, temp_right_more_trues

        # print division for bestThreshold
        # self.calculateGini(selectedFeature, bestThreshold, trainingList, wanna_print=omen)

        left_specimen, right_specimen = [], []
        for el in trainingList:
            if el.data[selectedFeature] <= bestThreshold:
                left_specimen.append(el)
            elif el.data[selectedFeature] > bestThreshold:
                right_specimen.append(el)

        return bestThreshold, bestGini, left_is_more_trues, right_is_more_trues, left_specimen, right_specimen

    def makeNode(self, training_list, unused_features, parent_gini, parent_ans, current_node_depth):
    
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

        # print(f"Depth: {current_node_depth}")

        # returning unused features back to the pool
        # kostyl
        if 'feature' in min_gini_elem.keys():
            chosen_features.remove(min_gini_elem['feature'])
                
        for feature in chosen_features:
            unused_features.append(feature)

        if min_gini < parent_gini:
            left_child = self.makeNode(min_gini_elem['left_specimen'], unused_features.copy(), min_gini, parent_ans, current_node_depth + 1)
            right_child = self.makeNode(min_gini_elem['right_specimen'], unused_features.copy(), min_gini, parent_ans, current_node_depth + 1)
            return TreeNode(min_gini_elem['feature'], min_gini_elem['threshold'], False, parent_ans, left_child, right_child)
        else:
            return TreeNode(None, None, True, parent_ans, None, None)
    
        # if min_gini > parent_gini and parent_ans != None:
        #     return TreeNode(None, None, True, parent_ans, None, None) # leaf
        # elif current_node_depth >= self.n_features - self.max_feat_select:
        #     return TreeNode(None, None, True, parent_ans, None, None)
        # elif min_gini == parent_gini:
        # else:
        #     try:
        #         left_child = self.makeNode(min_gini_elem['left_specimen'], unused_features.copy(), min_gini, parent_ans, current_node_depth + 1)
        #         right_child = self.makeNode(min_gini_elem['right_specimen'], unused_features.copy(), min_gini, parent_ans, current_node_depth + 1)
        #         return TreeNode(min_gini_elem['feature'], min_gini_elem['threshold'], False, parent_ans, left_child, right_child)
        #     except:
        #         print(current_node_depth)
        #         breakpoint()