from typing import List

import numpy as np
import scipy.stats
from analyze.measurement import constants
from analyze.results import MeasurementResult
from analyze.measurement.base import Measurement
from experiment.result import ExperimentResult


class VarianceInBinsMeasurement(Measurement):

    def __init__(self, num_of_bins: int = 10):
        super().__init__(constants.BINS_VARIANCE, "Variance of Opinions by Bins")
        self.num_of_bins = num_of_bins

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: self.mean_var_in_bins(opinions_list)
        )

    def mean_var_in_bins(self, opinions_list: List[float]) -> float:
        bin_means, bin_edges, binnumber = scipy.stats.binned_statistic(opinions_list, opinions_list, statistic='std', bins=self.num_of_bins, range=None)
        return np.mean(bin_means)
