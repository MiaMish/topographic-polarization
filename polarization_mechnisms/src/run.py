import concurrent.futures
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from experiment.experiment import Experiment
from simulation.config import SimulationConfig, SimulationType
from storage.results import StoreResults
from visualize.visualize import MEASUREMENTS_TO_VISUALIZE

BASE_LOG_PATH = f"{os.getcwd()}/../logs/"
BASE_DB_PATH = f"{os.getcwd()}/../resources/database/"
LOG_LEVEL = logging.DEBUG


def get_vanilla_similarity_conf():
    return SimulationConfig(
        simulation_type=SimulationType.SIMILARITY,
        num_of_agents=100,
        num_iterations=10000,
        mio=0.3,
        num_of_repetitions=200,
        switch_agent_rate=None,
        switch_agent_sigma=None,
        radical_exposure_eta=None,
        truncate_at=0.0001,
        epsilon=0.1,
        mark_stubborn_at=0.1,
        audit_iteration_predicate=lambda iteration_index: iteration_index % 50 == 0,
        display_name="Epsilon = 0.1")


def configs_to_run():
    configs = []
    # Vanilla confs
    for curr_epsilon in np.arange(0, 1.1, 0.1):
        for curr_mio in np.arange(0, 1.1, 0.1):
            similarity_conf = get_vanilla_similarity_conf()
            similarity_conf.epsilon = curr_epsilon
            similarity_conf.mio = curr_mio
            similarity_conf.display_name = f"Epsilon={curr_epsilon:.1f}::Mio={curr_mio:.1f}"
            configs.append(similarity_conf)
    return configs


def config_loger(is_worker: bool = False):
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
    logging.info(f"Configured logger for filename={log_file}")


def run_using_conf(config_index):
    config_loger(True)
    conf = configs_to_run()[config_index]
    logging.info(f"Running config_index={config_index} flow for config_display_name={conf.display_name}")
    logging.info(f"Config: {conf}")
    store_results = StoreResults(BASE_DB_PATH)
    results = Experiment(conf).run_experiment()
    store_results.append_experiment_result(results, store_actual_results=False)
    for measurement in MEASUREMENTS_TO_VISUALIZE:
        measurement_result = measurement.apply_measure(results)
        store_results.append_measurement(measurement_result)
    logging.info(f"Finished config_index={config_index} flow for config_display_name={conf.display_name}")
    return config_index


if __name__ == '__main__':
    config_loger(False)
    configs_to_run = configs_to_run()
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        for config_index_finished in executor.map(run_using_conf, range(0, len(configs_to_run))):
            logging.info(f"Finished config_index={config_index_finished} flow")
