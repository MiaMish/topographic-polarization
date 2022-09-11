import numpy as np


class Analysis:

    def __init__(self, config):
        self.config = config

    def l2(self, v1, v2):
        return np.linalg.norm(v1 - v2, ord=2);

    def lmax(self, v1, v2):
        return max(abs(v1 - v2));

    def lmin(self, v1, v2):
        return min(abs(v1 - v2));

    def cluster(self, pop):
        clusters = []
        used = set()
        for i in range(pop.shape[0]):
            if (i in used):
                continue
            used.update([i]);
            v1 = pop[i, :]
            added = False
            addTo = None
            for c in clusters:
                if (added):
                    break
                for m in c:
                    if (added):
                        break
                    v2 = pop[m, :]
                    dis = self.l2(v1, v2);
                    if (dis < self.config.clusterThreshold):
                        addTo = c
                        added = True
            if (added):
                addTo.update([i])
            else:
                nc = set([i]);
                clusters.append(nc)
        clusters.sort(key=len, reverse=True)
        return clusters

    def printClusters(self, pop, clusters):
        print("Clusters", len(clusters), ":");
        i = 0

        sumLen = 0
        for c in clusters:
            if (len(c) <= 3):
                print("... More ", pop.shape[0] - sumLen, "elements in ", len(clusters) - i, " clusters.")
                break
            el = next(iter(c));
            v = pop[el, :];
            print(i, ": ", len(c), "elements. Rep:", v);
            sumLen += len(c)
            i += 1

    def getClusterChar(self, pop, cluster):
        el = next(iter(cluster));
        v = pop[el, :];
        if (len(cluster) == 1):
            return v;
        for i in cluster:
            d = pop[i, :]
            if (self.lmax(d, v) > self.config.stepSize + 0.01):
                return None;
        return v;

    def measurePP(self, pop, clusters):
        allPs = [];
        allCs = [];

        # if (len(clusters)==2):
        #      print( "hey");
        bestScore = 0;
        for c in clusters:
            p = self.getClusterChar(pop, c)
            if (p is None):
                continue;
            for i in range(len(allPs)):
                p2 = -allPs[i];
                if (self.lmax(p, p2) > self.config.stepSize + 0.05):
                    continue;
                score = len(allCs[i]) + len(c);
                # print(score,allCs[i],c);
                if (score > bestScore):
                    bestScore = score;
            allPs.append(p);
            allCs.append(c);
        return bestScore

    def measurePnew(self, pop):
        close = 0;
        far = 0;
        all = 0;
        for i in range(self.config.popSize):
            t1 = pop[i, :];
            for j in range(i + 1, self.config.popSize):
                t2 = pop[j, :];
                if (self.lmax(t1, t2) < self.config.successThreshold):
                    close += 1;
                elif (self.lmin(t1, t2) > 2 - self.config.successThreshold):
                    far += 1;
                all += 1;
        close /= all;
        far /= all
        # print("CF",close,far);
        return (close, far);

    def measureMid(self, pop):
        midCount = 0
        for i in range(self.config.popSize):
            t1 = pop[i, :];
            mid = False
            for j in range(self.config.propNum):
                if (abs(t1[j]) < 0.8):
                    mid = True
            if (mid):
                midCount += 1;
        return (midCount / self.config.popSize);

    def measureCor(self, pop):
        cc = np.corrcoef(np.transpose(pop))
        ss = 0;
        tt = 0;
        for i in range(1, self.config.propNum):
            for j in range(i + 1, self.config.propNum):
                ss += abs(cc[i, j]);
                tt += 1
        res = ss / tt;
        return res;
        # print(cc);
        # print("cor", res);

    def analyzeAndPrint(self, pop, printRes):
        clusters = self.cluster(pop)
        if (printRes):
            self.printClusters(pop, clusters)
        self.pp = self.measurePP(pop, clusters) / self.config.popSize;
        self.pn = self.measurePnew(pop);
        self.rnear = self.pn[0];
        self.rfar = self.pn[1];
        self.cor = self.measureCor(pop);
        self.midRatio = self.measureMid(pop)
        if (printRes):
            print("pp=", self.pp);
            print("cor=" + str(self.cor))
            print("pn=" + str(self.pn))
            print("mid=" + str(self.midRatio))

    def printCorners(self, pop):
        corners = np.zeros([2 ** self.config.propNum])
        thr = 0.9
        for i in range(self.config.popSize):
            vec = pop[i, :];
            cornerId = 0
            inCorner = True
            for j in range(len(vec)):
                v = vec[j];
                if (v > thr):
                    cornerId += 2 ** j
                elif (v > -thr):
                    inCorner = False
                    break
            if (inCorner):
                corners[cornerId] += 1
        print("At corners:", end="")
        for k in corners:
            if (k > 0):
                print(" ", k / self.config.popSize, end="");
        print();
        sm = sum(corners)
        print("Outside corners:", (self.config.popSize - sm) / self.config.popSize)
