from treeCreator import treeCreator

class forest:
    trees = []
    treeCreate = treeCreator()
    def __init__(self, numOfTrees, specimenList):
        for i in range(numOfTrees):
            self.trees.append(self.treeCreate.makeNode(specimenList, [], 0, True))
            print(i, end='')

    def askForest(self, spec):
        numOfTrue = 0
        numOfFalse = 0
        for i in self.trees:
            if i.decide(spec):
                numOfTrue +=1
            else:
                numOfFalse +=1
        return True if numOfTrue >= numOfFalse else False
