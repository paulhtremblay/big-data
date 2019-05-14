"""
how to fill in a basic map
"""
import pprint
pp =pprint.PrettyPrinter(indent = 4)
from bokeh.plotting import figure, show, output_file
from numpy import nan
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models import Legend
from bokeh.palettes import Blues8
from bokeh.models import ColorMapper, LogColorMapper, LinearColorMapper
import random
import numpy as np
import json
import math
#from big_data_tools.bokeh_tools.map_legends import make_legends
from map_legends import make_legends

def _make_random_fill(l):
    colors = []
    for i in l:
        colors.append(random.choice(Blues8))
    return colors

def _make_random_data(l):
    return [random.randint(1,8) for x in l]

def use_data_source(d, map_width):
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    source = ColumnDataSource(data=dict(
                x=[d[x]['x'] for x in d.keys()],
                y=[d[x]['y'] for x in d.keys()],

            ))
    p.patches('x', 'y', source=source,
           )
    return p

def use_data_source_with_color_mapper(d, map_width):
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    color_mapper = LinearColorMapper(palette=Blues8)
    color_mapper.nan_color = 'gray'
    source = ColumnDataSource(data=dict(
                x=[d[x]['x'] for x in d.keys()],
                y=[d[x]['y'] for x in d.keys()],
                data = _make_random_data(d.keys()),

            ))
    p.patches('x', 'y', source=source,
        fill_color={'field': 'data', 'transform': color_mapper},
           )
    return p

def _make_legends_one(l):
    """legends is a list with the same length as data, or number of shapes. The choices should be the number in the pallette"""
    f  = []
    l2 = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',]
    for i in l:
        f.append(random.choice(l2))
    return f

def _make_legends_two(data):
    f  = []
    d = {1:'one', 2:'two', 3:'three', 4: 'four', 5: 'five', 6:'six', 7: 'seven', 8:'eight'}
    for i in data:
        f.append(d[i])
    return f

# a robust way to automtically generate labels
# needs to be unit tested with many examples??
def _make_legends(data, palette):
    the_min = min(data)
    the_max = max(data)
    step = (the_max - the_min)/(len(palette) - 1)
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
    for ii in list(data):
        n = math.floor((ii-the_min)/step)
        if n == len(palette):
            n -= 1
        labels_dict[ii] = labels[n]
    pp.pprint(labels_dict)
    # need to do the last step of mapping data to label
    assert False
    return labels_dict

def use_data_source_with_color_mapper_legends(d, map_width):
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    color_mapper = LinearColorMapper(palette=Blues8)
    color_mapper.nan_color = 'gray'
    legends = _make_legends_one(d.keys())
    source = ColumnDataSource(data=dict(
                x=[d[x]['x'] for x in d.keys()],
                y=[d[x]['y'] for x in d.keys()],
                data = _make_random_data(d.keys()),
                legend = legends

            ))
    p.patches('x', 'y', source=source,
        fill_color={'field': 'data', 'transform': color_mapper},
        legend = 'legend'
           )
    return p

def use_data_source_with_color_mapper_legends2(d, map_width):
    data = _make_random_data(d.keys())
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    color_mapper = LinearColorMapper(palette=Blues8)
    color_mapper.nan_color = 'gray'
    legends = _make_legends_two(data)
    source = ColumnDataSource(data=dict(
                x=[d[x]['x'] for x in d.keys()],
                y=[d[x]['y'] for x in d.keys()],
                data = data,
                legend = legends

            ))
    p.patches('x', 'y', source=source,
        fill_color={'field': 'data', 'transform': color_mapper},
        legend = 'legend'
           )
    return p

def use_data_source_with_color_mapper_legends_auto(d, map_width):
    #data = _make_random_data(d.keys())
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    color_mapper = LinearColorMapper(palette=Blues8)
    color_mapper.nan_color = 'gray'
    xs = []
    ys = []
    data = []
    for key in d.keys():
        if key == '04015':
            data.append(nan)
        else:
            data.append(random.randint(1,8))
        xs.append(d[key]['x'])
        ys.append(d[key]['y'])
    legends = make_legends(data, Blues8)
    source = ColumnDataSource(data=dict(
                x=xs,
                y=ys,
                data = data,
                legend = legends

            ))
    p.patches('x', 'y', source=source,
        fill_color={'field': 'data', 'transform': color_mapper},
        fill_alpha=0.7, line_color='white',
        legend = 'legend'
           )
    p.legend.location = "bottom_right"
    return p

def simple_fill(d, map_width):
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    p.patches([d[x]['x'] for x in d.keys()], 
            [d[x]['y'] for x in d.keys()
                ],
            fill_color = _make_random_fill(d.keys()),
            line_color = 'white',
            )
    return p

def main():
    #fill color
    map_width = 700
    with open('data/counties_non_territories_with_move.json', 'r') as read_obj:
        counties_move = json.load(read_obj) 
    p1 = simple_fill(counties_move, map_width)
    # example using source
    p2 = use_data_source(counties_move, map_width)
    p3 = use_data_source_with_color_mapper(counties_move, map_width)
    p4 = use_data_source_with_color_mapper_legends(counties_move, map_width)
    p5 = use_data_source_with_color_mapper_legends2(counties_move, map_width)
    p6 = use_data_source_with_color_mapper_legends_auto(counties_move, map_width)
    # use a mapper, which will assign colors for you
    grid = gridplot([p1, p2, p3, p4, p5, p6],  
        ncols = 2)
    show(grid)

if __name__ == '__main__':
    main()
