from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
p1 = figure()
x = [1, 2, 3, 4]
y = [x * x for x in x]
p1.line(x,y)
p2 = figure()
x2 = [2, 3, 4, 5]
y2 = [x * x for x in x2]
p2.line(x2,y2)
grid = gridplot([p1, p2], ncols = 2, height=500, width = 500)
show(grid)
