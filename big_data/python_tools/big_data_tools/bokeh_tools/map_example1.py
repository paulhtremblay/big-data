import pprint
pp =pprint.PrettyPrinter(indent = 4)
from bokeh.plotting import figure, show, output_file
from numpy import nan
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models import Legend
import numpy as np
import json

def main():
    map_width = 700
    with open('data/states_non_territories.json', 'r') as read_obj:
        states = json.load(read_obj) 
    p1 = figure(width = map_width, height = int(round(4/5 * map_width)))
    p1.patches([states[x]['x'] for x in states.keys()], 
            [states[x]['y'] for x in states.keys()
                ],
            fill_color = ['white' for x in states.keys()]
            )
    with open('data/counties_non_territories.json', 'r') as read_obj:
        counties = json.load(read_obj) 
    #need to map zip to fips
    with open('data/zip_fips.json', 'r') as read_obj:
        zips = json.load(read_obj)
    p2 = figure(width = map_width)
    p2.patches([counties[x]['x'] for x in counties.keys()], 
            [counties[x]['y'] for x in counties.keys()
                ],
            fill_color = ['white' for x in counties.keys()]
            )
    # just one county
    p3 = figure()
    zip_c ='98102'
    fips = zips[zip_c]['fips']
    p3.patches([counties[fips]['x'], ], [counties[fips]['y']], 
           fill_color=['red'],
            )
    # counties for just continental
    p4 = figure(width = map_width, height = int(round(3.5/5 * map_width)))
    p4.patches([counties[x]['x'] for x in counties.keys() if counties[x]['state'] not in  ['AK', 'HI']], 
            [counties[x]['y'] for x in counties.keys() if counties[x]['state'] not in  ['AK', 'HI'] ],
            fill_color = ['white' for x in counties.keys() if counties[x]['state'] not in ['AK', 'HI']],
            )
    # use 4/5 ration of height/width
    with open('data/states_states_resize.json', 'r') as read_obj:
        states2 = json.load(read_obj)
    p7 = figure(width=map_width, height = int(round(4/5 * map_width)))
    p7.patches([states2[x]['x'] for x in states2.keys()], 
            [states2[x]['y'] for x in states2.keys()
                ],
            fill_color = ['white' for x in states2.keys()]
            )
    grid = gridplot([p1, p2, p3, p4,  p7],  
        ncols = 2)
    show(grid)

if __name__ == '__main__':
    main()
