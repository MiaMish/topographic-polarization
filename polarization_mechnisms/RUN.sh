./cli.py clear-db
./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas None,0.2,0.4,0.6 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments

./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas 0.01,0.05,0.1 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py scatter-plot --store_file spread_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type SPREAD --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file covered_bins_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type COVERED_BINS --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file dispersion_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type DISPERSION --switch_agent_rate None --switch_agent_sigma None

./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas 0.001 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments

./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas 1,1.5,1.99 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py scatter-plot --store_file spread_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type SPREAD --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file covered_bins_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type COVERED_BINS --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file dispersion_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type DISPERSION --switch_agent_rate None --switch_agent_sigma None

./cli.py clear-db
./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas None,0.01,0.2,1,2,5 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py scatter-plot --store_file spread_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type SPREAD --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file covered_bins_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type COVERED_BINS --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file dispersion_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type DISPERSION --switch_agent_rate None --switch_agent_sigma None

./cli.py clear-db
./cli.py append-configs --simulation_types SIMILARITY --mios 0.2 --epsilons 0.2 --radical_exposure_etas None,0.01,0.2,1,2,5 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py scatter-plot --store_file spread_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type SPREAD --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file covered_bins_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type COVERED_BINS --switch_agent_rate None --switch_agent_sigma None
./cli.py scatter-plot --store_file dispersion_radical_similarity --simulation_type SIMILARITY --mio 0.2 --epsilon 0.2 --measurement_type DISPERSION --switch_agent_rate None --switch_agent_sigma None


./cli.py clear-db
./cli.py append-configs --simulation_types SIMILARITY,REPULSIVE --mios 0.2 --epsilons 0.2 --radical_exposure_etas None,0.01,0.05,0.1,0.2,0.4,0.6,1,2,3,5,10 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py generate-combined

./cli.py append-configs --simulation_types SIMILARITY,REPULSIVE --mios 0.2 --epsilons 0.2 --radical_exposure_etas 0.8,1.2,1.4,1.6,1.8,2,2.2,2.4 --switch_agent_rates None --switch_agent_sigmas None
./cli.py run-experiments
./cli.py generate-combined
