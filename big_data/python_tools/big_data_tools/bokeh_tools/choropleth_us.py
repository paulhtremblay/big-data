import sys
import math
import copy
import numpy as np
from bokeh.plotting import figure, show, output_file
try:
    from . import  choropleth_prep
except SystemError:
    import choropleth_prep

from bokeh.palettes import Blues8
from bokeh.palettes import Oranges
from bokeh.models import ColumnDataSource
from bokeh.models import ColorMapper, LogColorMapper, LinearColorMapper

import random

import pprint
pp = pprint.PrettyPrinter(indent=4)

import argparse

def get_type(string):
    if string not in ['state', 'country']:
        raise argparse.ArgumentTypeError('Use "state" or "county" for type')
    return string

def _get_exclude_dict(map_extent):
    if isinstance(map_extent, list):
        return map_extent
    if map_extent == 'continental_us':
        return ['AK', 'GU', 'HI', 'MP', 'PR', 'AS']
    elif map_extent == 'us':
        return ['GU', 'MP', 'PR', 'AS']
    else:
        return []

def _get_args():
    parser = argparse.ArgumentParser(description='Create a heat map of US')
    parser.add_argument('--verbose', '-verbose', action='store_true', help='Oracle base table name')
    parser.add_argument('--type', '-t', required=True, nargs="+", type=get_type,
        help = "The type of map--either counties, or state")
    parser.add_argument('--default-color', required=False,
        help = "color of states", type=str, default="white")
    parser.add_argument('--map-extent', required=False,
        help = "us,continental_us to indicate what to include",
        type=str, default="continental_us")
    return parser.parse_args()



def _join_to_polygon_dict(polygon_dict, the_dict):
    for key in list(polygon_dict.keys()):
        pass

def _get_colors(polygon_dict, colors_dict , default_color, map_extent):
    if colors_dict == None:
        colors_dict = {}
    colors = []
    legends = []
    exclude = _get_exclude_dict(map_extent)
    for key in list(polygon_dict.keys()):
        if key in exclude :
            continue
        for i in polygon_dict[key]:
            data = colors_dict.get(key)
            if not data:
                color = default_color
                legend = 'na'
            else:
                color = data[0]
                legend = data[1]
            colors.append(color)
            legends.append(legend)
    return colors, legends

def _main_init_dict(polygon_dict):
    new_d = {}
    for key in list(polygon_dict.keys()):
        new_d[key] = {'xs':[], 'ys':[]}
        for shape in polygon_dict[key]:
            new_d[key]['xs'].append(shape[0])
            new_d[key]['ys'].append(shape[1])
    return new_d

def flatten(the_dict, key):
    l = []
    for k in sorted(list(the_dict.keys())):
        for i in the_dict[k][key]:
            if i == None:
                pass
            l.append(i)
    return l

def add_data(polygon_dict, data_key, data_dict):
    for key in list(polygon_dict.keys()):
        polygon_dict[key][data_key] = []
        for i in polygon_dict[key]['xs']:
            polygon_dict[key][data_key].append(data_dict.get(key))

def _make_legends(data, palette):
    assert isinstance(data, dict)
    the_min = min(data.values())
    the_max = max(data.values())
    step = (the_max - the_min)/(len(palette))
    if step == 0:
        step = .01
    last = the_min
    labels = []
    next_ = the_max - 1
    while next_ <= the_max:
        next_ = last + step
        labels.append('{last}: {next_}'.format(
            next_ = round(next_,1),
            last = round(last,1)
            ))
        last = next_
    labels_dict= {}
    for key in list(data.keys()):
        n = math.floor((data[key]-the_min)/step)
        if n == len(palette):
            n -= 1
        labels_dict[key] = labels[n]
    return labels_dict

def f(x):
    if x[0] == None:
        return 0
    return x[0]

def _sort_all_data(xs, ys, data, legends):
    t = sorted(zip(data,xs, ys, legends),key=f)
    return [x[1] for x in t], [x[2] for x in t], [x[0] for x in t], [x[3] for x in t]

def _filter_points(d, max_xs = -50, min_xs = -125):
    new_d ={}
    for key in d:
        new_d[key] = []
        for counter, the_tuple in enumerate(d[key]):
            if not (max(the_tuple[0]) > max_xs or min(the_tuple[0]) < min_xs):
                new_d[key].append(the_tuple)
    return new_d

def make_us_map(the_type, title = "test map", plot_width = 1100, plot_height = 700,
        line_color = "white", line_width = 0.5, colors_dict = None,
        default_color = "white", map_extent = 'continental_us', data=None,
        palette = Blues8, reverse_palette = True):
    if reverse_palette:
        palette.reverse()
    assert colors_dict == None or data == None
    choropleth = choropleth_prep.Chorpleth(the_type = the_type)
    d = _main_init_dict(_filter_points(choropleth.points_dict))
    #del(d['DC'])
    add_data(d,'data',  data)
    add_data(d,'legend', _make_legends(data, palette))
    xs, ys, data, legends = _sort_all_data(flatten(d, 'xs'), flatten(d, 'ys'),
            flatten(d, 'data'), flatten(d, 'legend'))
    assert len(data) == len(xs)
    color_mapper = LinearColorMapper(palette=palette)
    source = ColumnDataSource(data=dict(
                x=xs,
                y=ys,
                data = data,
                legend = legends,

            ))
    p = figure(title=title, toolbar_location="left",
               plot_width=plot_width, plot_height=plot_height)
    p.patches('x', 'y', source=source,
           fill_color={'field': 'data', 'transform': color_mapper},
           fill_alpha=0.7, line_color=line_color,
           line_width=line_width, legend = 'legend')

    show(p)

if __name__ == '__main__':
    l = ['FL', 'CT', 'ND', 'ID', 'NC', 'AZ', 'LA', 'PR',
'OK', 'WA', 'VT', 'CA', 'MD', 'WI', 'VI', 'PA',
'MT', 'TN', 'MS', 'IA', 'SC', 'IL', 'VA', 'MA', 'UT', 'NV',
'RI', 'HI', 'AK', 'AS', 'GU', 'GA', 'MP', 'MO', 'ME', 'NY',
'NJ', 'DC', 'IN', 'MN', 'KY', 'NM', 'DE', 'WY', 'TX', 'AL',
'OR', 'CO', 'NH', 'KS', 'AR', 'NE', 'OH', 'WV', 'SD', 'MI',]
    data = {}
    for i in l:
        data[i] = random.random()
    del(data['DC'])
    args = _get_args()
    make_us_map(the_type = args.type[0], default_color = args.default_color,
            map_extent = args.map_extent, data = data, palette = Oranges[9])
