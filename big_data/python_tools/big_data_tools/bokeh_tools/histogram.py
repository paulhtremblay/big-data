from bokeh.plotting  import figure, show
import numpy as np

def hist(nums, p = None, density = True, bins=None):
    if bins != None:
        hist, edges = np.histogram(nums, density=density, bins = bins)
    else:
        hist, edges = np.histogram(nums, density=density)
    if p == None:
        p = figure()
    p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    return p
