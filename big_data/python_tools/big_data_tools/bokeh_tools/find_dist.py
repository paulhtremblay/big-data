from scipy import stats
from scipy.stats import probplot
import math
import scipy
import numpy as np
import pprint
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import pprint
pp = pprint.PrettyPrinter(indent = 4)

D = {'norm': stats.norm,
    'pareto':stats.pareto,
    'lognorm':stats.lognorm,
        }

def _sse(y1, y2):
    pp.pprint(y1)
    pp.pprint(y2)
    assert False
    return math.sqrt(sum((y1- y2) * (y1- y2))/len(y1))

def sse(y1, y2):
    return math.sqrt(sum((y1- y2) * (y1- y2))/len(y1))

def get_dist(dist_string):
    return D[dist_string]

def make_plot():
    pass

def pp_plot(data, dist, sparams = None, title= None):
    if not title:
        title = "{dist} QQ Plot".format(dist = dist)
    series = probplot(data, dist=dist, sparams= sparams)
    p = figure(title=title)
    x = series[0][0]
    y = series[0][1]
    slope = series[1][0]
    intercept = series[1][1]
    y2 = [z * slope + intercept for z in x]
    p.scatter(series[0][0],series[0][1], fill_color="red")
    p.line(x,y2, line_width =2)
    e = sse(series[0][1], y2)
    return p, e

def find_best(data, dists):
    ps = []
    es = []
    for i in dists:
        f = get_dist(i)
        params = f.fit(data)
        p, e =pp_plot(data, i, params) 
        ps.append(p)
        es.append((i, e))
    print(es)
    grid = gridplot(ps, ncols = 2, height=500, 
            width = 500)
    show(grid)

def _find_best(data):
    least_sse = np.inf
    best_f = None
    ps = []
    for i in ['lognorm', 'pareto', 'norm', 'lognorm']:
        f = get_dist(i)
        p = figure(title = i)
        hist, edges = np.histogram([x for x in data if x < f.ppf(0.99, b)], density=True )
        ps.append(p)
        p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
        params = f.fit(data)
        x = np.linspace(f.ppf(0.01, *params), f.ppf(0.99, *params), len(data))
        pdf = f.pdf(x, *params)
        p.line(x, pdf)
        pdf = f.pdf(x, *params)
        y, x = np.histogram(data, bins=1000, density=True)
        e = sse(pdf, y)
        print(i, e)
        if e < least_sse:
            least_sse = e
            best_f = i
    grid = gridplot(ps, ncols = 2, height=500, 
            width = 500)
    show(grid)
    return least_sse, best_f

if __name__ == '__main__':
    b = 2.62
    data = stats.pareto.rvs(b, loc = 3, size= 1000)
    data = [.83, .88, .88, 1.4, 1.09, 1.12, 1.29, 1.31,
            1.48, 1.49, 1.59, 1.62, 1.65, 1.71, 1.83]
    dists = ['pareto', 'norm', 'lognorm']
    var = np.var(data, ddof = 1)
    s = math.sqrt(var)
    d = stats.describe(data)
    print(d.variance)
    #find_best(data, dists)
