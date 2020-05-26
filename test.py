from forest import Forest
from specimen import Specimen
import random


import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

def accuracy(testing_specimen, predicted):
    good_choices = [1 for i in range(len(testing_specimen)) if testing_specimen[i].outCome == predicted[i]]
    return sum(good_choices) / len(predicted)


data = pd.read_csv('true_divorce_data.csv', index_col=0)
features, labels = data.loc[:, data.columns != 'Class'], data.loc[:, 'Class']

train_X, test_X, train_y, test_y = train_test_split(features, labels, test_size=0.33)

list_of_training_specimen = []

for index, row_val_series in train_X.iterrows():
    values = list(row_val_series)
    speciman = Specimen(values, bool(train_y[index]))
    list_of_training_specimen.append(speciman)

training_trues = sum([1 for spec in list_of_training_specimen if spec.outCome == True])
training_falses = len(list_of_training_specimen) - training_trues
print(training_trues, training_falses)
    
list_of_testing_specimen = []
for index, row_val_series in test_X.iterrows():
    values = list(row_val_series)
    speciman = Specimen(values, bool(test_y[index]))
    list_of_testing_specimen.append(speciman)

print("I'm here")

RFC = Forest(100, list_of_training_specimen)

# RFC.show()

predicted = RFC.predict(list_of_testing_specimen)

acc = accuracy(list_of_testing_specimen, predicted)
print(acc)