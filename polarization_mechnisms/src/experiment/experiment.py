import datetime
import logging

from tqdm import tqdm

from experiment.result import ExperimentResult
from simulation.config import SimulationConfig
from simulation.factory import create_simulation


class Experiment:

    def __init__(self, simulation_config: SimulationConfig) -> None:
        super().__init__()
        self.simulation_config = simulation_config

    def run_experiment(self) -> ExperimentResult:
        experiment_result = ExperimentResult(self.simulation_config)
        experiment_result.timestamp = datetime.datetime.now()
        for i in tqdm(range(self.simulation_config.num_of_repetitions), desc="Experiment Repetitions"):
            simulation = create_simulation(self.simulation_config)
            simulation_result = simulation.run_simulation()
            experiment_result.add_simulation_result(i, simulation_result)
        experiment_result.run_time = datetime.datetime.now() - experiment_result.timestamp
        logging.info(f"Experiment finished. {experiment_result}")
        return experiment_result
