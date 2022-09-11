from analyze.analyzer import avg_results_gif
from simulation.config import SimulationConfig, SimulationType
from experiment.experiment import Experiment

if __name__ == "__main__":
    simulation_config = SimulationConfig(SimulationType.SIMILARITY)
    experiment = Experiment(2, simulation_config)
    results = experiment.run_experiment()
    for k in results.simulation_map:
        print(results.simulation_map.get(k).get_results_df())
    avg_results_gif(simulation_config, results, '/Users/miajoskowicz/dev/personal/topographic-polarization/polarization_mechnisms/out/my.gif')
