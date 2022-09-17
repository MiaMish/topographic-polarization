from enum import Enum
from typing import Callable, List

DEFAULT_RADICAL_EXPOSURE_ETA = None
DEFAULT_SWITCH_AGENT_SIGMA = 0.2
DEFAULT_SWITCH_AGENT_RATE = None
DEFAULT_NUM_OF_REPETITIONS = 20
DEFAULT_MIO = 0.4
DEFAULT_NUM_OF_ITERATIONS = 300
DEFAULT_NUM_OF_AGENTS = 30
DEFAULT_EPSILON = 0.1
DEFAULT_MARK_STUBBORN_AT = 0.25
DEFAULT_TRUNCATE_AT = 0.001


def default_audit_iteration_predicate(iteration_num: int, num_iterations: int):
    return iteration_num == 1 or (iteration_num + 1) % 30 == 0 or (iteration_num - 1) == num_iterations


class SimulationType(Enum):
    SIMILARITY = 0
    REPULSIVE = 1
    ASSIMILATION = 2


class SimulationConfig:

    def __init__(
            self,
            simulation_type: SimulationType,
            num_of_agents: int = DEFAULT_NUM_OF_AGENTS,
            num_iterations: int = DEFAULT_NUM_OF_ITERATIONS,
            mio: float = DEFAULT_MIO,
            num_of_repetitions: int = DEFAULT_NUM_OF_REPETITIONS,
            switch_agent_rate: float or None = DEFAULT_SWITCH_AGENT_RATE,
            switch_agent_sigma: float or None = DEFAULT_SWITCH_AGENT_SIGMA,
            radical_exposure_eta: float or None = DEFAULT_RADICAL_EXPOSURE_ETA,
            truncate_at: float = DEFAULT_TRUNCATE_AT,
            epsilon: float = DEFAULT_EPSILON,
            mark_stubborn_at: float = DEFAULT_MARK_STUBBORN_AT,
            audit_iteration_predicate: Callable[[int], bool] = lambda iteration_index:
            default_audit_iteration_predicate(iteration_index, DEFAULT_NUM_OF_ITERATIONS),
    ):
        """

        :param simulation_type:
        :param num_of_agents:
        :param num_iterations:
        :param mio: Represents the sensitivity for the opinions of the neighbors.
        If mio is big -> the neighbors have more effect on the agent's opinion.
        :param num_of_repetitions:
        :param switch_agent_rate:
        :param switch_agent_sigma:
        :param radical_exposure_eta: Agent j is influencing in a specific interaction only if 
        a random boolean variable is true. 
        That variable takes the value true with probability p=radical_exposure_eta * abs(0.5 - opinion of j). 
        :param truncate_at: If the update opinion of an agent is outside [x, 1-x],
        we truncate their opinion to be equal to x (or 1-x).
        This is done to prevent cases where opinions are outside ot the valid range ([0, 1]).
        :param epsilon:
        :param mark_stubborn_at: Relevant only for type == ASSIMILATION.
        In that flow, if the initial opinion of an agent is not in between [x, 1 - x] it is marked as stubborn.
        Stubborn agents do not change their opinions through the simulation.
        :param audit_iteration_predicate: determines if iteration is audited
        """
        self.simulation_type = simulation_type
        self.num_of_agents = num_of_agents
        self.num_iterations = num_iterations
        self.mio = mio
        self.num_of_repetitions = num_of_repetitions
        self.switch_agent_rate = switch_agent_rate
        self.switch_agent_sigma = switch_agent_sigma
        self.radical_exposure_eta = radical_exposure_eta
        self.truncate_at = truncate_at
        self.epsilon = epsilon
        self.mark_stubborn_at = mark_stubborn_at
        self.audit_iteration_predicate = audit_iteration_predicate

    def __str__(self):
        flow_config_str = f"flow_type={self.simulation_type}\n" \
                          f"num_of_agents={self.num_of_agents}\n" \
                          f"num_iterations={self.num_iterations}\n" \
                          f"mio={self.mio}\n" \
                          f"num_of_repetitions={self.num_of_repetitions}" \
                          f"switch_agent_rate={self.switch_agent_rate}\n" \
                          f"switch_agent_sigma={self.switch_agent_sigma}\n" \
                          f"radical_exposure_eta={self.radical_exposure_eta}\n" \
                          f"truncate_at={self.truncate_at}\n" \
                          f"epsilon={self.epsilon}\n" \
                          f"mark_stubborn_at={self.mark_stubborn_at}\n"
        return flow_config_str

    def audited_iterations(self) -> List[int]:
        return [i for i in range(self.num_iterations) if self.audit_iteration_predicate(i)]
