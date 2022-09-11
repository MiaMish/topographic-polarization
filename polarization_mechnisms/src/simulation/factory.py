from simulation.assimilation import AssimilationSimulation
from simulation.config import SimulationConfig, SimulationType
from simulation.repulsive import RepulsiveSimulation
from simulation.similarity import SimilaritySimulation
from simulation.simulation import Simulation


def create_simulation(simulation_config: SimulationConfig) -> Simulation:
    if simulation_config.simulation_type == SimulationType.REPULSIVE:
        return RepulsiveSimulation(simulation_config)
    elif simulation_config.simulation_type == SimulationType.SIMILARITY:
        return SimilaritySimulation(simulation_config)
    elif simulation_config.simulation_type == SimulationType.ASSIMILATION:
        return AssimilationSimulation(simulation_config)
    raise NotImplementedError(f"No constructor for simulation_type={simulation_config.simulation_type}")
