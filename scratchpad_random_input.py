import numpy as np
import time


ALPHA = 0.5
deg_sym = u'\u00b0'

def low_pass_test(input_list, output_list=None):
    if not output_list: return input_list

    for i in range(3):
        output[i] = output_list[i] + ALPHA * (input_list[i] - output_list[i])
    return output



# print(sample_input)
output = None
while True:
    sample_input = np.random.uniform(low=0.0, high=10.0, size=(3,))
    input_list = sample_input.tolist()
    # print(type(input_list))

    if output == None:
        output = low_pass_test(input_list)
        output = low_pass_test(input_list, output)

    print("Input vals: {:>1.6f} {:>1.6f} {:>1.6f} | Output vals: {:>1.6f} {:>1.6f} {:>1.6f} {}".format(*input_list, *output, deg_sym))
    time.sleep(0.5)
