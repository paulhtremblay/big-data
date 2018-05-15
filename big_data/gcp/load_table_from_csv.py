import sys
from google.cloud import bigquery
client = bigquery.Client()
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
#configuration.load.sourceFormat
#configuration.copy.destinationTable
dataset_ref = client.dataset('babynames')
dataset = bigquery.Dataset(dataset_ref)
#job_config.projectId = 'paul-henry-tremblay'
load_job = client.load_table_from_uri(
        'gs://paulhenrytremblay/yob1945.txt',
    dataset_ref.table('names_2014'),
    job_config=job_config)  # API request


assert load_job.job_type == 'load'
load_job.result()  # Waits for table load to complete.
assert client.get_table(dataset_ref.table('names_2014')).num_rows == 50
