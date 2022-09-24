from typing import Dict

from simulation.result import SimulationResult, IterationResult


class ExperimentResult:

    def __init__(self) -> None:
        # TODO: change from dict to pd/np obj for performance
        self.simulation_map: Dict[str, SimulationResult] = {}

    def add_simulation_result(self, repetition: int, to_results: SimulationResult) -> None:
        self.simulation_map[f"{repetition}"] = to_results

    def get_simulation_result_at(self, repetition: int) -> SimulationResult:
        return self.simulation_map.get(f"{repetition}")

    def get_iteration_from_all_repetitions(self, iteration_index: int) -> Dict[str, IterationResult]:
        return {
            repetition: self.get_simulation_result_at(int(repetition)).get_iteration(iteration_index)
            for repetition in self.simulation_map.keys()
        }
