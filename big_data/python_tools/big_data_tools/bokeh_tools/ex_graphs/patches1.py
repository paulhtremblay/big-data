import pprint
pp =pprint.PrettyPrinter(indent = 4)
from bokeh.plotting import figure, show, output_file
from numpy import nan
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models import Legend
def main():
    #the nan makes two separate shapes, but keeps these shapes grouped together.
    p = figure()
    x = [1, 2, 3, 3, 2, 1, nan, 2, 3, 4, 4, 3, 2]
    y = [1, 2, 3, 2, 1, 0, nan, 1, 2, 3, 2, 1, 0]
    x2 =  [x +4  for x in x]
    y2 =  [x +4  for x in y]
    p.patch(x,y ,
            color="lightgrey",  alpha=.5
            )
    p.patch(x2,y2 ,
            color="blue",  alpha=.5
            )
    p2 = figure()
    xs = [x , x2]
    ys =  [y , y2]
    p2.patches(xs, ys, 
           fill_color=['red', 'blue'],
            )
    #now use source, for legends
    source = ColumnDataSource(data=dict(
                x=xs,
                y=ys,
                legends = ['first', 'second'],
                fill_colors = ['red', 'blue']
            ))
    p3 = figure()
    p3.patches('x', 'y', legend = 'legends',fill_color = 'fill_colors',  source =  source)
    grid = gridplot([p, p2, p3],  
        ncols = 2, height=500, width = 500)
    show(grid)

if __name__ == '__main__':
    main()
