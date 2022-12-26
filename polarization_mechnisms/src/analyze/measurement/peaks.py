import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import argrelmax, argrelmin

from analyze.measurement import constants
from analyze.results import MeasurementResult
from analyze.measurement.base import Measurement
from experiment.result import ExperimentResult


# Bramson et el., 2016 section 2.5
# Ordering all opinions in bins and calculating the % of agents in each bin.
# For example, if we have 2 bins and opinion dist [0.2, 0.4, 0.9],
# then the first bin (0, 0.5) contains 2/3 of the agents and the second one (0.5, 1) contains 1/3.
# Then, we apply smoothing on the created curve to remove small "jumps" and look for local maxes.
# A vector is more polarized if it has a small number of peek points, but not 0 or 1.
# In general (it's not tested by this...) if the peeks are far apart from each other => the dist is more polarized
class PeaksMeasurement(Measurement):

    def __init__(self):
        super().__init__(constants.NUM_OF_LOCAL_MAX, "Number of Local Peak Points")

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: self._num_of_local_extreme_points(opinions_list)
        )

    def _num_of_local_extreme_points(self, opinions_list, num_of_bins=100):
        bins_dist = np.histogram(opinions_list, bins=num_of_bins)[0] / len(opinions_list)
        fitted_curve = UnivariateSpline(range(num_of_bins), bins_dist, s=5)
        applied_curve = fitted_curve(range(num_of_bins))
        return len(argrelmax(applied_curve)) + len(argrelmin(applied_curve))
