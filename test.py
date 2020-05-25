from forest import forest
from specimen import specimen
import random

specimenList = []
for i in range(5):
    data = []
    for j in range(3):
        data.append(random.randrange(10))
        #data.append(random.randrange(200))

   # print(data)

    rand = True
    spec = specimen(data, rand)
    print(spec.data, spec.outCome)
    specimenList.append(spec)

for i in range(5):
    data = []
    for j in range(3):
        data.append(random.randrange(10)+10)
        #data.append(random.randrange(200))

   # print(data)

    rand = False
    spec = specimen(data, rand)

    specimenList.append(spec)
    print(spec.data, spec.outCome)

testForest = forest(10, specimenList)

print(testForest.askForest([1, 2, 3]))
