from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.embed import json_item
import pprint
pp = pprint.PrettyPrinter(indent = 4)

import json
#create a new plot (with a title) using figure
p = figure(plot_width=400, plot_height=400, title="My Line Plot")

# add a line renderer
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)

item_text = json.dumps(json_item(p, "myplot"))
pp.pprint(item_text)

