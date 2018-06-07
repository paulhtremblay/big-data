from bokeh.io import output_notebook, show
from bokeh.plotting import figure
p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], radius=15, line_color="navy", fill_color="orange", fill_alpha=0.5)

show(p) # show the results
