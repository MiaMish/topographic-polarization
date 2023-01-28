import datetime
from abc import abstractmethod, ABC

import numpy as np
from numpy import random, abs, ndarray

from simulation.config import SimulationConfig, MioDistType
from simulation.result import IterationResult, SimulationResult

DEFAULT_MIN_MIO = 0.05


class Simulation(ABC):

    def __init__(
            self,
            simulation_config: SimulationConfig
    ):
        self.simulation_config = simulation_config
        self.opinions_list: ndarray = self._init_opinion_list()

    def _init_opinion_list(self) -> ndarray:
        return random.uniform(0.0, 1.0, self.simulation_config.num_of_agents)

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
        probability_to_be_exposed = 1 - self.simulation_config.radical_exposure_eta * abs(0.5 - passive_agent_opinion)
        if probability_to_be_exposed > 1:
            return True
        if probability_to_be_exposed < 0:
            return False
        return np.random.binomial(1, probability_to_be_exposed) == 1

    def mio_to_use(self, agent: int) -> float:
        if self.simulation_config.mio_dist_type is None:
            result = self.simulation_config.mio
            return result
        max_mio = 2 * self.simulation_config.mio - DEFAULT_MIN_MIO
        min_mio = DEFAULT_MIN_MIO

        # In general,
        # mio_to_use = ax^2 + bx + c, when x is the agent's index.
        # a, b and c are calculated according to the distribution type.
        a = b = c = 0
        if self.simulation_config.mio_dist_type == MioDistType.UNIFORM:
            # No `a` (should be linear)
            a = 0
            # ((max_min - min_mio) / (num_of_agents - 1))
            b = ((max_mio - min_mio) / (self.simulation_config.num_of_agents - 1))
            # min_mio
            c = min_mio
        if self.simulation_config.mio_dist_type == MioDistType.UP:
            # 4 * min_mio / (num_of_agents - 1)**2
            a = 4 * min_mio * (1 / ((self.simulation_config.num_of_agents - 1) * (self.simulation_config.num_of_agents - 1)))
            # (max_mio - 5 * min_mio) / (num_of_agents - 1)
            b = (max_mio - 5 * min_mio) / (self.simulation_config.num_of_agents - 1)
            # min_mio
            c = min_mio
        if self.simulation_config.mio_dist_type == MioDistType.DOWN:
            # min_mio / (num_of_agents - 1)**2
            a = min_mio * (1 / ((self.simulation_config.num_of_agents - 1) * (self.simulation_config.num_of_agents - 1)))
            # -1 * max_mio / (num_of_agents - 1)
            b = - max_mio / (self.simulation_config.num_of_agents - 1)
            # max_mio
            c = max_mio
        return a * agent * agent + b * agent + c

    def run_simulation(self) -> SimulationResult:
        results = SimulationResult()
        results.timestamp = datetime.datetime.now()
        for iteration in range(self.simulation_config.num_iterations):
            if self.simulation_config.should_audit_iteration(iteration):
                results.add_iteration_result(iteration, IterationResult(self.opinions_list))
            if self._should_switch_agents():
                agent_to_switch = random.choice(range(self.simulation_config.num_of_agents), replace=False)
                new_agent_opinion = self._truncate_opinion(random.normal(self.opinions_list[agent_to_switch], self.simulation_config.switch_agent_sigma))
                self.opinions_list[agent_to_switch] = new_agent_opinion
                continue
            agent_i, agent_j = random.choice(range(self.simulation_config.num_of_agents), 2, replace=False)
            if self._is_exposed_to_passive(self.opinions_list[agent_j]):
                self.opinions_list = self._update_opinions(agent_i, agent_j)
        results.run_time = datetime.datetime.now() - results.timestamp
        return results

    @abstractmethod
    def _update_opinions(self, agent_i: int, agent_j: int) -> ndarray:
        pass
