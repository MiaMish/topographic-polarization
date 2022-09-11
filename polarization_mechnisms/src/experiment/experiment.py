from experiment.result import ExperimentResult
from simulation.config import SimulationConfig
from simulation.factory import create_simulation


class Experiment:

    def __init__(self, repetitions: int, simulation_config: SimulationConfig) -> None:
        super().__init__()
        self.repetitions = repetitions
        self.simulation_config = simulation_config

    def run_experiment(self) -> ExperimentResult:
        experiment_result = ExperimentResult()
        for i in range(self.repetitions):
            simulation = create_simulation(self.simulation_config)
            simulation_result = simulation.run_simulation()
            experiment_result.add_simulation_result(i, simulation_result)
        return experiment_result

