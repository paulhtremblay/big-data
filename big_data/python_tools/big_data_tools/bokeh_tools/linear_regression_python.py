from scipy import stats
import random
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter

x = range(100)
y = [random.randint(0,1)  for x in range(100) ]
y1 = []
constant = .5
for i in y:
    y1.append(i + constant)
    constant += .05
y = y1
p = figure(plot_width=800, plot_height=300, title="Title")
p.line(x, y, line_width =2,legend=None )
p.yaxis.formatter=NumeralTickFormatter(format="0,")
#fitted
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
p.line(x, [x * slope + intercept for x in x])
p.line(x, [x * slope + intercept + std_err * 2 for x in x])
p.line(x, [x * slope + intercept - std_err * 2 for x in x])
show(p)
print(slope, intercept, r_value, p_value, std_err)

