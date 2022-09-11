# from copy import deepcopy
# from datetime import datetime
#
# from numpy import random
#
# from analyzer import print_avg_results
# from helpers import generate_weights_dict, choose_stubborn_agents, update_opinion_assimilation
#
#
# def run_similarity_flow(
#         title,
#         num_of_agents=300,
#         num_iterations=300,
#         scatter_every=30,
#         mio=0.4,
#         num_of_repetitions=20,
#         epsilon=0.1,
#         switch_agent_rate=None,
#         switch_agent_sigma=0.2,
#         radical_exposure_eta=None
# ):
#     print(f"Running similarity flow for:\n"
#           f"title={title}\n"
#           f"num_of_agents={num_of_agents}\n"
#           f"num_iterations={num_iterations}\n"
#           f"scatter_every={scatter_every}\n"
#           f"mio={mio}\n"
#           f"epsilon={epsilon}\n"
#           f"num_of_repetitions={num_of_repetitions}\n"
#           f"epsilon={epsilon}\n"
#           f"switch_agent_rate={switch_agent_rate}\n"
#           f"switch_agent_sigma={switch_agent_sigma}\n"
#           f"radical_exposure_eta={radical_exposure_eta}")
#     random.seed(10)
#     results = [{} for _ in range(num_of_repetitions)]
#     for repetition in range(num_of_repetitions):
#         opinions_list = initial_opinion_list(num_of_agents)
#         switch_agents_at_iterations = generate_switch_agents_at_iterations(switch_agent_rate, num_iterations)
#         for iteration in range(1, num_iterations):
#             if iteration == 1 or (iteration + 1) % scatter_every == 0 or (iteration - 1) == num_iterations:
#                 to_results = sorted(deepcopy(opinions_list))
#                 results[repetition][f"{iteration}"] = to_results
#             if switch_agents_at_iterations[iteration] == 1:
#                 agent_to_switch = random.choice(range(num_of_agents), replace=False)
#                 new_agent_opinion = truncate_opinion(random.normal(opinions_list[agent_to_switch], switch_agent_sigma))
#                 opinions_list[agent_to_switch] = new_agent_opinion
#             agent_i, agent_j = random.choice(range(num_of_agents), 2, replace=False)
#             new_opinion_i = opinions_list[agent_i]
#             new_opinion_j = opinions_list[agent_j]
#             if is_similar_enough(epsilon, opinions_list[agent_i], opinions_list[agent_j]) and is_exposed_to_passive(radical_exposure_eta, opinions_list[agent_j]):
#                 new_opinion_i = opinions_list[agent_i] + mio * (opinions_list[agent_j] - opinions_list[agent_i])
#             if is_similar_enough(epsilon, opinions_list[agent_i], opinions_list[agent_j]) and is_exposed_to_passive(radical_exposure_eta, opinions_list[agent_i]):
#                 new_opinion_j = opinions_list[agent_j] + mio * (opinions_list[agent_i] - opinions_list[agent_j])
#             opinions_list = [new_opinion_i if k == agent_i else (new_opinion_j if k == agent_j else opinions_list[k]) for k in range(num_of_agents)]
#     print_avg_results(results, title)
#
#
# def run_assimilation_flow(
#         title,
#         num_of_agents=30,
#         num_iterations=5,
#         scatter_every=1,
#         mio=0.1,
#         percent_of_stubborn_agents_threshold=0.5,
#         num_of_repetitions=5,
#         switch_agent_rate=None,
#         switch_agent_sigma=0.2
# ):
#     print(f"Running assimilation flow for:\n"
#           f"title={title}\n"
#           f"num_of_agents={num_of_agents}\n"
#           f"num_iterations={num_iterations}\n"
#           f"scatter_every={scatter_every}\n"
#           f"mio={mio}\n"
#           f"percent_of_stubborn_agents_threshold={percent_of_stubborn_agents_threshold}\n"
#           f"num_of_repetitions={num_of_repetitions}"
#           f"switch_agent_rate={switch_agent_rate}\n"
#           f"switch_agent_sigma={switch_agent_sigma}\n")
#     random.seed(10)
#     results = [{} for _ in range(num_of_repetitions)]
#     for repetition in range(num_of_repetitions):
#         repetition_start = datetime.now()
#         print(f"Starting repetition #{repetition} out of {num_of_repetitions}")
#         weights_dict = generate_weights_dict(num_of_agents)
#         opinions_list = initial_opinion_list(num_of_agents)
#         stubborn_agents = choose_stubborn_agents(percent_of_stubborn_agents_threshold, opinions_list)
#         switch_agents_at_iterations = generate_switch_agents_at_iterations(switch_agent_rate, num_iterations)
#         for iteration in range(1, num_iterations):
#             if iteration == 1 or (iteration + 1) % scatter_every == 0 or (iteration - 1) == num_iterations:
#                 to_results = sorted(deepcopy(opinions_list))
#                 results[repetition][f"{iteration}"] = to_results
#             if switch_agents_at_iterations[iteration] == 1:
#                 agent_to_switch = random.choice(range(num_of_agents), replace=False)
#                 new_agent_opinion = truncate_opinion(random.normal(opinions_list[agent_to_switch], switch_agent_sigma))
#                 opinions_list[agent_to_switch] = new_agent_opinion
#             opinions_list = [update_opinion_assimilation(opinions_list, stubborn_agents, weights_dict, i, mio) for i in range(num_of_agents)]
#         print(f"Finished repetition #{repetition} in {(repetition_start - datetime.now()).seconds} seconds")
#     print_avg_results(results, title)
