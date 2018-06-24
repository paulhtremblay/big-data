import sys
import math
import numpy as np
from bokeh.plotting import figure, show, output_file
try:
    from . import  choropleth_prep
except SystemError:
    import choropleth_prep

from bokeh.palettes import Blues8
from bokeh.palettes import Oranges

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

def _get_points(the_dict,index, map_extent):
    points = []
    exclude = _get_exclude_dict(map_extent)
    for key in list(the_dict.keys()):
        if key in exclude :
            continue
        for i in the_dict[key]:
            points.append(i[index])
    return points

def _reverse_palete(palette):
    new_palette = []
    pos = len(palette) - 1
    while pos >= 0:
        new_palette.append(palette[pos])
        pos -= 1
    return new_palette

def make_colors(data, palette, reverse = True):
    assert isinstance(data, dict)
    if reverse == True:
        palette = _reverse_palete(palette)
    the_min = min(data.values())
    the_max = max(data.values())
    step = (the_max - the_min)/(len(palette) -1)
    colors_dict = {}
    if step == 0:
        step = .01
    for key in list(data.keys()):
        colors_dict[key] = palette[math.floor((data[key]-the_min)/step)]
    return colors_dict

def _get_colors(polygon_dict, colors_dict , default_color, map_extent):
    if colors_dict == None:
        colors_dict = {}
    colors = []
    exclude = _get_exclude_dict(map_extent)
    for key in list(polygon_dict.keys()):
        if key in exclude :
            continue
        for i in polygon_dict[key]:
            colors.append(colors_dict.get(key, default_color))
    return colors

def make_us_map(the_type, title = "test map", plot_width = 1100, plot_height = 700,
        line_color = "white", line_width = 0.5, colors_dict = None,
        default_color = "white", map_extent = 'continental_us', data=None,
        palette = Blues8):
    assert colors_dict == None or data == None
    choropleth = choropleth_prep.Chorpleth(the_type = the_type)
    xs = _get_points(choropleth.points_dict, 0, map_extent)
    ys = _get_points(choropleth.points_dict, 1, map_extent)
    if data:
        colors_dict = make_colors(data, palette)
    fill_colors = _get_colors(choropleth.points_dict,
        colors_dict = colors_dict, default_color = default_color, map_extent = map_extent)
    if fill_colors:
        assert len(xs) == len(fill_colors)
    p = figure(title=title, toolbar_location="left",
               plot_width=plot_width, plot_height=plot_height)
    p.patches(xs, ys,
              fill_alpha=0.7,
              fill_color=fill_colors,
              line_color=line_color, line_width=line_width)
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
    args = _get_args()
    make_us_map(the_type = args.type[0], default_color = args.default_color,
            map_extent = args.map_extent, data = data, palette = Oranges[9])
