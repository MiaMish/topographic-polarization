#!/usr/bin/env python3
import concurrent
import concurrent.futures
import logging
import click
import analyze.measurement.constants as measurement_constants
import run.run as run
import storage.constants as db_constants
from run.util import RunStatus
from simulation.config import SimulationType
from storage.results import StoreResults

DEFAULT_NUM_OF_AGENTS = 100
DEFAULT_NUM_OF_ITERATIONS = 10000
DEFAULT_NUM_OF_REPETITIONS = 40


@click.group()
@click.option("--use_log_file", is_flag=True, show_default=True, default=False, help="Log master process to file.")
@click.option('--base_db_path', 'base_db_path', type=str, default=run.BASE_DB_PATH)
def cli(use_log_file: bool, base_db_path: str):
    run.config_loger(False, use_log_file=use_log_file)
    StoreResults.init(base_db_path)


@cli.resultcallback()
def process_result(result, **kwargs):
    click.echo(f'Finished!')


@cli.command()
def clear_db():
    StoreResults.instance().clear_db()
    StoreResults.instance().bootstrap_db_files()

@cli.command()
@click.option('--simulation_types', 'simulation_types', type=str, default="SIMILARITY,REPULSIVE")
@click.option('--num_of_agents', 'num_of_agents', type=str, default=f"{DEFAULT_NUM_OF_AGENTS}")
@click.option('--num_iterations', 'num_iterations', type=str, default=f"{DEFAULT_NUM_OF_ITERATIONS}")
@click.option('--mios', 'mios', type=str, default="0.2,0.4")
@click.option('--num_of_repetitions', 'num_of_repetitions', type=str, default=f"{DEFAULT_NUM_OF_REPETITIONS}")
@click.option('--switch_agent_rates', 'switch_agent_rates', type=str, default="None,5")
@click.option('--switch_agent_sigmas', 'switch_agent_sigmas', type=str, default="None,0.2")
@click.option('--radical_exposure_etas', 'radical_exposure_etas', type=str, default="None,0.2")
@click.option('--epsilons', 'epsilons', type=str, default="0.2,0.4,0.6")
def append_configs(
        simulation_types: str,
        num_of_agents: str,
        num_iterations: str,
        mios: str,
        num_of_repetitions: str,
        switch_agent_rates: str,
        switch_agent_sigmas: str,
        radical_exposure_etas: str,
        epsilons: str
):
    StoreResults.instance().bootstrap_db_files()
    configs_list_to_run = run.configs_to_run(
        simulation_types=[SimulationType.SIMILARITY if t == "SIMILARITY" else SimulationType.REPULSIVE for t in
                          simulation_types.split(",")],
        num_of_agents=[int(n) if n != "None" else None for n in num_of_agents.split(",")],
        num_iterations=[int(n) if n != "None" else None for n in num_iterations.split(",")],
        mios=[float(n) if n != "None" else None for n in mios.split(",")],
        num_of_repetitions=[int(n) if n != "None" else None for n in num_of_repetitions.split(",")],
        switch_agent_rates=[int(n) if n != "None" else None for n in switch_agent_rates.split(",")],
        switch_agent_sigmas=[float(n) if n != "None" else None for n in switch_agent_sigmas.split(",")],
        radical_exposure_etas=[float(n) if n != "None" else None for n in radical_exposure_etas.split(",")],
        epsilons=[float(n) if n != "None" else None for n in epsilons.split(",")]
    )
    StoreResults.instance().add_configs_to_run(configs_list_to_run)


@cli.command()
@click.option('--simulation_type', 'simulation_type', type=click.Choice(["SIMILARITY", "REPULSIVE"]))
@click.option('--num_of_agent',  'num_of_agent', type=int, default=DEFAULT_NUM_OF_AGENTS)
@click.option('--num_iteration', 'num_iteration', type=int, default=DEFAULT_NUM_OF_ITERATIONS)
@click.option('--mio', 'mio', type=float, default=None)
@click.option('--num_of_repetition', 'num_of_repetition', type=int, default=DEFAULT_NUM_OF_REPETITIONS)
@click.option('--switch_agent_rate', 'switch_agent_rate', type=str, default=None)
@click.option('--switch_agent_sigma', 'switch_agent_sigma', type=str, default=None)
@click.option('--radical_exposure_eta', 'radical_exposure_eta', type=str, default=None)
@click.option('--epsilon', 'epsilon', type=str, default=None)
@click.option('--measurement_type', 'measurement_type', type=click.Choice([
    measurement_constants.NUM_OF_CLUSTERS,
    measurement_constants.COVERED_BINS,
    measurement_constants.DISCONNECT_INDEX,
    measurement_constants.DISPERSION,
    measurement_constants.NUM_OF_LOCAL_MAX,
    measurement_constants.RIPLEY_ESTIMATOR,
    measurement_constants.SPREAD]
))
@click.option('--store_file', 'store_file', type=str)
def scatter_plot(
        simulation_type: str,
        num_of_agent: int,
        num_iteration: int,
        mio: int,
        num_of_repetition: int,
        switch_agent_rate: str,
        switch_agent_sigma: str,
        radical_exposure_eta: str,
        epsilon: str,
        measurement_type: str,
        store_file: str
):
    filters = {
        db_constants.SIMULATION_TYPE: simulation_type,
        db_constants.NUM_OF_AGENTS: num_of_agent,
        db_constants.NUM_ITERATIONS: num_iteration,
        db_constants.NUM_OF_REPETITIONS: num_of_repetition
    }

    if mio is not None:
        filters[db_constants.MIO] = mio
    if switch_agent_rate is not None:
        filters[db_constants.SWITCH_AGENT_RATE] = int(switch_agent_rate) if switch_agent_rate != "None" else None
    if switch_agent_sigma is not None:
        filters[db_constants.SWITCH_AGENT_SIGMA] = float(switch_agent_sigma) if switch_agent_sigma != "None" else None
    if radical_exposure_eta is not None:
        filters[db_constants.RADICAL_EXPOSURE_ETA] = float(radical_exposure_eta) if radical_exposure_eta != "None" else None
    if epsilon is not None:
        filters[db_constants.EPSILON] = float(epsilon) if epsilon != "None" else None

    run.scatter_plot(filters, measurement_type, store_file)


@cli.command()
def generate_combined():
    StoreResults.instance().combine_db_to_single_table()

@cli.command()
# @click.option("--use_log_file_workers", is_flag=True, show_default=True, default=True, help="Log workers to file.")
@click.option('--max_workers', 'max_workers', type=int, default=12)
@click.option('--max_experiments', 'max_experiments', type=int, default=2000)
@click.option("--generate_gif", is_flag=True, default=False)
def run_experiments(max_workers: int, max_experiments: int, generate_gif: bool):
    to_run = StoreResults.instance().get_configs_to_run(limit=max_experiments)
    logging.info(f"Stating to run {len(to_run)} configs using {max_workers} workers.")
    if max_workers == 1:
        completed_tasks = 0
        for conf_to_run in to_run:
            finished_conf, finished_results, finished_measurement_results = run.run_using_conf(conf_to_run)
            StoreResults.instance().append_measurements(finished_results.experiment_id, finished_measurement_results)
            StoreResults.instance().append_experiment_result(finished_results, store_actual_results=False, generate_gif=generate_gif)
            StoreResults.instance().update_config_run_status(finished_conf.config_id, RunStatus.SUCCESS)
            completed_tasks += 1
            logging.info(f"Completed task #{completed_tasks} (out of {len(to_run)})")
        return

    pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
    futures_list = [pool.submit(run.run_using_conf, conf_to_run) for conf_to_run in to_run]
    completed_tasks = 0
    for completed_future in concurrent.futures.as_completed(futures_list):
        exception = completed_future.exception()
        if exception is not None:
            raise exception
        finished_conf, finished_results, finished_measurement_results = completed_future.result()
        StoreResults.instance().append_measurements(finished_results.experiment_id, finished_measurement_results)
        StoreResults.instance().append_experiment_result(finished_results, store_actual_results=False)
        StoreResults.instance().update_config_run_status(finished_conf.config_id, RunStatus.SUCCESS)
        completed_tasks += 1
        logging.info(f"Completed task #{completed_tasks} (out of {len(to_run)})")


@cli.command()
def test_func():
    click.echo(f"I'm here so you will be able to test the cli :)")


if __name__ == '__main__':
    cli()
