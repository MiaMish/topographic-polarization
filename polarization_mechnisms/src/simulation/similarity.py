import numpy as np
from numpy import ndarray

from simulation.config import SimulationConfig
from simulation.simulation import Simulation


class SimilaritySimulation(Simulation):

    def __init__(self, simulation_config: SimulationConfig):
        super().__init__(simulation_config)

    def _is_similar_enough(self, active_opinion: float, passive_opinion: float) -> bool:
        return (-1 * self.simulation_config.epsilon) < active_opinion - passive_opinion < self.simulation_config.epsilon

    def _update_opinions(self, agent_i: int, agent_j: int) -> ndarray:
        new_opinion_i = self.opinions_list[agent_i]
        new_opinion_j = self.opinions_list[agent_j]
        agents_are_similar_enough = self._is_similar_enough(self.opinions_list[agent_i], self.opinions_list[agent_j])
        if agents_are_similar_enough and self._is_exposed_to_passive(self.opinions_list[agent_j]):
            new_opinion_i = self.opinions_list[agent_i] + self.mio_to_use(agent_j) * (
                    self.opinions_list[agent_j] - self.opinions_list[agent_i])
            new_opinion_i = self._truncate_opinion(new_opinion_i)
        if agents_are_similar_enough and self._is_exposed_to_passive(self.opinions_list[agent_i]):
            new_opinion_j = self.opinions_list[agent_j] + self.mio_to_use(agent_j) * (
                    self.opinions_list[agent_i] - self.opinions_list[agent_j])
            new_opinion_j = self._truncate_opinion(new_opinion_j)
        new_opinions = np.array(self.opinions_list)
        new_opinions[agent_i] = new_opinion_i
        new_opinions[agent_j] = new_opinion_j
        return new_opinions
