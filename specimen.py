"""
    Created By:         Jan Dzięgiel
    Date of creation:   29.05.2020
    Github:             https://github.com/Vedir18
"""

class Specimen():

    """
        A class that represents a single training example
    """

    def __init__(self, givenData=[], givenOutcome=False):

        """
            An initializer for the Specimen class

            :param givenData:       a list of the features
            :param givenOutcome:    a class of the training example
        """

        self.data = givenData
        self.outCome = givenOutcome
