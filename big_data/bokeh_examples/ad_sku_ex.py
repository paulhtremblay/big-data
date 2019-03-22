import sys
import networkx as nx
from bokeh.models import Plot, ColumnDataSource, Range1d, from_networkx, Circle,MultiLine
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.io import show, output_file
from bokeh.palettes import Viridis

import pprint
pp = pprint.PrettyPrinter(indent=4)

#define graph

G = nx.DiGraph()
G.add_edges_from( [('User', 'ad1'), ('User', 'ad2'), ('ad1', 'sku1'), ('ad2', 'sku2')])
G['User']['ad1']['weight'] = 1
G['User']['ad2']['weight'] = 5
G['ad1']['sku1']['weight'] = 1
G['ad2']['sku2']['weight'] = 1


node_size = [50, 20, 20, 20, 20]
node_initial_pos = [(-0.5,0), (0.5,0), (0,0.25),(0,-0.25), (.6, 0)]
node_color = [Viridis[10][0], Viridis[10][9],Viridis[10][9],'blue', 'blue']
index= ['User', 'ad1', 'ad2', 'sku1', 'sku2']
G.nodes['User']['name'] = 'User'
G.nodes['ad1']['name'] = 'ad1'
G.nodes['ad2']['name'] = 'ad2'
G.nodes['sku1']['name'] = 'sku1'
G.nodes['sku2']['name'] = 'sku2'


graph_renderer = from_networkx(G, nx.spring_layout, scale=0.5, center=(0,0))
plot = Plot(plot_height=1000, plot_width=1000,
                    x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
#node_labels = nx.get_node_attributes(G, 'club')
#node_labels = {key:key for key in G.nodes}
node_labels = nx.get_node_attributes(G, 'name')
line_size = [1,2, 3, 4, 5]
source = ColumnDataSource(data=dict(
                node_size = node_size,
                node_color = node_color,
                node_initial_pos = node_initial_pos,
                index= index,
                names =  [node_labels[i] for i in index],
                x = x,
                y = y,
                line_size = line_size,
            ))


labels = LabelSet(x='x', y='y', text='names', source=source,
                          background_fill_color='white')


node_initial_pos = {'User':(-0.5,0), 'ad1':(.5,.50),'ad2':(0,0),'sku1':(0,-0.25), 'sku2':(0,.25)}
#graph_renderer = from_networkx(G, nx.shell_layout, scale=0.5, center=(0,0))
#style
graph_renderer.node_renderer.data_source = source
graph_renderer.node_renderer.glyph = Circle(fill_color = 'node_color',size = 'node_size', line_color = None)

graph_renderer.edge_renderer.glyph = MultiLine(line_color="blue", line_alpha=0.8)

graph_renderer.edge_renderer.data_source.data["line_width"] = [G.get_edge_data(a,b)['weight'] for a, b in G.edges()]
graph_renderer.edge_renderer.glyph.line_width = {'field': 'line_width'}
plot.renderers.append(graph_renderer)


plot.renderers.append(graph_renderer)
plot.renderers.append(labels)
output_file('test.html')

show(plot)


