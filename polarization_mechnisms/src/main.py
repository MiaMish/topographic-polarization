#!/usr/bin/env python3
import concurrent
import concurrent.futures
import logging

import yaml
from yaml import SafeLoader

import run.run as run
from run.util import RunStatus
from simulation.config import SimulationType
from storage.results import StoreResults

DEFAULT_NUM_OF_AGENTS = 100
DEFAULT_NUM_OF_ITERATIONS = 10000
DEFAULT_NUM_OF_REPETITIONS = 40
use_log_file = False

CONFIG_FILES_DIR = 'resources'
BASE_RESULT_PATH = "../resources/april06"


def clear_db():
    StoreResults.instance().clear_db()
    StoreResults.instance().bootstrap_db_files()


def append_configs(
        simulation_types: tuple[str] = (SimulationType.SIMILARITY, SimulationType.REPULSIVE),
        num_of_agents: tuple[int] = (DEFAULT_NUM_OF_AGENTS,),
        num_iterations: tuple[int] = (DEFAULT_NUM_OF_ITERATIONS,),
        mios: tuple[float] = (0.2, 0.4),
        num_of_repetitions: tuple[int] = (DEFAULT_NUM_OF_REPETITIONS,),
        switch_agent_rates: tuple[int] = (None, 5),
        switch_agent_sigmas: tuple[float] = (None, 0.2),
        radical_exposure_etas: tuple[float] = (None, 0.2),
        epsilons: tuple[float] = (0.2, 0.4, 0.6),
        mio_sigmas: tuple[float] = (None,),
):
    StoreResults.instance().bootstrap_db_files()
    configs_list_to_run = run.configs_to_run(
        simulation_types=[SimulationType[t] for t in simulation_types],
        num_of_agents=list(num_of_agents),
        num_iterations=list(num_iterations),
        mios=list(mios),
        num_of_repetitions=list(num_of_repetitions),
        switch_agent_rates=list(switch_agent_rates),
        switch_agent_sigmas=list(switch_agent_sigmas),
        radical_exposure_etas=list(radical_exposure_etas),
        epsilons=list(epsilons),
        mio_sigmas=list(mio_sigmas),
    )
    StoreResults.instance().add_configs_to_run(configs_list_to_run)


def generate_combined():
    StoreResults.instance().combine_db_to_single_table()


def run_experiments(max_workers: int = 12, max_experiments: int = 2000, generate_gif: bool = False):
    to_run = StoreResults.instance().get_configs_to_run(limit=max_experiments)
    logging.info(f"Stating to run {len(to_run)} configs using {max_workers} workers.")
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
    futures_list = [pool.submit(run.run_using_conf, conf_to_run) for conf_to_run in to_run]
    completed_tasks = 0
    for completed_future in concurrent.futures.as_completed(futures_list):
        exception = completed_future.exception()
        if exception is not None:
            raise exception
        finished_conf, finished_results, finished_measurement_results = completed_future.result()
        StoreResults.instance().append_measurements(finished_results.experiment_id, finished_measurement_results)
        StoreResults.instance().append_experiment_result(finished_results, store_actual_results=False, generate_gif=generate_gif)
        StoreResults.instance().update_config_run_status(finished_conf.config_id, RunStatus.SUCCESS)
        completed_tasks += 1
        logging.info(f"Completed task #{completed_tasks} (out of {len(to_run)})")


def meta_configs_from_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.load(f, Loader=SafeLoader)
    for item in data:
        yield item


def main():
    run.config_loger(False, use_log_file=False)

    StoreResults.init(f'{BASE_RESULT_PATH}/stubbornness/')
    clear_db()
    for meta_config in meta_configs_from_yaml(f'{CONFIG_FILES_DIR}/stubbornness_config.yaml'):
        append_configs(**meta_config)
        run_experiments()
    generate_combined()

    StoreResults.init(f'{BASE_RESULT_PATH}/radical_exposure/')
    clear_db()
    for meta_config in meta_configs_from_yaml(f'{CONFIG_FILES_DIR}/radical_exposure_config.yaml'):
        append_configs(**meta_config)
        run_experiments()
    generate_combined()

    StoreResults.init(f'{BASE_RESULT_PATH}/switch_agent_rate/')
    clear_db()
    for meta_config in meta_configs_from_yaml(f'{CONFIG_FILES_DIR}/switch_agent_rate_config.yaml'):
        append_configs(**meta_config)
        run_experiments()
    generate_combined()

    StoreResults.init(f'{BASE_RESULT_PATH}/switch_agent_sigma/')
    clear_db()
    for meta_config in meta_configs_from_yaml(f'{CONFIG_FILES_DIR}/switch_agent_sigma_config.yaml'):
        append_configs(**meta_config)
        run_experiments()
    generate_combined()


if __name__ == '__main__':
    main()
