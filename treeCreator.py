from specimen import specimen
from treeNode import treeNode
import random
from operator import itemgetter

class treeCreator:
    def calculateGini(self, checkedValue, threshold,  specimenList):
        leftTrues, rightTrues, leftFalse, rightFalse = 0, 0, 0, 0
        leftGini, rightGini = 0, 0
        for spec in specimenList:
            breakpoint()
            if spec.data[checkedValue] < threshold:
                if spec.outCome:
                    leftTrues += 1
                else:
                    leftFalse += 1
            else:
                if spec.outCome:
                    rightTrues += 1
                else:
                    rightFalse +=1

        try:
            leftGini = 1 - (leftTrues/(leftTrues+leftFalse))**2 - (leftFalse/(leftTrues+leftFalse))**2
        except:
            print(f"leftGini LF {leftFalse} LT {leftTrues} RF {rightFalse} RT {rightTrues}")
        try:
            rightGini = 1 - (rightTrues/(rightTrues+rightFalse))**2 - (rightFalse/(rightTrues+rightFalse))**2
        except:
            print(f"rightGini LF {leftFalse} LT {leftTrues} RF {rightFalse} RT {rightTrues}")
        nodeGini = ((rightFalse+rightTrues)*rightGini + (leftTrues+leftFalse)*leftGini)/(rightTrues+rightFalse+leftTrues+leftFalse)
        return nodeGini, leftTrues>leftFalse, rightTrues>rightFalse

    def chooseThreshold(self, checkedValue, specimenList):
        bestThreshold = 0
        bestGini = 0
        leftAns, rightAns = False, False
        specimenList.sort(key=lambda spec: spec.data[checkedValue])

        for i in range(len(specimenList)-1):
            tempThreshold = specimenList[i].data[checkedValue]+specimenList[i+1].data[checkedValue]
            tempGini, tempLeftAns, tempRightAns = self.calculateGini(checkedValue, tempThreshold, specimenList)
            if  tempGini > bestGini:
                bestThreshold = tempThreshold
                bestGini = tempGini
                leftAns, rightAns = tempLeftAns, tempRightAns
        return bestThreshold, bestGini, leftAns, rightAns

    def makeNode(self, specimenList, usedValuesList, parentGini, parentAns):
        variableA = 0
        variableB = 0
        cantUseVal = True
        while(cantUseVal):
            variableA = random.randrange(len(specimenList[0].data))
            if (usedValuesList.count(variableA) < 1):
                cantUseVal = False
            else:
                cantUseVal = True

        cantUseVal = True
        while(cantUseVal):
            variableB = random.randrange(len(specimenList[0].data))
            if (usedValuesList.count(variableB) < 1 and variableB != variableA):
                cantUseVal = False
            else:
                cantUseVal = True

        thresholdA, giniA, leftAnswerA, rightAnswerA = self.chooseThreshold(variableA, specimenList)
        thresholdB, giniB, leftAnswerB, rightAnswerB = self.chooseThreshold(variableB, specimenList)

        checkedValue = variableA if giniA > giniB else variableB
        threshold = thresholdA if giniA > giniB else  thresholdB
        bestGini = giniA if giniA > giniB else giniB
        leftAnswer = leftAnswerA if giniA > giniB else leftAnswerB
        rightAnswer = rightAnswerA if giniA > giniB else rightAnswerB


        if bestGini < parentGini:
            return treeNode(checkedValue, threshold, True, parentAns, None, None)
        else:
            usedValuesList.append(checkedValue)
            leftChild = self.makeNode(specimenList, usedValuesList, bestGini, leftAnswer)
            rightChild = self.makeNode(specimenList, usedValuesList, bestGini, rightAnswer)
            return treeNode(checkedValue, threshold, False, parentAns, leftChild, rightChild)











