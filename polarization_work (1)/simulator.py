from statistics import mean
import numpy as np
import utils
from population import Population
from analysis import Analysis


class Simulator:

    def __init__(self, config):
        self.config = config
        self.population = Population(self.config)

        self.choiceTrait = None
        self.interactTrait = None

    # An efficient algorithm for choosing a number based on a weighted distribution
    # Not used in final runs
    def myChoice(self, weights):
        s = sum(weights)
        r = np.random.uniform(0, 1)
        i = 0
        cs = 0
        for w in weights:
            cs += w / s
            if r < cs:
                return i
            i += 1
        return len(weights) - 1

    # Find an interaction partner for i
    def findPartner(self, i):
        # Case of random choice
        if np.random.uniform(0, 1) < self.config.probRandPartner:
            res = np.random.randint(0, self.config.popSize - 1)
            if res == i:
                res += 1
                # Generate and store weights for update step
            self.w1 = np.random.normal(self.population.traits[i, self.choiceTrait], self.config.std)
            self.w2 = np.random.normal(self.population.traits[res, self.choiceTrait], self.config.std)
            return res
        ts = self.population.traits[:, self.choiceTrait]
        ws = np.random.normal(ts, self.config.std)

        # find distance from individual i
        aws = abs(ws - ws[i])

        j = None
        # Unused code. Only the else part is used.
        if self.config.interactionWeightedSelection:
            pp = self.config.interactionWeightPower
            if self.config.learnInteractionTrust:
                # pp=1-self.population.trustWeightsYes[i,self.choiceTrait]
                pp = self.population.trustWeightsYes[i, self.choiceTrait] / (
                            self.population.trustWeightsYes[i, self.choiceTrait] + self.population.trustWeightsNo[
                        i, self.choiceTrait])
                # if (i==0 and self.choiceTrait==0 and np.random.uniform(0,1)<0.01):
                # print("pp=",pp)

            # if (i==0):
            #        print(pp);
            dis = 0.5 ** (aws * pp)
            dis[i] = 0
            # if (i==0):
            #        print(j,dis);

            # dis=dis/sum(dis)
            # j=np.random.choice(range(self.config.popSize),p=dis)

            j = self.myChoice(dis)
        else:
            # Choose closest individual based on aws
            # mark i as nan to avoid selecting it
            aws[i] = np.nan
            j = np.nanargmin(aws)

        # Store weights for update step
        self.w1 = ws[i]
        self.w2 = ws[j]

        if self.config.verbose:
            print("Choice trait:", self.choiceTrait)
            print("Individual1=", i, "t=", ts[i], "w=", ws[i])
            print("Individual2=", j, "t=", ts[j], "w=", ws[j])

        return j

    def chooseTraits(self):
        # self.choiceTrait,self.interactTrait = np.random.choice(self.config.propNum, 2, replace=False)
        # An efficient way to choose two traits without repetition:
        self.choiceTrait = np.random.randint(0, self.config.propNum)
        self.interactTrait = np.random.randint(0, self.config.propNum - 1)
        if self.interactTrait >= self.choiceTrait:
            self.interactTrait += 1
        # Uncomment this to get both to be equal:
        # self.interactTrait=self.choiceTrait;

    def interact(self, i, j):
        t1 = self.population.traits[i, self.interactTrait]
        t2 = self.population.traits[j, self.interactTrait]
        w1 = np.random.normal(t1, self.config.std)
        w2 = np.random.normal(t2, self.config.std)

        succ = (abs(w1 - w2) < self.config.successThreshold)

        if self.config.verbose:
            print("Interact trait", self.interactTrait)
            print("Individual1=", i, "t=", t1, "w=", w1)
            print("Individual2=", j, "t=", t2, "w=", w2)
            print("Succ=", succ)

        return succ

    # Move trait "trait" of individual i relative that that of j
    # "scale" is used to scale step size
    def moveTrait(self, i, j, trait, scale):

        t1 = self.population.traits[i, trait]
        orgT1 = t1
        t2 = self.population.traits[j, trait]

        if True:
            # dir is the direction to move towards interaction partner
            # On failing interactions the scale will be negative, so movement will be in the opposite direction
            dir = np.sign(self.w2 - self.w1)
        else:
            # UNUSED
            dir = np.sign(t2 - t1)
            if dir == 0 and scale < 0 and self.config.breakTies:
                dir = np.random.choice([-1, 1])

        step = dir * self.config.stepSize * scale

        if self.config.withBoundaries:
            t1 += step
            t1 = self.fixBoundaries(t1)
        else:
            t1 += step
            # dist=0
            # at1=abs(t1)
            # dist=max(at1-1,0);
            # weight=0.1**dist
            # friction=weight*self.config.outOfBoundsFriction
            # t1 += step * friction

        # Unused code:
        # if moving towards individual j, make sure we don't move too far
        if scale > 0:
            if (t1 < t2) == (t2 < orgT1):
                t1 = t2

        if self.config.verbose:
            print("Moving from trait", self.choiceTrait, "from", self.population.traits[i, self.choiceTrait], "to", t1)
        self.population.traits[i, trait] = t1

    # def moveAllTraits(self, i,j,scale):
    #    for k in range(self.config.propNum):
    #      self.moveTrait(i,j,k,scale)

    def fixBoundaries(self, t):
        if t < -1:
            return -1
        if t > 1:
            return 1
        return t

    # Update after a successful interaction
    # Since attractScale is usually 0, this code will be unused
    def actSuccess(self, i, j):
        scale = self.config.attractScale
        if self.config.learnInteractionTrust:
            self.population.trustWeightsYes[i, self.choiceTrait] += 1
            # self.population.trustWeightsYes[i, self.choiceTrait] = self.population.trustWeightsYes[i,
            # self.choiceTrait]*0.9+0.1
        if scale == 0:
            return
        if self.config.weightedSteps:
            scale *= self.population.traitWeights[i, self.interactTrait]
        self.moveTrait(i, j, self.choiceTrait, scale)

    # Update after a failing interaction

    def actFailure(self, i, j):
        # repulseScale is usually 1.
        # We negate it so that moveTrait called below will move away from j, and not towards j
        scale = -self.config.repulseScale
        if self.config.learnInteractionTrust:
            self.population.trustWeightsNo[i, self.choiceTrait] += 1
            # self.population.trustWeightsYes[i, self.choiceTrait] = self.population.trustWeightsYes[i,
            # self.choiceTrait]*0.9
        if scale == 0:
            return
        if self.config.weightedSteps:
            scale *= self.population.traitWeights[i, self.interactTrait]
        self.moveTrait(i, j, self.choiceTrait, scale)
        # self.moveTrait(i, j, self.interactTrait, scale)

    def simulateIndividual(self, i):

        self.chooseTraits()

        j = self.findPartner(i)
        succ = self.interact(i, j)
        if succ:
            self.actSuccess(i, j)
        else:
            self.actFailure(i, j)

        if self.config.verbose:
            utils.waitForInput(self.config)
        return succ

    def simulateIter(self):

        countSucc = 0
        for i in range(self.config.popSize):
            countSucc += self.simulateIndividual(i)
        return countSucc
        # print(self.population.traits[0,:])
        # utils.waitForInput(self.config)

    def simulate(self, iters, reportIters=1, printRes=True):
        ana = Analysis(self.config)
        sr = []
        self.firstP = None
        for i in range(iters):
            countSucc = self.simulateIter()

            sr.append(countSucc)
            if (i + 1) % reportIters == 0:

                # if (i>20000):
                #          self.config.probRandPartner=0.2
                # if (self.config.probRandPartner>0.201):
                #          self.config.probRandPartner-=0.1;

                self.sr = mean(sr) / self.config.popSize
                sr = []
                # print(len(sr),mean(sr));
                ana.analyzeAndPrint(self.population.traits, printRes)

                self.cor = ana.cor
                self.rnear = ana.rnear
                self.rfar = ana.rfar
                self.midRatio = ana.midRatio
                # if (self.pp>=self.config.ppThreshold and (self.firstP is None)):
                #          self.firstP=i+1;
                if printRes:
                    print(i + 1, ",", self.sr, ",", self.cor, ",", self.rnear, ",", self.rfar, ",", self.midRatio)
                    # print("Finished iteration ", (i + 1));
                    # print("Success rate:", self.sr)
                    # print("cor:", self.cor)
                    # print("rnear,rfar:", self.rnear,self.rfar)
                    # print("rp=",self.config.probRandPartner)
                    # ana.printCorners(self.population.traits)
                    print(self.population.traits[range(10), :])
            #  print(self.population.trustWeightsYes[range(3), :])
            # print(self.population.traits)

    def addMeasure(self, mm):
        mm.add(self.sr, self.cor, self.rnear, self.rfar, self.midRatio)
