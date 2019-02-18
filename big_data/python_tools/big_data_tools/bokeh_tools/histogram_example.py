from bokeh.plotting  import figure, show
from bokeh.models import Legend
import numpy as np
from scipy.signal import savgol_filter

def line_historgram():
    #positive skew
    percent_skew = 50
    size = 1000
    amount_skew = 4 
    start = size - int(round(size * percent_skew/100))
    nums =  np.random.normal(size = size)
    nums = sorted(nums)
    x = range(len(nums))
    for i  in range(start, len(nums) -1):
        nums[i] = nums[i] * amount_skew
    p = figure()
    hist, edges = np.histogram(nums)
    legen = 'histogram'
    hist2, edges2 = np.histogram(nums, bins=500)
    y = hist2
    y = savgol_filter(y, 101, 2)
    p.line(edges2, y)
    show(p)

def skewed_histogram():
    #positive skew
    percent_skew = 5
    size = 1000
    amount_skew = 5 
    start = size - int(round(size * percent_skew/100))
    nums =  np.random.normal(size = size)
    nums = sorted(nums)
    x = range(len(nums))
    for i  in range(start, len(nums) -1):
        nums[i] = nums[i] * amount_skew
    p = figure()
    hist, edges = np.histogram(nums)
    legen = 'histogram'
    r = p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    legend = Legend(items=[
            (None , [r]),
            ], location=(10, 0))
    p.add_layout(legend, 'right')
    #legend.background_fill_color = "green"
    hist2, edges2 = np.histogram(nums, bins=50)
    #r2 = p.quad(top = hist2, bottom=0, left=edges2[:-1], right=edges2[1:], alpha = .4)
    p.line(edges2, hist2)
    show(p)

def histogram():
    nums =  np.random.normal(size = 100)
    p = figure()
    hist, edges = np.histogram(nums)
    legen = 'histogram'
    r = p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    legend = Legend(items=[
            (None , [r]),
            ], location=(10, 0))
    p.add_layout(legend, 'right')
    #legend.background_fill_color = "green"
    show(p)

if __name__ == '__main__':
    #skewed_histogram()
    line_historgram()
