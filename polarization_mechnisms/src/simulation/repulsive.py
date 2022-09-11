from typing import List

from simulation.config import SimulationConfig

from simulation.simulation import Simulation


class RepulsiveSimulation(Simulation):

    def __init__(self, simulation_config: SimulationConfig):
        super().__init__(simulation_config)

    def _update_opinions(self, agent_i, agent_j) -> List[float]:
        new_opinion_i = self.opinions_list[agent_i]
        new_opinion_j = self.opinions_list[agent_j]
        if self._is_exposed_to_passive(self.opinions_list[agent_j]):
            new_opinion_i = self._truncate_opinion(self.opinions_list[agent_i] + self.simulation_config.mio * (
                        1 - 2 * (abs(self.opinions_list[agent_j] - self.opinions_list[agent_i]))))
        if self._is_exposed_to_passive(self.opinions_list[agent_i]):
            new_opinion_j = self._truncate_opinion(self.opinions_list[agent_j] + self.simulation_config.mio * (
                        1 - 2 * (abs(self.opinions_list[agent_i] - self.opinions_list[agent_j]))))
        return [new_opinion_i if k == agent_i else (new_opinion_j if k == agent_j else self.opinions_list[k]) for k in
                range(self.simulation_config.num_of_agents)]
