from specimen import Specimen

class TreeNode:

    def __init__(self, selectedFeature, threshold, isLeaf, node_answer, leftNode=None, rightNode=None):
        self.selectedFeature = selectedFeature
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.node_answer = node_answer

    """Returns a decision of a tree"""
    def decide(self, spec):
        if self.isLeaf:
            return self.node_answer
        else:
            return self.rightNode.decide(spec) if spec.data[self.selectedFeature] > self.threshold else self.leftNode.decide(spec)