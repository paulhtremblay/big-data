import os
import pprint
import csv

import timeit
import MySQLdb
import argparse

pp =pprint.PrettyPrinter(indent = 4)

def _get_args():
    parser = argparse.ArgumentParser(description='Run tests with inexes on database')
    parser.add_argument('--verbose', '-verbose', action='store_true', help='verbose messaging')
    parser.add_argument('--no-primary-key', action='store_true', help='run test for no primary key')
    parser.add_argument('--primary-key', action='store_true', help='run test for  primary key')
    parser.add_argument('--primary-key', action='store_true', help='run test for  primary key')
    return parser.parse_args()


def write_csv(path, results):
    with open(path, 'w') as write_obj:
        writer = csv.DictWriter(write_obj, fieldnames=['num_rows', 'time'])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def _get_mysql_db(host, user, pw, db):
    return MySQLdb.connect(host,
        user, pw, db )

def _create_one_tb(conn, primary_key = ''):
    cursor = conn.cursor()
    cursor.execute("""
        drop table if exists test55 """)
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("""
    create table test55
    (pk int not null {primary_key} ,
            name1 varchar(30) not null ,
            name2 varchar(30) not null
    )
    """.format(primary_key = primary_key))
    cursor.close()

def _create_base_table(conn, path, table):
    cursor = conn.cursor()
    cursor.execute("""
        drop table if exists {table};
    """.format(table = table))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("""
    create table {table}
    (pk int not null primary key ,
            name1 varchar(30) not null ,
            name2 varchar(30) not null
    )
    """.format(table = table))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("""
    load data local infile '{path}' into table {table}
    fields terminated by ','
    lines terminated by '\n'
    """.format(table = table, path = path))
    cursor.close()

def _test_load_one_tb(cursor, table, base_table, number):
    cursor.execute("""
insert into {table}
select * from {base_table} limit {number}
;
    """.format(table = table, number = number, base_table = base_table))

def _create_temp_table(conn, table, base_table, num_rows, primary_key = ''):
    cursor = conn.cursor()
    cursor.execute("""
        drop table if exists {table}
    """.format(table = table))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("""
create table {table}
(pk int not null {primary_key},
	name1 varchar(30) not null ,
	name2 varchar(30) not null
)
    """.format(table = table, primary_key = primary_key))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("""
insert into {table} 
select * from {base_table} limit {number}
;
    """.format(table = table, number = num_rows, base_table = base_table))
    cursor.close()

def _create_temp_tables(conn, primary_key, num_rows):
    _create_temp_table(conn, table = 'test11', base_table = 'test1', primary_key = primary_key,  num_rows = num_rows)
    _create_temp_table(conn, table = 'test22', base_table = 'test2', primary_key = primary_key,  num_rows = num_rows)
    _create_temp_table(conn, table = 'test33', base_table = 'test3', primary_key = primary_key,  num_rows = num_rows)


def _creat_base_tables(conn):
    _create_base_table(conn, 'test1.txt', 'test1')
    _create_base_table(conn, 'test2.txt', 'test2')
    _create_base_table(conn, 'test3.txt', 'test3')

def max_query(cursor):
    cursor.execute("""
select max(t1.name1) 
from test11 t1
inner join test22 t2
on t1.pk = t2.pk
inner join test33 t3
on t3.pk = t2.pk
    """)


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def _primary_key(conn):
    result = []
    verbose = True
    for i in [1e5, 2e5, 3e5, 4e5, 6e5, 7e5, 8e5, 9e5, 1e6,  1.4e6, 1.8e6, 2e6,
            ]:
        if verbose:
            print("creating tables for {i}".format(i = i))
        _create_temp_tables(conn, 'Primary Key', int(i))
        cursor = conn.cursor()
        cursor.execute("""RESET QUERY CACHE""")
        cursor.close()
        cursor = conn.cursor()
        wrapped = wrapper(max_query, cursor)
        t = timeit.timeit(wrapped, number=1)
        if verbose:
            print("max took {t} seconds".format(t = round(t,1)))
        cursor.close()
        result.append({'num_rows':i, 'time': t})
    write_csv('primary_key.csv', result)

def _no_primary_key(conn):
    result = []
    verbose = True
    for i in [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
            15000, 20000, 25000, 30000, 60000
            ]:
        if verbose:
            print("creating tables for {i}".format(i = i))
        _create_temp_tables(conn, '', i)
        if verbose:
            print("created tables for {i}".format(i = i))
        cursor = conn.cursor()
        wrapped = wrapper(max_query, cursor)
        t = timeit.timeit(wrapped, number=1)
        cursor.close()
        result.append({'num_rows':i, 'time': t})
    write_csv('no_primary_key.csv', result)


def main():
    args = _get_args()
    print(args)

def main_():
    conn = _get_mysql_db(host = 'pi-oasis-dev-cluster.cluster-ctiutsvmu8ci.us-west-2.rds.amazonaws.com', 
        user = 'admin', pw = os.environ['AURORA_DB_PASSWORD'], db = 'app_dev')
    #_no_primary_key(conn)
    #_primary_key(conn)
    _create_one_tb(conn = conn, primary_key = '')
    cursor = conn.cursor()
    wrapped = wrapper( _test_load_one_tb, cursor, 'test55', 'test1', int(1e6))
    t = timeit.timeit(wrapped, number=1)
    print(t)
    cursor.close()

if __name__ == '__main__':
    main()

