import numpy as np
from ripleyk import ripleyk

from analyze.measurement import constants
from analyze.results import MeasurementResult
from analyze.measurement.base import Measurement
from experiment.result import ExperimentResult


# TODO: I think my entire approach here is incorrect...
# Take a look: https://stats.stackexchange.com/questions/122668/is-there-a-measure-of-evenness-of-spread
class RipleyEstimatorMeasurement(Measurement):

    def __init__(self, radius: float = 0.5, bounding_radius=1):
        super().__init__(constants.RIPLEY_ESTIMATOR, "Ripley Estimator")
        self.radius = radius
        self.bounding_radius = bounding_radius

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: ripleyk.calculate_ripley(self.radius, self.bounding_radius, d1=np.arange(0, len(opinions_list)), d2=np.sort(opinions_list))
        )
