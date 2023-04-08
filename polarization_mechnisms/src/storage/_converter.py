import json
import string
import uuid

import math
from datetime import datetime, timedelta
from typing import List, Dict
from uuid import UUID

import pandas as pd
from pandas import DataFrame

import storage.constants as db_constants
from analyze.results import MeasurementResult
from experiment.result import ExperimentResult
from run.util import RunStatus
from simulation.config import SimulationConfig, SimulationType
from simulation.result import SimulationResult


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
                json.dumps(iteration_result.get_opinions().tolist())
            ]


def experiment_results_to_df(experiment_result: ExperimentResult) -> DataFrame:
    return pd.DataFrame({
        db_constants.EXPERIMENT_ID: [experiment_result.experiment_id],
        db_constants.TIMESTAMP: [int(experiment_result.timestamp.timestamp())],
        db_constants.RUN_TIME: [experiment_result.run_time.seconds],
        db_constants.CONFIG_ID: [experiment_result.simulation_configs.config_id],
        db_constants.EXPERIMENT_TAGS: [[]]
    })


def _gen_experiment_result(
        simulation_configs: SimulationConfig,
        experiment_id: uuid.UUID,
        timestamp: datetime,
        run_time: timedelta,
        simulation_map: Dict[str, SimulationResult] = None
) -> ExperimentResult:
    result = ExperimentResult(simulation_configs)
    result.experiment_id = experiment_id
    result.timestamp = timestamp
    result.run_time = run_time
    if simulation_map is not None:
        result.simulation_map = simulation_map
    return result


def df_to_experiment_results(
        simulation_configs: List[SimulationConfig],
        experiment_results_df: DataFrame
) -> List[ExperimentResult]:
    simulation_configs_dict = {simulation_config.config_id: simulation_config for simulation_config in
                               simulation_configs}
    result = []
    for row in zip(experiment_results_df[db_constants.EXPERIMENT_ID],
                   experiment_results_df[db_constants.TIMESTAMP],
                   experiment_results_df[db_constants.RUN_TIME],
                   experiment_results_df[db_constants.CONFIG_ID]):
        if uuid.UUID(row[3]) not in simulation_configs_dict:
            continue
        result.append(
            _gen_experiment_result(simulation_configs_dict[uuid.UUID(row[3])], uuid.UUID(row[0]), row[1], row[2]))
    return result


def df_to_measurements(df: DataFrame, experiment_id: UUID, display_name: string) -> List[MeasurementResult]:
    groups_dict = df.groupby(db_constants.MEASUREMENT_TYPE).groups
    result = []
    for measurement_type in groups_dict.keys():
        filtered_df = df[df[db_constants.MEASUREMENT_TYPE] == measurement_type]
        result.append(MeasurementResult(
            filtered_df[db_constants.VALUE].to_numpy(),
            filtered_df[db_constants.SAMPLE_SDT].to_numpy(),
            filtered_df[db_constants.X].to_numpy(),
            experiment_id,
            str(measurement_type),
            display_name)
        )
    return result


def experiment_configs_to_df(simulation_configs: List[SimulationConfig], run_status: RunStatus) -> DataFrame:
    epoch_now = int(datetime.now().timestamp() * 1000)
    return pd.DataFrame(data={
        db_constants.CONFIG_ID: [simulation_config.config_id for simulation_config in simulation_configs],
        db_constants.SIMULATION_TYPE: [simulation_config.simulation_type.name for simulation_config in
                                       simulation_configs],
        db_constants.NUM_OF_AGENTS: [simulation_config.num_of_agents for simulation_config in simulation_configs],
        db_constants.NUM_ITERATIONS: [simulation_config.num_iterations for simulation_config in simulation_configs],
        db_constants.MIO: [simulation_config.mio for simulation_config in simulation_configs],
        db_constants.MIO_SIGMA: [simulation_config.mio_sigma for simulation_config in
                                 simulation_configs],
        db_constants.NUM_OF_REPETITIONS: [simulation_config.num_of_repetitions for simulation_config in
                                          simulation_configs],
        db_constants.SWITCH_AGENT_RATE: [simulation_config.switch_agent_rate for simulation_config in
                                         simulation_configs],
        db_constants.SWITCH_AGENT_SIGMA: [simulation_config.switch_agent_sigma for simulation_config in
                                          simulation_configs],
        db_constants.RADICAL_EXPOSURE_ETA: [simulation_config.radical_exposure_eta for simulation_config in
                                            simulation_configs],
        db_constants.TRUNCATE_AT: [simulation_config.truncate_at for simulation_config in simulation_configs],
        db_constants.EPSILON: [simulation_config.epsilon for simulation_config in simulation_configs],
        db_constants.MARK_STUBBORN_AT: [simulation_config.mark_stubborn_at for simulation_config in simulation_configs],
        db_constants.DISPLAY_NAME: [simulation_config.display_name for simulation_config in simulation_configs],
        db_constants.AUDIT_EVERY_X_ITERATIONS: [simulation_config.audit_iteration_every for simulation_config in
                                                simulation_configs],
        db_constants.STATUS: [run_status] * len(simulation_configs),
        db_constants.TIMESTAMP: [epoch_now] * len(simulation_configs)
    })


def measurements_to_df(measurement_results: List[MeasurementResult]) -> DataFrame:
    df = pd.DataFrame(data={
        db_constants.EXPERIMENT_ID: [],
        db_constants.MEASUREMENT_TYPE: [],
        db_constants.X: [],
        db_constants.VALUE: [],
        db_constants.SAMPLE_SDT: []
    })
    for measurement_result in measurement_results:
        df = df.append(pd.DataFrame(data={
            db_constants.EXPERIMENT_ID: [measurement_result.experiment_id] * len(measurement_result.y),
            db_constants.MEASUREMENT_TYPE: [measurement_result.measurement_type] * len(measurement_result.y),
            db_constants.X: measurement_result.x,
            db_constants.VALUE: measurement_result.y,
            db_constants.SAMPLE_SDT: measurement_result.sample_stds
        }), ignore_index=True)
    return df


def df_to_experiment_configs(row) -> SimulationConfig:
    return SimulationConfig(
        config_id=UUID(row[db_constants.CONFIG_ID]),
        simulation_type=SimulationType[row[db_constants.SIMULATION_TYPE]],
        num_of_agents=int(row[db_constants.NUM_OF_AGENTS]),
        num_iterations=int(row[db_constants.NUM_ITERATIONS]),
        mio=float(row[db_constants.MIO]),
        mio_sigma=None if math.isnan(row[db_constants.MIO_SIGMA]) else float(
            row[db_constants.MIO_SIGMA]),
        num_of_repetitions=int(row[db_constants.NUM_OF_REPETITIONS]),
        switch_agent_rate=None if math.isnan(row[db_constants.SWITCH_AGENT_RATE]) else float(
            row[db_constants.SWITCH_AGENT_RATE]),
        switch_agent_sigma=None if math.isnan(row[db_constants.SWITCH_AGENT_SIGMA]) else float(
            row[db_constants.SWITCH_AGENT_SIGMA]),
        radical_exposure_eta=None if math.isnan(row[db_constants.RADICAL_EXPOSURE_ETA]) else float(
            row[db_constants.RADICAL_EXPOSURE_ETA]),
        truncate_at=float(row[db_constants.TRUNCATE_AT]),
        epsilon=float(row[db_constants.EPSILON]),
        mark_stubborn_at=float(row[db_constants.MARK_STUBBORN_AT]),
        display_name=row[db_constants.DISPLAY_NAME],
        audit_iteration_every=int(float(row[db_constants.AUDIT_EVERY_X_ITERATIONS]))
    )
