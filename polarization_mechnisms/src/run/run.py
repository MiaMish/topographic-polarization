import copy
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from analyze.results import MeasurementResult
from experiment.experiment import Experiment
from experiment.result import ExperimentResult
from simulation.config import SimulationConfig, SimulationType
from visualize.visualize import MEASUREMENTS_TO_VISUALIZE

BASE_LOG_PATH = f"{os.getcwd()}/../logs/"
BASE_DB_PATH = f"{os.getcwd()}/../resources/database/"
LOG_LEVEL = logging.INFO
MAX_WORKERS = 12
USE_LOG_FILE = False


def get_vanilla_similarity_conf():
    return SimulationConfig(
        simulation_type=SimulationType.SIMILARITY,
        num_of_agents=100,
        num_iterations=10000,
        mio=0.3,
        num_of_repetitions=5,
        switch_agent_rate=None,
        switch_agent_sigma=None,
        radical_exposure_eta=None,
        truncate_at=0.0001,
        epsilon=0.1,
        mark_stubborn_at=0.1,
        audit_iteration_every=None,
        display_name="Epsilon = 0.1")


def x(configs, to_apply, variation_list_to_apply):
    new_configs = []
    for config in configs:
        for variation in variation_list_to_apply:
            variation_to_append = to_apply(copy.deepcopy(config), variation)
            variation_to_append.config_id = uuid.uuid4()
            new_configs.append(variation_to_append)
    return new_configs


def configs_to_run():
    configs = [get_vanilla_similarity_conf()]

    def change_simulation_type(config, simulation_type):
        config.simulation_type = simulation_type
        return config

    def change_num_of_agents(config, num_of_agents):
        config.num_of_agents = num_of_agents
        return config

    def change_num_iterations(config, num_iterations):
        config.num_iterations = num_iterations
        return config

    def change_mio(config, mio):
        config.mio = mio
        return config

    def change_num_of_repetitions(config, num_of_repetitions):
        config.num_of_repetitions = num_of_repetitions
        return config

    def change_switch_agent_rate(config, switch_agent_rate):
        config.switch_agent_rate = switch_agent_rate
        return config

    def change_switch_agent_sigma(config, switch_agent_sigma):
        config.switch_agent_sigma = switch_agent_sigma
        return config

    def change_radical_exposure_eta(config, radical_exposure_eta):
        config.radical_exposure_eta = radical_exposure_eta
        return config

    def change_epsilon(config, epsilon):
        config.epsilon = epsilon
        return config

    configs = x(configs, change_simulation_type, [SimulationType.SIMILARITY, SimulationType.REPULSIVE, SimulationType.ASSIMILATION])
    configs = x(configs, change_num_of_agents, [100])
    configs = x(configs, change_num_iterations, [10000])
    configs = x(configs, change_mio, [0.2, 0.4])
    configs = x(configs, change_num_of_repetitions, [400])
    configs = x(configs, change_switch_agent_rate, [None, 5])
    configs = x(configs, change_switch_agent_sigma, [None, 0.2])
    configs = x(configs, change_radical_exposure_eta, [None, 0.2])
    configs = x(configs, change_epsilon, [0.2, 0.4, 0.6])

    return configs


def config_loger(is_worker: bool = False, use_log_file: bool = True):
    log_file = None
    if use_log_file:
        log_dir = f"{BASE_LOG_PATH}{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
        if is_worker:
            log_dir = f"{log_dir}/{os.getppid()}"
        else:
            log_dir = f"{log_dir}/{os.getpid()}"
        log_file = f"{log_dir}/{os.getpid()}.log"
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            encoding="utf-8",
            level=LOG_LEVEL,
            filename=log_file,
            format='PID=%(process)d TIME=[%(asctime)s] NAME=%(name)s LEVEL=%(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        logging.basicConfig(
            encoding="utf-8",
            level=LOG_LEVEL,
            format='PID=%(process)d TIME=[%(asctime)s] NAME=%(name)s LEVEL=%(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    logging.info(f"Configured logger for filename={log_file}")


def run_using_conf(conf: SimulationConfig) -> tuple[SimulationConfig, ExperimentResult, list[MeasurementResult]]:
    config_loger(True)
    logging.info(f"Starting to run with config: {conf}")
    results = Experiment(conf).run_experiment()
    measurement_results = []
    for measurement in MEASUREMENTS_TO_VISUALIZE:
        measurement_results.append(measurement.apply_measure(results))
    return conf, results, measurement_results
