import os
import MySQLdb
import csv

from numpy import array

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

import pprint
pp =pprint.PrettyPrinter(indent = 4)

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
    conn = _get_mysql_db(host = _get_host(), user = _get_db_user(), pw = _get_db_pw(), db = _get_db())
    cur = conn.cursor()
    cur.execute(""" select date, 
sum(number_of_casualties) as number_of_casualties
from accidents_2015 
group by date
    """)
    l = [int(x[1]) for x in cur.fetchall()]
    p1 = figure(title="Normal Distribution (μ=0, σ=0.5)",tools="save",
                        background_fill_color="#E8DDCB")
    mu, sigma = 0, 0.5
    hist, edges = np.histogram(l, density=True, bins=50)
    output_file('histogram.html', title="histogram.py example")
    p1.line(edges[1:], hist, line_width=2, color="red", legend="fitted")
    show(p1)

if __name__ == '__main__':
    main()
