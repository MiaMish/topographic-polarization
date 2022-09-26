from typing import List, Callable

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from numpy import ndarray

from analyze import measurment
from experiment.result import ExperimentResult

COLORS = ['b', 'c', 'y', 'm', 'r', 'g']


def visualize_results(experiment_results: List[ExperimentResult]):
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    _scatter_plot(experiment_results, lambda experiment_result: measurment.spread(experiment_result))
    plt.title("Spread: Delta Between Max and Min Opinions")
    plt.ylim([0, 1])
    plt.show()

    _scatter_plot(experiment_results, lambda experiment_result: measurment.dispersion(experiment_result))
    plt.title("Dispersion: Variance of Opinions")
    plt.ylim([0, 1])
    plt.show()

    _scatter_plot(experiment_results, lambda experiment_result: measurment.covered_bins(experiment_result))
    plt.title("Covered Bins: % of Covered Deciles")
    plt.ylim([0, 1])
    plt.show()

    _scatter_plot(experiment_results, lambda experiment_result: measurment.num_of_local_max(experiment_result))
    plt.title("Number of Local Peak Points")
    plt.show()

    _scatter_plot(experiment_results, lambda experiment_result: measurment.disconnect_index(experiment_result))
    plt.title("Disconnect Index")
    plt.ylim([0, 1])
    plt.show()

    # to_plot = measurment.num_of_clusters(experiment_result)
    # plt.scatter(range(0, len(to_plot)), to_plot)
    # plt.title("Number of Clusters: Elbow Method for KNN")
    # plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    # plt.xlabel("Iteration")
    # plt.show()


def _scatter_plot(experiment_results: List[ExperimentResult], to_plot_func: Callable[[ExperimentResult], ndarray]):
    scattered = []
    names = []
    for i in range(len(experiment_results)):
        experiment_result = experiment_results[i]
        to_plot = to_plot_func(experiment_result)
        scattered.append(plt.scatter(range(0, len(to_plot)), to_plot, color=COLORS[i % len(COLORS)]))
        names.append(experiment_result.simulation_configs.display_name)
    plt.legend(scattered,
               names,
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.xlabel("Iteration")
