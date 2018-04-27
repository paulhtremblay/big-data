import os
import pprint
import random
import string
import csv
import tempfile

import timeit
import MySQLdb
import argparse

pp =pprint.PrettyPrinter(indent = 4)


def _get_host():
    return 'data-blog.cqz4vljrvgvw.us-west-2.rds.amazonaws.com'

def _get_db():
    return 'test'

def _get_db_user():
    return 'admin'

def _gen_random():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(30, 49)))

def _get_db_pw():
    return os.environ['INDEX_TEST_DB_PW']

def _make_csv_file(num_rows, num_columns):
    fh, path = tempfile.mkstemp()
    with open(path, 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for i in range(num_rows):
            temp = [i]
            for j in range(num_columns):
                temp.append(_gen_random())
            csv_writer.writerow(temp)
    return fh, path

def _get_args():
    parser = argparse.ArgumentParser(description='Run tests with inexes on database')
    parser.add_argument('--verbose', '-verbose', action='store_true', help='verbose messaging')
    parser.add_argument('--no-primary-key', action='store_true', help='run test for no primary key')
    parser.add_argument('--primary-key', action='store_true', help='run test for  primary key')
    parser.add_argument('--insert-test', action='store_true', help='run test for insert rows')
    parser.add_argument('--delete-test', action='store_true', help='run test for delete rows')
    parser.add_argument('--create-base1', action='store_true', help='create base table 1')
    parser.add_argument('--create-base2', action='store_true', help='create base table 1')
    parser.add_argument('--num-insertions', type=int, help='number of insertions')
    parser.add_argument('--num-rows', type=int, help='number of rows')
    parser.add_argument('--num-columns', type=int, help='number of columns')
    return parser.parse_args()


def write_csv(path, results):
    with open(path, 'w') as write_obj:
        writer = csv.DictWriter(write_obj, fieldnames=['num_rows', 'time'])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def _write_results(path, results, fieldnames):
    if not os.path.isdir('data_out'):
        os.makedirs('data_out')
    path = os.path.join('data_out', path)
    with open(path, 'w') as write_obj:
        writer = csv.DictWriter(write_obj, fieldnames=fieldnames)
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

def _create_base_table(conn, table, num_columns, num_rows):
    fh, path = _make_csv_file(num_columns = num_columns, num_rows = num_rows, )
    cursor = conn.cursor()
    cursor.execute("""
        drop table if exists {table};
    """.format(table = table))
    cursor.close()
    cursor = conn.cursor()
    s = 'create table {table} \n(pk int not null primary key ,'.format(table = table) + \
        ',\n'.join(['name{x} varchar(50) not null'.format(x = x) for x in range(1, num_columns + 1)]) +\
        ')'
    cursor.execute(s)
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(""" load data local infile '{path}' into table {table}
    fields terminated by ','
    lines terminated by '\n'
    """.format(table = table, path = path))
    cursor.close()
    os.close(fh)
    os.remove(path)
    conn.commit()

def _test_load_one_tb(cursor, table, base_table, number):
    cursor.execute("""
insert into {table}
select * from {base_table} limit {number}
;
    """.format(table = table, number = number, base_table = base_table))

def create_base_table1(conn):
    _create_base_table(conn, 'base_test1.txt', 'test1')

def create_base_table2(conn):
    """Table with longer rows"""
    _create_base_table(conn, 'base_test2.txt', 'test2')

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
	name1 varchar(50) not null ,
	name2 varchar(50) not null
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
    conn.commit()

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

def _delete_rows(conn, table, row_list):
    cursor = conn.cursor()
    cursor.execute("""delete from {table} where pk in ({pks})""".format(table = table, pks = ','.join([str(x) for x in row_list])))
    conn.commit()

def _insert_func(cursor, table, row_list):
    l = """insert into table {table} values({pk})
    """.format(table = table, pk = ','.join([str(x) for x in row_list]))
    l = []
    for i in row_list:
        l.append("({pk}, 'xxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')".format(pk = i))

    l = 'insert into {table} values{values}'.format(table = table, values = ',\n'.join(l))
    cursor.execute(l)

def _delete_func(cursor, table, row_list):
    for i in row_list:
        cursor.execute("""delete from {table} where pk = {pk}""".format(pk =  i, table = table))

def delete_test(num_rows = 100):
    conn = _get_mysql_db(host = _get_host(), user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    _create_temp_table(conn, table = 'test_delete_pk', base_table = 'test_base1', num_rows = num_rows, primary_key = 'primary key')
    _create_temp_table(conn, table = 'test_delete_npk', base_table = 'test_base1', num_rows = num_rows, primary_key = '')
    cursor = conn.cursor()
    pk_results = []
    npk_results = []
    for i in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 10000, 100000]:
        row_list = random.sample(range(1, num_rows), i)
        wrapped = wrapper(_delete_func, cursor, 'test_delete_pk', row_list)
        tpk = timeit.timeit(wrapped, number=1)
        pk_results.append({'time':tpk, 'num_rows':i})
        wrapped = wrapper(_insert_func, cursor, 'test_delete_npk', row_list)
        tnpk = timeit.timeit(wrapped, number=1)
        npk_results.append({'time':tnpk, 'num_rows':i})
    _write_results('pk_delete_results.csv', pk_results, ['time', 'num_rows'])
    _write_results('npk_delete_results.csv', npk_results, ['time', 'num_rows'])
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("drop table test_delete_pk"); 
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("drop table test_delete_npk"); 
    cursor.close()
    conn.commit()


def insert_test(num_rows = 100):
    conn = _get_mysql_db(host = _get_host(), user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    _create_temp_table(conn, table = 'test_insert_pk', base_table = 'test_base1', num_rows = num_rows, primary_key = 'primary key')
    _create_temp_table(conn, table = 'test_insert_npk', base_table = 'test_base1', num_rows = num_rows, primary_key = '')
    cursor = conn.cursor()
    pk_results = []
    npk_results = []
    for i in [1000, 10000,50000 ]:
        row_list = random.sample(range(1, num_rows), i)
        _delete_rows(conn, 'test_insert_pk', row_list)
        _delete_rows(conn, 'test_insert_npk', row_list)
        wrapped = wrapper(_insert_func, cursor, 'test_insert_pk', row_list)
        tpk = timeit.timeit(wrapped, number=1)
        pk_results.append({'time':tpk, 'num_rows':i})
        wrapped = wrapper(_insert_func, cursor, 'test_insert_npk', row_list)
        tnpk = timeit.timeit(wrapped, number=1)
        npk_results.append({'time':tnpk, 'num_rows':i})
    _write_results('pk_insert_results.csv', pk_results, ['time', 'num_rows'])
    _write_results('npk_insert_results.csv', npk_results, ['time', 'num_rows'])
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("drop table test_insert_pk"); 
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("drop table test_insert_npk"); 
    cursor.close()
    conn.commit()

def create_table_test():
    conn = _get_mysql_db(host = _get_host(), 
        user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    _create_one_tb(conn = conn, primary_key = '')
    cursor = conn.cursor()
    wrapped = wrapper( _test_load_one_tb, cursor, 'test55', 'test1', int(1e6))
    t = timeit.timeit(wrapped, number=1)
    cursor.close()

def create_base1():
    conn = _get_mysql_db(host = _get_host(), 
        user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    _create_base_table(conn, table = 'test_base1')

def create_base2(num_rows, num_columns):
    conn = _get_mysql_db(host = _get_host(), 
        user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    _create_base_table(conn, table = 'test_base2', num_columns = num_columns, num_rows = num_rows)

def main():
    args = _get_args()
    if args.insert_test == True:
        insert_test(num_rows = args.num_rows)
    elif args.create_base1 == True:
        create_base1()
    elif args.create_base2 == True:
        create_base2(num_columns = args.num_columns, num_rows = args.num_rows)
    elif args.delete_test == True:
        delete_test(num_rows = args.num_rows)
    else:
        raise ValueError("Please choose an option")

if __name__ == '__main__':
    main()

