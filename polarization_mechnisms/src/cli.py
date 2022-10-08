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
    print(f"before {use_log_file}")
    run.config_loger(False, use_log_file=use_log_file)
    StoreResults.init(base_db_path)


@cli.resultcallback()
def process_result(result, **kwargs):
    click.echo(f'Finished!\n{result}\n{kwargs}')


@cli.command()
def clear_db():
    StoreResults.instance().clear_db()
    StoreResults.instance().bootstrap_db_files()
    logging.info(f"Finished!")


@cli.command()
def append_configs():
    StoreResults.instance().bootstrap_db_files()
    configs_list_to_run = run.configs_to_run()
    StoreResults.instance().add_configs_to_run(configs_list_to_run)
    logging.info(f"Finished!")


@cli.command()
# @click.option("--use_log_file_workers", is_flag=True, show_default=True, default=True, help="Log workers to file.")
@click.option('--max_workers', 'max_workers', type=int, default=12)
@click.option('--max_experiments', 'max_experiments', type=int, default=2000)
def run_experiments(max_workers: int, max_experiments: int):
    to_run = StoreResults.instance().get_configs_to_run(limit=max_experiments)
    logging.info(f"Stating to run {len(to_run)} configs using {max_workers} workers.")
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for finished_conf, finished_results, finished_measurement_results in executor.map(run.run_using_conf, to_run):
            StoreResults.instance().append_measurements(finished_results.experiment_id, finished_measurement_results)
            StoreResults.instance().append_experiment_result(finished_results, store_actual_results=False)
            StoreResults.instance().update_config_run_status(finished_conf.config_id, RunStatus.SUCCESS)
    logging.info(f"Finished!")


@cli.command()
def test_func():
    print(f"HI")


if __name__ == '__main__':
    cli()
