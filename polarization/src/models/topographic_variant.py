import numpy as np
from ..columns_consts import ColumnNames


def topographic_generate_attributes(regions):
    agent_attributes = {
        ColumnNames.REGION: None if regions is None else np.random.choice(list(regions.keys()), p=list(regions.values())),
        ColumnNames.NO_SHARING_COMBO: 0
    }
    return agent_attributes


def topographic_select_passive(active_agent, df):
    region_of_active = active_agent.at[active_agent.index[0], ColumnNames.REGION]
    return df.loc[df[ColumnNames.REGION] == region_of_active].sample()


def topographic_update_attributes(active_agent, interaction_successful, regions, no_sharing_combo_threshold):
    if interaction_successful:
        active_agent.at[active_agent.index[0], ColumnNames.NO_SHARING_COMBO] = 0
    if not interaction_successful \
            and regions is not None \
            and len(regions.keys()) > 1 \
            and active_agent.at[active_agent.index[0], ColumnNames.NO_SHARING_COMBO] == no_sharing_combo_threshold:
        other_regions = [region for region in list(regions.keys()) if
                         region != active_agent.at[active_agent.index[0], ColumnNames.REGION]]
        new_region = np.random.choice(other_regions)
        active_agent.at[active_agent.index[0], ColumnNames.REGION] = new_region
        active_agent.at[active_agent.index[0], ColumnNames.NO_SHARING_COMBO] = 0

    if not interaction_successful \
            and regions is not None \
            and len(regions.keys()) > 1 \
            and active_agent.at[active_agent.index[0], ColumnNames.NO_SHARING_COMBO] < no_sharing_combo_threshold:
        active_agent.at[active_agent.index[0], ColumnNames.NO_SHARING_COMBO] += 1
    return active_agent
