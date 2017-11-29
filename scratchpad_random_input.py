import numpy as np
import time
import ResponsiveValue
import random

ALPHA = 0.5
deg_sym = u'\u00b0'


def low_pass_test(input_list, output_list=None):
    if not output_list: return input_list

    for i in range(3):
        output[i] = output_list[i] + ALPHA * (input_list[i] - output_list[i])
    return output


def low_pass_filter(self, input, output=None):
    if not output: return input

    output_filtered = output + self.ALPHA * (input - output)
    return output_filtered


# smoothVal = None
# // affects the curve of movement amount > snap amount
# // smaller amounts like 0.001 make it ease slower
# // larger amounts like 0.1 make it less smooth
SNAP_MULTIPLIER = 0.007


def dynamicFilter(val, smoothVal=None):
    if smoothVal == None: smoothVal = 0
    diff = val - smoothVal
    snap = snapCurve(diff - SNAP_MULTIPLIER)

    smoothVal += (val - smoothVal) * snap

    return smoothVal


def snapCurve(x):
    y = 1 / (x + 1)
    y = (1 - y) * 2
    if y > 1:
        return 1
    else:
        return y


# print(sample_input)
output = None
responsiveVal = None
while True:
    sample_input = np.random.uniform(low=0.0, high=10.0, size=(3,))
    input_list = sample_input.tolist()
    sample_val = random.uniform(0.1, 2.5)

    responsive_value = ResponsiveValue.ResponsiveValue()
    responsive_value.update(sample_val)
    print('New Value: {}\t{}\t{}\t{}\t{}\t{}'.format(
        sample_val,
        responsive_value.has_changed,
        responsive_value.raw_value,
        responsive_value.responsive_value,  # the smoothed out value
        responsive_value.sleeping,
        responsive_value._error_EMA))

    if responsiveVal == None:
        responsiveVal = dynamicFilter(sample_val)
    else:
        responsiveVal = dynamicFilter(sample_val, responsiveVal)

    # print("Before filter: {} After filter: {}".format(sample_val, responsiveVal))

    if output == None:
        output = low_pass_test(input_list)
    else:
        output = low_pass_test(input_list, output)

    # print("Input vals: {:>1.6f} {:>1.6f} {:>1.6f} | Output vals: {:>1.6f} {:>1.6f} {:>1.6f} {}".format(*input_list,
    #                                                                                                    *output,
                                                                                                       # deg_sym))
    time.sleep(0.5)
