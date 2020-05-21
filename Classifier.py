import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
from operator import itemgetter


class MyRFClassifier():
    
    def __init__(self, random_state, n_estimators=100, criterion='gini', min_samples_split=2,\
                 max_tree_depth=None, max_features='auto', bootstrap=True, n_chosen_indexes=100):
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.min_samples_split = min_samples_split
        self.max_tree_depth = max_tree_depth
        self.bootstrap = bootstrap
        self.n_chosen_indexes = n_chosen_indexes
        
        self.trees = []
        
    def fit(self, train_X, train_y):
        
        for el in range(self.n_estimators):
            
            # bootstrap stuff
            indexes_chosen = self.bagging(train_X, train_y)
            
            chunk_X, chunk_y = train_X.loc[train_X.index.isin(indexes_chosen)], train_y.loc[train_y.index.isin(indexes_chosen)]
            
            # build a tree based on this data
            tree = DecisionTreeClassifier(random_state=0) # change it later for your own implementation
            tree.fit(chunk_X, chunk_y)
            self.trees.append(tree)
            
            
    def bagging(self, train_X, train_y):
        indexes_chosen = set()
        for el in train_X.index:
            if len(indexes_chosen) != self.n_chosen_indexes:
                item = random.choice(train_X.index)
                indexes_chosen.add(item)
        return list(indexes_chosen)

    def predict(self, test_X):
        predicted_by_every_tree = []
        for tree in self.trees:
            predicted_answers = tree.predict(test_X)
            predicted_by_every_tree.append(predicted_answers)
        
        forest_prediction = []
        all_votes = [{cls: 0 for cls in set(predicted_by_every_tree[0])} for j in range(len(test_X))]
        
        for i in range(len(predicted_by_every_tree[0])):
            for j in range(len(predicted_by_every_tree)):
                value = predicted_by_every_tree[j][i]
                if value in all_votes[i].keys():
                    all_votes[i][value] += 1
                else:
                    all_votes[i][value] = 1
                
        forest_prediction = [max(dic.items(), key=itemgetter(1))[0] for dic in all_votes]
        return forest_prediction


divorce_data = pd.read_csv('divorce_data.csv', index_col=0)
features, labels = divorce_data.loc[:, divorce_data.columns != "Class"], pd.Series([int(i) for i in divorce_data.loc[:, 'Class']])
train_X, test_X, train_y, test_y = train_test_split(features, labels)


def cross_val_scores(classifier, features, labels, num_chunks):
    
    scores = np.array([])
    loss = [0 for i in range(num_chunks)]
    
    for i in range(num_chunks):
        
        begin, end = int(i * len(features) / num_chunks), int((i + 1) * len(features) / num_chunks)
        test_X, test_y = features[begin: end], labels[begin: end]
        tr_X = pd.concat([features.loc[features.index < begin], features.loc[features.index >= end]])
        tr_y = pd.concat([labels.loc[labels.index < begin], labels.loc[labels.index >= end]])
        
        classifier.fit(tr_X, tr_y)
        pred = classifier.predict(test_X)
        acc = accuracy_score(test_y, pred)
        loss[i] = 1 - acc
        
        scores = np.append(scores, acc)
        
    return scores, sum(loss) / len(loss)

trees_data  = [2, 5, 10, 50, 100]
for n_trees in trees_data:
    clf = MyRFClassifier(random_state=0, n_estimators=n_trees)
    scores = cross_val_scores(clf, features, labels, 17)
    print(f"Num of trees: {n_trees}, Error_score: {scores[1]}")
