import sys
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from bokeh.io import show, output_file

from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pprint
pp = pprint.PrettyPrinter(indent=4)

def _make_ads_dict(data, counter = 1, the_type = 'ads'):
    assert isinstance(data, list)
    the_dict = {}
    for i in data:
        if the_dict.get(i[0]) == None:
            the_dict[i[0]]  =   {'pos':counter, 'edges' : []}
            counter += 1
        if the_type == 'ads':
            the_dict[i[0]]['edges'].append(i[1])
    return the_dict, counter

def _make_skus_dict(data, counter):
    skus_pos = {}
    for i in data:
        if skus_pos.get(i[1]) == None:
            skus_pos[i[1]]  =   {'pos':counter}
            counter += 1
    return skus_pos

def _make_edges(ads_pos, skus_pos, data, default_width = .5):
    edge_widths =[default_width]
    edge_colors =['red']
    ed = {'start':[0], 'end':[0]}
    for counter, i in enumerate(data.keys()):
        ed['start'].append(0)
        ed['end'].append(counter + 1)
        edge_widths.append(default_width * data[i])
        edge_colors.append('red')
    for i in ads_pos.keys():
        p =  ads_pos[i]['pos']
        for j in ads_pos[i]['edges']:
            edge_widths.append(default_width)
            edge_colors.append('black')
            ed['start'].append(p)
            end = skus_pos.get(j, {}).get('pos')
            ed['end'].append(end)
    return ed, edge_widths, edge_colors

def _make_fill_colors(ads_pos, skus_pos, user_color, 
        ad_color, sku_color):
    fill_c =[Spectral8[0]]
    fill_c.extend(Spectral8[1] for x in ads_pos.keys())
    fill_c.extend(Spectral8[2] for x in skus_pos.keys())
    return fill_c

def _make_increment(num, width, max_num):
    if num > max_num:
        num = max_num
    return width/(num -1 )

def _init_start_layout(start_value, inc):
    return start_value  

def _make_layout_raw(the_dict, start_p = 1, start_x_value = -1, 
        depth = .3, max_num = 5, current_depth = None, graph_layout = None):
    """
    max_num = the maximum number for 1 row
    """
    inc = _make_increment(len(list(the_dict.keys())),2, max_num)
    x_value = _init_start_layout(start_x_value, inc)
    width = 0
    for counter, i  in enumerate(the_dict.keys()):
        width += 1
        graph_layout[counter + start_p] = ((x_value, 1 - current_depth))
        x_value += inc 
        if width == max_num + 1 :
            x_value = _init_start_layout(start_x_value, inc)
            current_depth += depth
            width = 0
    return graph_layout, counter + start_p + 1, current_depth + depth

def _make_layout(ads_pos, skus_pos,  start_p = 1, start_x_value = -1, 
        depth = .3, max_num = 5, current_depth = None, graph_layout = None, 
        ):
    graph_layout = { 0: (0, 1.0)}
    graph_layout, start_p, current_depth = _make_layout_raw(the_dict = ads_pos,  depth = depth, 
            graph_layout =  graph_layout, current_depth =  depth, max_num = max_num)
    graph_layout, start_p, current_depth  = _make_layout_raw(the_dict = skus_pos,  depth = depth, 
            graph_layout =graph_layout, start_p = start_p, current_depth =  current_depth, 
            max_num = max_num)
    return graph_layout

def _make_labels(graph_layout, ads_pos, skus_pos,  x_offset, y_offset):
    source = ColumnDataSource(data=dict(x  = [graph_layout[x][0] for x in graph_layout.keys()], 
        y = [graph_layout[x][1] for x in graph_layout.keys()], 
        names=['User'] + list(ads_pos.keys()) +  list(skus_pos.keys())))
    labels = LabelSet(x='x', y='y', text='names', level='glyph',
                  x_offset=x_offset, y_offset=y_offset, source=source, render_mode='canvas')
    return labels

def make_user_graph(data, data2, oval_height = 0.1, oval_width=0.2, branch_depth = .6, 
        user_color = Spectral8[0], ad_color = Spectral8[1] , sku_color = Spectral8[2],
        label_x_offset = -15, label_y_offset = 10, p =  None, 
        max_num_in_row = 5, line_width = .5
        ):
    if not p:
        p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
            tools="", toolbar_location=None, plot_width = 1000)
    ads_pos, counter = _make_ads_dict(data)
    skus_pos = _make_skus_dict(data, counter = counter)
    graph = GraphRenderer()
    graph.node_renderer.glyph = Oval(height=oval_height, width=oval_width, fill_color="fill_color", name="text")
    node_indices = list(range(len(ads_pos.keys()) + len(skus_pos.keys()) + 1))
    graph.node_renderer.data_source.data = dict(index=node_indices, fill_color=_make_fill_colors(
        ads_pos, skus_pos,  ad_color = ad_color, sku_color = sku_color, user_color = user_color))
    eds, edge_widths, edge_colors = _make_edges(ads_pos, skus_pos, data2, default_width =  line_width)
    graph.edge_renderer.data_source.data = eds
    graph_layout= _make_layout(ads_pos = ads_pos, skus_pos = skus_pos,  depth = branch_depth, 
            max_num = max_num_in_row)
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    p.add_layout(_make_labels(graph_layout = graph_layout, ads_pos = ads_pos,
        skus_pos = skus_pos, x_offset = label_x_offset, 
        y_offset =  label_y_offset))
    graph.edge_renderer.data_source.data["line_width"] = edge_widths
    graph.edge_renderer.glyph.line_width = {'field': 'line_width'}
    graph.edge_renderer.data_source.data["line_color"] = edge_colors
    graph.edge_renderer.glyph.line_color = {'field': 'line_color'}
    p.renderers.append(graph)
    return  p

if __name__ == '__main__':
    data =  [('ad1','sku1'), ('ad1','sku2'), ('ad2','sku2')]
    #make_user_graph(data)
    #data =  [('ad1','sku1'), ('ad1','sku2'), ('ad2','sku2'),('ad3', 'sku3')]
    data =  [('ad1','sku1'), 
            ('ad1','sku2'), 
            ('ad2','sku2'),
            ('ad3', 'sku3'),
            ('ad1', 'sku3'),
            ('ad2', 'sku3'),
            ('ad4', 'sku3'),
            ('ad4', 'sku1'),
            ('ad4', 'sku2'),
            ('ad5', 'sku1'),
            ('ad6', 'sku1'),
            ('ad7', 'sku1'),
            ('ad8', 'sku1'),
            ('ad9', 'sku1'),
            ('ad10', 'sku3'),
            ('ad11', 'sku3'),
            ('ad12', 'sku3'),
            ]
    data2 =  { 'ad1':1,
               'ad2':1,
               'ad3':1,
               'ad4':1,
               'ad5':3,
               'ad6':3,
               'ad7':1,
               'ad8':5,
               'ad9':1,
               'ad10':1,
               'ad11':1,
               'ad12':1,
            }
    p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
            tools="", toolbar_location=None, plot_width = 1000)
    make_user_graph(data, data2, p=p, max_num_in_row=12)
    show(p)
