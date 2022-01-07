
# Polarization Models
## High Level Model Structure
All the implemented models has the same high level structure:

### Initialization:
* Create #NUM_OF_AGENTS# agents.
* Assign to each agent a features vector using #generate_features# function and additional attributes using #generate_attributes# function.

### Iterations
Run #NUM_OF_ITERATIONS# iterations.
In each iteration: 
* Choose active_agent randomly.
* Choose passive_agent using #passive_selection# function.
* Check if the interaction between the agents was successful using the #agents_interact# function.
* Change the features vector of the active agent based on the interaction using the #update_features# function. 
* Change the attribute vector of the active agent based on the interaction using the #update_attributes# function.

The #generate_features#, #generate_attributes#, #passive_selection#, #agents_interact#, #update_features# and #update_attributes# functions change in each model.

## Models Variations
### Classic Axelrod
| Function | Description |
| --- | --- |
| generate_features | Each feature in the features vector gets a random integer value ("trait") between 0 and #NUM_OF_TRAITS#. |
| generate_attributes | Each agent is assigned an (x, y) location on a grid of size sqrt(#NUM_OF_AGENTS# X #NUM_OF_AGENTS#). |
| passive_selection | Select a random agent from the region of the agent. |
| agents_interact | Interaction is successful in probability <num of features that the agents share> / #NUM_OF_FEATURES#. A feature is shared between two agents iff both of them have the same trait for that feature. E.g., the probability agents with the vectors (7, 6, 5), (8, 6, 5) will interact successfully is 2/3. |
| update_features | If ite interaction is successfully, one of the dissimilar traits is choosen randomaly and the active agents changes it's trait so it will match the passive agent. For example, if the agent with the feature vector (7, 6, 5) interacted successfully with (8, 5, 5), it will change it's features vector to either (8, 6, 5) or (7, 5, 5). | 
| update_attributes | None |

### Topographic Variant Axelrod
| Function | Description |
| --- | --- |
| generate_features | Same as "Classic Axelrod". |
| generate_attributes | Assigned a region randomly (uniformly) from range (0, #NUM_OF_REGIONS#). |
| passive_selection | Select a random agent from the same region of the agent. |
| agents_interact | Same as "Classic Axelrod". |
| update_features | Same as "Classic Axelrod". |
| update_attributes | If (a) the interaction was not successful and (b) the last #NO_SHARING_COMBO_THRESHOLD# of the active agents were not successful, change the agent's region to a random region from range (0, #NUM_OF_REGIONS#). |
