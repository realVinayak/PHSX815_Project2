import numpy as np
from file_list_utils import read_list
from utils import get_log_likelihood_ratio, get_fnr
import matplotlib.pyplot as plt
from compound_gaussian import MIN_X, MAX_X, ALPHA, N_samples, N_measurement, DEPTH
from histogram_utils import get_histogram_data


def get_probability_from_hist(hist_data, hist_bins, sample):
    bin_index = 0
    probability = 0
    if hist_bins[0] <= sample <= hist_bins[-1]:
        while bin_index <= len(hist_bins) - 2:
            if hist_bins[bin_index] <= sample <= hist_bins[bin_index + 1]:
                break
            bin_index += 1
        probability = hist_data[bin_index]
    return probability


def plot_atomic_result(llr_dist_1, llr_dist_2, lambda_alpha, num_meas, depth):
    file_name = f'./outputs/histograms/measurements_{num_meas}_depth_{depth}.png'
    llr_dist_1_probs, llr_dist_1_bins = get_histogram_data(llr_dist_1,
                                                           100)
    llr_dist_2_probs, llr_dist_2_bins = get_histogram_data(llr_dist_2,
                                                           100)
    plt.plot([], 'r')
    plt.plot([], 'g')
    plt.plot([], 'black')
    plt.plot(llr_dist_1_bins, llr_dist_1_probs, 'r', linewidth=0.8)
    plt.vlines(lambda_alpha, 0,
               max(max(llr_dist_1_probs), max(llr_dist_2_probs)),
               color='black', linewidth=1)
    plt.plot(llr_dist_2_bins, llr_dist_2_probs, 'g', linewidth=0.8
             )
    plt.xlabel('\u03BB = L(H2)/L(H1)')
    plt.ylabel('Probability')
    plt.title(f'{num_meas} number of measurements and depth {depth}')
    plt.legend(['P(\u03BB|H1)', 'P(\u03BB|H2)', f'\u03BB\u1D45 = {round(lambda_alpha, 2)}'])
    plt.savefig(file_name)
    plt.show()
    plt.clf()


def analyze_atomic(num_meas, depth):
    file_name = f'./outputs/measurements/measurements_{num_meas}_{depth}_hypo_'
    hypothesis_1 = read_list(f'{file_name}{1}.txt')
    hypothesis_2 = read_list(f'{file_name}{2}.txt')
    hypothesis_1_data, hypothesis_1_bins = np.histogram(hypothesis_1, 100,
                                                        density=True)
    hypothesis_2_data, hypothesis_2_bins = np.histogram(hypothesis_2, 100,
                                                        density=True)
    llr_distribution_h1 = [get_log_likelihood_ratio(raw_meas,
                                                    lambda
                                                        x: get_probability_from_hist(
                                                        hypothesis_2_data,
                                                        hypothesis_2_bins, x),
                                                    lambda
                                                        x: get_probability_from_hist(
                                                        hypothesis_1_data,
                                                        hypothesis_1_bins, x))
                           for raw_meas in hypothesis_1]
    llr_distribution_h2 = [get_log_likelihood_ratio(raw_meas,
                                                    lambda
                                                        x: get_probability_from_hist(
                                                        hypothesis_2_data,
                                                        hypothesis_2_bins, x),
                                                    lambda
                                                        x: get_probability_from_hist(
                                                        hypothesis_1_data,
                                                        hypothesis_1_bins, x))
                           for raw_meas in hypothesis_2]

    llr_distribution_h1 = list(
        filter(lambda llr: MIN_X <= llr <= MAX_X, llr_distribution_h1))
    llr_distribution_h2 = list(
        filter(lambda llr: MIN_X <= llr <= MAX_X, llr_distribution_h2))
    llr_distribution_h1.sort()
    llr_distribution_h2.sort()
    _lambda_alpha = np.percentile(llr_distribution_h1, 100 * ALPHA)
    fnr = get_fnr(llr_distribution_h2, _lambda_alpha)

    print('n_meas: ', num_meas)
    print('depth: ', depth)
    print('lamda alpha: ', _lambda_alpha)
    print('false negative rate: ', fnr)
    plot_atomic_result(llr_distribution_h1, llr_distribution_h2, _lambda_alpha, num_meas, depth)
    return round(fnr, 2)

def driver():
    fnr_matrix = np.zeros((N_measurement, DEPTH))
    for num_meas in range(N_measurement):
        for depth in range(DEPTH):
            fnr_matrix[num_meas][depth] = analyze_atomic(num_meas+1, depth+1)
    print(fnr_matrix)
    fig, ax = plt.subplots()
    im = ax.imshow(fnr_matrix, cmap='hot')

    for row in range(N_measurement):
        for col in range(DEPTH):
            text = ax.text(col, row, fnr_matrix[row][col], ha="center", va="center",
                           color="w" if fnr_matrix[row][col] < 0.5 else 'black')

    ax.set_yticks(range(N_measurement), labels=range(1, N_measurement+1))
    ax.set_xticks(range(DEPTH), labels=range(1, DEPTH+1))
    plt.title('False Negative Rate Heatmap')
    ax.figure.colorbar(im)
    plt.ylabel('Number of Measurements')
    plt.xlabel('Depth')
    fig.savefig('fnr_heatmap.png')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    driver()