#!/usr/bin/env python3
import concurrent
import logging
import click
import concurrent.futures
import run.run as run
from run.util import RunStatus
from storage.results import StoreResults


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
def append_configs():
    StoreResults.instance().bootstrap_db_files()
    configs_list_to_run = run.configs_to_run()
    StoreResults.instance().add_configs_to_run(configs_list_to_run)


@cli.command()
# @click.option("--use_log_file_workers", is_flag=True, show_default=True, default=True, help="Log workers to file.")
@click.option('--max_workers', 'max_workers', type=int, default=12)
@click.option('--max_experiments', 'max_experiments', type=int, default=2000)
def run_experiments(max_workers: int, max_experiments: int):
    to_run = StoreResults.instance().get_configs_to_run(limit=max_experiments)
    logging.info(f"Stating to run {len(to_run)} configs using {max_workers} workers.")
    if max_workers == 1:
        completed_tasks = 0
        for conf_to_run in to_run:
            finished_conf, finished_results, finished_measurement_results = run.run_using_conf(conf_to_run)
            StoreResults.instance().append_measurements(finished_results.experiment_id, finished_measurement_results)
            StoreResults.instance().append_experiment_result(finished_results, store_actual_results=False)
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
