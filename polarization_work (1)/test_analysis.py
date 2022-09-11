import unittest

import numpy as np

from config import Config
from analysis import Analysis


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.config.clusterThreshold = 2

    def testL2(self):
        v1 = np.array([1, 0, 0, 2, -4])
        v2 = np.array([0, 0, 3, -4, 5])
        a = Analysis(self.config)
        l2 = a.l2(v1, v2)
        self.assertAlmostEqual(11.26942767, l2)

    def testClustering(self):
        for rep in range(10):
            p1 = np.random.normal(0, 0.1, [10, 5])
            p2 = np.random.normal([0, 0, 10, 10, -10], 0.1, [5, 5])
            p3 = np.random.normal([10, 0, -10, 0, 0], 0.1, [2, 5])
            pop = np.concatenate((p1, p2, p3), axis=0)

            pr = list(range(pop.shape[0]))
            np.random.shuffle(pr)

            labels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2]
            plabels = [labels[x] for x in pr]

            rpop = pop[pr, :]

            a = Analysis(self.config)
            cs = a.cluster(rpop)
            lens = {2, 5, 10}
            lenToLabel = {2: 2, 5: 1, 10: 0}
            for c in cs:
                l = len(c)
                self.assertTrue(l in lens)
                lens.remove(l)
                orgLabels = [plabels[m] for m in c]

                expectedLabels = [lenToLabel[l]] * l
                # print(orgLabels," " ,expectedLabels)
                self.assertEqual(expectedLabels, orgLabels)
            print("Trial passed")
            a.printClusters(rpop, cs)

            # lens.update([l]);

            # print(len(c))
            # print(cs)

        self.assertEqual(True, True)

    def testClusterChar(self):
        a = Analysis(self.config)
        pop = np.array([
            [1, 1, 1],
            [1, 0.8, 1],

            [1, -1, 1],
            [1, -1, 1],
            [1, -1, 1],

            [-1, 1, -1],
            [-1, 1, -1]])
        self.assertIsNone(a.getClusterChar(pop, {0, 1}))
        self.assertTrue(([1, -1, 1] == a.getClusterChar(pop, {2, 3, 4})).all())
        self.assertTrue(([-1, 1, -1] == a.getClusterChar(pop, {5, 6})).all())

    def testMeasurePP(self):
        a = Analysis(self.config)
        pop = np.array([
            [1, -1, 1],
            [1, -1, 1],
            [1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]])
        self.assertEqual(5, a.measurePP(pop, [{0, 1, 2}, {3, 4}]))
        self.assertEqual(0, a.measurePP(pop, [{0, 1}, {2, 3, 4}]))
        self.assertEqual(2, a.measurePP(pop, [{4}, {0}]))

        pop = np.array([
            [1, -1, 1],
            [1, -1, 1],
            [1, -1, 1],

            [-1, 1, -1],

            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],

            [-1, 1, -1],
            [-1, 0.9, -1],
            [-1, 1, -1],

            [-1, -1, -1],
            [-1, -1, -1]

        ])
        print("here")
        self.assertEqual(6, a.measurePP(pop,
                                        [{0, 1, 2}, {3}, {4, 5, 6, 7}, {8, 9, 10}, {11, 12}]))

    def testMid(self):

        a = Analysis(self.config)
        pop = np.array([
            [1, -1, 1],
            [1, 0.7, 1],
            [0.9, -0.9, 0.9],
            [-1, 1, -1],
            [0, 0, 0]])
        self.config.popSize = 5
        self.config.propNum = 3
        self.assertEqual(2 / 5, a.measureMid(pop))

    def testPairs(self):
        a = Analysis(self.config)
        self.config.popSize = 5
        self.config.propNum = 3
        pop = np.array([
            [1, 1, -0.9],
            [1, 0.9, -0.9],
            [0.95, 0.97, -0.9],
            [-1, -1, 1],
            [-0.9, -0.9, 0.9]])
        self.assertEqual((0.4, 0.6), a.measurePnew(pop))

    def testCor(self):
        a = Analysis(self.config)
        self.config.popSize = 5
        self.config.propNum = 3
        pop = np.array([
            [1, -1, 1],
            [1, -1, 1],
            [1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]])
        self.assertEqual(1, a.measureCor(pop))

# if __name__ == '__main__':
#  unittest.main()
