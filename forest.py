from treeCreator import TreeCreator
import random
class Forest:

    def __init__(self, numOfTrees, trainingList, max_feat_select=2):
        self.trees = []
        self.TreeCreator = TreeCreator(len(trainingList[0].data), max_feat_select)
        self.trainingList = trainingList
        self.n_estimators = numOfTrees
        features = [i for i in range(len(self.trainingList[0].data))]
        bagged = self.bagging()
        for i in range(len(bagged)):
            # unused_features = features.copy()
            self.trees.append(self.TreeCreator.makeNode(bagged[i], features.copy(), 1, None, 1))
            print(i)
    
    def predict(self, testing_specimen_list):
        values = []
        for spec in testing_specimen_list:
            values.append(self.predict_one(spec))
        return values
    
    def predict_one(self, spec):
        numOfTrue = 0
        numOfFalse = 0
        for tree in self.trees:
            if tree.decide(spec):
                numOfTrue += 1
            else:
                numOfFalse += 1
        return numOfTrue > numOfFalse


    def bagging(self):
        bagged_samples = []
        for i in range(self.n_estimators):
            sample = []
            for j in range(len(self.trainingList)):
                sample.append(random.choice(self.trainingList))
            bagged_samples.append(sample)
        return bagged_samples