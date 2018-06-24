import sys
from collections import OrderedDict
import numpy as np
from bokeh.plotting import figure, show, output_file

import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_quantiles(data):
    # data is a list of lists
    final = []
    for i in data:
        q1 = np.percentile(i, 25)
        q2 = np.percentile(i, 50)
        q3 = np.percentile(i, 75)
        iqr = q3 - q1
        final.append((q1 - 1.5*iqr, q3 + 1.5*iqr,q1, q2,  q3,  [x for x in i if x < q1 - (1.5 * iqr) or x >q3 + (1.5 * iqr)  ]))
    return final


def make_box_raw(p, cats, upper, lower, q1, q2, q3, out):
    p.segment(cats, lower, cats, upper)
    p.vbar(cats, 0.7, q1, q2, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q2, q3, fill_color="#3B8686", line_color="black")
    p.rect(cats, lower, 0.2, 0.01, line_color="black")
    p.rect(cats, upper, 0.2, 0.01, line_color="black")
    for k, v in out.items():
        for point in v:
            p.circle([k], [point], size=6, color="#F38630", fill_alpha=0.6)
    return p

def zip_data(cats, data):
    zip_data = list(zip(*data))
    outs = OrderedDict()
    for counter, i in enumerate(cats):
        if len(zip_data[5][counter]) != 0:
            outs[i] = zip_data[5][counter]
    return zip_data, outs

def box_plot(cats, data, p = None):
    if not p:
        p = figure(tools="save", background_fill_color="#EFE8E2", x_range=cats)
    f, outs = zip_data(cats, get_quantiles(data))
    return make_box_raw(p, cats, f[0], f[1], f[2], f[3], f[4], outs)

