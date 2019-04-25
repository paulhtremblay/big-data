import datetime
from bokeh.io import show
from bokeh.plotting import figure
from  big_data_tools.bokeh_tools.bar import bar
from  big_data_tools.bokeh_tools.histogram import hist 
from  big_data_tools.bokeh_tools.box_plot import box_plot 
from  big_data_tools.bokeh_tools.prob_plot import prob_plot 
from bokeh.layouts import gridplot
from bokeh.models import NumeralTickFormatter
from bokeh.models import DatetimeTickFormatter

#needed just for example

import numpy as np

#bar 
labels = ['first', 'second', 'third', 'fourth']
p_bar = figure(x_range=labels, plot_height=500, plot_width = 1000, title="my test title")
bar(labels, [1, 2, 3,4], p =p_bar)

#histogram
p_hist = hist([1,1,1,1,15,5,5, 10, 10,10,8])

#box plot
cats = ['a', 'b']
data = [[1, 2, 3], [4, 5, 6]]
p_box = box_plot(cats, data)

# simple line
p_simple_line = figure(title = "line example")
p_simple_line.yaxis.axis_label = "Y label"
p_simple_line.xaxis.axis_label = "X label"
p_simple_line.line([1, 2, 3, 4, 5, 6], [1000000, 2000000, 3000000, 3000000, 3000000, 3000000], line_width =2, 
        legend='line 1' )
p_simple_line.yaxis.formatter=NumeralTickFormatter(format="0,")

#p with date
p_with_date = figure(title = "date_example")
p_with_date.line([datetime.datetime(2019,1,1), datetime.datetime(2019,1,2), 
    datetime.datetime(2019,1,3), datetime.datetime(2019,1,4), datetime.datetime(2019,1,5), datetime.datetime(2019,1,6)], 
    [1, 2, 3, 4, 5, 6], 
    line_width =2, 
        legend='line with date' )
p_with_date.xaxis.formatter=DatetimeTickFormatter()
#see https://bokeh.pydata.org/en/latest/docs/reference/models/formatters.html


# get probability density for a set of discret values
discrete_values = [{'value':1, 'num_occurences':33},
    {'value':2, 'num_occurences':22},
    {'value':3, 'num_occurences':10},
    {'value':4, 'num_occurences':55},
        ]  
total_sum_of_discrete_values = sum([x['num_occurences'] for x  in discrete_values])
probabilty_of_each = [x['num_occurences']/total_sum_of_discrete_values for x in discrete_values] 
p_discrete_pdf = figure(title = "PDF")
p_discrete_pdf.line(x = [x['value'] for x in discrete_values], y = probabilty_of_each)

#QQ plot Normal
p_qq_normal = prob_plot(np.random.normal(size = 1000), 'norm')

#QQ plot Weibul
p_qq_weibul = prob_plot(np.random.weibull(a = .5, size = 1000), 'weibull_min', sparams= (.5,))

grid = gridplot([p_bar, p_hist, p_box, 
    p_simple_line, 
    p_with_date,
    p_discrete_pdf, p_qq_normal,
    p_qq_weibul,
    ], 
    ncols = 2, height=500, width = 500)
show(grid)
