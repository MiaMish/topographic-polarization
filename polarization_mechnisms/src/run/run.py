import copy
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

import colorlog

from analyze.measurement.factory import MeasurementFactory
from analyze.results import MeasurementResult
from experiment.experiment import Experiment
from experiment.result import ExperimentResult
from simulation.config import SimulationConfig, SimulationType
from storage.results import StoreResults
from visualize.visualize import MEASUREMENTS_TO_VISUALIZE, scatter_plot_from_measurements
import storage.constants as db_constants

BASE_LOG_PATH = f"{os.getcwd()}/../logs/"
BASE_DB_PATH = f"{os.getcwd()}/../resources/database_3/"
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


def configs_to_run(
        simulation_types: List[SimulationType],
        num_of_agents: List[int],
        num_iterations: List[int],
        mios: List[float],
        num_of_repetitions: List[int],
        switch_agent_rates: List[int],
        switch_agent_sigmas: List[float],
        radical_exposure_etas: List[float],
        epsilons: List[float],
        mio_sigmas: List[float],
):
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

    def change_mio_sigma(config, mio_sigma):
        config.mio_sigma = mio_sigma
        return config

    configs = x(configs, change_simulation_type, simulation_types)
    configs = x(configs, change_num_of_agents, num_of_agents)
    configs = x(configs, change_num_iterations, num_iterations)
    configs = x(configs, change_mio, mios)
    configs = x(configs, change_num_of_repetitions, num_of_repetitions)
    configs = x(configs, change_switch_agent_rate, switch_agent_rates)
    configs = x(configs, change_switch_agent_sigma, switch_agent_sigmas)
    configs = x(configs, change_radical_exposure_eta, radical_exposure_etas)
    configs = x(configs, change_epsilon, epsilons)
    configs = x(configs, change_mio_sigma, mio_sigmas)

    logging.info(f"Using configs to run for:\n"
                 f"simulation_types: {simulation_types}\n"
                 f"num_of_agents: {num_of_agents}\n"
                 f"num_iterations: {num_iterations}\n"
                 f"mios: {mios}\n"
                 f"num_of_repetitions: {num_of_repetitions}\n"
                 f"switch_agent_rates: {switch_agent_rates}\n"
                 f"switch_agent_sigmas: {switch_agent_sigmas}\n"
                 f"radical_exposure_etas: {radical_exposure_etas}\n"
                 f"epsilons: {epsilons}\n"
                 f"mio_sigmas: {mio_sigmas}")
    return configs


def config_loger(is_worker: bool = False, use_log_file: bool = True):
    log_fmt = 'PID=%(process)d TIME=[%(asctime)s] NAME=%(name)s LEVEL=%(levelname)s %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
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
            format=log_fmt,
            datefmt=date_format
        )
        return
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(f'%(log_color)s{log_fmt}', datefmt=date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def run_using_conf(conf: SimulationConfig) -> tuple[SimulationConfig, ExperimentResult, list[MeasurementResult]]:
    config_loger(True, False)
    logging.info(f"Starting to run with config: {conf}")
    results = Experiment(conf).run_experiment()
    measurement_results = []
    for measurement in MEASUREMENTS_TO_VISUALIZE:
        measurement_results.append(measurement.apply_measure(results))
    return conf, results, measurement_results


def scatter_plot(filters: Dict[str, Any], measurement_type: str, store_file: str, figures_dir_path: str):
    # filters = {
    #     db_constants.SIMULATION_TYPE: SimulationType.SIMILARITY.name,
    #     db_constants.NUM_OF_AGENTS: 100,
    #     db_constants.NUM_ITERATIONS: 1000,
    #     db_constants.MIO: 0.2,
    #     db_constants.NUM_OF_REPETITIONS: 10,
    #     db_constants.SWITCH_AGENT_RATE: 5,
    #     db_constants.SWITCH_AGENT_SIGMA: None,
    #     db_constants.RADICAL_EXPOSURE_ETA: 0.2,
    #     db_constants.EPSILON: 0.2
    # }
    img_file_path = f"{figures_dir_path}{store_file}.png"
    log_file_path = f"{figures_dir_path}figures.logs"
    logging.info("Using file_path: %s measurement_type: %s and filters: %s", img_file_path, measurement_type, filters)

    non_filtered_props = []
    if db_constants.MIO not in filters is not None:
        display_name_extractor = lambda simulation_config: f"mio={simulation_config.mio}"
        non_filtered_props.append(db_constants.MIO)
    if db_constants.SWITCH_AGENT_RATE not in filters is not None:
        display_name_extractor = lambda simulation_config: f"switch_agent_rate={simulation_config.switch_agent_rate}"
        non_filtered_props.append(db_constants.SWITCH_AGENT_RATE)
    if db_constants.SWITCH_AGENT_SIGMA not in filters is not None:
        display_name_extractor = lambda simulation_config: f"switch_agent_sigma={simulation_config.switch_agent_sigma}"
        non_filtered_props.append(db_constants.SWITCH_AGENT_SIGMA)
    if db_constants.RADICAL_EXPOSURE_ETA not in filters is not None:
        display_name_extractor = lambda simulation_config: f"radical_exposure_eta={simulation_config.radical_exposure_eta}"
        non_filtered_props.append(db_constants.RADICAL_EXPOSURE_ETA)
    if db_constants.EPSILON not in filters is not None:
        display_name_extractor = lambda simulation_config: f"epsilon={simulation_config.epsilon}"
        non_filtered_props.append(db_constants.EPSILON)

    if len(non_filtered_props) > 1:
        raise Exception(f"You must have at most 1 non filtered props. Your non filtered props are: {non_filtered_props}")

    to_scatter = MeasurementFactory().by_name(measurement_type)
    configs = StoreResults.instance().retrieve_configurations(filters=filters)
    logging.info(f"Found {len(configs)} matching configs")
    for config in configs:
        logging.info("----------------")
        logging.info(config)
    measurements = StoreResults.instance().retrieve_measurement_results_for_configs(configs, display_name_extractor)
    filtered_measurements = [measurement for measurement in measurements if measurement.measurement_type == to_scatter.name]
    logging.info(f"Found {len(filtered_measurements)} matching measurements")
    for measurement in filtered_measurements:
        logging.info("----------------")
        logging.info(f"{measurement.measurement_type} {measurement.display_name} {measurement.experiment_id}")
    scatter_plot_from_measurements(to_scatter, filtered_measurements, store_in_file=img_file_path)
    with open(log_file_path, 'a') as fin:
        fin.write(f"-----\n"
                  f"file_path: {img_file_path}\n"
                  f"measurement_type: {measurement_type}\n"
                  f"filters: {filters}\n"
                  f"non_filtered_props={non_filtered_props}")

