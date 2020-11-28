from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import gridplot

def bar(labels, nums, height = 500, title = None, p = None):
    #output_file("bars.html")
    if not p:
        p = figure(x_range=labels, plot_height=height, title=title)
    p.vbar(x=labels, top=nums, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

def stacked_bar():
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ["2015", "2016", "2017"]
    colors = ["#c9d9d3", "#718dbf", "#e84d60"]

    data = {'fruits' : fruits,
            '2015'   : [2, 1, 4, 3, 2, 4],
            '2016'   : [5, 3, 4, 2, 4, 6],
            '2017'   : [3, 2, 4, 4, 5, 3]}

    p = figure(x_range=fruits, plot_height=250, title="Fruit Counts by Year",
               toolbar_location=None, tools="")

    p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
                 legend_label=years)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    return p

if __name__ == '__main__':
    #p = bar(['first', 'second', 'third', 'fourth'], [1, 2, 3,4])
    #show(p)
    labels = ['first', 'second', 'third', 'fourth']
    p1 = figure(x_range=labels, plot_height=500, plot_width = 1000, title="my test title")
    bar(labels, [1, 2, 3,4], p =p1)
    p2 = stacked_bar()
    grid = gridplot([p1, p2], ncols = 2)
    show(grid)

