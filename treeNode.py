from specimen import specimen
class treeNode:
    def __init__(self, checkedValue, threshold, isAnswer, answer, rightNode, leftNode):
        self.checkedValue = checkedValue
        self.threshold = threshold
        self.isAnswer = isAnswer
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.answer = answer





    def Decide(self, spec):
        if self.isAnswer:
            return self.answer
        else:
            return self.rightNode.Decide(spec) if spec.data[self.checkedValue] > self.threshold else self.leftNode.Decide(spec)
