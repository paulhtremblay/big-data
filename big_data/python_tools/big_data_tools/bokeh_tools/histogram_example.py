from bokeh.plotting  import figure, show
import numpy as np
hist, edges = np.histogram(nums, density=True)
p = figure()
p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
