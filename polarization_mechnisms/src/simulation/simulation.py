from abc import abstractmethod, ABC
from typing import List

import numpy as np
from numpy import random, abs

from simulation.config import SimulationConfig
from simulation.result import IterationResult, SimulationResult


class Simulation(ABC):

    def __init__(
            self,
            simulation_config: SimulationConfig
    ):
        self.simulation_config = simulation_config
        self.opinions_list = self._init_opinion_list()

    def _init_opinion_list(self) -> List[float]:
        return [random.uniform(0.0, 1.0) for _ in range(0, self.simulation_config.num_of_agents)]

    def _should_switch_agents(self) -> bool:
        if self.simulation_config.switch_agent_rate is None:
            return False
        else:
            return np.random.binomial(1, 1 / self.simulation_config.switch_agent_rate) == 1

    def _truncate_opinion(self, opinion: float) -> float:
        # TODO: I'm not sure if it's the right logic... Consider other options.
        if opinion > 1 - self.simulation_config.truncate_at:
            return 1 - self.simulation_config.truncate_at
        if opinion < self.simulation_config.truncate_at:
            return self.simulation_config.truncate_at
        return opinion

    def _is_exposed_to_passive(self, passive_agent_opinion: float) -> bool:
        if self.simulation_config.radical_exposure_eta is None:
            return True
        return np.random.binomial(1, self.simulation_config.radical_exposure_eta * abs(0.5 - passive_agent_opinion)) == 1

    def run_simulation(self) -> SimulationResult:
        results = SimulationResult()
        for iteration in range(self.simulation_config.num_iterations):
            if self.simulation_config.audit_iteration_predicate(iteration):
                results.add_iteration_result(iteration, IterationResult(self.opinions_list))
            if self._should_switch_agents():
                agent_to_switch = random.choice(range(self.simulation_config.num_of_agents), replace=False)
                new_agent_opinion = self._truncate_opinion(self.opinions_list[agent_to_switch])
                self.opinions_list[agent_to_switch] = new_agent_opinion
                continue
            agent_i, agent_j = random.choice(range(self.simulation_config.num_of_agents), 2, replace=False)
            if self._is_exposed_to_passive(self.opinions_list[agent_j]):
                self.opinions_list = self._update_opinions(agent_i, agent_j)
        return results

    @abstractmethod
    def _update_opinions(self, agent_i: int, agent_j: int) -> List[float]:
        pass
