import csv
import datetime
import json
import os
import uuid
from typing import Dict
from uuid import UUID

from numpy import ndarray

import storage.constants as db_constants
from analyze.measurment import MeasurementType
from experiment.result import ExperimentResult
from simulation.config import SimulationConfig, SimulationType
from simulation.result import SimulationResult, IterationResult
from storage import _converter as converter


class DataCorruption(Exception):
    pass


class StoreResults:

    def __init__(self, base_path: str) -> None:
        self.base_path = base_path

    def bootstrap_db_files(self, force: bool = False) -> None:
        print(f"Bootstrapping DB in {self.base_path}")
        for table_name, table_fields in db_constants.TABLES.items():
            if force or not os.path.isfile(self.base_path + table_name):
                print(f"Bootstrapping {table_name}...")
                with open(self.base_path + table_name, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(table_fields)

    def append_measurement(self, experiment_result: ExperimentResult, measurement: ndarray,
                           measurement_type: MeasurementType):
        print(f"Appending to {db_constants.MEASUREMENTS}...")
        with open(self.base_path + db_constants.MEASUREMENTS, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(converter.measurement_to_rows(experiment_result, measurement, measurement_type))

    def append_experiment_result(self, experiment_result: ExperimentResult):
        start = datetime.datetime.now()

        print(f"Appending to {db_constants.EXPERIMENT_CONFIGS}...")
        with open(self.base_path + db_constants.EXPERIMENT_CONFIGS, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(converter.experiment_config_to_row(experiment_result.simulation_configs))

        print(f"Appending to {db_constants.EXPERIMENT_RESULT}...")
        with open(self.base_path + db_constants.EXPERIMENT_RESULT, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(converter.experiment_results_to_row(experiment_result))

        print(f"Appending to {db_constants.SIMULATION_RESULT}...")
        with open(self.base_path + db_constants.SIMULATION_RESULT, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(converter.simulation_results_to_rows(experiment_result))

        print(f"Appending to {db_constants.ITERATION_RESULT}...")
        with open(self.base_path + db_constants.ITERATION_RESULT, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(converter.iteration_results_to_rows(experiment_result))

        print(f"Finished appending experiment result with ID {experiment_result.experiment_id} to DB."
              f"Took {(datetime.datetime.now() - start).seconds} seconds.")

    def retrieve_configuration(self, config_id: UUID) -> SimulationConfig or None:
        print(f"Reading from {db_constants.EXPERIMENT_CONFIGS}...")
        with open(self.base_path + db_constants.EXPERIMENT_CONFIGS, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row[db_constants.CONFIG_ID] != str(config_id):
                    continue
                simulation_config = SimulationConfig(
                    simulation_type=SimulationType[row[db_constants.SIMULATION_TYPE]],
                    num_of_agents=int(row[db_constants.NUM_OF_AGENTS]),
                    num_iterations=int(row[db_constants.NUM_ITERATIONS]),
                    mio=float(row[db_constants.MIO]),
                    num_of_repetitions=int(row[db_constants.NUM_OF_REPETITIONS]),
                    switch_agent_rate=None if row[db_constants.SWITCH_AGENT_RATE] == '' else float(
                        row[db_constants.SWITCH_AGENT_RATE]),
                    switch_agent_sigma=None if row[db_constants.SWITCH_AGENT_SIGMA] == '' else float(
                        row[db_constants.SWITCH_AGENT_SIGMA]),
                    radical_exposure_eta=None if row[db_constants.RADICAL_EXPOSURE_ETA] == '' else float(
                        row[db_constants.RADICAL_EXPOSURE_ETA]),
                    truncate_at=float(row[db_constants.TRUNCATE_AT]),
                    epsilon=float(row[db_constants.EPSILON]),
                    mark_stubborn_at=float(row[db_constants.MARK_STUBBORN_AT]),
                    display_name=row[db_constants.DISPLAY_NAME]
                )
                simulation_config.config_id = row[db_constants.CONFIG_ID]
                return simulation_config
        return None

    def retrieve_iteration_results(self, experiment_id: UUID, repetition: int) -> Dict[str, IterationResult]:
        print(f"Reading from {db_constants.ITERATION_RESULT}...")
        iteration_results = {}
        with open(self.base_path + db_constants.ITERATION_RESULT, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row[db_constants.EXPERIMENT_ID] != str(experiment_id) or row[db_constants.REPETITION] != str(
                        repetition):
                    continue
                opinions_list = json.loads(row[db_constants.OPINIONS_LIST])
                iteration_result = IterationResult(opinions_list)
                iteration_result.experiment_id = experiment_id
                iteration_result.repetition = repetition
                iteration_result.iteration = row[db_constants.ITERATION]
                iteration_results[row[db_constants.ITERATION]] = iteration_result
        return iteration_results

    def retrieve_simulation_result(self, experiment_id: UUID, repetition: int) -> SimulationResult or None:
        print(f"Reading from {db_constants.SIMULATION_RESULT}...")
        with open(self.base_path + db_constants.SIMULATION_RESULT, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row[db_constants.EXPERIMENT_ID] != str(experiment_id) or row[db_constants.REPETITION] != str(
                        repetition):
                    continue
                simulation_result = SimulationResult()
                simulation_result.timestamp = datetime.datetime.fromtimestamp(int(row[db_constants.TIMESTAMP]))
                simulation_result.run_time = datetime.timedelta(seconds=int(row[db_constants.RUN_TIME]))
                simulation_result.iteration_map = self.retrieve_iteration_results(experiment_id, repetition)
                return simulation_result
        return None

    def retrieve_experiment_results(self, experiment_id: UUID) -> ExperimentResult or None:
        print(f"Reading from {db_constants.EXPERIMENT_RESULT}...")
        with open(self.base_path + db_constants.EXPERIMENT_RESULT, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row[db_constants.EXPERIMENT_ID] != str(experiment_id):
                    continue
                config_id = uuid.UUID(row[db_constants.CONFIG_ID])
                simulation_config = self.retrieve_configuration(config_id)
                if simulation_config is None:
                    raise DataCorruption(f"experiment_id exist in {db_constants.EXPERIMENT_RESULT} table, "
                                         f"but the related config (ID: {config_id}) was not found.")
                experiment_result = ExperimentResult(simulation_config)
                experiment_result.experiment_id = experiment_id
                experiment_result.timestamp = datetime.datetime.fromtimestamp(int(row[db_constants.TIMESTAMP]))
                experiment_result.run_time = datetime.timedelta(seconds=int(row[db_constants.RUN_TIME]))
                for repetition in range(simulation_config.num_of_repetitions):
                    experiment_result.add_simulation_result(repetition,
                                                            self.retrieve_simulation_result(experiment_id, repetition))
                simulation_config.audited_iterations = None
                experiment_result.simulation_configs = simulation_config
                return experiment_result
        return None

    def retrieve_experiment_ids(self) -> set[UUID]:
        result = set()
        print(f"Reading from {db_constants.EXPERIMENT_RESULT}...")
        with open(self.base_path + db_constants.EXPERIMENT_RESULT, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                result.add(uuid.UUID(row[db_constants.EXPERIMENT_ID]))
        return result
