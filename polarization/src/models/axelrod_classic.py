import math
import numpy as np
from ..columns_consts import ColumnNames


def _get_dissimilar_traits(active_traits, num_of_features, passive_traits):
    dissimilar_traits = []
    for i in range(num_of_features):
        if active_traits[i] != passive_traits[i]:
            dissimilar_traits.append(i)
    return dissimilar_traits


def classic_generate_features(num_of_features, traits):
    agent_features = {
        ColumnNames.TRAITS: np.random.choice(traits, size=num_of_features),
    }
    return agent_features


def classic_generate_attributes(agent_num, num_of_agents):
    agent_attributes = {
        ColumnNames.LOCATION: (
            int(agent_num / math.sqrt(num_of_agents)),
            int(agent_num % math.sqrt(num_of_agents))
        ),
    }
    return agent_attributes


def classic_select_passive(active_agent, df):
    location_of_active = active_agent.at[active_agent.index[0], ColumnNames.LOCATION]
    possible_locations = [(location_of_active[0] - 1, location_of_active[1]),
                          (location_of_active[0] + 1, location_of_active[1]),
                          (location_of_active[0], location_of_active[1] - 1),
                          (location_of_active[0], location_of_active[1] + 1)]
    return df.loc[df[ColumnNames.LOCATION].isin(possible_locations)].sample()


def classic_agents_interact(active_agent, passive_agent):
    active_traits = active_agent.at[active_agent.index[0], ColumnNames.TRAITS]
    passive_traits = passive_agent.at[passive_agent.index[0], ColumnNames.TRAITS]
    num_of_features = len(passive_traits)
    dissimilar_traits = _get_dissimilar_traits(active_traits, num_of_features, passive_traits)
    probability_to_share = (num_of_features - len(dissimilar_traits)) / num_of_features
    return np.random.binomial(n=1, p=probability_to_share)


def classic_update_features(active_agent, passive_agent, interaction_successful):
    active_traits = active_agent.at[active_agent.index[0], ColumnNames.TRAITS]
    passive_traits = passive_agent.at[passive_agent.index[0], ColumnNames.TRAITS]
    num_of_features = len(passive_traits)
    dissimilar_traits = _get_dissimilar_traits(active_traits, num_of_features, passive_traits)
    if len(dissimilar_traits) == 0:
        return active_agent
    if interaction_successful:
        trait_to_share = np.random.choice(dissimilar_traits)
        active_traits[trait_to_share] = passive_traits[trait_to_share]
    active_agent.at[active_agent.index[0], ColumnNames.TRAITS] = active_traits
    return active_agent

