import numpy as np
from numpy import ndarray
from sklearn.cluster import KMeans

from analyze.measurement import constants
from analyze.measurement.base import Measurement
from analyze.results import MeasurementResult
from experiment.result import ExperimentResult


# Bramson et el., 2016 section 2.4
# Calculating num of clusters using the elbow method (unsupervised).
class ClustersCountMeasurement(Measurement):

    def __init__(self):
        super().__init__(constants.NUM_OF_CLUSTERS, "Number of Clusters (KNN + Elbow Method)")

    def ylim(self):
        return 0, 1

    def apply_measure(self, experiment_result: ExperimentResult) -> MeasurementResult:
        return self._apply_measure_using_opinion_list_func(
            experiment_result,
            lambda opinions_list: self._num_of_clusters(np.array(opinions_list))
        )

    def _num_of_clusters(self, opinions_list: ndarray, k_range: np.ndarray = None) -> int:
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
