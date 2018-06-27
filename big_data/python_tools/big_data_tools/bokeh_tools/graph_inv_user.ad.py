import sys
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from bokeh.io import show, output_file
#from bokeh.models import Axis 


from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pprint
pp = pprint.PrettyPrinter(indent=4)


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
        graph_layout[the_dict[i]['pos']] = ((x_value, 1 - current_depth))
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


def _make_node_indices(data):
    d = {}
    x = len(data.keys())
    count = 1
    for key in data.keys():
        count += 1
        for i in data[key]['skus']:
            d[i] = True
    return count + len(list(d.keys()))

def _make_ads_dict(data):
    ads_dict = {}
    skus_dict = {}
    for counter, key in enumerate(sorted(list(data.keys()))):
        ads_dict[key] = {'edges':data[key]['skus'], 'pos':counter + 1}
    counter += 2
    for key in sorted(list(ads_dict.keys())):
        for i in ads_dict[key]['edges']:
            if skus_dict.get(i) == None:
                skus_dict[i]  = {'pos': counter}
                counter  += 1
    return ads_dict, skus_dict

def _make_edges(ads_pos, skus_pos, data, default_width = .5):
    edge_widths =[default_width]
    edge_colors =['red']
    ed = {'start':[0], 'end':[0]}
    for counter, i in enumerate(sorted(list(data.keys()))):
        ed['start'].append(0)
        ed['end'].append(ads_pos[i]['pos'])
        edge_widths.append(default_width * data[i]['num_visits'])
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

def make_user_graph(data, oval_height = 0.1, oval_width=0.2, branch_depth = .6, 
        user_color = Spectral8[0], ad_color = Spectral8[1] , sku_color = Spectral8[2],
        label_x_offset = -15, label_y_offset = 10, p =  None, 
        max_num_in_row = 5, line_width = .5
        ):
    if not p:
        p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
            tools="", toolbar_location=None, plot_width = 1000)
    #ads_pos, counter = _make_ads_dict(data)
    #skus_pos = _make_skus_dict(data, counter = counter)
    graph = GraphRenderer()
    graph.node_renderer.glyph = Oval(height=oval_height, width=oval_width, fill_color="fill_color", name="text")
    node_indices = [x for x in range(_make_node_indices(data))]
    ads_pos, skus_pos =  _make_ads_dict(data)
    graph.node_renderer.data_source.data = dict(index=node_indices, fill_color=_make_fill_colors(
        ads_pos, skus_pos,  ad_color = ad_color, sku_color = sku_color, user_color = user_color))
    eds, edge_widths, edge_colors = _make_edges(ads_pos, skus_pos, data, default_width =  line_width)
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
    data3 =  { 'ad1':{'num_visits':1,'skus':['sku1', 'sku2',  'sku3', ]},
        'ad2':{'num_visits':1, 'skus':['sku2']},
        'ad3':{'num_visits':1,'skus':['sku3']},
        'ad4':{'num_visits':1,'skus':['sku3', 'sku1', 'sku2']},
        'ad5':{'num_visits':3, 'skus':['sku1']},
        'ad6':{'num_visits':3, 'skus':['sku1']},
        'ad7':{'num_visits':1, 'skus':['sku1']},
        'ad8':{'num_visits':10, 'skus':['sku1']},
        'ad9':{'num_visits':1, 'skus':['sku1']},
        'ad10':{'num_visits':1, 'skus':['sku3']},
        'ad11':{'num_visits':1, 'skus':['sku3']},
        'ad12':{'num_visits':1, 'skus':['sku3']},
            }
    p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
            tools="", toolbar_location=None, plot_width = 1000)
    make_user_graph(data3,  p=p, max_num_in_row=12)
    p.grid.visible = False
    p.axis.visible = False
    show(p)
