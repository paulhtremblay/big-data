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
    #p = bar(['first', 'second', 'third', 'fourth'], [1, 2, 3,4])
    #show(p)
    labels = ['first', 'second', 'third', 'fourth']
    p = figure(x_range=labels, plot_height=500, plot_width = 1000, title="my test title")
    bar(labels, [1, 2, 3,4], p =p)
    show(p)
