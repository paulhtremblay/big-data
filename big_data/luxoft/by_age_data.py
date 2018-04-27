import os
import MySQLdb
import csv


def main():
    conn = MySQLdb.connect('data-blog.cqz4vljrvgvw.us-west-2.rds.amazonaws.com' , 'admin', 
             os.environ['BIG_DATA_DB_PW'], 'uk_accidents' )
    cur = conn.cursor()
    cur.execute("""
select date, age_band, sum(number_of_casualties)
from 
(
select  
date, 
case when age_of_casualty  >=21 and age_of_casualty < 26 then '21-25' 
	when age_of_casualty  >=26 and age_of_casualty < 31 then '26-30'
when age_of_casualty  >=31 and age_of_casualty < 36 then '31-35'
when age_of_casualty  >=36 and age_of_casualty < 41 then '36-40' 
end as age_band,
number_of_casualties
from 
accidents_2015 accidents
inner join casualities_2015 casualities
on casualities.accident_index = accidents.accident_index
inner join age_band
on age_band.code = casualities.age_band_of_casualty
where age_of_casualty  >= 21 and age_of_casualty < 41
and car_passenger = 0
) temp
group by date, age_band

    """)
    with open('../data_out/by_age.csv', 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['date', 'age_band', 'casualities'])
        for line in cur:
            csv_writer.writerow(line)


if __name__ == '__main__':
    main()

