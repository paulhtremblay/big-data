from bokeh.plotting  import figure, show
from bokeh.models import Legend
import numpy

def hist(nums, bins = None, legend =  None, p = None):
    if bins:
        hist, edges = numpy.histogram(nums, bins=bins)
    else:
        hist, edges = numpy.histogram(nums)
    if not p:
        p = figure()
    r = p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    if legend !=  None:
        legend = Legend(items=[
                (legend , [r]),
                ], location=(10, 0))
        p.add_layout(legend, 'right')
        #legend.background_fill_color = "green"
    return p

if __name__ == '__main__':
    hist([1,1,1,1,15,5,5, 10, 10,10,8], legend="my legend")
