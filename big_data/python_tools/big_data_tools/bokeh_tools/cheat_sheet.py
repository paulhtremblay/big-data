import os
from google.cloud import bigquery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Documents/ad-tech-test-204121-b0a06f7251e6.json'
client = bigquery.Client()
client.query("""slelect * from foo""")

from big_data_tools.bokeh_tools.all_p import *
from bokeh.palettes import *
# data = {'MA':10, 'NH':9}
# make_us_map(the_type = 'state', default_color="blue", data = data, # palette=Oranges[9])
# see https://bokeh.pydata.org/en/latest/docs/reference/palettes.html

#client.query("""slelect * from foo""")

from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure, show, output_file
#p.yaxis.formatter=NumeralTickFormatter(format="0,")
#p.xaxis.formatter=NumeralTickFormatter(format="0,")

# to get all graphs wrapper
from big_data_tools.bokeh_tools.all_p import *


p = figure(x_range=labels, plot_height=500,  title="my test title")
print('{x:,}'.format(x = x))#commas
