import sys
import math
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from bokeh.io import show, output_file

from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pprint
pp = pprint.PrettyPrinter(indent=4)
N = 8
node_indices = list(range(N))

plot = figure(title="Graph Layout Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
    tools="", toolbar_location=None)

graph = GraphRenderer()
#just one oval
graph.node_renderer.glyph = Oval(height=0.1, width=0.2, fill_color="fill_color", name="text")

fill_c = [Spectral8[0] for x in Spectral8]
fill_c[0] = Spectral8[1]
text  =  ['a', 'a', 'a', 'a', 'a', 'a', 'a']
ed = {'start': [0, 0, 0, 0, 1, 2, 3, 4,1], 'end': [0, 1, 2, 3, 4, 5, 6, 7, 7]}
graph.node_renderer.data_source.data = dict(index=node_indices, fill_color=fill_c)
graph.edge_renderer.data_source.data = ed

### start of layout code
circ = [i*2*math.pi/8 for i in node_indices]
x = [math.cos(i) for i in circ]
y = [math.sin(i) for i in circ]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph_layout = {   0: (0, 1.0),
    1: (-.75, 0.75),
    2: (0, .75),
    3: (0.75, 0.75),
    4: (-1.0, 1.2246467991473532e-16),
    5: (-0.7071067811865477, -0.7071067811865475),
    6: (-1.8369701987210297e-16, -1.0),
    7: (0.7071067811865475, -0.7071067811865477)
}
#graph_layout[0] = (0,1)
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
x = [graph_layout[x][0] for x in graph_layout.keys()]
y = [graph_layout[x][1] for x in graph_layout.keys()]
names  =  list(graph_layout.keys())

source = ColumnDataSource(data=dict(x  = x, y = y, names=names))
labels = LabelSet(x='x', y='y', text='names', level='glyph',
              x_offset=10, y_offset=10, source=source, render_mode='canvas')

plot.add_layout(labels)

plot.renderers.append(graph)

show(plot)
