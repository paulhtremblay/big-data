import psycopg2
import os

HOST = os.environ['REDSHIFT_HOST']
#host can be gotten from going to the cluster
# look for OBDC URL
#Server=<name>.<string>.<region>.redshift.amazonaws.com
PORT = 5439 # redshift default
USER = os.environ['REDSHIFT_USER']
PASSWORD = os.environ['REDSHIFT_PASSWD']
DATABASE = 'dev'

def db_connection():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )
    return conn

example_query = "select p_partkey, p_name, p_mfgr, p_category from part where p_mfgr is null"

conn = db_connection()
try:
    cursor = conn.cursor()
    cursor.execute(example_query)
    results = cursor.fetchone() 
    print(results)
finally:
    conn.close()

