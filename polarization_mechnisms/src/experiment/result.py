from typing import Dict

from simulation.result import SimulationResult


class ExperimentResult:

    def __init__(self) -> None:
        # TODO: change from dict to pd/np obj for performance
        self.simulation_map: Dict[str, SimulationResult] = {}

    def add_simulation_result(self, repetition: int, to_results: SimulationResult) -> None:
        self.simulation_map[f"{repetition}"] = to_results

