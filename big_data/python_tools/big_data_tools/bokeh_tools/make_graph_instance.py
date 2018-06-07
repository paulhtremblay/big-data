from bokeh.plotting import figure
def make_p(width = 400, height = 400, x_axis_type = None, title=""):
    return figure(plot_width=width, plot_height=height, x_axis_type=x_axis_type, title=title)
