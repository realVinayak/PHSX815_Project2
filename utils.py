import math


# Returns log likelihood ratio given callbacks for first probability and
# second probability and measurement
def get_log_likelihood_ratio(measurement, get_first_prob, get_second_prob):
    first_prob = get_first_prob(measurement)
    second_prob = get_second_prob(measurement)
    log_likelihood_ratio = math.log(
        max(first_prob, 10**(-20)) / max(second_prob, 10**(-20)))
    return log_likelihood_ratio

# Returns false negative rate given llr measurements and lambda threshold
def get_fnr(llr_measurements, lambda_threshold):
    llr_passed_count = 0
    for llr in llr_measurements:
        if llr > lambda_threshold:
            break
        llr_passed_count += 1
    return llr_passed_count / len(llr_measurements)