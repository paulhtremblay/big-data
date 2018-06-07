import make_kml_map
import csv

with open ('../temp_data/part-r-00000-452ee7ed-3845-44fd-af23-fd3fb4800d16.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    make_kml_map.make_map(csv_reader)


