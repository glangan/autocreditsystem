import numpy as np
import matplotlib.pyplot as plt

#level1 = ['48023', 'CAB201', 'COMP115', 'FIT1040', 'INFO1103']
level2 = ['KIT207', 'KIT204', 'KIT206', 'KIT205', 'KIT201']
#count elements in a nested dictionary
def count_nested(mdict):
    count = 0
    for key, value in mdict.iteritems():
        for key2 in value.keys():
            count += 1

    return count

#count elements higher than a threshold in a nested dictionary
def count_nested_threshold(mdict, threshold):
    count = 0
    for key, value in mdict.iteritems():
        for nested_key, nested_value in value.iteritems():
            if nested_value >= threshold:
                count += 1

    return count
#count elements using levels
def count_nested_threshold_pos(mdict, threshold):
    count = 0
    for key, value in mdict.iteritems():
        for nested_key, nested_value in value.iteritems():
            if nested_value >= threshold:
                if (key in level2 or nested_key in level2):
                    continue
                else:
                    count += 1

    return count

#calculate false positive and false negative error rates
def error_rates(more_sim, others_sim, threshold):
    #calculate number of items in both dicts
    number_more_sim = count_nested(more_sim)
    number_others_sim = count_nested(others_sim)

    #calculate number of false positive and false negative
    false_negative = number_more_sim - count_nested_threshold(more_sim, threshold)
    false_positive = count_nested_threshold_pos(others_sim, threshold)

    #rates
    fn_rate = false_negative / float(number_more_sim)
    fp_rate = false_positive / ((float(number_others_sim)) - 100)

    return [fn_rate, fp_rate]

#Plot false negative and false positive rates
def plot_ds(more_sim, others_sim):
    values = np.arange(0.0, 1.0, 0.01)
    fp_values = []
    fn_values = []
    for val in values:
        result = error_rates(more_sim, others_sim, val)
        fn_values.append(result[0])
        fp_values.append(result[1])

    plt.plot(values, fp_values, label="False Positive Rate", color='b', linewidth=2.0, linestyle='--')
    plt.plot(values, fn_values, label="False Negative Rate", color='b', linewidth=2.0, linestyle='-')
    plt.xlabel('Threshold')
    plt.ylabel('Rate')
    plt.legend(loc = 3)
    plt.grid()
    plt.show()

#Calculate false negative rate
def error_fn(more_sim, threshold):
    number_more_sim = count_nested(more_sim)
    false_negative = number_more_sim - count_nested_threshold(more_sim, threshold)
    fn_rate = false_negative / float(number_more_sim)
    return fn_rate

#Plot false negative rate only
def plot_fn(more_sim):
    values = np.arange(0, 1.0, 0.01)
    fn_values = []
    for val in values:
        fn_values.append(error_fn(more_sim, val))
    plt.plot(values, fn_values, label="False Negative Rate", color='b', linewidth=2.0)
    plt.xlabel('Threshold')
    plt.ylabel('Rate')
    plt.legend(loc = 2)
    plt.grid()
    plt.show()

def print_thr(sim, thr):
    for key, value in sim.iteritems():
        for k, v in value.iteritems():
            if v >= thr:
                print key + ' - ' + k
