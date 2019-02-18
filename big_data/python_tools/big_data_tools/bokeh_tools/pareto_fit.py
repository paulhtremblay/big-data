from scipy import stats
import copy
import math
import scipy
import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import pprint

scipy.__version__

def pareto_cdf(alpha):
    1 - (xm/x)^alpha

def sse(y1, y2):
    return math.sqrt(sum((y1- y2) * (y1- y2))/len(y1))

def pure_pareto(b):
    p = figure(title = "pure pdf")
    x = np.linspace(stats.pareto.ppf(0.01, b), stats.pareto.ppf(0.99, b), 100)
    y = stats.pareto.pdf(x, b)
    p.line(x,y, line_color="red", line_width=2)
    return p

def pareto_diff_loc(b):
    p = figure(title = "different locations")
    x1 = np.linspace(stats.pareto.ppf(0.01, b, 1), stats.pareto.ppf(0.99, b, 1), 100)
    y1 = stats.pareto.pdf(x1, b, 1)
    p.line(x1,y1, line_color="red", line_width=2, legend="1")
    x2 = np.linspace(stats.pareto.ppf(0.01, b, 3), stats.pareto.ppf(0.99, b, 3), 100)
    y2 = stats.pareto.pdf(x2, b, 3)
    p.line(x2,y2, line_color="blue", line_width=2, legend="3")
    return p

def figure_out_sse(b):
    data = stats.pareto.rvs(b, size= 1000)
    params = stats.pareto.fit(data)
    x = np.linspace(1, stats.pareto.ppf(0.99, params[0]), len(data))
    pdf = stats.pareto.pdf(x, params[0])
    y, x = np.histogram(data, bins=1000, density=True)
    e = sse(pdf, y)
    print(e)
    data_norm = stats.norm.rvs(b, size= 1000)
    y, x = np.histogram(data_norm, bins=1000, density=True)
    e = sse(pdf, y)
    print(e)

def fit_pareto(b):
    p = figure(title = "fitted")
    data = stats.pareto.rvs(b, size= 1000)
    hist, edges = np.histogram([x for x in data if x < stats.pareto.ppf(0.99, b)], density=True )
    p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    params = stats.pareto.fit(data)
    x = np.linspace(1, stats.pareto.ppf(0.99, params[0]), len(data))
    y = stats.pareto.pdf(x, params[0])
    p.line(x, y)
    return p

def fit_pareto2(b):
    b = 1
    loc = 3
    p = figure(title = "fitted")
    data = stats.pareto.rvs(b, loc=loc, size= 1000)
    hist, edges = np.histogram([x for x in data if x < stats.pareto.ppf(0.99, b, loc = loc)], density=True )
    p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    params = stats.pareto.fit(data)
    x = np.linspace(stats.pareto.ppf(0.01, *params), stats.pareto.ppf(0.99, *params), len(data))
    y = stats.pareto.pdf(x, *params)
    p.line(x, y, line_width=2)
    return p

def main():
    b = 2.62
    p_pure = pure_pareto(b)
    p_fit = fit_pareto(b)
    p_fit2 = fit_pareto2(b)
    p_diff_loc = pareto_diff_loc(b)
    figure_out_sse(b)
    grid = gridplot([p_pure, p_fit, p_diff_loc, p_fit2], ncols = 2, height=500, 
            width = 500)
    show(grid)

if __name__ == '__main__':
    main()
