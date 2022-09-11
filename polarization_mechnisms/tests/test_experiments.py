import logging
import random
from typing import Callable, Dict

import numpy
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from experiment.experiment import Experiment
from simulation.config import SimulationConfig, SimulationType


@pytest.fixture(autouse=True)
def run_around_tests():
    numpy.random.seed(42)
    yield


@pytest.fixture
def vanilla_simulation_conf() -> Callable[[SimulationType], SimulationConfig]:
    return lambda simulation_type: SimulationConfig(
        simulation_type=simulation_type,
        num_of_agents=5,
        num_iterations=5,
        mio=0.3,
        num_of_repetitions=2,
        switch_agent_rate=None,
        switch_agent_sigma=None,
        radical_exposure_eta=None,
        truncate_at=0.001,
        epsilon=0.4,
        mark_stubborn_at=0.1,
        audit_iteration_predicate=lambda iteration_index: True)


def _run_experiment(simulation_config: SimulationConfig, expected: Dict[str, pd.DataFrame]):
    experiment = Experiment(simulation_config)
    results = experiment.run_experiment()
    for repetition in range(simulation_config.num_of_repetitions):
        simulation_results_df = results.get_simulation_result_at(repetition).get_results_df()
        print(f"Repetition {repetition}\n"
              f"Expected:\n"
              f"{expected.get(str(repetition))}\n"
              f"Actual:\n"
              f"{simulation_results_df}")
        assert_frame_equal(simulation_results_df, expected.get(str(repetition)))


def test_similarity_vanilla(vanilla_simulation_conf):
    simulation_config = vanilla_simulation_conf(SimulationType.SIMILARITY)
    expected = {
        "0": pd.DataFrame([
            [0.156019, 0.374540, 0.598658, 0.731994, 0.950714],
            [0.156019, 0.374540, 0.598658, 0.731994, 0.950714],
            [0.156019, 0.374540, 0.598658, 0.731994, 0.950714],
            [0.156019, 0.481776, 0.598658, 0.624758, 0.950714],
            [0.156019, 0.481776, 0.598658, 0.624758, 0.950714],
        ], index=['0', '1', '2', '3', '4']),
        "1": pd.DataFrame([
            [0.139494, 0.291229, 0.292145, 0.431945, 0.611853],
            [0.139494, 0.292145, 0.333444, 0.389730, 0.611853],
            [0.197679, 0.275259, 0.292145, 0.389730, 0.611853],
            [0.220953, 0.251985, 0.292145, 0.389730, 0.611853],
            [0.220953, 0.251985, 0.388057, 0.389730, 0.515940],
        ], index=['0', '1', '2', '3', '4'])
    }
    _run_experiment(simulation_config, expected)


def test_assimilation_vanilla(vanilla_simulation_conf):
    simulation_config = vanilla_simulation_conf(SimulationType.ASSIMILATION)
    expected = {
        "0": pd.DataFrame([
            [0.156019, 0.374540, 0.598658, 0.731994, 0.950714],
            [0.308998, 0.446259, 0.584406, 0.667818, 0.950714],
            [0.415491, 0.501633, 0.586485, 0.638776, 0.950714],
            [0.492102, 0.546092, 0.597929, 0.630813, 0.950714],
            [0.549276, 0.583050, 0.614456, 0.635228, 0.950714],
        ], index=['0', '1', '2', '3', '4']),
        "1": pd.DataFrame([
            [0.597900, 0.775133, 0.894827, 0.939499, 0.969585],
            [0.686553, 0.798032, 0.872175, 0.939499, 0.969585],
            [0.748663, 0.818871, 0.864756, 0.939499, 0.969585],
            [0.793184, 0.837474, 0.865838, 0.939499, 0.969585],
            [0.825862, 0.853865, 0.871371, 0.939499, 0.969585],
        ], index=['0', '1', '2', '3', '4'])
    }
    _run_experiment(simulation_config, expected)


def test_repulsive_vanilla(vanilla_simulation_conf):
    simulation_config = vanilla_simulation_conf(SimulationType.REPULSIVE)
    expected = {
        "0": pd.DataFrame([
            [0.156019, 0.374540, 0.598658, 0.731994, 0.950714],
            [0.156019, 0.328836, 0.598658, 0.731994, 0.905010],
            [0.156019, 0.283131, 0.598658, 0.731994, 0.859305],
            [0.156019, 0.313813, 0.598658, 0.762676, 0.859305],
            [0.092024, 0.313813, 0.598658, 0.698682, 0.859305],
        ], index=['0', '1', '2', '3', '4']),
        "1": pd.DataFrame([
            [0.139494, 0.291229, 0.292145, 0.431945, 0.611853],
            [0.139494, 0.292145, 0.506800, 0.611853, 0.647515],
            [0.219110, 0.292145, 0.586416, 0.611853, 0.647515],
            [0.292145, 0.298727, 0.611853, 0.647515, 0.666033],
            [0.298727, 0.400320, 0.647515, 0.666033, 0.720028],
        ], index=['0', '1', '2', '3', '4'])
    }
    _run_experiment(simulation_config, expected)
