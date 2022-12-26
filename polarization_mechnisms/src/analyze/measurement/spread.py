from analyze.measurement import constants
from analyze.results import MeasurementResult
from analyze.measurement.base import Measurement
from experiment.result import ExperimentResult


# Bramson et el., 2016 section 2.1
class SpreadMeasurement(Measurement):

    def __init__(self):
        super().__init__(constants.SPREAD, "Delta Between Max and Min Opinions")

    def ylim(self):
        return 0, 1

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: max(opinions_list) - min(opinions_list)
        )
