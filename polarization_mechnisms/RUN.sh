mkdir -p "$PWD/../resources/feb04/stubbornness/"
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" clear-db

#Repulsive for constant mio between 0 and 0.5
#min_val: 0.000000, max_val: 0.500000, step: 0.050000
#0.000000,0.050000,0.100000,0.150000,0.200000,0.250000,0.300000,0.350000,0.400000,0.450000,0.500000
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types REPULSIVE --mios 0.000000,0.050000,0.100000,0.150000,0.350000,0.400000,0.450000,0.50000 --mio_sigmas None --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

#Repulsive for normal distribution with constant mio=0.2
#min_val: 0.000001, max_val: 0.077641, step: 0.007764
#0.000001,0.007765,0.015529,0.023293,0.031057,0.038821,0.046585,0.054349,0.062113,0.069877,0.077641
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types REPULSIVE --mios 0.2 --mio_sigmas 0.000001,0.007765,0.015529,0.023293,0.031057,0.038821,0.046585,0.054349,0.062113,0.069877,0.077641 --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

#Repulsive for normal distribution with constant sigma=0.075
#min_val: 0.193200, max_val: 0.306800, step: 0.011360
#0.193200,0.204560,0.215920,0.227280,0.238640,0.250000,0.261360,0.272720,0.284080,0.295440,0.306800
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types REPULSIVE --mios 0.193200,0.2,0.204560,0.215920,0.227280,0.238640,0.25,0.261360,0.272720,0.284080,0.295440,0.3,0.306800 --mio_sigmas 0.075,None --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

#Similarity for constant mio between 0 and 1
#min_val: 0.000000, max_val: 1.000000, step: 0.100000
#0.000000,0.100000,0.200000,0.300000,0.400000,0.500000,0.600000,0.700000,0.800000,0.900000,1.000000
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types SIMILARITY --mios 0.000000,0.100000,0.900000,1.000000 --mio_sigmas None --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

#Similarity for normal distribution with constant mio=0.2
#min_val: 0.000001, max_val: 0.077641, step: 0.007764
#0.000001,0.007765,0.015529,0.023293,0.031057,0.038821,0.046585,0.054349,0.062113,0.069877,0.077641
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types SIMILARITY --mios 0.2 --mio_sigmas 0.000001,0.007765,0.015529,0.023293,0.031057,0.038821,0.046585,0.054349,0.062113,0.069877,0.077641 --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

#Similarity for normal distribution with constant sigma=0.075
#min_val: 0.193200, max_val: 0.806800, step: 0.061360
#0.193200,0.254560,0.315920,0.377280,0.438640,0.500000,0.561360,0.622720,0.684080,0.745440,0.806800
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" append-configs --simulation_types SIMILARITY --mios 0.193200,0.2,0.254560,0.3,0.315920,0.377280,0.4,0.438640,0.5,0.561360,0.6,0.622720,0.684080,0.7,0.745440,0.8,0.806800 --mio_sigmas 0.075,None --epsilons 0.2 --radical_exposure_etas None --switch_agent_rates None --switch_agent_sigmas None

./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" run-experiments
./cli.py --base_db_path "$PWD/../resources/feb04/stubbornness/" generate-combined
