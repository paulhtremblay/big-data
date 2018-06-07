import json
import pprint
pp = pprint.PrettyPrinter(indent = 4)
with open('us-10m.json', 'r') as read_obj:
    j = json.load(read_obj)

print(list(j.keys()))
pp.pprint(j['objects']['counties'])
#pp.pprint(j)
