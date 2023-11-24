import copy
import numpy as np
import math


def jackknife_error(data):
    leave_one_out = []
    for i in range(len(data)):
        x = copy.deepcopy(data)
        x.remove(data[i])
        i_th_jackknife_replicate = np.nanmean(x)
        leave_one_out.append(i_th_jackknife_replicate)
    leave_one_out = np.array(leave_one_out)
    mean_leave_one_out = np.nanmean(leave_one_out)
    jackknife_variance = ((len(data)-1)/len(data)) * sum(np.power((leave_one_out - mean_leave_one_out), 2))
    jackknife_error = math.sqrt(jackknife_variance)
    return jackknife_error

def get_pitches(codeword_list):
    pitches = []
    for cwd in codeword_list:
        pitches.append(tuple([p.midi for p in cwd]))
    return pitches