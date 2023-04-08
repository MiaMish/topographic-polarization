from typing import List

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from analyze.measurement.base import Measurement
from analyze.measurement.binsvar import VarianceInBinsMeasurement
from analyze.measurement.coveredbins import CoveredBinsMeasurement
from analyze.measurement.dispersion import DispersionMeasurement
from analyze.measurement.spread import SpreadMeasurement
from analyze.results import MeasurementResult
from experiment.result import ExperimentResult

COLORS = ['b', 'c', 'y', 'm', 'r', 'g']
MEASUREMENTS_TO_VISUALIZE = [
    SpreadMeasurement(),
    DispersionMeasurement(),
    # PeaksMeasurement(),
    CoveredBinsMeasurement(),
    # DisconnectIndexMeasurement(),
    VarianceInBinsMeasurement()
]


def _colors_generator():
    i = 0
    while True:
        yield COLORS[i % len(COLORS)]
        i += 1


def visualize_results(experiment_results: List[ExperimentResult]):
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    for measurement in MEASUREMENTS_TO_VISUALIZE:
        measurement_results = []
        for experiment_result in experiment_results:
            measurement_results.append(measurement.apply_measure(experiment_result))
        scatter_plot_from_measurements(measurement, measurement_results)


def scatter_plot_from_measurements(measurement: Measurement, measurement_results: List[MeasurementResult], store_in_file: str = None):
    scattered = []
    names = []
    colors_iter = _colors_generator()
    for measurement_result in measurement_results:
        scattered.append(plt.scatter(measurement_result.x, measurement_result.y, color=next(colors_iter)))
        names.append(measurement_result.display_name)
    plt.legend(scattered,
               names,
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.xlabel("Iteration")
    plt.title(f"{measurement.name}: {measurement.description}")
    ylim = measurement.ylim()
    if ylim is not None:
        plt.ylim([0, 1])
    # plt.show()
    if store_in_file is not None:
        plt.savefig(store_in_file)
