import math
import numpy as np

def make_legends(data, palette):
    the_min = np.nanmin(data)
    the_max = np.nanmax(data)
    x = np.linspace(the_min, the_max, len(palette) + 1 )
    step = (the_max - the_min)/(len(palette) )
    if step == 0:
        step = .01
    last = the_min
    labels = []
    next_ = the_max - 1
    while next_ <= the_max:
        next_ = last + step
        labels.append('{last}: {next_}'.format(
            next_ = round(next_,1),
            last = round(last,1)
            ))
        last = next_
    labels_dict= {}
    labels_list = []
    for i in list(data):
        if np.isnan(i):
            labels_list.append('N/A')
            continue
        n = math.floor((i-the_min)/step)
        if n == len(palette):
            n -= 1
        labels_dict[i] = labels[n]
        labels_list.append(labels[n])
    return labels_list
