import math


# Returns log likelihood ratio given callbacks for first probability and
# second probability and measurement
def get_log_likelihood_ratio(measurement, get_first_prob, get_second_prob):
    first_prob = get_first_prob(measurement)
    second_prob = get_second_prob(measurement)
    log_likelihood_ratio = math.log(
        max(first_prob, 10**(-50)) / max(second_prob, 10**(-50)))
    return log_likelihood_ratio

# Returns false negative rate given llr measurements and lambda threshold
def get_fnr(llr_measurements, lambda_threshold):
    llr_passed_count = 0
    for llr in llr_measurements:
        if llr > lambda_threshold:
            break
        llr_passed_count += 1
    return llr_passed_count / len(llr_measurements)

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
