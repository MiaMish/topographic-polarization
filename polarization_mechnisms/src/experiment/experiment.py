from experiment.result import ExperimentResult
from simulation.config import SimulationConfig
from simulation.factory import create_simulation


class Experiment:

    def __init__(self, simulation_config: SimulationConfig) -> None:
        super().__init__()
        self.simulation_config = simulation_config

    def run_experiment(self) -> ExperimentResult:
        experiment_result = ExperimentResult()
        for i in range(self.simulation_config.num_of_repetitions):
            simulation = create_simulation(self.simulation_config)
            simulation_result = simulation.run_simulation()
            experiment_result.add_simulation_result(i, simulation_result)
        return experiment_result

