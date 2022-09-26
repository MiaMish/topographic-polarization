from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from analyze import measurment
from experiment.result import ExperimentResult


def visualize_results(experiment_result: ExperimentResult):
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    to_plot = measurment.spread(experiment_result)
    plt.scatter(range(0, len(to_plot)), to_plot)
    plt.title("Spread: Delta Between Max and Min Opinions")
    plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    plt.xlabel("Iteration")
    plt.ylim([0, 1])
    plt.show()

    to_plot = measurment.dispersion(experiment_result)
    plt.scatter(range(0, len(to_plot)), to_plot)
    plt.title("Dispersion: Variance of Opinions")
    plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    plt.xlabel("Iteration")
    plt.ylim([0, 1])
    plt.show()

    to_plot = measurment.covered_bins(experiment_result)
    plt.scatter(range(0, len(to_plot)), to_plot)
    plt.title("Covered Bins: % of Covered Deciles")
    plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    plt.xlabel("Iteration")
    plt.ylim([0, 1])
    plt.show()

    # to_plot = measurment.num_of_clusters(experiment_result)
    # plt.scatter(range(0, len(to_plot)), to_plot)
    # plt.title("Number of Clusters: Elbow Method for KNN")
    # plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    # plt.xlabel("Iteration")
    # plt.show()

    to_plot = measurment.num_of_local_max(experiment_result)
    plt.scatter(range(0, len(to_plot)), to_plot)
    plt.title("Number of Local Peak Points")
    plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    plt.xlabel("Iteration")
    plt.show()

    to_plot = measurment.disconnect_index(experiment_result)
    plt.scatter(range(0, len(to_plot)), to_plot)
    plt.title("Disconnect Index")
    plt.suptitle(f"Experiment: {experiment_result.simulation_configs.display_name}")
    plt.xlabel("Iteration")
    # plt.ylim([0, 1])
    plt.show()



