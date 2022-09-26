EXPERIMENT_CONFIGS = "experiment_configs"
EXPERIMENT_RESULT = "experiment_result"
SIMULATION_RESULT = "simulation_result"
ITERATION_RESULT = "iteration_result"
TABLES = {
    EXPERIMENT_CONFIGS: [
        "config_id",
        "simulation_type",
        "num_of_agents",
        "num_iterations",
        "mio",
        "num_of_repetitions",
        "switch_agent_rate",
        "switch_agent_sigma",
        "radical_exposure_eta",
        "truncate_at",
        "epsilon",
        "mark_stubborn_at",
        "display_name"
    ],
    EXPERIMENT_RESULT: [
        "experiment_id",
        "timestamp",
        "run_time",
        "config_id",
    ],
    SIMULATION_RESULT: [
        "experiment_id",
        "repetition",
        "timestamp",
        "run_time"
    ],
    ITERATION_RESULT: [
        "experiment_id",
        "repetition",
        "iteration",
        "opinions_list"
    ]
}
