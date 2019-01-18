import math
import csv
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
from scipy import stats
data = []
with open('data.txt', 'r') as read_obj:
    csv_reader = csv.DictReader(read_obj, delimiter = "\t")
    for line in csv_reader:
        data.append((float(line['PovPct']), float(line['Brth15to17'])))

data = sorted(data)
pov_pct = [x[0] for x in data]
birth_15_to_17 = [x[1] for x in data]
p = figure(plot_width=800, plot_height=300, title="Title")
p.circle(pov_pct, birth_15_to_17,  size=10, color="navy", alpha=0.5)
p.yaxis.formatter=NumeralTickFormatter(format="0,")
#fitted
slope, intercept, r_value, p_value, std_err = stats.linregress(pov_pct,birth_15_to_17)
p.line(pov_pct, [x * slope + intercept for x in pov_pct])
#show(p)
S = 0
print(slope, intercept, r_value, p_value, std_err)
for i in data:
    x = i[0]
    y = i[1]
    y_hat = x * slope + intercept
    S += (y- y_hat) * (y - y_hat)
S = math.sqrt(S/(len(pov_pct)))
p.line(pov_pct, [x * slope + intercept + S * 2 for x in pov_pct])
p.line(pov_pct, [x * slope + intercept - S * 2 for x in pov_pct])
show(p)


