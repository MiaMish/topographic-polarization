import numpy as np
import numpy.testing
import pytest

from analyze import measurment
from experiment.result import ExperimentResult
from simulation.config import SimulationConfig, SimulationType
from simulation.result import SimulationResult, IterationResult


@pytest.fixture(autouse=True)
def run_around_tests():
    np.random.seed(42)
    yield


@pytest.fixture
def simulation_result() -> ExperimentResult:
    first_simulation_result = SimulationResult()
    first_simulation_result.add_iteration_result(0, IterationResult([0.156019, 0.374540, 0.598658, 0.731994, 0.950714]))
    first_simulation_result.add_iteration_result(1, IterationResult([0.156019, 0.374540, 0.598658, 0.731994, 0.950714]))
    first_simulation_result.add_iteration_result(2, IterationResult([0.156019, 0.374540, 0.598658, 0.731994, 0.950714]))
    first_simulation_result.add_iteration_result(3, IterationResult([0.156019, 0.481776, 0.598658, 0.624758, 0.950714]))
    first_simulation_result.add_iteration_result(4, IterationResult([0.156019, 0.481776, 0.598658, 0.624758, 0.950714]))

    second_simulation_result = SimulationResult()
    second_simulation_result.add_iteration_result(0, IterationResult([0.139494, 0.291229, 0.292145, 0.431945, 0.611853]))
    second_simulation_result.add_iteration_result(1, IterationResult([0.139494, 0.292145, 0.333444, 0.389730, 0.611853]))
    second_simulation_result.add_iteration_result(2, IterationResult([0.197679, 0.275259, 0.292145, 0.389730, 0.611853]))
    second_simulation_result.add_iteration_result(3, IterationResult([0.220953, 0.251985, 0.292145, 0.389730, 0.611853]))
    second_simulation_result.add_iteration_result(4, IterationResult([0.220953, 0.251985, 0.388057, 0.389730, 0.515940]))

    third_simulation_result = SimulationResult()
    third_simulation_result.add_iteration_result(0, IterationResult([0.230894, 0.241025, 0.609997, 0.683264, 0.833195]))
    third_simulation_result.add_iteration_result(1, IterationResult([0.230894, 0.241025, 0.676956, 0.683264, 0.766235]))
    third_simulation_result.add_iteration_result(2, IterationResult([0.230894, 0.241025, 0.676956, 0.683264, 0.766235]))
    third_simulation_result.add_iteration_result(3, IterationResult([0.230894, 0.241025, 0.676956, 0.683264, 0.766235]))
    third_simulation_result.add_iteration_result(4, IterationResult([0.230894, 0.241025, 0.676956, 0.683264, 0.766235]))

    fourth_simulation_result = SimulationResult()
    fourth_simulation_result.add_iteration_result(0, IterationResult([0.19639, 0.333412, 0.354446, 0.673702, 0.984192]))
    fourth_simulation_result.add_iteration_result(1, IterationResult([0.19639, 0.333412, 0.354446, 0.673702, 0.984192]))
    fourth_simulation_result.add_iteration_result(2, IterationResult([0.19639, 0.333412, 0.450223, 0.577925, 0.984192]))
    fourth_simulation_result.add_iteration_result(3, IterationResult([0.19639, 0.333412, 0.450223, 0.577925, 0.984192]))
    fourth_simulation_result.add_iteration_result(4, IterationResult([0.19639, 0.333412, 0.450223, 0.577925, 0.984192]))

    experiment_result = ExperimentResult()
    experiment_result.add_simulation_result(0, first_simulation_result)
    experiment_result.add_simulation_result(1, second_simulation_result)
    experiment_result.add_simulation_result(2, third_simulation_result)
    experiment_result.add_simulation_result(3, fourth_simulation_result)
    return experiment_result


@pytest.fixture
def simulation_conf() -> SimulationConfig:
    return SimulationConfig(
        simulation_type=SimulationType.SIMILARITY,
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


def test_spread(simulation_result, simulation_conf):
    actual = measurment.spread(simulation_result, simulation_conf)
    expected = np.array([0.66428925, 0.64754925, 0.633003, 0.6271845, 0.60320625])
    print(f"Expected:\n"
          f"{expected}\n"
          f"Actual\n"
          f"{actual}")
    numpy.testing.assert_almost_equal(actual, expected)
    #     plt.plot(spreads)
    #     plt.show()


def test_dispersion(simulation_result, simulation_conf):
    actual = measurment.dispersion(simulation_result, simulation_conf)
    expected = np.array([0.0603636, 0.05890159, 0.05597123, 0.0531616, 0.05101511])
    print(f"Expected:\n"
          f"{expected}\n"
          f"Actual\n"
          f"{actual}")
    numpy.testing.assert_almost_equal(actual, expected)


def test_covered_bins(simulation_result, simulation_conf):
    actual = measurment.covered_bins(simulation_result, simulation_conf)
    expected = np.array([0.4, 0.4, 0.425, 0.4, 0.4])
    print(f"Expected:\n"
          f"{expected}\n"
          f"Actual\n"
          f"{actual}")
    numpy.testing.assert_almost_equal(actual, expected)


def test_num_of_clusters(simulation_result, simulation_conf):
    actual = measurment.num_of_clusters(simulation_result, simulation_conf)
    expected = np.array([2, 2, 2, 2.25, 2.25])
    print(f"Expected:\n"
          f"{expected}\n"
          f"Actual\n"
          f"{actual}")
    numpy.testing.assert_almost_equal(actual, expected)
