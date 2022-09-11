from statistics import mean


class Measurements:

    def __init__(self):
        self.rnear = []
        self.rfar = []
        self.cor = []
        self.sr = []
        self.firstP = []
        self.midRatio = []

    def add(self, sr, cor, rnear, rfar, midRatio):
        if cor is None:
            raise Exception("cor none")
        if sr is None:
            raise Exception("sr none")
        self.sr.append(sr)
        self.cor.append(cor)
        self.rnear.append(rnear)
        self.rfar.append(rfar)
        self.midRatio.append(midRatio)

    def __str__(self):
        res = ""
        res += "Results: (average of " + str(len(self.pp)) + " runs)\n"
        res += "pp=" + str(mean(self.pp)) + " successRate=" + str(mean(self.sr))
        res += "\n"
        res += str(len(self.firstP)) + " has firstP, mean="
        if len(self.firstP) > 0:
            res += str(mean(self.firstP))
        else:
            res += "None"
        res += "\n"
        return res

    def printTitles(self, cfg):
        f = open(cfg.logFile, "a")
        f.write(f',num runs, succcess rate, mean-abs-cor,  nearpairs,farpairs,midRatio')
        f.close()

    def printContent(self, cfg):
        f = open(cfg.logFile, "a")
        f.write(
            f',{len(self.sr)},{mean(self.sr)},{mean(self.cor)},{mean(self.rnear)},{mean(self.rfar)},{mean(self.midRatio)}')
        f.close()
