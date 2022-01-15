import time
import pandas as pd
from tqdm import tqdm
from ..models.axelrod_classic import *
from ..models.topographic_variant import *

# Default values to run the model
DEFAULT_NO_SHARING_COMBO_THRESHOLD = 4
DEFAULT_DISPLAY_NAME = "Axelrod Model"
DEFAULT_NUM_OF_ITERATIONS = 100001
DEFAULT_NUM_OF_TRAITS = 10
DEFAULT_NUM_OF_FEATURES = 5
DEFAULT_NUM_OF_AGENTS = 100


def _run_axelrod(num_of_agents,
                 num_of_features,
                 num_of_iterations,
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
        revised_active_agent, update_features_additional_info = update_features(active_agent, passive_agent,
                                                                                interaction_successful)
        revised_active_agent, update_attributes_additional_info = update_attributes(revised_active_agent.copy(),
                                                                                    interaction_successful)
        df.loc[active_agent.index[0]] = revised_active_agent.loc[revised_active_agent.index[0]]

        # update iteration polarization metrics
        traits_value_count = df[ColumnNames.TRAITS].apply(lambda x: str(x)).value_counts()
        polarization_metrics_df = polarization_metrics_df.append({**{
            "iteration": iteration_num,
            "giant size ratio": traits_value_count[0] / df.shape[0],
            "groups count": traits_value_count.size,
            "is interaction successful": interaction_successful
        }, **update_features_additional_info, **update_attributes_additional_info}, ignore_index=True)

    print(f"\nFinished running \"{display_name}\" in {int(time.time()) - start}s")

    polarization_metrics_df = polarization_metrics_df.add_prefix(f"\"{display_name}\" ")
    polarization_metrics_df = polarization_metrics_df.rename(columns={f"\"{display_name}\" iteration": "iteration"})
    return polarization_metrics_df.set_index("iteration"), df


def run_classic(num_of_agents=DEFAULT_NUM_OF_AGENTS,
                num_of_features=DEFAULT_NUM_OF_FEATURES,
                num_of_traits=DEFAULT_NUM_OF_TRAITS,
                num_of_iterations=DEFAULT_NUM_OF_ITERATIONS,
                display_name=DEFAULT_DISPLAY_NAME):
    print(f"Running Axelrod with:\n"
          f"display_name: {display_name}\n"
          f"num_of_agents: {num_of_agents}\n"
          f"num_of_features: {num_of_features}\n"
          f"num_of_traits: {num_of_traits}\n"
          f"num_of_iterations: {num_of_iterations}\n")
    return _run_axelrod(num_of_agents=num_of_agents,
                        num_of_features=num_of_features,
                        num_of_iterations=num_of_iterations,
                        display_name=display_name,
                        generate_attributes=lambda agent_num: classic_generate_attributes(agent_num, num_of_agents),
                        generate_features=lambda _: classic_generate_features(num_of_features,
                                                                              np.arange(num_of_traits)),
                        passive_selection=classic_select_passive,
                        agents_interact=classic_agents_interact,
                        update_features=classic_update_features,
                        update_attributes=lambda *args: (args[0], {}))


def run_topographic(regions,
                    no_sharing_combo_threshold=DEFAULT_NO_SHARING_COMBO_THRESHOLD,
                    num_of_agents=DEFAULT_NUM_OF_AGENTS,
                    num_of_features=DEFAULT_NUM_OF_FEATURES,
                    num_of_traits=DEFAULT_NUM_OF_TRAITS,
                    num_of_iterations=DEFAULT_NUM_OF_ITERATIONS,
                    display_name=DEFAULT_DISPLAY_NAME):
    print(f"Running Axelrod with:\n"
          f"display_name: {display_name}\n"
          f"num_of_agents: {num_of_agents}\n"
          f"num_of_features: {num_of_features}\n"
          f"num_of_traits: {num_of_traits}\n"
          f"num_of_iterations: {num_of_iterations}\n"
          f"regions: {regions}\n"
          f"no_sharing_combo_threshold: {no_sharing_combo_threshold}")
    return _run_axelrod(num_of_agents=num_of_agents,
                        num_of_features=num_of_features,
                        num_of_iterations=num_of_iterations,
                        display_name=display_name,
                        generate_attributes=lambda agent_num: topographic_generate_attributes(regions),
                        generate_features=lambda _: classic_generate_features(num_of_features,
                                                                              np.arange(num_of_traits)),
                        passive_selection=topographic_select_passive,
                        agents_interact=classic_agents_interact,
                        update_features=classic_update_features,
                        update_attributes=lambda active_agent, interaction_successful: topographic_update_attributes(
                            active_agent, interaction_successful, regions, no_sharing_combo_threshold))
