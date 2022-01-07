import math
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import seaborn as sns
from sklearn.manifold import MDS

# Default values to run the model
DEFAULT_NO_SHARING_COMBO_THRESHOLD = 4
DEFAULT_DISPLAY_NAME = "Axelrod Model"
DEFAULT_NUM_OF_INTERVALS = 100
DEFAULT_NUM_OF_ITERATIONS = 100001
DEFAULT_NUM_OF_TRAITS = 10
DEFAULT_NUM_OF_FEATURES = 5
DEFAULT_NUM_OF_AGENTS = 100


#####################
# Private Functions #
#####################

class _ColumnNames:
    NO_SHARING_COMBO = "no_sharing_combo"
    LOCATION = "location"
    TRAITS = "traits"
    REGION = "region"


def _generate_agent(agent_num, num_of_agents, num_of_features, traits, regions):
    return {
        _ColumnNames.REGION: None if regions is None else np.random.choice(list(regions.keys()), p=list(regions.values())),
        _ColumnNames.LOCATION: (
            int(agent_num / math.sqrt(num_of_agents)),
            int(agent_num % math.sqrt(num_of_agents))
        ),
        _ColumnNames.TRAITS: np.random.choice(traits, size=num_of_features),
        _ColumnNames.NO_SHARING_COMBO: 0
    }


def _agents_interact(active_agent, passive_agent, num_of_features, regions, no_sharing_combo_threshold):
    active_traits = active_agent.at[active_agent.index[0], _ColumnNames.TRAITS]
    passive_traits = passive_agent.at[passive_agent.index[0], _ColumnNames.TRAITS]
    dissimilar_traits = _get_dissimilar_traits(active_traits, num_of_features, passive_traits)
    probability_to_share = (num_of_features - len(dissimilar_traits)) / num_of_features
    if len(dissimilar_traits) == 0:
        return active_agent
    if np.random.binomial(n=1, p=probability_to_share):
        trait_to_share = np.random.choice(dissimilar_traits)
        active_traits[trait_to_share] = passive_traits[trait_to_share]
        active_agent.at[active_agent.index[0], _ColumnNames.NO_SHARING_COMBO] = 0
    elif regions is not None \
            and len(regions.keys()) > 1 \
            and active_agent.at[active_agent.index[0], _ColumnNames.NO_SHARING_COMBO] == no_sharing_combo_threshold:
        other_regions = [region for region in list(regions.keys()) if
                         region != active_agent.at[active_agent.index[0], _ColumnNames.REGION]]
        new_region = np.random.choice(other_regions)
        active_agent.at[active_agent.index[0], _ColumnNames.REGION] = new_region
        active_agent.at[active_agent.index[0], _ColumnNames.NO_SHARING_COMBO] = 0
    else:
        active_agent.at[active_agent.index[0], _ColumnNames.NO_SHARING_COMBO] += 1
    active_agent.at[active_agent.index[0], _ColumnNames.TRAITS] = active_traits
    return active_agent


def _get_dissimilar_traits(active_traits, num_of_features, passive_traits):
    dissimilar_traits = []
    for i in range(num_of_features):
        if active_traits[i] != passive_traits[i]:
            dissimilar_traits.append(i)
    return dissimilar_traits


def _print_as_grid(df):
    # prepare data for dimension reduction
    matrix = np.zeros((len(df), len(df.at[0, _ColumnNames.TRAITS])))
    for index, row in df.iterrows():
        matrix[index, :] = row[_ColumnNames.TRAITS]

    # reduce dimensionality
    all_rows_in_matrix_are_the_same = np.all(matrix == matrix[0])
    traits_in_single_dim = np.full((len(df), 1), 1)
    if not all_rows_in_matrix_are_the_same:
        mds = MDS(random_state=0, n_components=1)
        traits_in_single_dim = mds.fit_transform(matrix)

    # create grid to print
    divided_by_regions = df.at[0, _ColumnNames.REGION] is not None
    if divided_by_regions:
        regions = list(df[_ColumnNames.REGION].unique())
        regions.sort()
        print(regions)
        num_of_rows = len(regions)
        grid = [[] for _ in range(num_of_rows)]
        mask = [[] for _ in range(num_of_rows)]
        for index, row in df.iterrows():
            grid[regions.index(row[_ColumnNames.REGION])].append(traits_in_single_dim[index, 0])
            mask[regions.index(row[_ColumnNames.REGION])].append(False)
        num_of_columns = max([len(row) for row in grid])
        for row_num in range(len(grid)):
            grid[row_num].sort()
            grid[row_num] += [-1] * (num_of_columns - len(grid[row_num]))
            mask[row_num] += [True] * (num_of_columns - len(mask[row_num]))
    else:
        grid = [[None for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
        mask = [[False for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
        for index, row in df.iterrows():
            grid[row[_ColumnNames.LOCATION][0]][row[_ColumnNames.LOCATION][1]] = traits_in_single_dim[index, 0]

    # print as heatmap
    sns.heatmap(data=np.array(grid), cbar=False, mask=np.array(mask))
    plt.show()


def _update_polarization_metrics(df, iteration_num, polarization_metrics_df, update_interval, display_name):
    if iteration_num % update_interval == 0:
        traits_value_count = df[_ColumnNames.TRAITS].apply(lambda x: str(x)).value_counts()
        polarization_metrics_df = polarization_metrics_df.append({
            "iteration": iteration_num,
            f"\"{display_name}\" giant size ratio": traits_value_count[0] / df.shape[0],
            f"\"{display_name}\" groups count": traits_value_count.size
        }, ignore_index=True)
    return polarization_metrics_df


def show_polarization_metrics(polarization_metrics_df):
    polarization_metrics_df.plot(
        y=[col for col in list(polarization_metrics_df.columns) if col.endswith(" groups count")],
        title="Group Count"
    )
    plt.show()
    polarization_metrics_df.plot(
        y=[col for col in list(polarization_metrics_df.columns) if col.endswith(" giant size ratio")],
        title="Giant Size Ratio",

    )
    plt.show()
    print("Polarization Metrics Summary:")
    print(polarization_metrics_df.tail(1).transpose().to_markdown())


####################
# Public Functions #
####################


def select_passive_by_x_y(active_agent, df):
    location_of_active = active_agent.at[active_agent.index[0], _ColumnNames.LOCATION]
    possible_locations = [(location_of_active[0] - 1, location_of_active[1]),
                          (location_of_active[0] + 1, location_of_active[1]),
                          (location_of_active[0], location_of_active[1] - 1),
                          (location_of_active[0], location_of_active[1] + 1)]
    return df.loc[df[_ColumnNames.LOCATION].isin(possible_locations)].sample()


def select_passive_by_region(active_agent, df):
    region_of_active = active_agent.at[active_agent.index[0], _ColumnNames.REGION]
    return df.loc[df[_ColumnNames.REGION] == region_of_active].sample()


def run_axelrod(num_of_agents=DEFAULT_NUM_OF_AGENTS,
                num_of_features=DEFAULT_NUM_OF_FEATURES,
                num_of_traits=DEFAULT_NUM_OF_TRAITS,
                num_of_iterations=DEFAULT_NUM_OF_ITERATIONS,
                update_interval=DEFAULT_NUM_OF_INTERVALS,
                display_name=DEFAULT_DISPLAY_NAME,
                passive_selection=select_passive_by_x_y,
                regions=None,
                no_sharing_combo_threshold=DEFAULT_NO_SHARING_COMBO_THRESHOLD):
    print(f"Running Axelrod with:\n"
          f"display_name: {display_name}\n"
          f"num_of_agents: {num_of_agents}\n"
          f"num_of_features: {num_of_features}\n"
          f"num_of_traits: {num_of_traits}\n"
          f"num_of_iterations: {num_of_iterations}\n"
          f"update_interval: {update_interval}\n"
          f"regions: {regions}\n"
          f"no_sharing_combo_threshold: {no_sharing_combo_threshold}")
    start = int(time.time())
    polarization_metrics_df = pd.DataFrame()
    agents = [_generate_agent(agent_num=i, num_of_agents=num_of_agents, num_of_features=num_of_features,
                              traits=np.arange(num_of_traits), regions=regions) for i in range(num_of_agents)]
    df = pd.DataFrame(data=agents)
    for iteration_num in tqdm(range(num_of_iterations)):
        active_agent = df.sample()
        passive_agent = passive_selection(active_agent, df)
        revised_active_agent = _agents_interact(active_agent, passive_agent, num_of_features, regions,
                                                no_sharing_combo_threshold)
        df.loc[active_agent.index[0]] = revised_active_agent.loc[revised_active_agent.index[0]]
        polarization_metrics_df = _update_polarization_metrics(df, iteration_num, polarization_metrics_df,
                                                               update_interval, display_name)
    _print_as_grid(df)
    print(f"\nFinished running \"{display_name}\" in {int(time.time()) - start}s")
    show_analyze_by_region(df)

    return polarization_metrics_df.set_index("iteration"), df


def show_analyze_by_region(df):
    df["traits_as_str"] = df[_ColumnNames.TRAITS].apply(lambda x: str(x))
    analyze_by_region_df = pd.DataFrame()
    analyze_by_region_df["unique_traits"] = df.groupby(_ColumnNames.REGION)["traits_as_str"].nunique()
    analyze_by_region_df["population_size"] = df.groupby(_ColumnNames.REGION).size()
    print(analyze_by_region_df.to_markdown())
