from typing import List

import numpy as np
from numpy import random, abs

from flow_config import SimulationConfig, DEFAULT_EPSILON
from flow_results import FlowResults, IterationResult


class _BaseFlow:

    def __init__(
            self,
            flow_config: SimulationConfig
    ):
        self.flow_config = flow_config

    def __str__(self):
        return f"type={type(self).__name__}\n" \
               f"{self.flow_config}"

    def initial_opinion_list(self) -> List[float]:
        return [random.uniform(0.0, 1.0) for _ in range(0, self.flow_config.num_of_agents)]

    def generate_switch_agents_at_iteration(self):
        if self.flow_config.switch_agent_rate is None:
            return 0
        else:
            return np.random.binomial(1, 1 / self.flow_config.switch_agent_rate)

    def truncate_opinion(self, opinion_of_agent_to_switch):
        opinion = random.normal(opinion_of_agent_to_switch, self.flow_config.switch_agent_sigma)
        if opinion > 0.999:
            return 0.999
        if opinion < 0.001:
            return 0.001
        return opinion

    def is_exposed_to_passive(self, passive_agent_opinion):
        if self.flow_config.radical_exposure_eta is None:
            return True
        return np.random.binomial(1, self.flow_config.radical_exposure_eta * abs(0.5 - passive_agent_opinion)) == 1

    def run_flow(self) -> FlowResults:
        print(f"Starting to run {self}")
        random.seed(10)
        results = FlowResults(self.flow_config.num_of_repetitions, self.flow_config.num_of_agents)
        for repetition in range(self.flow_config.num_of_repetitions):
            opinions_list = self.initial_opinion_list()
            for iteration in range(1, self.flow_config.num_iterations):
                # update results
                if iteration == 1 or (iteration + 1) % self.flow_config.scatter_every == 0 or (
                        iteration - 1) == self.flow_config.num_iterations:
                    results.add_repetition_result(repetition, iteration, IterationResult(opinions_list))
                if self.generate_switch_agents_at_iteration() == 1:
                    agent_to_switch = random.choice(range(self.flow_config.num_of_agents), replace=False)
                    new_agent_opinion = self.truncate_opinion(opinions_list[agent_to_switch])
                    opinions_list[agent_to_switch] = new_agent_opinion
                agent_i, agent_j = random.choice(range(self.flow_config.num_of_agents), 2, replace=False)
                if self.is_exposed_to_passive(opinions_list[agent_j]):
                    opinions_list = self.update_opinions(opinions_list, agent_i, agent_j)
        return results

    def update_opinions(self, opinions_list, agent_i, agent_j):
        pass


class SimilarityFlow(_BaseFlow):

    def __init__(self, flow_config: SimulationConfig):
        super().__init__(flow_config)

    def is_similar_enough(self, active_opinion, passive_opinion):
        return (-1 * self.flow_config.epsilon) < active_opinion - passive_opinion < self.epsilon

    def update_opinions(self, opinions_list, agent_i, agent_j):
        new_opinion_i = opinions_list[agent_i]
        new_opinion_j = opinions_list[agent_j]
        if self.is_similar_enough(opinions_list[agent_i],
                                  opinions_list[agent_j]):
            new_opinion_i = opinions_list[agent_i] + self.flow_config.mio * (
                    opinions_list[agent_j] - opinions_list[agent_i])
        if self.is_similar_enough(opinions_list[agent_i],
                                  opinions_list[agent_j]):
            new_opinion_j = opinions_list[agent_j] + self.flow_config.mio * (
                    opinions_list[agent_i] - opinions_list[agent_j])
        return [
            new_opinion_i if k == agent_i else (new_opinion_j if k == agent_j else opinions_list[k]) for k in
            range(self.flow_config.num_of_agents)]

    def __str__(self):
        return f"{super().__str__()}" \
               f"epsilon={self.epsilon}"


class RepulsiveFlow(_BaseFlow):

    def __init__(self, flow_config: SimulationConfig):
        super().__init__(flow_config)


class AssimilationFlow(_BaseFlow):
    def __init__(self, flow_config: SimulationConfig):
        super().__init__(flow_config)

    def update_opinion_assimilation(self, opinions_list, stubborn_agents, weights_dict, agent, mio):
        prev_opinion = opinions_list[agent]
        if agent in stubborn_agents:
            return prev_opinion
        neighbors_opinions = [prev_opinion_for_neighbor - prev_opinion for prev_opinion_for_neighbor in opinions_list]
        neighbors_opinions_weights_mul_sum = sum(
            [neighbors_opinions[j] * weights_dict[f'{agent}'][j] for j in range(len(opinions_list))])
        return prev_opinion + mio * neighbors_opinions_weights_mul_sum

    def update_opinions(self, opinions_list, agent_i, agent_j):
        weights_dict = generate_weights_dict(num_of_agents)
        opinions_list = initial_opinion_list(num_of_agents)
        stubborn_agents = choose_stubborn_agents(percent_of_stubborn_agents_threshold, opinions_list)
        return [self.update_opinion_assimilation(opinions_list, stubborn_agents, weights_dict, i, mio) for i in
                range(num_of_agents)]
