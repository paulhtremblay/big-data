import os
# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()
for bucket in storage_client.list_buckets():
    print(bucket)
bucket = storage_client.bucket('paulhenrytremblay')
blob = bucket.blob('file_from_upload.txt')
with open('sample.txt', 'rb') as read_obj:
    blob.upload_from_string(
        b'some text',
        content_type='text/plain')
print(dir(blob))
blob = bucket.blob('file_from_upload2.txt')
with open('sample2.txt', 'rb') as read_obj:
    blob.upload_from_file(
            read_obj,
        content_type='text/plain')



