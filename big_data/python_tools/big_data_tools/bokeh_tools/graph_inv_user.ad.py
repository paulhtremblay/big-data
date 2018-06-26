import sys
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from bokeh.io import show, output_file

from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pprint
pp = pprint.PrettyPrinter(indent=4)

def make_ads_dict(data, counter = 1, the_type = 'ads'):
    assert isinstance(data, list)
    the_dict = {}
    for i in data:
        if the_dict.get(i[0]) == None:
            the_dict[i[0]]  =   {'pos':counter, 'edges' : []}
            counter += 1
        if the_type == 'ads':
            the_dict[i[0]]['edges'].append(i[1])
    return the_dict, counter

def make_skus_dict(data, counter):
    skus_pos = {}
    for i in data:
        if skus_pos.get(i[1]) == None:
            skus_pos[i[1]]  =   {'pos':counter}
        counter += 1
    return skus_pos

def make_edges(ads_pos, skus_pos):
    ed = {'start':[0 for x in  range(len(ads_pos.keys()) +1)], 'end':[x for x in  range(len(ads_pos.keys()) +1)]}
    for i in ads_pos.keys():
        p =  ads_pos[i]['pos']
        for j in ads_pos[i]['edges']:
            ed['start'].append(p)
            end = skus_pos.get(j, {}).get('pos')
            ed['end'].append(end)
    return ed

def make_fill_colors(ads_pos, skus_pos):
    fill_c =[Spectral8[0]]
    fill_c.extend(Spectral8[1] for x in ads_pos.keys())
    fill_c.extend(Spectral8[2] for x in skus_pos.keys())
    return fill_c

def make_first_layout(ads_pos, skus_pos, start_p = 1, start_x_value = -.75, depth = .3):
    graph_layout = { 0: (0, 1.0)}
    x_value = start_x_value
    for counter, i  in enumerate(ads_pos.keys()):
        graph_layout[counter + start_p] = ((x_value, 1 - depth))
        x_value += .5
    start_p =  counter  + start_p + 1
    x_value = start_x_value
    for counter, i  in enumerate(skus_pos.keys()):
        graph_layout[counter + start_p] = ((x_value, 1 - (2 * depth)))
        x_value += .5
    return graph_layout

def make_labels(graph_layout, ads_pos, skus_pos):
    source = ColumnDataSource(data=dict(x  = [graph_layout[x][0] for x in graph_layout.keys()], 
        y = [graph_layout[x][1] for x in graph_layout.keys()], 
        names=['User'] + list(ads_pos.keys()) +  list(skus_pos.keys())))
    labels = LabelSet(x='x', y='y', text='names', level='glyph',
                  x_offset=10, y_offset=10, source=source, render_mode='canvas')
    return labels

def make_user_graph(data):
    plot = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
        tools="", toolbar_location=None)
    ads_pos, counter = make_ads_dict(data)
    skus_pos = make_skus_dict(data, counter = counter)
    graph = GraphRenderer()
    graph.node_renderer.glyph = Oval(height=0.1, width=0.2, fill_color="fill_color", name="text")
    node_indices = list(range(len(ads_pos.keys()) + len(skus_pos.keys()) + 1))
    graph.node_renderer.data_source.data = dict(index=node_indices, fill_color=make_fill_colors(ads_pos, skus_pos))
    graph.edge_renderer.data_source.data = make_edges(ads_pos, skus_pos)
    graph_layout= make_first_layout(ads_pos = ads_pos, skus_pos = skus_pos,  depth = .3)
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    plot.add_layout(make_labels(graph_layout = graph_layout, ads_pos = ads_pos,skus_pos = skus_pos))
    plot.renderers.append(graph)
    show(plot)

if __name__ == '__main__':
    data =  [('ad1','sku1'), ('ad1','sku2'), ('ad2','sku2')]
    make_user_graph(data)
