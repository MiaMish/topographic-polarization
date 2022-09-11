from typing import List, Dict

from numpy import random

from simulation.config import SimulationConfig
from simulation.simulation import Simulation


class AssimilationSimulation(Simulation):

    def __init__(self, simulation_config: SimulationConfig):
        super().__init__(simulation_config)
        self.weights_dict: Dict[str, List[int]] = self._init_weights_dict()
        self.stubborn_agents: List[int] = self._mark_stubborn_agents()

    def _mark_stubborn_agents(self) -> List[int]:
        return [i for i in range(len(self.opinions_list))
                if self.opinions_list[i] > self.simulation_config.mark_stubborn_at
                or self.opinions_list[i] < (1 - self.simulation_config.mark_stubborn_at)]

    def _init_weights_dict(self) -> Dict[str, List[int]]:
        weights_dict = {}
        for i in range(0, self.simulation_config.num_of_agents):
            weights_dict[f'{i}'] = []
            weights = random.multinomial(10000, [1.0 / (self.simulation_config.num_of_agents - 1)] * (
                    self.simulation_config.num_of_agents - 1))
            index_in_weights = 0
            for j in range(0, self.simulation_config.num_of_agents):
                if i == j:
                    weights_dict[f'{i}'].append(0)
                else:
                    weights_dict[f'{i}'].append(weights[index_in_weights] / 10000.0)
                    index_in_weights += 1
        return weights_dict

    def _update_single_opinion(self, agent: int) -> float:
        agent_opinion = self.opinions_list[agent]
        if agent in self.stubborn_agents:
            return agent_opinion
        distance_from_neighbors_opinions = [neighbor_opinion - agent_opinion for neighbor_opinion in self.opinions_list]
        neighbors_cumulative_effect = sum([
            distance_from_neighbors_opinions[j] * self.weights_dict[f'{agent}'][j]
            for j in range(len(self.opinions_list))
        ])
        return agent_opinion + self.simulation_config.mio * neighbors_cumulative_effect

    def _update_opinions(self, agent_i, agent_j):
        return [self._update_single_opinion(i) for i in range(self.simulation_config.num_of_agents)]
