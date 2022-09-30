from abc import ABC, abstractmethod
from typing import Callable, List

import numpy as np
from numpy import mean

from analyze.results import MeasurementResult
from experiment.result import ExperimentResult


class Measurement(ABC):

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        pass

    def _apply_measure_using_opinion_list_func(
            self,
            experiment_result: ExperimentResult,
            measure_for_opinion_list: Callable[[List[float]], float]
    ) -> MeasurementResult:
        results = []
        x = []
        for iteration_index in range(experiment_result.simulation_configs.num_iterations):
            iteration_spreads = []
            iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
            if iterations_result is None:
                continue
            x.append(iteration_index)
            for iteration_result in iterations_result.values():
                iteration_spreads.append(measure_for_opinion_list(iteration_result.opinions_list))
            results.append(mean(iteration_spreads))
        return MeasurementResult(
            y=np.array(results, dtype=float),
            x=np.array(x, dtype=int),
            experiment_id=experiment_result.experiment_id,
            measurement_type=self.name
        )

    def ylim(self) -> None or (float, float):
        return None
