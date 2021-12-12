import math
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

# set seed
np.random.seed(42)

# string constants
NO_SHARING_COMBO = "no_sharing_combo"
LOCATION = "location"
TRAITS = "traits"
REGION = "region"


def generate_agent(agent_num, num_of_agents, num_of_features, traits, regions):
    return {
        REGION: None if regions is None else np.random.choice(list(regions.keys()), p=list(regions.values())),
        LOCATION: (
            int(agent_num / math.sqrt(num_of_agents)),
            int(agent_num % math.sqrt(num_of_agents))
        ),
        TRAITS: np.random.choice(traits, size=num_of_features),
        NO_SHARING_COMBO: 0
    }


def select_passive_by_x_y(active_agent, df):
    location_of_active = active_agent.at[active_agent.index[0], LOCATION]
    possible_locations = [(location_of_active[0] - 1, location_of_active[1]),
                          (location_of_active[0] + 1, location_of_active[1]),
                          (location_of_active[0], location_of_active[1] - 1),
                          (location_of_active[0], location_of_active[1] + 1)]
    return df.loc[df[LOCATION].isin(possible_locations)].sample()


def select_passive_by_region(active_agent, df):
    region_of_active = active_agent.at[active_agent.index[0], REGION]
    return df.loc[df[REGION] == region_of_active].sample()


def agents_interact(active_agent, passive_agent, num_of_features, regions, no_sharing_combo_threshold):
    active_traits = active_agent.at[active_agent.index[0], TRAITS]
    passive_traits = passive_agent.at[passive_agent.index[0], TRAITS]
    dissimilar_traits = get_dissimilar_traits(active_traits, num_of_features, passive_traits)
    probability_to_share = (num_of_features - len(dissimilar_traits)) / num_of_features
    if len(dissimilar_traits) == 0:
        return active_agent
    if np.random.binomial(n=1, p=probability_to_share):
        trait_to_share = np.random.choice(dissimilar_traits)
        active_traits[trait_to_share] = passive_traits[trait_to_share]
        active_agent.at[active_agent.index[0], NO_SHARING_COMBO] = 0
    elif regions is not None \
            and len(regions.keys()) > 1 \
            and active_agent.at[active_agent.index[0], NO_SHARING_COMBO] == no_sharing_combo_threshold:
        other_regions = [region for region in list(regions.keys()) if
                         region != active_agent.at[active_agent.index[0], REGION]]
        new_region = np.random.choice(other_regions)
        active_agent.at[active_agent.index[0], REGION] = new_region
        active_agent.at[active_agent.index[0], NO_SHARING_COMBO] = 0
    else:
        active_agent.at[active_agent.index[0], NO_SHARING_COMBO] += 1
    active_agent.at[active_agent.index[0], TRAITS] = active_traits
    return active_agent


def get_dissimilar_traits(active_traits, num_of_features, passive_traits):
    dissimilar_traits = []
    for i in range(num_of_features):
        if active_traits[i] != passive_traits[i]:
            dissimilar_traits.append(i)
    return dissimilar_traits


def print_as_grid(df, width, height):
    grid = [[None for _ in range(width)] for _ in range(height)]
    for index, row in df.iterrows():
        grid[row[LOCATION][0]][row[LOCATION][1]] = str(row[TRAITS])
    print("------------------------")
    for row in grid:
        print(", ".join(row))
    print("------------------------")


def update_polarization_metrics(df, iteration_num, polarization_metrics_df, update_interval, display_name):
    if iteration_num % update_interval == 0:
        # print_as_grid(df, int(math.sqrt(df.shape[0])), int(math.sqrt(df.shape[0])))
        traits_value_count = df[TRAITS].apply(lambda x: str(x)).value_counts()
        polarization_metrics_df = polarization_metrics_df.append({
            "iteration": iteration_num,
            display_name + " giant size ratio": traits_value_count[0] / df.shape[0],
            display_name + " groups count": traits_value_count.size
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


def run_axelrod(num_of_agents=100,
                num_of_features=5,
                num_of_traits=10,
                num_of_iterations=100001,
                update_interval=100,
                display_name="Axelrod Model",
                passive_selection=select_passive_by_x_y,
                regions=None,
                no_sharing_combo_threshold=4):
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
    agents = [generate_agent(agent_num=i, num_of_agents=num_of_agents, num_of_features=num_of_features,
                             traits=np.arange(num_of_traits), regions=regions) for i in range(num_of_agents)]
    df = pd.DataFrame(data=agents)
    for iteration_num in tqdm(range(num_of_iterations)):
        active_agent = df.sample()
        passive_agent = passive_selection(active_agent, df)
        revised_active_agent = agents_interact(active_agent, passive_agent, num_of_features, regions,
                                               no_sharing_combo_threshold)
        df.loc[active_agent.index[0]] = revised_active_agent.loc[revised_active_agent.index[0]]
        polarization_metrics_df = update_polarization_metrics(df, iteration_num, polarization_metrics_df,
                                                              update_interval, display_name)
    print(f"\nFinished running {display_name} in {int(time.time()) - start}s")
    show_analyze_by_region(df)

    return polarization_metrics_df.set_index("iteration"), df


def show_analyze_by_region(df):
    df["traits_as_str"] = df[TRAITS].apply(lambda x: str(x))
    analyze_by_region_df = pd.DataFrame()
    analyze_by_region_df["unique_traits"] = df.groupby(REGION)["traits_as_str"].nunique()
    analyze_by_region_df["population_size"] = df.groupby(REGION).size()
    print(analyze_by_region_df.to_markdown())
