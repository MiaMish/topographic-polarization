import logging
import os
import shutil
import string
from pathlib import Path
from typing import List, Dict, Any, Callable
from uuid import UUID

import pandas as pd

import storage.constants as db_constants
from analyze.analyzer import avg_results_gif
from analyze.results import MeasurementResult
from experiment.result import ExperimentResult
from run.util import RunStatus
from simulation.config import SimulationConfig
from storage import _converter as converter


class DataCorruption(Exception):
    pass


class StoreResults:

    __instance = None

    @staticmethod
    def instance():
        if StoreResults.__instance is None:
            raise Exception("Not initialized!")
        return StoreResults.__instance

    @staticmethod
    def init(base_path: str):
        StoreResults(base_path)
        logging.info(f"Initialized DB instance for path: {base_path}")

    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        if StoreResults.__instance is not None:
            logging.warning("Already initialized!")
        StoreResults.__instance = self

    def clear_db(self):
        logging.info(f"Clearing DB from: {self.base_path}")
        try:
            shutil.rmtree(self.base_path)
        except FileNotFoundError:
            logging.info("Nothing to delete, DB is already clear.")
        logging.info(f"DB is cleared from {self.base_path}")

    def bootstrap_db_files(self, force: bool = False) -> None:
        logging.info(f"Bootstrapping DB in {self.base_path}")
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
        Path(f"{self.base_path}/figures/").mkdir(parents=True, exist_ok=True)
        for table_name, table_fields in db_constants.TABLES.items():
            if table_name == db_constants.MEASUREMENTS:
                continue
            if force or not os.path.isfile(self.base_path + table_name):
                logging.info(f"Bootstrapping {table_name}...")
                pd.DataFrame(data={table_field: [] for table_field in table_fields}).to_csv(self.base_path + table_name, index=False, na_rep='NULL')
        logging.info(f"DB is bootstrapped in {self.base_path}")

    def bootstrap_measurement_file_if_needed(self, experiment_id: UUID):
        directory_path = self.base_path + self._partition_prefix(experiment_id)
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(directory_path + db_constants.MEASUREMENTS):
            pd.DataFrame({table_field: [] for table_field in db_constants.TABLES[db_constants.MEASUREMENTS]})\
                .to_csv(directory_path + db_constants.MEASUREMENTS, index=False, na_rep='NULL')

    def append_measurements(self, experiment_id: UUID, measurement_results: List[MeasurementResult]):
        self.bootstrap_measurement_file_if_needed(experiment_id)
        directory_path = self.base_path + self._partition_prefix(experiment_id)
        existing_df = pd.read_csv(directory_path + db_constants.MEASUREMENTS, na_values=['NULL'])
        as_df = converter.measurements_to_df(measurement_results)
        existing_df = existing_df.append(as_df, ignore_index=True)
        existing_df.to_csv(directory_path + db_constants.MEASUREMENTS, index=False, na_rep='NULL')

    def retrieve_measurement_results_for_experiment(self, experiment_id: UUID, display_name: string) -> List[MeasurementResult]:
        directory_path = self.base_path + self._partition_prefix(experiment_id)
        from_db = pd.read_csv(directory_path + db_constants.MEASUREMENTS, na_values=['NULL'])
        filtered_df = from_db[from_db[db_constants.EXPERIMENT_ID] == str(experiment_id)]
        a = converter.df_to_measurements(filtered_df, experiment_id, display_name)
        return a

    def retrieve_measurement_results(self) -> List[MeasurementResult]:
        return self.retrieve_measurement_results_for_configs(self.retrieve_configurations(), lambda simulation_config: simulation_config.display_name)

    def retrieve_measurement_results_for_configs(self, simulation_configs: List[SimulationConfig], display_name_extractor: Callable[[SimulationConfig], str]) -> List[MeasurementResult]:
        experiment_results_df = pd.read_csv(self.base_path + db_constants.EXPERIMENT_RESULT, na_values=['NULL'])
        experiment_results = converter.df_to_experiment_results(simulation_configs, experiment_results_df)
        results = []
        for experiment_result in experiment_results:
            display_name = display_name_extractor(experiment_result.simulation_configs)
            results = results + (self.retrieve_measurement_results_for_experiment(experiment_result.experiment_id, display_name))
        return results

    def append_experiment_result(self, experiment_result: ExperimentResult, store_actual_results: bool = True, generate_gif: bool = True):
        existing_df = pd.read_csv(self.base_path + db_constants.EXPERIMENT_RESULT, na_values=['NULL'])
        existing_df = existing_df.append(converter.experiment_results_to_df(experiment_result), ignore_index=True)
        existing_df.to_csv(self.base_path + db_constants.EXPERIMENT_RESULT, index=False, na_rep='NULL')
        if generate_gif:
            gif_path = f"{self.base_path}/figures/{experiment_result.experiment_id}.gif"
            avg_results_gif(experiment_result.simulation_configs, experiment_result, gif_path)
            logging.info(f"Stored gif in: {gif_path}")
        # if store_actual_results:
        #     logging.debug(f"Appending to {db_constants.SIMULATION_RESULT}...")
        #     with open(self.base_path + db_constants.SIMULATION_RESULT, 'a') as csv_file:
        #         writer = csv.writer(csv_file)
        #         writer.writerows(converter.simulation_results_to_rows(experiment_result))
        #
        #     logging.debug(f"Appending to {db_constants.ITERATION_RESULT}...")
        #     with open(self.base_path + db_constants.ITERATION_RESULT, 'a') as csv_file:
        #         writer = csv.writer(csv_file)
        #         writer.writerows(converter.iteration_results_to_rows(experiment_result))

    def retrieve_configurations(self, filters: Dict[str, Any] = None) -> List[SimulationConfig]:
        from_db = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        filtered_df = from_db
        logging.info("Total configs from DB: %s", len(filtered_df))
        for filter_by in filters.keys() if filters is not None else []:
            if filters[filter_by] is None:
                filtered_df = filtered_df[filtered_df[filter_by].isnull()]
            else:
                filtered_df = filtered_df[filtered_df[filter_by] == filters[filter_by]]
            logging.info("Total filtered configs by %s=%s. Num of configs after filtering configs: %s", filter_by, filters[filter_by], len(filtered_df))
        return [converter.df_to_experiment_configs(row) for index, row in filtered_df.iterrows()]

    def retrieve_configuration(self, config_id: UUID) -> SimulationConfig or None:
        from_db = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        filtered_df = from_db[from_db[db_constants.CONFIG_ID] == str(config_id)]
        if filtered_df.shape[0] == 0:
            return None
        return converter.df_to_experiment_configs(filtered_df.iloc[0])

    # def retrieve_iteration_results(self, experiment_id: UUID, repetition: int) -> Dict[str, IterationResult]:
    #     logging.debug(f"Reading from {db_constants.ITERATION_RESULT}...")
    #     iteration_results = {}
    #     with open(self.base_path + db_constants.ITERATION_RESULT, 'r') as csv_file:
    #         reader = csv.DictReader(csv_file)
    #         for row in reader:
    #             if row[db_constants.EXPERIMENT_ID] != str(experiment_id) or row[db_constants.REPETITION] != str(
    #                     repetition):
    #                 continue
    #             opinions_list = json.loads(row[db_constants.OPINIONS_LIST])
    #             iteration_result = IterationResult(opinions_list)
    #             iteration_result.experiment_id = experiment_id
    #             iteration_result.repetition = repetition
    #             iteration_result.iteration = row[db_constants.ITERATION]
    #             iteration_results[row[db_constants.ITERATION]] = iteration_result
    #     return iteration_results
    #
    # def retrieve_simulation_result(self, experiment_id: UUID, repetition: int) -> SimulationResult or None:
    #     logging.debug(f"Reading from {db_constants.SIMULATION_RESULT}...")
    #     with open(self.base_path + db_constants.SIMULATION_RESULT, 'r') as csv_file:
    #         reader = csv.DictReader(csv_file)
    #         for row in reader:
    #             if row[db_constants.EXPERIMENT_ID] != str(experiment_id) or row[db_constants.REPETITION] != str(
    #                     repetition):
    #                 continue
    #             simulation_result = SimulationResult()
    #             simulation_result.timestamp = datetime.datetime.fromtimestamp(int(row[db_constants.TIMESTAMP]))
    #             simulation_result.run_time = datetime.timedelta(seconds=int(row[db_constants.RUN_TIME]))
    #             simulation_result.iteration_map = self.retrieve_iteration_results(experiment_id, repetition)
    #             return simulation_result
    #     return None
    #
    # def retrieve_experiment_results(self, experiment_id: UUID) -> ExperimentResult or None:
    #     logging.debug(f"Reading from {db_constants.EXPERIMENT_RESULT}...")
    #     with open(self.base_path + db_constants.EXPERIMENT_RESULT, 'r') as csv_file:
    #         reader = csv.DictReader(csv_file)
    #         for row in reader:
    #             if row[db_constants.EXPERIMENT_ID] != str(experiment_id):
    #                 continue
    #             config_id = uuid.UUID(row[db_constants.CONFIG_ID])
    #             simulation_config = self.retrieve_configuration(config_id)
    #             if simulation_config is None:
    #                 raise DataCorruption(f"experiment_id exist in {db_constants.EXPERIMENT_RESULT} table, "
    #                                      f"but the related config (ID: {config_id}) was not found.")
    #             experiment_result = ExperimentResult(simulation_config)
    #             experiment_result.experiment_id = experiment_id
    #             experiment_result.timestamp = datetime.datetime.fromtimestamp(int(row[db_constants.TIMESTAMP]))
    #             experiment_result.run_time = datetime.timedelta(seconds=int(row[db_constants.RUN_TIME]))
    #             for repetition in range(simulation_config.num_of_repetitions):
    #                 experiment_result.add_simulation_result(repetition,
    #                                                         self.retrieve_simulation_result(experiment_id, repetition))
    #             simulation_config.audited_iterations = None
    #             experiment_result.simulation_configs = simulation_config
    #             return experiment_result
    #     return None
    #
    # def retrieve_experiment_ids(self) -> set[UUID]:
    #     result = set()
    #     logging.debug(f"Reading from {db_constants.EXPERIMENT_RESULT}...")
    #     with open(self.base_path + db_constants.EXPERIMENT_RESULT, 'r') as csv_file:
    #         reader = csv.DictReader(csv_file)
    #         for row in reader:
    #             result.add(uuid.UUID(row[db_constants.EXPERIMENT_ID]))
    #     return result
    #
    # def retrieve_measurement_results(self, experiment_id: UUID, measurement_type: str) -> MeasurementResult:
    #     logging.debug(f"Reading from {db_constants.MEASUREMENTS}...")
    #     Path(self.base_path + self._partition_prefix(experiment_id)).mkdir(parents=True, exist_ok=True)
    #     df = pd.read_csv(self.base_path + self._partition_prefix(experiment_id) + db_constants.MEASUREMENTS)
    #     filtered_df = df[(df[db_constants.EXPERIMENT_ID] == str(experiment_id)) &
    #                      (df[db_constants.MEASUREMENT_TYPE] == measurement_type)]
    #     return MeasurementResult(
    #         experiment_id=experiment_id,
    #         measurement_type=measurement_type,
    #         x=filtered_df[db_constants.X],
    #         y=filtered_df[db_constants.VALUE]
    #     )

    @staticmethod
    def _partition_prefix(id_for_partition: UUID) -> str:
        # return f"{id_for_partition.hex[0]}/{id_for_partition.hex[1]}/"
        return ""

    def add_configs_to_run(self, configs: List[SimulationConfig]):
        from_db = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        df_merged = from_db.append(converter.experiment_configs_to_df(configs, RunStatus.PENDING), ignore_index=True)
        df_merged.to_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, index=False, na_rep='NULL')

    def update_config_run_status(self, config_id: UUID, new_status: RunStatus):
        from_db = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        from_db.loc[from_db[db_constants.CONFIG_ID] == str(config_id), db_constants.STATUS] = str(new_status)
        from_db.to_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, index=False, na_rep='NULL')

    def get_configs_to_run(self, limit: int = 5000) -> List[SimulationConfig]:
        from_db = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        pending_df = from_db[from_db[db_constants.STATUS] == str(RunStatus.PENDING)]
        limited_pending_df = pending_df.head(n=limit)
        logging.debug(f"Total configs in DB: {from_db.shape[0]}, "
                      f"out of them {pending_df.shape[0]} in {RunStatus.PENDING} status. "
                      f"Using limit of {limit}.")
        return [converter.df_to_experiment_configs(row) for index, row in limited_pending_df.iterrows()]

    def combine_db_to_single_table(self):
        configs_df = pd.read_csv(self.base_path + db_constants.EXPERIMENT_CONFIGS, na_values=['NULL'])
        experiment_results_df = pd.read_csv(self.base_path + db_constants.EXPERIMENT_RESULT, na_values=['NULL'])
        measurements_df = pd.read_csv(self.base_path + db_constants.MEASUREMENTS, na_values=['NULL'])
        experiment_results_combined = pd.merge(experiment_results_df, configs_df, on=db_constants.CONFIG_ID, how="left")
        experiment_results_combined.to_csv(self.base_path + db_constants.COMBINED_EXPERIMENT, index=False, na_rep='NULL')
        combined_df = pd.merge(measurements_df, experiment_results_combined, on=db_constants.EXPERIMENT_ID, how="left")
        combined_df.to_csv(self.base_path + db_constants.COMBINED_MEASUREMENTS, index=False, na_rep='NULL')
