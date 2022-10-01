import uuid
from datetime import datetime, timedelta
from typing import Dict

from simulation.config import SimulationConfig
from simulation.result import SimulationResult, IterationResult


class ExperimentResult:

    def __init__(self, simulation_configs) -> None:
        # TODO: change from dict to pd/np obj for performance
        self.experiment_id: uuid.UUID = uuid.uuid4()
        self.timestamp: datetime or None = None
        self.run_time: timedelta or None = None
        self.simulation_map: Dict[str, SimulationResult] = {}
        self.simulation_configs: SimulationConfig = simulation_configs

    def add_simulation_result(self, repetition: int, to_results: SimulationResult) -> None:
        self.simulation_map[f"{repetition}"] = to_results

    def get_simulation_result_at(self, repetition: int) -> SimulationResult:
        return self.simulation_map.get(f"{repetition}")

    def get_iteration_from_all_repetitions(self, iteration_index: int) -> Dict[str, IterationResult] or None:
        result = {}
        for repetition in self.simulation_map.keys():
            iteration_result = self.get_simulation_result_at(int(repetition)).get_iteration(iteration_index)
            if iteration_result is None:
                return None
            result[repetition] = self.get_simulation_result_at(int(repetition)).get_iteration(iteration_index)
        return result

    def __str__(self) -> str:
        return f"experiment_id={self.experiment_id}\n" \
               f"timestamp={self.timestamp}\n" \
               f"run_time={self.run_time}"
