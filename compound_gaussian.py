import numpy as np
import matplotlib.pyplot as plt
import math
from utils import get_log_likelihood_ratio, get_fnr
from perf_wrapper import perf_wrapper
from file_list_utils import write_list

N_samples = 100000
N_measurement = 7
MIN_X = -100
MAX_X = 100
ALPHA = 0.95
DEPTH = 7
GAMMA_1 = 2
GAMMA_2 = 3

def std_deviation_generator(depth):
    return 1 / math.pow(depth + 1, 0.5)


def mean_shift(depth):
    return 1 / ((depth + 1) ** 2)


def compound_gaussian(depth, initial_mean, num_measurements):
    experiment_sum = 0
    for meas_index in range(num_measurements):
        final_sample = initial_mean
        for counter in range(depth):
            final_sample = np.random.normal(final_sample,
                                            0.5 if counter == 0 else abs(final_sample))
        experiment_sum += final_sample
    return experiment_sum / num_measurements



def generate_measurements(num_meas, depth):
    hypothesis_1 = []
    hypothesis_2 = []
    file_name = f'./outputs/measurements/measurements_{num_meas}_{depth}_hypo_'
    for counter in range(N_samples):
        hypothesis_1.append(compound_gaussian(depth, GAMMA_1, num_meas))
        hypothesis_2.append(compound_gaussian(depth, GAMMA_2, num_meas))
    write_list(hypothesis_1, f'{file_name}{1}.txt')
    write_list(hypothesis_2, f'{file_name}{2}.txt')
    return hypothesis_1, hypothesis_2

def driver(num_meas, depth):
    generate_measurements(num_meas, depth)


if __name__ == '__main__':
    for n_meas in range(N_measurement):
        for depth in range(DEPTH):
            driver(n_meas+1, depth+1)

