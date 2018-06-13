import os
from google.cloud import bigquery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Documents/ad-tech-test-204121-b0a06f7251e6.json'
client = bigquery.Client()
client.query("""slelect * from foo""")


from bokeh.models import NumeralTickFormatter

    p.yaxis.formatter=NumeralTickFormatter(format="0,")
