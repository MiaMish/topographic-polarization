
# Tables names
EXPERIMENT_CONFIGS = "experiment_configs"
EXPERIMENT_RESULT = "experiment_result"
SIMULATION_RESULT = "simulation_result"
ITERATION_RESULT = "iteration_result"
MEASUREMENTS = "measurements"

# Fields names
OPINIONS_LIST = "opinions_list"
ITERATION = "iteration"
REPETITION = "repetition"
RUN_TIME = "run_time"
EXPERIMENT_TAGS = "experiment_tags"
TIMESTAMP = "timestamp"
EXPERIMENT_ID = "experiment_id"
DISPLAY_NAME = "display_name"
MARK_STUBBORN_AT = "mark_stubborn_at"
EPSILON = "epsilon"
TRUNCATE_AT = "truncate_at"
RADICAL_EXPOSURE_ETA = "radical_exposure_eta"
SWITCH_AGENT_SIGMA = "switch_agent_sigma"
SWITCH_AGENT_RATE = "switch_agent_rate"
NUM_OF_REPETITIONS = "num_of_repetitions"
MIO = "mio"
NUM_ITERATIONS = "num_iterations"
NUM_OF_AGENTS = "num_of_agents"
SIMULATION_TYPE = "simulation_type"
CONFIG_ID = "config_id"
MEASUREMENT_TYPE = "measurement_type"
X = "x"
VALUE = "value"

TABLES = {
    EXPERIMENT_CONFIGS: [
        CONFIG_ID,
        SIMULATION_TYPE,
        NUM_OF_AGENTS,
        NUM_ITERATIONS,
        MIO,
        NUM_OF_REPETITIONS,
        SWITCH_AGENT_RATE,
        SWITCH_AGENT_SIGMA,
        RADICAL_EXPOSURE_ETA,
        TRUNCATE_AT,
        EPSILON,
        MARK_STUBBORN_AT,
        DISPLAY_NAME
    ],
    EXPERIMENT_RESULT: [
        EXPERIMENT_ID,
        TIMESTAMP,
        RUN_TIME,
        CONFIG_ID,
        EXPERIMENT_TAGS
    ],
    SIMULATION_RESULT: [
        EXPERIMENT_ID,
        REPETITION,
        TIMESTAMP,
        RUN_TIME
    ],
    ITERATION_RESULT: [
        EXPERIMENT_ID,
        REPETITION,
        ITERATION,
        OPINIONS_LIST
    ],
    MEASUREMENTS: [
        EXPERIMENT_ID,
        MEASUREMENT_TYPE,
        X,
        VALUE
    ]
}
