import time

import numpy as np
from config import Config
from simulator import Simulator
from measurements import Measurements
import numpy

cfg = Config()

cfg.verbose = False
cfg.std = 0.01
cfg.popSize = 40
cfg.propNum = 5

cfg.attractScale = 0
cfg.repulseScale = 1
cfg.breakTies = False
cfg.withBoundaries = True
cfg.outOfBoundsFriction = 0

cfg.probRandPartner = 0
cfg.interactionWeightedSelection = False
cfg.interactionWeightPower = 0.1
cfg.learnInteractionTrust = False
cfg.logFile = "output/res.txt"

fullRun = True
# fullRun=False

if fullRun:
    numGens = 20000
    measureIter = 1000
    repeats = 10
else:
    numGens = 20
    measureIter = 10
    repeats = 2

cfg.deleteLog()
cfg.printTitles()

m = Measurements()
m.printTitles(cfg)

cfg.printEol()


def doFullRuns(withLearningRange, stdRange, popSizeRange, propNumRange, wrange, repeats):
    startTime = time.time()
    counter = 0
    runNum = 0
    if (not withLearningRange[0]):
        runNum += len(stdRange) * len(popSizeRange) * len(propNumRange) * len(wrange) * repeats
    if (len(withLearningRange) > 1):
        runNum += len(stdRange) * len(popSizeRange) * len(propNumRange) * repeats

    for wlearn in withLearningRange:
        cfg.learnInteractionTrust = wlearn
        for std in stdRange:
            cfg.std = std
            for popSize in popSizeRange:
                cfg.popSize = popSize
                for propNum in propNumRange:
                    cfg.propNum = propNum
                    awrange = wrange
                    if (wlearn):
                        awrange = [0]
                    for pp in awrange:
                        cfg.probRandPartner = pp

                        m = Measurements()
                        for rep in range(repeats):
                            counter += 1
                            print(f'Starting run {counter}/{runNum} . . .')
                            simulator = Simulator(cfg)
                            # print("Starting sim . . . ");
                            simulator.simulate(numGens, measureIter, False)
                            simulator.addMeasure(m)

                            end = time.time()
                            es = (end - startTime) / 60.0
                            print("Elapsed: %.2f minutes, estimated remaining %.2f minutes" % (
                            es, es / counter * (runNum - counter)))

                        cfg.printContent()
                        m.printContent(cfg)
                        cfg.printEol()
                        print("Wrote to results log")
                        # exit(0);


# Re-create main results:
doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[50], propNumRange=[5], wrange=np.linspace(0, 1, 11),
           repeats=10)
doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[30], propNumRange=[3], wrange=np.linspace(0, 1, 11),
           repeats=10)

# Sensitivity checks
#
if False:
    rr = 4
    doFullRuns(stdRange=[0.02], withLearningRange=[False], popSizeRange=[50], propNumRange=[5],
               wrange=np.linspace(0, 1, 11), repeats=rr)
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[100], propNumRange=[5],
               wrange=np.linspace(0, 1, 11), repeats=rr)
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[100], propNumRange=[10],
               wrange=np.linspace(0, 1, 11), repeats=rr)

    cfg.successThreshold = 0.1
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[50], propNumRange=[5],
               wrange=np.linspace(0, 1, 11), repeats=rr)
    cfg.stepSize = 0.2
    cfg.successThreshold = 0.3
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[50], propNumRange=[5],
               wrange=np.linspace(0, 1, 11), repeats=rr)

# Unbounded space
if False:
    rr = 4
    cfg.withBoundaries = False
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[30], propNumRange=[3],
               wrange=np.linspace(0, 1, 11), repeats=rr)

# Unused
if False:
    numGens = 40000
    cfg.successThreshold = 0.1
    cfg.stepSize = 0.025
    rr = 2
    doFullRuns(stdRange=[0.1], withLearningRange=[False], popSizeRange=[50], propNumRange=[5],
               wrange=np.linspace(0, 1, 11), repeats=rr)

# cfg.successThreshold=0.3
# cfg.stepSize=0.2;
# doFullRuns(stdRange=[0.1],withLearningRange=[False],popSizeRange=[50],propNumRange=[5],wrange=np.linspace(0,1,11),repeats=rr);


# repeats=3
# withLearningRange=[False]
# popSizeRange=[30]
# propNumRange=[3]
# wrange=[0];
