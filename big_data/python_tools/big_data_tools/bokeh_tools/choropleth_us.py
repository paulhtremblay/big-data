import sys
from bokeh.plotting import figure, show, output_file
import choropleth_prep
import pprint
pp = pprint.PrettyPrinter(indent=4)

import argparse

def get_type(string):
    if string not in ['state', 'country']:
        raise argparse.ArgumentTypeError('Use "state" or "county" for type')
    return string

def get_exclude_dict(map_extent):
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

def get_points(the_dict,index, map_extent):
    points = []
    exclude = get_exclude_dict(map_extent)
    for key in list(the_dict.keys()):
        if key in exclude :
            continue
        for i in the_dict[key]:
            points.append(i[index])
    return points

def get_colors(polygon_dict, colors_dict , default_color, map_extent):
    colors = []
    exclude = get_exclude_dict(map_extent)
    for key in list(polygon_dict.keys()):
        if key in exclude :
            continue
        for i in polygon_dict[key]:
            colors.append(colors_dict.get(key, default_color))
    return colors

def main(the_type, title = "test map", plot_width = 1100, plot_height = 700,
        line_color = "white", line_width = 0.5, colors_dict = {},
        default_color = "white", map_extent = 'continental_us'):
    choropleth = choropleth_prep.Chorpleth(the_type = the_type)
    xs = get_points(choropleth.points_dict, 0, map_extent)
    ys = get_points(choropleth.points_dict, 1, map_extent)
    fill_colors = get_colors(choropleth.points_dict,
            colors_dict = colors_dict, default_color = default_color, map_extent = map_extent)
    assert len(xs) == len(fill_colors)
    p = figure(title=title, toolbar_location="left",
               plot_width=plot_width, plot_height=plot_height)
    p.patches(xs, ys,
              fill_alpha=0.7,
              fill_color=fill_colors,
              line_color=line_color, line_width=line_width)
    show(p)


if __name__ == '__main__':
    args = _get_args()
    main(the_type = args.type[0], default_color = args.default_color,
            map_extent = args.map_extent)
