import sys
from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from bokeh.io import show, output_file


from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pprint
pp = pprint.PrettyPrinter(indent=4)

class GraphTwoLevel:

    def __init__(self):
        pass

    def _make_fill_colors(self, second_level_pos, third_level_pos, top_color, 
            second_level_color, third_level_color):
        fill_c =[top_color]
        fill_c.extend(second_level_color for x in second_level_pos.keys())
        fill_c.extend(third_level_color for x in third_level_pos.keys())
        return fill_c

    def _make_increment(self, num, width, max_num):
        if num > max_num:
            num = max_num
        if num == 1:
            return width/2
        return width/(num -1 )

    def _init_start_layout(self, start_value, inc, num_left):
        if num_left == 1:
            return   start_value + 2.2/2
        return start_value  

    def _make_layout_raw(self, the_dict, start_p = 1, start_x_value = -1, 
            depth = .3, max_num = 5, current_depth = None, graph_layout = None):
        """
        max_num = the maximum number for 1 row
        """
        inc = self._make_increment(len(list(the_dict.keys())),2, max_num)
        x_value = self._init_start_layout(start_x_value, inc, len(list(the_dict.keys())))
        width = 0
        for counter, i  in enumerate(the_dict.keys()):
            width += 1
            graph_layout[the_dict[i]['pos']] = ((x_value, 1 - current_depth))
            x_value += inc 
            if width == max_num  :
                x_value = self._init_start_layout(start_x_value, inc, len(list(the_dict.keys())) - counter - 1)
                current_depth += depth
                width = 0
                inc = self._make_increment(len(list(the_dict.keys())) - counter - 1, 2, max_num)
        return graph_layout, counter + start_p + 1, current_depth + depth

    def _make_layout(self, second_level_pos, third_level_pos,  start_p = 1, start_x_value = -1, 
            depth = .3, max_num = 5, current_depth = None, graph_layout = None, 
            ):
        graph_layout = { 0: (0, 1.0)}
        graph_layout, start_p, current_depth = self._make_layout_raw(the_dict = second_level_pos,  depth = depth, 
                graph_layout =  graph_layout, current_depth =  depth, max_num = max_num)
        graph_layout, start_p, current_depth  = self._make_layout_raw(the_dict = third_level_pos,  depth = depth, 
                graph_layout =graph_layout, start_p = start_p, current_depth =  current_depth, 
                max_num = max_num)
        return graph_layout

    def _make_labels(self, graph_layout, second_level_pos, third_level_pos,  x_offset, y_offset, top_level_name):
        source = ColumnDataSource(data=dict(x  = [graph_layout[x][0] for x in graph_layout.keys()], 
            y = [graph_layout[x][1] for x in graph_layout.keys()], 
            names=[top_level_name] + list(second_level_pos.keys()) +  list(third_level_pos.keys())))
        labels = LabelSet(x='x', y='y', text='names', level='glyph',
                      x_offset=x_offset, y_offset=y_offset, source=source, render_mode='canvas')
        return labels


    def _make_node_indices(self, data):
        d = {}
        x = len(data.keys())
        count = 1
        for key in data.keys():
            count += 1
            for i in data[key]['to_nodes']:
                d[i['name']] = True
        return count + len(list(d.keys()))

    def _make_pos_dict(self, data):
        second_level_dict = {}
        third_level_dict = {}
        for counter, key in enumerate(list(data.keys())):
            second_level_dict[key] = {'edges':[x['name'] for x in data[key]['to_nodes']] , 'pos':counter + 1}
        counter += 2
        for key in second_level_dict.keys():
            for i in second_level_dict[key]['edges']:
                if third_level_dict.get(i) == None:
                    third_level_dict[i]  = {'pos': counter}
                    counter  += 1
        return second_level_dict, third_level_dict

    def _make_edges(self, second_level_pos, third_level_pos, data, default_width = .5):
        edge_widths =[default_width]
        edge_colors =['red']
        ed = {'start':[0], 'end':[0]}
        for counter, i in enumerate(list(data.keys())):
            ed['start'].append(0)
            ed['end'].append(second_level_pos[i]['pos'])
            edge_widths.append(default_width * data[i]['level1_edge_width'])
            edge_colors.append('red')
        for i in second_level_pos.keys():
            p =  second_level_pos[i]['pos']
            for counter, j in enumerate(second_level_pos[i]['edges']):
                edge_widths.append(default_width * data[i]['to_nodes'][counter]['edge_width'])
                edge_colors.append('black')
                ed['start'].append(p)
                end = third_level_pos.get(j, {}).get('pos')
                ed['end'].append(end)
        return ed, edge_widths, edge_colors

    def make_user_graph(self, data, top_level_name, oval_height = 0.1, oval_width=0.2, branch_depth = .6, 
            top_color = Spectral8[0], second_level_color = Spectral8[1] , third_level_color = Spectral8[2],
            label_x_offset = -15, label_y_offset = 10, p =  None, 
            max_num_in_row = 5, line_width = .5
            ):
        if not p:
            p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
                tools="", toolbar_location=None, plot_width = 1000)
        graph = GraphRenderer()
        graph.node_renderer.glyph = Oval(height=oval_height, width=oval_width, fill_color="fill_color", name="text")
        node_indices = [x for x in range(self._make_node_indices(data))]
        second_level_pos, third_level_pos =  self._make_pos_dict(data)
        graph.node_renderer.data_source.data = dict(index=node_indices, fill_color=self._make_fill_colors(
            second_level_pos, third_level_pos,  second_level_color = second_level_color, third_level_color = third_level_color, top_color = top_color))
        eds, edge_widths, edge_colors = self._make_edges(second_level_pos, third_level_pos, data, default_width =  line_width)
        graph.edge_renderer.data_source.data = eds
        graph_layout= self._make_layout(second_level_pos = second_level_pos, third_level_pos = third_level_pos,  depth = branch_depth, 
                max_num = max_num_in_row)
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        p.add_layout(self._make_labels(graph_layout = graph_layout, second_level_pos = second_level_pos,
            third_level_pos = third_level_pos, x_offset = label_x_offset, 
            y_offset =  label_y_offset, top_level_name = top_level_name))
        graph.edge_renderer.data_source.data["line_width"] = edge_widths
        graph.edge_renderer.glyph.line_width = {'field': 'line_width'}
        graph.edge_renderer.data_source.data["line_color"] = edge_colors
        graph.edge_renderer.glyph.line_color = {'field': 'line_color'}
        p.renderers.append(graph)
        return  p

if __name__ == '__main__':
    data = [
            ('ad1',{'level1_edge_width':1, 'to_nodes':[{'name':'sku2','edge_width':1},{'name':'sku3','edge_width':1},]}),
            ('ad2',{'level1_edge_width':1, 'to_nodes':[{'name':'sku2','edge_width':2},]}),
            ('ad3',{'level1_edge_width':1, 'to_nodes':[{'name':'sku2','edge_width':1},]}),
            ]
    data = OrderedDict(data)
    p = figure(title="Test Ad Graph", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
            tools="", toolbar_location=None, plot_width = 1000)
    g = GraphTwoLevel()
    g.make_user_graph(data,  p=p, max_num_in_row=13, top_level_name = 'User')
    p.grid.visible = False
    p.axis.visible = False
    show(p)
