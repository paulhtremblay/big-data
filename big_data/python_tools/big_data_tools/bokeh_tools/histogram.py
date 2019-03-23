from bokeh.plotting  import figure, show
import numpy as np

def hist(nums):
    hist, edges = np.histogram(nums, density=True)
    p = figure()
    p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    return p

if __name__ == '__main__':
    p = hist([1,1,1,1,15,5,5, 10, 10,10,8])
