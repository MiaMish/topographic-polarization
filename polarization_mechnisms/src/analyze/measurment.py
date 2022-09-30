from enum import Enum
from typing import Callable, List

import numpy as np
import ripleyk
from numpy import mean, ndarray, var, sort
from scipy.interpolate import UnivariateSpline
from scipy.signal import argrelmax, argrelmin
from sklearn.cluster import KMeans

from experiment.result import ExperimentResult


# TODO - all functions here have REALLY bad performance and it's easy to fix it...


class MeasurementType(Enum):
    SPREAD = "Delta Between Max and Min Opinions"
    DISPERSION = "Variance of Opinions"
    COVERED_BINS = "% of Covered Deciles"
    NUM_OF_LOCAL_MAX = "Number of Local Peak Points"

    def __init__(self, description: str):
        self.description = description


def _apply_measure(
        experiment_result: ExperimentResult,
        measure_for_opinion_list: Callable[[List[float]], float]
) -> ndarray:
    results = []
    for iteration_index in range(experiment_result.simulation_configs.num_iterations):
        iteration_spreads = []
        iterations_result = experiment_result.get_iteration_from_all_repetitions(iteration_index)
        if iterations_result is None:
            continue
        for iteration_result in iterations_result.values():
            iteration_spreads.append(measure_for_opinion_list(iteration_result.opinions_list))
        results.append(mean(iteration_spreads))
    return np.array(results, dtype=float)


# Bramson et el., 2016 section 2.1
def spread(experiment_result: ExperimentResult) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: max(opinions_list) - min(opinions_list))


# Bramson et el., 2016 section 2.2
def dispersion(experiment_result: ExperimentResult) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: var(opinions_list))


# Bramson et el., 2016 section 2.3
# Limitation: the num of bins is arbitrary
def covered_bins(experiment_result: ExperimentResult, num_of_bins: int = 10) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: np.count_nonzero(np.histogram(opinions_list, num_of_bins)[0] != 0) / num_of_bins)


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
def num_of_clusters(experiment_result: ExperimentResult) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: _num_of_clusters(np.array(opinions_list)))


def _num_of_local_extreme_points(opinions_list, num_of_bins=100):
    bins_dist = np.histogram(opinions_list, bins=num_of_bins)[0] / len(opinions_list)
    fitted_curve = UnivariateSpline(range(num_of_bins), bins_dist, s=5)
    applied_curve = fitted_curve(range(num_of_bins))
    return len(argrelmax(applied_curve)) + len(argrelmin(applied_curve))


# Bramson et el., 2016 section 2.5
# Ordering all opinions in bins and calculating the % of agents in each bin.
# For example, if we have 2 bins and opinion dist [0.2, 0.4, 0.9],
# then the first bin (0, 0.5) contains 2/3 of the agents and the second one (0.5, 1) contains 1/3.
# Then, we apply smoothing on the created curve to remove small "jumps" and look for local maxes.
# A vector is more polarized if it has a small number of peek points, but not 0 or 1.
# In general (it's not tested by this...) if the peeks are far apart from each other => the dist is more polarized
def num_of_local_max(experiment_result: ExperimentResult) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: _num_of_local_extreme_points(opinions_list))


# TODO: I think my entire approach here is incorrect...
# Take a look: https://stats.stackexchange.com/questions/122668/is-there-a-measure-of-evenness-of-spread
def ripley_estimator(experiment_result: ExperimentResult, radius=0.5, bounding_radius=1) -> ndarray:
    return _apply_measure(experiment_result, lambda opinions_list: ripleyk.calculate_ripley(radius, bounding_radius, d1=np.arange(0, len(opinions_list)), d2=np.sort(opinions_list)))


def _min_removal_for_disconnect(opinions_list: ndarray, disconnect_factor):
    if len(opinions_list) == 2:
        return opinions_list[:1]
    closest_pair = (0, 1)
    for i in range(1, len(opinions_list)):
        if opinions_list[i] - opinions_list[i - 1] < disconnect_factor:
            return opinions_list
        if opinions_list[i] - opinions_list[i - 1] < opinions_list[closest_pair[1]] - opinions_list[closest_pair[0]]:
            closest_pair = (i-1, i)
    opinions_list_without_left = np.delete(opinions_list, closest_pair[0])
    opinions_list_without_right = np.delete(opinions_list, closest_pair[1])
    _disconnect_index_without_left_in_pair = _min_removal_for_disconnect(opinions_list_without_left, disconnect_factor)
    _disconnect_index_without_right_in_pair = _min_removal_for_disconnect(opinions_list_without_right, disconnect_factor)
    if len(_disconnect_index_without_left_in_pair) < len(_disconnect_index_without_right_in_pair):
        return _disconnect_index_without_left_in_pair
    return _disconnect_index_without_right_in_pair


# See note in “Dispersion Point,” 2021; This is Option #1.
def disconnect_index(experiment_result: ExperimentResult, disconnect_factor=0.2):
    return _apply_measure(experiment_result, lambda opinions_list: len(opinions_list) - len(_min_removal_for_disconnect(sort(opinions_list), disconnect_factor)))
