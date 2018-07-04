from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.graphs import from_networkx
import networkx as nx

G = nx.karate_club_graph()

plot = figure(title="Karate Club Graph", tools="", x_range=(-1.5, 1.5),
                  y_range=(-1.5, 1.5), toolbar_location=None)
graph = from_networkx(G, nx.spring_layout)
plot.renderers.append(graph)

x, y = zip(*graph.layout_provider.graph_layout.values())
node_labels = nx.get_node_attributes(G, 'club')
source = ColumnDataSource({'x': x, 'y': y,
                               'club': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x', y='y', text='club', source=source,
                          background_fill_color='white')
print(node_labels)
nx.get_node_attributes(G, 'club')
plot.renderers.append(labels)
show(plot)
