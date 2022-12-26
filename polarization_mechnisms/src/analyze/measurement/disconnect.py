import numpy as np
from numpy import ndarray, sort

from analyze.measurement import constants
from analyze.results import MeasurementResult
from analyze.measurement.base import Measurement
from experiment.result import ExperimentResult


# See note in “Dispersion Point,” 2021; This is Option #1.
class DisconnectIndexMeasurement(Measurement):

    def __init__(self, disconnect_factor: float = 0.2):
        super().__init__(constants.DISCONNECT_INDEX, "Disconnect Index")
        self.disconnect_factor = disconnect_factor

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: len(opinions_list) - len(self._min_removal_for_disconnect(sort(opinions_list), self.disconnect_factor))
        )

    def _min_removal_for_disconnect(self, opinions_list: ndarray, disconnect_factor):
        if len(opinions_list) == 2:
            return opinions_list[:1]
        closest_pair = (0, 1)
        for i in range(1, len(opinions_list)):
            if opinions_list[i] - opinions_list[i - 1] < disconnect_factor:
                return opinions_list
            if opinions_list[i] - opinions_list[i - 1] < opinions_list[closest_pair[1]] - opinions_list[closest_pair[0]]:
                closest_pair = (i-1, i)
        opinions_list_without_left = np.delete(opinions_list, closest_pair[0])
        opinions_list_without_right = np.delete(opinions_list, closest_pair[1])
        _disconnect_index_without_left_in_pair = self._min_removal_for_disconnect(opinions_list_without_left, disconnect_factor)
        _disconnect_index_without_right_in_pair = self._min_removal_for_disconnect(opinions_list_without_right, disconnect_factor)
        if len(_disconnect_index_without_left_in_pair) < len(_disconnect_index_without_right_in_pair):
            return _disconnect_index_without_left_in_pair
        return _disconnect_index_without_right_in_pair
