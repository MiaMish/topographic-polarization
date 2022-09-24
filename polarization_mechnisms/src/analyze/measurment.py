import numpy as np
from numpy import mean, ndarray, var
from sklearn.cluster import KMeans

from experiment.result import ExperimentResult
from simulation.config import SimulationConfig

# TODO - all functions here have REALLY bad performance and it's easy to fix it...


# Bramson et el., 2016 section 2.1
def spread(experiment_result: ExperimentResult, simulation_config: SimulationConfig) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(max(iteration_result.opinions_list) - min(iteration_result.opinions_list))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


# Bramson et el., 2016 section 2.2
def dispersion(experiment_result: ExperimentResult, simulation_config: SimulationConfig) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(var(iteration_result.opinions_list))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


def _percent_of_covered_bins(opinions_list, bins_range: ndarray) -> float:
    num_of_covered_bins = 0
    for i in range(1, len(bins_range)):
        if any(bins_range[i-1] < opinion <= bins_range[i] for opinion in opinions_list):
            num_of_covered_bins += 1
    return num_of_covered_bins / (len(bins_range) - 1)


# Bramson et el., 2016 section 2.3
def covered_bins(experiment_result: ExperimentResult, simulation_config: SimulationConfig, num_of_bins: int = 10) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(_percent_of_covered_bins(iteration_result.opinions_list, np.arange(0, 1 + 1 / num_of_bins, 1 / num_of_bins)))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


def _num_of_clusters(opinions_list: ndarray, k_range: np.ndarray = None) -> int:
    if k_range is None:
        k_range = np.arange(1, len(opinions_list))
    k_means_inertias = np.empty(k_range.size)
    # fitting k-means for each value of k
    for i, k in enumerate(k_range):
        kmeans = KMeans(k, random_state=42)
        kmeans.fit(opinions_list.reshape(-1, 1))
        k_means_inertias[i] = kmeans.inertia_

    # looking for the best k using the elbow method
    slope = (k_means_inertias[0] - k_means_inertias[-1]) / (k_range[0] - k_range[-1])
    intercept = k_means_inertias[0] - slope * k_range[0]
    y = k_range * slope + intercept
    return k_range[(y - k_means_inertias).argmax()]


# Bramson et el., 2016 section 2.4
# calculating optimal num of clusters using the elbow method.
def num_of_clusters(experiment_result: ExperimentResult, simulation_config: SimulationConfig) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(_num_of_clusters(np.array(iteration_result.opinions_list)))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)
