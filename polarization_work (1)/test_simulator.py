
import unittest
import numpy as np

from config import Config
from simulator import Simulator


class TestSimulator(unittest.TestCase):

  def setUp(self):
    self.config =Config()
    self.config.propNum =4
    self.config.popSize =10
    self.config.successThreshold =0.3
    self.config.std =0.1
    self.config.stepSize =0.1
    self.config.repulseScale =1
    self.config.attractScale = 1

  def testChooseProps(self):
    sim = Simulator(self.config)
    for i in range(100):
       sim.chooseTraits()
       self.assertNotEqual(sim.choiceTrait ,sim.interactTrait)
       self.assertLess(sim.choiceTrait ,self.config.propNum)
       self.assertLess(sim.interactTrait, self.config.propNum)

  def testFixBoundaries(self):
    sim = Simulator(self.config)
    self.assertEqual(0.5 ,sim.fixBoundaries(0.5))
    self.assertEqual(0, sim.fixBoundaries(0))
    self.assertEqual(-0.6, sim.fixBoundaries(-0.6))
    self.assertEqual(1, sim.fixBoundaries(1.1))
    self.assertEqual(-1, sim.fixBoundaries(-1.3))

  def testFindPartner(self):

    sim = Simulator(self.config)
    sim.population.traits =np.zeros((10 ,4))

    sim.population.traits[1][3] = 110
    sim.population.traits[2][3 ] =-50
    sim.population.traits[4][3 ] =-30
    sim.population.traits[8][3 ] =130

    sim.choiceTrait =3

    for i in range(10):
       self.assertEqual(8 ,sim.findPartner(1))
       self.assertEqual(1, sim.findPartner(8))
       self.assertEqual(4, sim.findPartner(2))
       self.assertEqual(2, sim.findPartner(4))


  def testInteract(self):

    sim = Simulator(self.config)
    sim.population.traits =np.zeros((10 ,4))

    sim.population.traits[1][2 ] =110
    sim.population.traits[2][2 ] =-50
    sim.population.traits[4][2 ] =-50
    sim.population.traits[8][2 ] =110

    sim.interactTrait =2

    for rep in range(10):

      succCount =0
      for i in range(100):
        if sim.interact(1 ,8):
          succCount +=1
      self.assertLessEqual(85 ,succCount)

      succCount = 0
      for i in range(100):
        if sim.interact(1, 2):
          succCount += 1
      self.assertLessEqual(succCount ,10)

  def testActFailure(self):

    sim = Simulator(self.config)
    sim.population.traits =np.zeros((10 ,4))

    sim.population.traits[1][1 ] =0.8
    sim.population.traits[2][1 ] =0.7
    sim.population.traits[3][1] = 0.8
    sim.population.traits[4][1] = 0.9



    sim.choiceTrait =1
    sim.w1= sim.population.traits[1][1]
    sim.w2 = sim.population.traits[2][1]
    sim.actFailure(1 ,2)
    self.assertAlmostEqual(0.9 ,sim.population.traits[1][1])

    sim.w1 = sim.population.traits[3][1]
    sim.w2 = sim.population.traits[4][1]
    sim.actFailure(3 ,4)
    self.assertAlmostEqual(0.7, sim.population.traits[3][1])
