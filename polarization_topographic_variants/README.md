# Overview

todo

# Polarization Models

## High Level Model Structure

All the implemented models have the same high level structure:

### Initialization:

* Create `NUM_OF_AGENTS` agents.
* Assign each agent a features vector using the `generate_features` function.
* Assign each agent an additional attributes vector using the `generate_attributes` function.

### Iterations

Run `NUM_OF_ITERATIONS` iterations.
In each iteration: 
* Choose an active agent randomly.
* Choose a passive agent using the `passive_selection` function.
* Check if the interaction between the agents is successful using the `agents_interact` function.
* Change the features vector of the active agent based on the interaction using the `update_features` function. 
* Change the attribute vector of the active agent based on the interaction using the `update_attributes` function.

## Functions

The following functions are model-specific: 
* `generate_features`
* `generate_attributes`
* `passive_selection`
* `agents_interact`
* `update_features`
* `update_attributes`

## Parameters

In addition to model-specific parameters, there are few parameters that are shared by all models:

| Parameter | Default Value | Description |
| --- | --- | --- |
| `NUM_OF_FEATURES` | 5 | Size of features vector. |
| `NUM_OF_AGENTS` | 100 | Number of agents that are participating. |
| `NUM_OF_ITERATIONS` | 100001 | Number of iterations that are executed. |

## Models Variations

### Classic Axelrod

#### Overview

Based on the article: Axelrod, R. (1997). The Dissemination of Culture: A Model with Local Convergence and Global Polarization. Journal of Conflict Resolution, 41(2), 203–226. https://doi.org/10.1177/0022002797041002001

todo

#### Functions

| Function | Description |
| --- | --- |
| generate_features | Each feature in the features vector gets a random integer value ("trait") between 0 and `NUM_OF_TRAITS`. |
| generate_attributes | Each agent is assigned an (x, y) location on a grid of size sqrt(`NUM_OF_AGENTS`) X sqrt(`NUM_OF_AGENTS`). |
| passive_selection | Select a random neighbor of the agent. |
| agents_interact | Interaction is successful in probability `num of features that the agents share` / `NUM_OF_FEATURES`. A feature is shared between two agents iff both of them have the same trait for that feature. E.g., the probability agents with the vectors (7, 6, 5), (8, 6, 5) will interact successfully is 2/3. |
| update_features | If ite interaction is successfully, one of the dissimilar traits is chosen randomly and the active agents changes it's trait so it will match the passive agent. For example, if the agent with the feature vector (7, 6, 5) interacted successfully with (8, 5, 5), it will change it's features vector to either (8, 6, 5) or (7, 5, 5). | 
| update_attributes | None |

#### Parameters

The parameters specific to this model are:

| Parameter | Default Value | Description |
| --- | --- | --- |
| `NUM_OF_TRAITS` | 10 |  An integer between (0, `NUM_OF_TRAITS`) is assigned as the trait for each of the agent's features. |

In addition, this model posses the following constraints on these parameters:

| Parameter | Constraint |
| --- | --- |
| `NUM_OF_AGENTS` | sqrt(`NUM_OF_AGENTS`) must be an integer. |

### Topographic Variant Axelrod

#### Overview

todo

#### Functions

| Function | Description |
| --- | --- |
| generate_features | Same as "Classic Axelrod". |
| generate_attributes | Assigned a region randomly (uniformly) from range (0, `NUM_OF_REGIONS`). |
| passive_selection | Select a random agent from the same region of the agent. |
| agents_interact | Same as "Classic Axelrod". |
| update_features | Same as "Classic Axelrod". |
| update_attributes | If (a) the interaction was not successful and (b) the last `NO_SHARING_COMBO_THRESHOLD` of the active agents were not successful, change the agent's region to a random region from range (0, `NUM_OF_REGIONS`). |

#### Parameters

The parameters specific to this model are:

| Parameter | Default Value | Description |
| --- | --- | --- |
| `NUM_OF_REGIONS` |  | Each agent belongs to one region from range (0, `NUM_OF_REGIONS`). |
| `NO_SHARING_COMBO_THRESHOLD` | 4 | If the past `NO_SHARING_COMBO_THRESHOLD` interactions of the active agent were not successful, it will choose another random region. |

# Measuring Polarization

todo

* Process of polarization vs state of polarization.
* Visual aids
 