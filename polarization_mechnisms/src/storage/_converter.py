import json

from numpy import ndarray

from analyze.measurment import MeasurementType
from experiment.result import ExperimentResult
from simulation.config import SimulationConfig


def simulation_results_to_rows(experiment_result: ExperimentResult):
    for repetition, simulation_result in experiment_result.simulation_map.items():
        yield [
            experiment_result.experiment_id,
            repetition,
            int(simulation_result.timestamp.timestamp()),
            simulation_result.run_time.seconds
        ]


def iteration_results_to_rows(experiment_result: ExperimentResult):
    for repetition, simulation_result in experiment_result.simulation_map.items():
        for iteration, iteration_result in simulation_result.iteration_map.items():
            yield [
                experiment_result.experiment_id,
                repetition,
                iteration,
                json.dumps(iteration_result.opinions_list)
            ]


def experiment_results_to_row(experiment_result: ExperimentResult):
    experiment_results_row = [
        experiment_result.experiment_id,
        int(experiment_result.timestamp.timestamp()),
        experiment_result.run_time.seconds,
        experiment_result.simulation_configs.config_id,
    ]
    return experiment_results_row


def experiment_config_to_row(simulation_config: SimulationConfig):
    experiment_config_row = [
        simulation_config.config_id,
        simulation_config.simulation_type.name,
        simulation_config.num_of_agents,
        simulation_config.num_iterations,
        simulation_config.mio,
        simulation_config.num_of_repetitions,
        simulation_config.switch_agent_rate,
        simulation_config.switch_agent_sigma,
        simulation_config.radical_exposure_eta,
        simulation_config.truncate_at,
        simulation_config.epsilon,
        simulation_config.mark_stubborn_at,
        simulation_config.display_name
    ]
    return experiment_config_row


def measurement_to_rows(experiment_result: ExperimentResult, measurement: ndarray, measurement_type: MeasurementType):
    for i in range(len(measurement)):
        yield [
            experiment_result.experiment_id,
            measurement_type.name,
            i,
            measurement[i]
        ]
