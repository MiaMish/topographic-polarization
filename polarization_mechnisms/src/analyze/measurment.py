import numpy as np
from numpy import mean, ndarray, var
from scipy.interpolate import UnivariateSpline
from scipy.signal import argrelmax, argrelmin
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


# Bramson et el., 2016 section 2.3
def covered_bins(experiment_result: ExperimentResult, simulation_config: SimulationConfig, num_of_bins: int = 10) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(np.count_nonzero(np.histogram(iteration_result.opinions_list, num_of_bins)[0] != 0) / num_of_bins)
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
# Calculating num of clusters using the elbow method (unsupervised).
def num_of_clusters(experiment_result: ExperimentResult, simulation_config: SimulationConfig) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(_num_of_clusters(np.array(iteration_result.opinions_list)))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


def _num_of_local_extreme_points(opinions_list, num_of_bins=100):
    bins_dist = np.histogram(opinions_list, bins=num_of_bins)[0] / len(opinions_list)
    fitted_curve = UnivariateSpline(range(num_of_bins), bins_dist, s=5)
    applied_curve = fitted_curve(range(num_of_bins))
    return len(argrelmax(applied_curve)) + len(argrelmin(applied_curve))


# Bramson et el., 2016 section 2.5
# Ordering all opinions in bins and calculating the % of agents in each bin.
# For example, if we have 2 bins and opinion dist [0.2, 0.4, 0.9],
# then the first bin (0, 0.5) contains 2/3 of the agents and the second one (0.5, 1) contains 1/3.
# Then, we apply smoothing on the created curve and look for local min and maxes.
# Calculating num of clusters using the elbow method (unsupervised).
def num_of_local_max(experiment_result: ExperimentResult, simulation_config: SimulationConfig) -> ndarray:
    results = []
    for iteration_index in simulation_config.audited_iterations():
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        for iteration_result in iterations_result.values():
            iteration_spreads.append(_num_of_local_extreme_points(iteration_result.opinions_list))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


