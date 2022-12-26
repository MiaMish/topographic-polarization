import numpy as np

from analyze.measurement import constants
from analyze.measurement.base import Measurement
from analyze.results import MeasurementResult
from experiment.result import ExperimentResult


# Bramson et el., 2016 section 2.3
# Limitation: the num of bins is arbitrary
class CoveredBinsMeasurement(Measurement):

    def __init__(self, num_of_bins: int = 10):
        super().__init__(constants.COVERED_BINS, "% of Covered Deciles")
        self.num_of_bins = num_of_bins

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: np.count_nonzero(np.histogram(opinions_list, self.num_of_bins)[0] != 0) / self.num_of_bins
        )
