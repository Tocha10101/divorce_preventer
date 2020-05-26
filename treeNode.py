from specimen import Specimen

class TreeNode:

    def __init__(self, selectedFeature, threshold, isLeaf, assigned_class, rightNode=None, leftNode=None):
        self.selectedFeature = selectedFeature
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.assigned_class = assigned_class

    def decide(self, spec):
        if self.isLeaf:
            return self.assigned_class
        else:
            return self.rightNode.decide(spec) if spec.data[self.selectedFeature] > self.threshold else self.leftNode.decide(spec)