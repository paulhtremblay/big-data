import os
import MySQLdb
import csv

def _get_host():
    return 'data-blog.cqz4vljrvgvw.us-west-2.rds.amazonaws.com'

def _get_db():
    return 'uk_accidents'

def _get_db_user():
    return 'admin'

def _get_db_pw():
    return os.environ['INDEX_TEST_DB_PW']

def _get_mysql_db(host, user, pw, db):
    return MySQLdb.connect(host,
        user, pw, db )

def main():
    the_max = 0
    conn = _get_mysql_db(host = _get_host(), user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    for f in [f for f in os.listdir('/home/henry/Downloads/tmp/') ]:
        if f in ['local_authority_highway.csv']:
            print('skipping {f}'.format(f = f))
            continue
        table = os.path.splitext(f)[0]
        with open(os.path.join('/home/henry/Downloads/tmp/', f), 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            for line in csv_reader:
                if len(line[1]) > the_max:
                    the_max = len(line[1])
        cursor = conn.cursor()
        cursor.execute("""drop table if exists {table}""".format(table = table))
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("""create table {table}(
            code integer primary key not null,
            label varchar({the_max}) not null
            )""".format(table = table, the_max = the_max)) 
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("""load data local infile '{the_file}' into table {table} 
        fields terminated by ',' enclosed by '"'  lines terminated by '\n' ignore 1 lines""".format(table = table, 
            the_file = os.path.join('/home/henry/Downloads/tmp/', f)))
        cursor.close()
        conn.commit()

if __name__ == '__main__':
    main()
