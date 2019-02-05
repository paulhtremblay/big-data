import math
from scipy.stats import probplot
import scipy.stats
import numpy as np
from bokeh.plotting import figure, show
import pprint
pp = pprint.PrettyPrinter(indent = 4)

def make_plot_normal():
    pd_series = np.random.normal(size = 100)
    series1 = probplot(pd_series, dist="norm")
    p1 = figure(title="Normal QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p1.scatter(series1[0][0],series1[0][1], fill_color="red")
    p1.line(x,y2, line_width =2)
    show(p1)


def make_plot_exp():
    pd_series = np.random.exponential(size = 100)
    series1 = probplot(pd_series, dist=scipy.stats.expon)
    p1 = figure(title="Exponential QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p1.scatter(series1[0][0],series1[0][1], fill_color="red")
    p1.line(x,y2, line_width =2)
    show(p1)

if __name__ == '__main__':
    make_plot()
