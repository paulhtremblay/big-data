import os
import sys
import google
from google.cloud import bigquery

def two_projects():
    bigquery_client = bigquery.Client()
    [x  for x in bigquery_client.query(""" SELECT  name, gender,count FROM `external-project-203816.clickstream_main.external_table` limit 2""")]
    [x  for x in bigquery_client.query(""" SELECT name, gender,count as num FROM `paul-henry-tremblay.babynames.names_2014` limit 2""")]


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/a6002538/Downloads/external-project-203816-d93d70229145.json'
    two_projects()
