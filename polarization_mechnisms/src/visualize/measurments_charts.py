import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import storage.constants as db_constants
from analyze.measurement import constants as measurement_constants
from simulation.config import SimulationType

BASE_RESULT_PATH = "../resources/april06"


def to_visualize_name(to_convert):
    if to_convert == measurement_constants.BINS_VARIANCE:
        return "Bins Variance"
    elif to_convert == measurement_constants.SPREAD:
        return "Spread"
    elif to_convert == measurement_constants.COVERED_BINS:
        return "Covered Bins"
    elif to_convert == measurement_constants.DISPERSION:
        return "Variance"
    elif to_convert == db_constants.MIO_SIGMA:
        return "Mio Standard Deviation"
    elif to_convert == SimulationType.REPULSIVE:
        return "Repulsive"
    elif to_convert == SimulationType.SIMILARITY:
        return "Similarity"
    elif to_convert == db_constants.SWITCH_AGENT_SIGMA:
        return "Turnover Standard Deviation"
    elif to_convert == db_constants.SWITCH_AGENT_RATE:
        return "Turnover Mean Rate"
    elif to_convert == db_constants.RADICAL_EXPOSURE_ETA:
        return "Radical Exposure Eta"
    else:
        return to_convert.capitalize()


def read_basic_df(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df[db_constants.X] == 9999]
    return df


def plot_measurement(df, measurement_type, simulation_type, x_column, mechanism_name, inner_filters):
    filtered_df = df[df[db_constants.MEASUREMENT_TYPE] == measurement_type]
    filtered_df = filtered_df[filtered_df[db_constants.SIMULATION_TYPE] == simulation_type.name]
    if inner_filters:
        for inner_filter in inner_filters:
            print(f"inner filter: {inner_filter}")
            if inner_filter[1] is None:
                inner_filtered_df = filtered_df[filtered_df[inner_filter[0]].isna()]
            else:
                inner_filtered_df = filtered_df[filtered_df[inner_filter[0]] == inner_filter[1]]
            plot_x_y(inner_filtered_df, x_column, color=inner_filter[2])
    else:
        plot_x_y(filtered_df, x_column)
    plt.xlabel(to_visualize_name(x_column))
    plt.ylabel(to_visualize_name(measurement_type))
    title = f"{mechanism_name} - {to_visualize_name(simulation_type)} - {to_visualize_name(measurement_type)} by {to_visualize_name(x_column)}"
    plt.title(title)
    # plt.show()
    plt.savefig(f'{BASE_RESULT_PATH}/figures/{title.replace("-", "").replace(" ", "_")}.png')
    plt.close()

def plot_all_charts(df, x_column, mechanism_name, inner_filters=None):
    df[x_column] = df[x_column].astype(float)
    df = df.sort_values(by=x_column, ignore_index=True)

    # Create 8 charts
    for measurement_type in [measurement_constants.BINS_VARIANCE, measurement_constants.SPREAD,
                             measurement_constants.COVERED_BINS, measurement_constants.DISPERSION]:
        for simulation_type in [SimulationType.REPULSIVE, SimulationType.SIMILARITY]:
            plot_measurement(df, measurement_type, simulation_type, x_column, mechanism_name, inner_filters)



def plot_x_y(filtered_df, x_column, color=None, label=None):
    filtered_df = filtered_df.drop_duplicates([
        db_constants.MEASUREMENT_TYPE, db_constants.SIMULATION_TYPE, db_constants.NUM_OF_AGENTS,
        db_constants.NUM_ITERATIONS, db_constants.MIO, db_constants.MIO_SIGMA, db_constants.NUM_OF_REPETITIONS,
        db_constants.SWITCH_AGENT_RATE, db_constants.SWITCH_AGENT_SIGMA, db_constants.RADICAL_EXPOSURE_ETA,
        db_constants.EPSILON
    ])
    # Define the x and y values for the line chart
    x = filtered_df[x_column]
    y = filtered_df["value"]
    # Calculate the confidence interval using the sample standard deviation
    sample_std = filtered_df["sample_std"]
    n = len(filtered_df)
    # t-value for 95% confidence interval and n-1 degrees of freedom
    t = 2.093
    error = t * (sample_std / np.sqrt(n))
    upper_bound = y + error
    lower_bound = y - error
    # Create the line chart with confidence interval
    plt.plot(x, y, color=color, label=label)
    plt.fill_between(x, lower_bound, upper_bound, alpha=0.3, color=color)


def stubbornness_by_sigma_mio(csv_path):
    df = read_basic_df(csv_path)
    df = df[df[db_constants.MIO] == 0.20000]
    plot_all_charts(df, db_constants.MIO_SIGMA, 'Stubbornness')


def stubbornness_by_mio(csv_path):
    df = read_basic_df(csv_path)
    plot_all_charts(df, db_constants.MIO, 'Stubbornness', inner_filters=[(db_constants.MIO_SIGMA, None, None), (db_constants.MIO_SIGMA, 0.075, 'orange')])


def radical_exposure_by_eta(csv_path):
    df = read_basic_df(csv_path)
    plot_all_charts(df, db_constants.RADICAL_EXPOSURE_ETA, 'Radical Exposure')


def switch_agent_rate(csv_path):
    df = read_basic_df(csv_path)
    plot_all_charts(df, db_constants.SWITCH_AGENT_RATE, 'Turnover')


def switch_agent_sigma(csv_path):
    df = read_basic_df(csv_path)
    plot_all_charts(df, db_constants.SWITCH_AGENT_SIGMA, 'Turnover')


def main():
    stubbornness_by_sigma_mio(f'{BASE_RESULT_PATH}/stubbornness/combined_measurements.csv')
    stubbornness_by_mio(f'{BASE_RESULT_PATH}/stubbornness/combined_measurements.csv')
    radical_exposure_by_eta(f'{BASE_RESULT_PATH}/radical_exposure/combined_measurements.csv')
    switch_agent_rate(f'{BASE_RESULT_PATH}/switch_agent_rate/combined_measurements.csv')
    switch_agent_sigma(f'{BASE_RESULT_PATH}/switch_agent_sigma/combined_measurements.csv')


if __name__ == '__main__':
    main()
