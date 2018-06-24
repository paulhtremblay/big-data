from bokeh.io import show, output_file
from bokeh.plotting import figure

def bar(labels, nums, height = 500, title = None, p = None):
    #output_file("bars.html")
    if not p:
        p = figure(x_range=labels, plot_height=height, title=title)
    p.vbar(x=labels, top=nums, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

if __name__ == '__main__':
    bar(['first', 'second', 'third', 'fourth'], [1, 2, 3,4])
