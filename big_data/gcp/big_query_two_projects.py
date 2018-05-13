import os
import sys
import google
from google.cloud import bigquery
# Instantiates a client
#print(dir(bigquery))
#print(dir(bigquery.external_config))
#sys.exit(1)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Downloads/external-project-203816-d93d70229145.json'


bigquery_client = bigquery.Client()
x = bigquery_client.query(""" SELECT  name, gender,count FROM `external-project-203816.clickstream_main.external_table` limit 2""")

for i in x:
    print(i)

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Downloads/paul-henry-tremblay-5b7d3c62880b.json'
#bigquery_client = bigquery.Client()
x = bigquery_client.query(""" SELECT name, gender,count as num FROM `paul-henry-tremblay.babynames.names_2014` limit 2""")

try:
    for i in x:
        print(i)
except google.api_core.exceptions.Forbidden:
    print("Failed on paul-henry-tremblaly")

