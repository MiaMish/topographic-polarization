from config import Config
from simulator import Simulator
import cProfile
import pstats

# This file is used to play around with a single run

print("Starting")

cfg = Config()

cfg.verbose = False
cfg.std = 0.1
cfg.popSize = 50
cfg.propNum = 5

cfg.attractScale = 0
cfg.repulseScale = 1
cfg.breakTies = False
cfg.withBoundaries = True
cfg.outOfBoundsFriction = 0

cfg.probRandPartner = 0.4
cfg.interactionWeightedSelection = False
cfg.interactionWeightPower = 0
cfg.learnInteractionTrust = False
# cfg.withBoundaries=False

# cfg.weightedSteps=True
# cfg.verbose=True

simulator = Simulator(cfg)

if True:
    # simulator.simulate(100,10)
    simulator.simulate(20000, 1000, True)
else:
    cProfile.run('simulator.simulate(4000,400)', 'mystats')
    p = pstats.Stats('mystats')
    p.strip_dirs().sort_stats('tottime').print_stats(20)
