import csv
import pprint
import choropleth_us
#from . import  choropleth_prep
import choropleth_prep
pp = pprint.PrettyPrinter(indent = 4)

import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Blues8
import numpy as np
from bokeh.layouts import gridplot

def get_data():
    p = '/home/henry/Downloads/MCM_NFLIS_Data.csv'
    f = {}
    s = {}
    with open(p, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            state = row['State']
            fips = row['FIPS_Combined']
            year = int(row['YYYY'])
            num_reports = int(row['DrugReports'])
            if not f.get(year):
                f[year] = {}
            if not f[year].get(fips):
                f[year][fips] = 0
            if not s.get(year):
                s[year] = {}
            if not s[year].get(state):
                s[year][state] = 0
            f[year][fips] += num_reports
            s[year][state] += num_reports
    return f, s

def _main():
    choropleth = choropleth_prep.Chorpleth(the_type = 'state')
    xs, ys = choropleth.get_points_flatten('MA')
    xs2, ys2 = choropleth.get_points_flatten('NH')
    p = figure(title="test", toolbar_location="left",
           plot_width=1100, plot_height=700)
    p.patches([xs, xs2], [ys, ys2],
          fill_alpha=0.7,
          fill_color = ['green', 'blue'],
          line_color="white", line_width=0.5)
    #show(p)

def get_color(num, p85):
    [11. , 46., 105.8,274.]
     #5.   12.   17.4  30.2  50.   77.  107.  180.6 371.2
    """
    if num >= p85:
        return 'red'
    return 'white'
    """
    if num <= 5:
        return Blues8[6]
    elif num <= 12:
        return Blues8[6]
    elif num <= 17:
        return Blues8[5]
    elif num <= 30:
        return Blues8[5]
    elif num <= 50:
        return Blues8[3]
    elif num <= 77:
        return Blues8[3]
    elif num <= 107:
        return Blues8[1]
    elif num <= 180:
        return Blues8[1]
    return Blues8[0]

def make_county(county, year, choropleth):
    nums = []
    for key in county[year].keys():
        nums.append(county[year][key])
    p85 = np.percentile(nums, 85)
    p = figure(title=str(year))
    xs = []
    ys = []
    fill_colors = []
    for key in county[year].keys():
        num = county[year][key]
        x, y = choropleth.get_points_flatten(str(key))
        if x == None:
            continue
        xs.append(x)
        ys.append(y)
        fill_colors.append(get_color(num, p85))
    p.patches(xs, ys,
          fill_alpha=0.7,
          fill_color = fill_colors,
          line_color="white", line_width=0.001)
    return p

def main():
    county, state  = get_data()
    choropleth = choropleth_prep.Chorpleth(the_type = 'county')


    p1 = make_county(county, 2010, choropleth)
    p2 = make_county(county, 2011, choropleth)
    p3 = make_county(county, 2012, choropleth)
    p4 = make_county(county, 2013, choropleth)
    p5 = make_county(county, 2014, choropleth)
    p6 = make_county(county, 2015, choropleth)
    p7 = make_county(county, 2016, choropleth)
    p8 = make_county(county, 2017, choropleth)

    grid = gridplot([p1, p2, p3, p4, p5, p6, p7, p8], ncols = 2)
    show(grid)


    #pp.pprint(county[2010])
    #choropleth_us.make_us_map(the_type = 'county', data = county[2010])
    #choropleth_us.make_us_map(the_type = 'state', data = state[2010])

if __name__ == '__main__':
    main()
