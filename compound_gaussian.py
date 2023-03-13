import numpy as np
from file_list_utils import write_list

N_experiments = 100000
N_measurement = 7
MIN_X = -100
MAX_X = 100
ALPHA = 0.95
DEPTH = 7
GAMMA_1 = 2
GAMMA_2 = 3


# Takes in the number of measurements, the initial_mean and depth and returns
# a sample drawn from the complex "compound" gaussian with input depth.
# Generates the first sample from normal(initial_mean, 0.5) and the remaining
# samples are drawn from normal(x_previous, abs(x_previous)) where x_previous
# is random sample from previous iteration. Repeats the process num_measurements
# times and then averages the result to simulate one experiment.
def compound_gaussian(depth, initial_mean, num_measurements):
    experiment_sum = 0
    for meas_index in range(num_measurements):
        final_sample = initial_mean
        for counter in range(depth):
            final_sample = np.random.normal(final_sample,
                                            0.5 if counter == 0 else abs(
                                                final_sample))
        experiment_sum += final_sample
    return experiment_sum / num_measurements


# Generates N_experiments samples from both hypothesis 1 and hypothesis 2
# for a particular number of measurements and depth.
# Stores the result in ./outputs/measurements
def generate_measurements(num_meas, depth):
    hypothesis_1 = []
    hypothesis_2 = []
    file_name = f'./outputs/measurements/measurements_{num_meas}_{depth}_hypo_'
    for counter in range(N_experiments):
        hypothesis_1.append(compound_gaussian(depth, GAMMA_1, num_meas))
        hypothesis_2.append(compound_gaussian(depth, GAMMA_2, num_meas))
    write_list(hypothesis_1, f'{file_name}{1}.txt')
    write_list(hypothesis_2, f'{file_name}{2}.txt')
    return hypothesis_1, hypothesis_2


# Simulates a set of experiments multiple times and varies n_meas and depth
# N_measurement and DEPTH are predefined constants at the top of this file
if __name__ == '__main__':
    for n_meas in range(N_measurement):
        for _depth in range(DEPTH):
            generate_measurements(n_meas + 1, _depth + 1)
