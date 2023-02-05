import datetime
from abc import abstractmethod, ABC

import numpy as np
from numpy import random, abs, ndarray
import scipy.stats as sps
from simulation.config import SimulationConfig
from simulation.result import IterationResult, SimulationResult

DEFAULT_MIN_MIO = 0.05


class Simulation(ABC):

    def __init__(
            self,
            simulation_config: SimulationConfig
    ):
        self.simulation_config = simulation_config
        self.opinions_list: ndarray = self._init_opinion_list()
        self.mio_list: ndarray = self._init_mio_list()

    def _init_opinion_list(self) -> ndarray:
        return random.uniform(0.0, 1.0, self.simulation_config.num_of_agents)

    def _init_mio_list(self) -> ndarray:
        if self.simulation_config.mio_sigma is None:
            return np.full(self.simulation_config.num_of_agents, self.simulation_config.mio)
        dist = sps.norm(loc=self.simulation_config.mio, scale=self.simulation_config.mio_sigma)
        mios = np.asarray([dist.ppf((agent + 0.5) / self.simulation_config.num_of_agents) for agent in range(self.simulation_config.num_of_agents)])
        if mios[0] < 0:
            raise ValueError("MIOs are negative")
        return mios

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
        return self.mio_list[agent]

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
