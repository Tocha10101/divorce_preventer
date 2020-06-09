"""
    Created by:         Jan Dzięgiel
    Date of creation:   29.05.2020
    Github:             https://github.com/Vedir18

"""

from specimen import Specimen

class TreeNode:

    """
        A class that represents a tree node
    """

    def __init__(self, selectedFeature, threshold, isLeaf, node_answer, leftNode=None, rightNode=None):

        """
            An initializer of the constructor

            :param selectedFeature:     A feature for which the split is performed
            :param threshold:           A boundary on which we split training examples
            :param isLeaf:              Tells if the node is leaf
            :param rightNode:           A link to a right child of the node
            :param leftNode:            A link to a left child of the node
            :param node_answer:         A decision the node give on testing example if the node is a leaf
        """
        self.selectedFeature = selectedFeature
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.node_answer = node_answer

    def decide(self, spec):

        """
            A method that performs the decision of a tree in case the node is a leaf

            :param:     testing example for which we should predict a class

            :return:    a class assigned
            :rtype:     bool
        """
        if self.isLeaf:
            return self.node_answer
        else:
            return self.rightNode.decide(spec) if spec.data[self.selectedFeature] > self.threshold else self.leftNode.decide(spec)