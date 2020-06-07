from specimen import Specimen

class TreeNode:

    def __init__(self, selectedFeature, threshold, isLeaf, node_answer, rightNode=None, leftNode=None):
        self.selectedFeature = selectedFeature
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.node_answer = node_answer

    def decide(self, spec):
        if self.isLeaf:
            return False if self.node_answer else True
        else:
            return self.rightNode.decide(spec) if spec.data[self.selectedFeature] > self.threshold else self.leftNode.decide(spec)