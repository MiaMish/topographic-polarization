import numpy as np


class Population:

    def __init__(self, config):
        self.config = config

        self.traits = np.random.uniform(-1, 1, [self.config.popSize, self.config.propNum])

        self.traitWeights = np.full((self.config.popSize, self.config.propNum), 0.1)
        for i in range(self.config.popSize):
            self.traitWeights[i, np.random.randint(0, self.config.propNum)] = 1

        self.trustWeightsYes = np.full((self.config.popSize, self.config.propNum), 0)
        self.trustWeightsNo = np.full((self.config.popSize, self.config.propNum), 10)
