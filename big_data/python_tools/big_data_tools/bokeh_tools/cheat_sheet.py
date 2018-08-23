import os
from google.cloud import bigquery
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.io import output_notebook, show

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Documents/ad-tech-test-204121-b0a06f7251e6.json'
client = bigquery.Client()
client.query("""slelect * from foo""")


p.yaxis.formatter=NumeralTickFormatter(format="0,")

p = figure(plot_width=800, plot_height=300, title="Title")

