"""
Util for parameters adjustments
"""

import numpy as np
from scipy.stats import norm

NUM_OF_AGENTS = 100


def is_valid(mio, sigma, min_mio=0.0, max_mio=1.0):
    return norm.ppf(0.5 / NUM_OF_AGENTS, loc=mio, scale=sigma) > min_mio and \
           norm.ppf((NUM_OF_AGENTS - 0.5) / NUM_OF_AGENTS, loc=mio, scale=sigma) < max_mio


def find_sigmas(mio, min_mio=0.0, max_mio=1.0, num_of_sigmas=10):
    sigmas = [sigma for sigma in np.arange(0.000001, 0.1, 0.1/10000) if is_valid(sigma=sigma, mio=mio, min_mio=min_mio, max_mio=max_mio)]
    to_input_array(sigmas, num_of_sigmas)


def find_mios(sigma, min_mio=0.0, max_mio=1.0, num_of_mios=10):
    mios = [mio for mio in np.arange(min_mio, max_mio, (max_mio - min_mio)/10000) if is_valid(sigma=sigma, mio=mio, min_mio=min_mio, max_mio=max_mio)]
    return to_input_array(mios, num_of_mios)


def to_input_array(possible_values, num_of_values=10):
    min_val = min(possible_values)
    max_val = max(possible_values)
    step = (max_val - min_val) / num_of_values
    result = np.arange(min_val, max_val, step)
    results_to_print = ",".join([f"{val:f}" for val in result])
    print(f"min_val: {min_val:f}, max_val: {max_val:f}, step: {step:f}\n{results_to_print}")
    return result


def find_mio_sigma_for_insistence_mechanism():
    # in repulsive, mio can get values between 0, 0.5
    print(f"Repulsive for constant mio between 0 and 0.5")
    to_input_array([0, 0.5])
    print(f"Repulsive for normal distribution with constant mio=0.2")
    find_sigmas(mio=0.2, min_mio=0, max_mio=0.5)
    print(f"Repulsive for normal distribution with constant sigma=0.075")
    find_mios(sigma=0.075, min_mio=0, max_mio=0.5)
    # in similarity, mio can get values between 0, 1
    print(f"Similarity for constant mio between 0 and 1")
    to_input_array([0, 1])
    print(f"Similarity for normal distribution with constant mio=0.2")
    find_sigmas(mio=0.2, min_mio=0, max_mio=1)
    print(f"Similarity for normal distribution with constant sigma=0.075")
    find_mios(sigma=0.075, min_mio=0, max_mio=1)


find_mio_sigma_for_insistence_mechanism()

