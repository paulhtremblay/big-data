import pprint
import choropleth_prep
import bokeh
from bokeh.plotting import figure, show, output_file

pp = pprint.PrettyPrinter(indent = 4)
choropleth = choropleth_prep.Chorpleth(the_type = 'state')
x, y = choropleth.get_points_flatten('MA')
width = 1000
height = int(round((max(y) - min(y))/(max(x) - min(x)) * width))
p = figure(title='test', width=width, height= height)
p.patches([x], [y],
          fill_alpha=0.7,
          line_color="white", line_width=0.5)
x2 = [min(x), max(x), min(x), max(x)]
y2 = [min(y), max(y), max(y), min(y)]
p.scatter(x2, y2, fill_color="red", size=10)
show(p)
