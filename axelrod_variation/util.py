import time
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm
import seaborn as sns
from sklearn.manifold import MDS
from axelrod_classic import *
from topographic_variant import *

# Default values to run the model
DEFAULT_NO_SHARING_COMBO_THRESHOLD = 4
DEFAULT_DISPLAY_NAME = "Axelrod Model"
DEFAULT_NUM_OF_INTERVALS = 100
DEFAULT_NUM_OF_ITERATIONS = 100001
DEFAULT_NUM_OF_TRAITS = 10
DEFAULT_NUM_OF_FEATURES = 5
DEFAULT_NUM_OF_AGENTS = 100


####################
# Metric Functions #
####################

# TODO - refactor

def _print_as_grid(df):
    # prepare data for dimension reduction
    matrix = np.zeros((len(df), len(df.at[0, ColumnNames.TRAITS])))
    for index, row in df.iterrows():
        matrix[index, :] = row[ColumnNames.TRAITS]

    # reduce dimensionality
    all_rows_in_matrix_are_the_same = np.all(matrix == matrix[0])
    traits_in_single_dim = np.full((len(df), 1), 1)
    if not all_rows_in_matrix_are_the_same:
        mds = MDS(random_state=0, n_components=1)
        traits_in_single_dim = mds.fit_transform(matrix)

    # create grid to print
    if ColumnNames.REGION in df.columns:
        regions = list(df[ColumnNames.REGION].unique())
        regions.sort()
        num_of_rows = len(regions)
        grid = [[] for _ in range(num_of_rows)]
        mask = [[] for _ in range(num_of_rows)]
        for index, row in df.iterrows():
            grid[regions.index(row[ColumnNames.REGION])].append(traits_in_single_dim[index, 0])
            mask[regions.index(row[ColumnNames.REGION])].append(False)
        num_of_columns = max([len(row) for row in grid])
        for row_num in range(len(grid)):
            grid[row_num].sort()
            grid[row_num] += [-1] * (num_of_columns - len(grid[row_num]))
            mask[row_num] += [True] * (num_of_columns - len(mask[row_num]))
    else:
        grid = [[None for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
        mask = [[False for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
        for index, row in df.iterrows():
            grid[row[ColumnNames.LOCATION][0]][row[ColumnNames.LOCATION][1]] = traits_in_single_dim[index, 0]

    # print as heatmap
    sns.heatmap(data=np.array(grid), cbar=False, mask=np.array(mask))
    plt.show()


def _update_polarization_metrics(df, iteration_num, polarization_metrics_df, update_interval, display_name):
    if iteration_num % update_interval == 0:
        traits_value_count = df[ColumnNames.TRAITS].apply(lambda x: str(x)).value_counts()
        polarization_metrics_df = polarization_metrics_df.append({
            "iteration": iteration_num,
            f"\"{display_name}\" giant size ratio": traits_value_count[0] / df.shape[0],
            f"\"{display_name}\" groups count": traits_value_count.size
        }, ignore_index=True)
    return polarization_metrics_df


def _show_analyze_by_region(df):
    if ColumnNames.REGION not in df.columns:
        return
    df["traits_as_str"] = df[ColumnNames.TRAITS].apply(lambda x: str(x))
    analyze_by_region_df = pd.DataFrame()
    analyze_by_region_df["unique_traits"] = df.groupby(ColumnNames.REGION)["traits_as_str"].nunique()
    analyze_by_region_df["population_size"] = df.groupby(ColumnNames.REGION).size()
    print(analyze_by_region_df.to_markdown())


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


#######################
# Run Model Functions #
#######################


def _run_axelrod(num_of_agents,
                 num_of_features,
                 num_of_iterations,
                 update_interval,
                 display_name,
                 generate_attributes,
                 generate_features,
                 passive_selection,
                 agents_interact,
                 update_features,
                 update_attributes):
    start = int(time.time())
    polarization_metrics_df = pd.DataFrame()
    agents = [{**generate_attributes(i), **generate_features(num_of_features)}
              for i in range(num_of_agents)]
    df = pd.DataFrame(data=agents)
    for iteration_num in tqdm(range(num_of_iterations)):
        active_agent = df.sample()
        passive_agent = passive_selection(active_agent, df)
        interaction_successful = agents_interact(active_agent, passive_agent)
        revised_active_agent = update_features(active_agent, passive_agent, interaction_successful)
        revised_active_agent = update_attributes(revised_active_agent, interaction_successful)
        df.loc[active_agent.index[0]] = revised_active_agent.loc[revised_active_agent.index[0]]
        polarization_metrics_df = _update_polarization_metrics(df, iteration_num, polarization_metrics_df,
                                                               update_interval, display_name)
    _print_as_grid(df)
    print(f"\nFinished running \"{display_name}\" in {int(time.time()) - start}s")
    _show_analyze_by_region(df)

    return polarization_metrics_df.set_index("iteration"), df


def run_classic(num_of_agents=DEFAULT_NUM_OF_AGENTS,
                num_of_features=DEFAULT_NUM_OF_FEATURES,
                num_of_traits=DEFAULT_NUM_OF_TRAITS,
                num_of_iterations=DEFAULT_NUM_OF_ITERATIONS,
                update_interval=DEFAULT_NUM_OF_INTERVALS,
                display_name=DEFAULT_DISPLAY_NAME):
    print(f"Running Axelrod with:\n"
          f"display_name: {display_name}\n"
          f"num_of_agents: {num_of_agents}\n"
          f"num_of_features: {num_of_features}\n"
          f"num_of_traits: {num_of_traits}\n"
          f"num_of_iterations: {num_of_iterations}\n"
          f"update_interval: {update_interval}")
    return _run_axelrod(num_of_agents=num_of_agents,
                        num_of_features=num_of_features,
                        num_of_iterations=num_of_iterations,
                        update_interval=update_interval,
                        display_name=display_name,
                        generate_attributes=lambda agent_num: classic_generate_attributes(agent_num, num_of_agents),
                        generate_features=lambda _: classic_generate_features(num_of_features, np.arange(num_of_traits)),
                        passive_selection=classic_select_passive,
                        agents_interact=classic_agents_interact,
                        update_features=classic_update_features,
                        update_attributes=lambda *args: args[0])


def run_topographic(regions,
                    no_sharing_combo_threshold=DEFAULT_NO_SHARING_COMBO_THRESHOLD,
                    num_of_agents=DEFAULT_NUM_OF_AGENTS,
                    num_of_features=DEFAULT_NUM_OF_FEATURES,
                    num_of_traits=DEFAULT_NUM_OF_TRAITS,
                    num_of_iterations=DEFAULT_NUM_OF_ITERATIONS,
                    update_interval=DEFAULT_NUM_OF_INTERVALS,
                    display_name=DEFAULT_DISPLAY_NAME):
    print(f"Running Axelrod with:\n"
          f"display_name: {display_name}\n"
          f"num_of_agents: {num_of_agents}\n"
          f"num_of_features: {num_of_features}\n"
          f"num_of_traits: {num_of_traits}\n"
          f"num_of_iterations: {num_of_iterations}\n"
          f"update_interval: {update_interval}\n"
          f"regions: {regions}\n"
          f"no_sharing_combo_threshold: {no_sharing_combo_threshold}")
    return _run_axelrod(num_of_agents=num_of_agents,
                        num_of_features=num_of_features,
                        num_of_iterations=num_of_iterations,
                        update_interval=update_interval,
                        display_name=display_name,
                        generate_attributes=lambda agent_num: topographic_generate_attributes(regions),
                        generate_features=lambda _: classic_generate_features(num_of_features, np.arange(num_of_traits)),
                        passive_selection=topographic_select_passive,
                        agents_interact=classic_agents_interact,
                        update_features=classic_update_features,
                        update_attributes=lambda active_agent, interaction_successful: topographic_update_attributes(active_agent, interaction_successful, regions, no_sharing_combo_threshold))

