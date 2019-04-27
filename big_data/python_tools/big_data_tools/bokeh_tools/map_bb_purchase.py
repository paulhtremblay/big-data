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
import csv


def make_map(d, map_width):
    rev_dict = {}
    with open('/Users/a6002538/Downloads/results-20190426-163009.csv', 'r') as read_obj:
        reader = csv.DictReader(read_obj)
        for row in reader:
            rev_dict[row['fips']] = float(row['rev'])
    p = figure(width=map_width, height = int(round(4/5 * map_width)))
    palette = Blues8
    palette.reverse()
    #color_mapper = LinearColorMapper(palette=palette)
    color_mapper = LogColorMapper(palette=palette)
    color_mapper.nan_color = 'gray'
    _data = []
    for key in d.keys():
        _data.append((rev_dict.get(key,0), d[key]['x'], d[key]['y']))
    _data = sorted(_data)
    data =  [x[0] for x in _data]
    xs =  [x[1] for x in _data]
    ys =  [x[2] for x in _data]
    #legends = make_legends(data, palette)
    log_list = [math.log(x) if x > 0 else 0 for x in data]
    perc = [1/len(palette) * x  for x in range(1, len(palette) + 1)]
    q = np.quantile(log_list, perc)
    ls = []
    prev = 0
    for i in q:
        n = '{0:,}'.format(round(math.exp(i)))
        ls.append('{p}:{n}'.format(p = prev, n = n ))
        prev = n
    ls.append('>')
    fill_colors = []
    legends = []
    for i in data:
        if i == 0 or math.log(i) <= q[0]:
            fill_colors.append(palette[0])
            legends.append(ls[0])
        elif math.log(i) <= q[1]:
            fill_colors.append(palette[1])
            legends.append(ls[1])
        elif math.log(i) <= q[2]:
            fill_colors.append(palette[2])
            legends.append(ls[2])
        elif math.log(i) <= q[3]:
            fill_colors.append(palette[3])
            legends.append(ls[3])
        elif math.log(i) <= q[4]:
            legends.append(ls[4])
            fill_colors.append(palette[4])
        elif math.log(i) <= q[5]:
            fill_colors.append(palette[5])
            legends.append(ls[5])
        elif math.log(i) <= q[6]:
            fill_colors.append('orange')
            legends.append(ls[6])
        elif math.log(i) <= q[7]:
            fill_colors.append('red')
            legends.append(ls[7])
        else:
            fill_colors.append('orange')
            legends.append(ls[8])
    source = ColumnDataSource(data=dict(
                x=xs,
                y=ys,
                data = data,
                legend = legends,
                fill_colors = fill_colors
            ))
    p.patches('x', 'y', source=source,
        fill_color = 'fill_colors',
        fill_alpha=0.7, line_color='black',
        line_width = .2,
        legend = 'legend'
           )
    p.legend.location = "bottom_right"
    return p

def main():
    map_width = 700
    with open('data/counties_non_territories_with_move.json', 'r') as read_obj:
        counties_move = json.load(read_obj) 
    p1 = make_map(counties_move, map_width)
    grid = gridplot([p1],  
        ncols = 2)
    show(grid)

if __name__ == '__main__':
    main()
