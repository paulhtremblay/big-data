import make_graph_instance
import datetime
import line_plot

def test_line_plot():
    p = make_graph_instance.make_p(title="test line plot", x_axis_type = 'datetime')
    x = [datetime.datetime(2013,1,1), datetime.datetime(2014,1,2),datetime.datetime(2015,1,3), datetime.datetime(2016,1,4),datetime.datetime(2017,1,5)]
    y =  [6, 7, 2, 4, 5]
    line_plot.line_plot(p,x,y)


if __name__ == '__main__':
    test_line_plot()
