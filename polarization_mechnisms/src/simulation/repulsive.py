import numpy as np
from numpy import ndarray

from simulation.config import SimulationConfig
from simulation.simulation import Simulation


class RepulsiveSimulation(Simulation):

    def __init__(self, simulation_config: SimulationConfig):
        super().__init__(simulation_config)

    def _update_opinions(self, agent_i, agent_j) -> ndarray:
        new_opinion_i = self.opinions_list[agent_i]
        new_opinion_j = self.opinions_list[agent_j]
        if self._is_exposed_to_passive(self.opinions_list[agent_j]):
            new_opinion_i = self._truncate_opinion(self.opinions_list[agent_i] + self.mio_to_use(agent_i) * (
                        1 - 2 * (abs(self.opinions_list[agent_j] - self.opinions_list[agent_i]))))
        if self._is_exposed_to_passive(self.opinions_list[agent_i]):
            new_opinion_j = self._truncate_opinion(self.opinions_list[agent_j] + self.mio_to_use(agent_j) * (
                        1 - 2 * (abs(self.opinions_list[agent_i] - self.opinions_list[agent_j]))))
        new_opinions = np.array(self.opinions_list)
        new_opinions[agent_i] = new_opinion_i
        new_opinions[agent_j] = new_opinion_j
        return new_opinions
