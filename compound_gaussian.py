import numpy as np
import matplotlib.pyplot as plt
import math
from utils import get_log_likelihood_ratio, get_fnr
from perf_wrapper import perf_wrapper

N_samples = 500000
N_measurement = 20
MIN_X = -20
MAX_X = 20
ALPHA = 0.95


def std_deviation_generator(depth):
    return 1 / math.pow(depth + 1, 0.5)


def mean_shift(depth):
    return 1 / ((depth + 1) ** 2)


def compound_gaussian(depth, initial_mean, num_measurements):
    experiment_sum = 0
    for meas_index in range(num_measurements):
        final_sample = initial_mean
        for counter in range(depth):
            final_sample = np.random.normal(final_sample + mean_shift(counter),
                                            std_deviation_generator(counter))
        experiment_sum += final_sample
    return experiment_sum / num_measurements


def get_probability_from_hist(hist_data, hist_bins, sample):
    bin_index = 0
    probability = 0
    if hist_bins[0] <= sample <= hist_bins[-1]:
        while bin_index <= len(hist_bins)-2:
            if hist_bins[bin_index] <= sample <= hist_bins[bin_index+1]:
                break
            bin_index += 1
        probability = hist_data[bin_index]
    return probability


def driver():
    hypothesis_1 = []
    hypothesis_2 = []
    for counter in range(N_samples):
        hypothesis_1.append(compound_gaussian(20, 1, N_measurement))
        hypothesis_2.append(compound_gaussian(20, 4, N_measurement))
    hypothesis_1_data, hypothesis_1_bins = np.histogram(hypothesis_1, 100,  density=True)
    hypothesis_2_data, hypothesis_2_bins = np.histogram(hypothesis_2, 100, density=False)
    llr_distribution_h1 = [get_log_likelihood_ratio(raw_meas,
                                                    lambda x: get_probability_from_hist(hypothesis_2_data, hypothesis_2_bins, x),
                                                    lambda x: get_probability_from_hist(hypothesis_1_data, hypothesis_1_bins, x))
                           for raw_meas in hypothesis_1]
    llr_distribution_h2 = [get_log_likelihood_ratio(raw_meas,
                                                    lambda x: get_probability_from_hist(hypothesis_2_data, hypothesis_2_bins, x),
                                                    lambda x: get_probability_from_hist(hypothesis_1_data, hypothesis_1_bins, x))
                           for raw_meas in hypothesis_2]

    llr_distribution_h1 = list(filter(lambda llr: MIN_X <= llr <= MAX_X, llr_distribution_h1))
    llr_distribution_h2 = list(filter(lambda llr: MIN_X <= llr <= MAX_X, llr_distribution_h2))
    llr_distribution_h1.sort()
    llr_distribution_h2.sort()
    _lambda_alpha = np.percentile(llr_distribution_h1, 100 * ALPHA)
    fnr = get_fnr(llr_distribution_h2, _lambda_alpha)
    print(len(llr_distribution_h1))
    print(len(llr_distribution_h2))
    print('lamda alpha: ', _lambda_alpha)
    print('false negative rate: ', fnr)
    plt.hist(llr_distribution_h1, 100, density=True)
    plt.hist(llr_distribution_h2, 100, density=True)
    plt.savefig('test.png')


if __name__ == '__main__':
    driver()
