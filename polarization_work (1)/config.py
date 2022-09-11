import os


class Config:

    def __init__(self):
        # property number
        self.propNum = 5

        # population size
        self.popSize = 40

        # simulation iter count
        self.iterCount = 1000

        # std when chosing weights from traits
        self.std = 0.1

        # threshold for successful interaction
        self.successThreshold = 0.3

        self.attractScale = 0
        self.repulseScale = 1

        # step size of unsuccesful interactions
        self.stepSize = 0.1

        self.clusterThreshold = 0.1

        self.probRandPartner = 0

        self.breakTies = False

        self.verbose = False

        self.weightedSteps = False

        self.withBoundaries = True

        self.outOfBoundsFriction = 0

        self.interactionWeightedSelection = False;
        self.interactionWeightPower = 0.1

        self.learnInteractionTrust = False
        self.logFile = None
        self.ppThreshold = 0.9

    def deleteLog(self):
        if os.path.exists(self.logFile):
            os.remove(self.logFile)

    def printTitles(self):
        f = open(self.logFile, "a")
        f.write("T, N, p, WithLearning, Std");
        f.close()

    def printContent(self):
        f = open(self.logFile, "a")
        f.write(f'{self.propNum},{self.popSize},{self.probRandPartner},{self.learnInteractionTrust},{self.std}');
        f.close()

    def printEol(self):
        f = open(self.logFile, "a")
        f.write("\n");
        f.close()

    def __str__(self):
        res = ""
        res += "Property-number:" + str(self.propNum) + " Population-size:" + str(self.popSize) + "\n"
        res += "Iter-count:" + str(self.iterCount)
        res += "Cluster-threshold:" + str(self.clusterThreshold) + "\n"
        res += "Weighted-steps:" + str(self.weightedSteps) + "\n"
        return res;
