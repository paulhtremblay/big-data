import os
import MySQLdb

def _get_host():
    return 'data-blog.cqz4vljrvgvw.us-west-2.rds.amazonaws.com'

def _get_db():
    return 'uk_accidents'

def _get_db_user():
    return 'admin'

def _get_db_pw():
    return os.environ['LUXOFT_DB_PW']

def _get_mysql_db(host, user, pw, db):
    return MySQLdb.connect(host,
        user, pw, db )

def _write_point(write_obj, longitude, latitude, name, description = ''):
    write_obj.write("""<Placemark>
<name>{name}</name>
<description>{description}</description>
<Point>
  <coordinates>{latitude},{longitude}</coordinates>
</Point>
</Placemark>\n""".format(latitude = latitude, longitude = longitude, description
    = description, name = name))


def main():

    #51.53077
    #51.52902
    conn = _get_mysql_db(host = _get_host(),
        user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    cursor = conn.cursor()
    cursor.execute("""select * from (select accident_index, latitude, longitude
            from accidents_2015
            where longitude < .29954 and longitude > -.52908
            and latitude> 51.26019 and latitude < 51.68958
            ) temp 
            """)
    with open('/home/paul/Downloads/uk_accidents.kml', 'w') as write_obj:
        write_obj.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
        write_obj.write("""<kml xmlns="http://www.opengis.net/kml/2.2">\n""")
        write_obj.write("""<Document>\n""")
        for counter, l in enumerate(cursor):
            _write_point(write_obj, l[1], l[2], l[0])
        write_obj.write("""</Document>\n""")
        write_obj.write("""</kml>""")
        print(counter)

if __name__ == '__main__':
    main()
