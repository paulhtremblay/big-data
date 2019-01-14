import numpy as np
from scipy.signal import savgol_filter
#np.set_printoptions(precision=2)
import random
from bokeh.io import  show
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
#x = np.array([2, 2, 5, 2, 1, 0, 1, 4, 9])

def line_plot(p, x, y, line_width = 2, legend=None):
    p.line(x,y, line_width =line_width,legend=legend )
    #p.yaxis.formatter=NumeralTickFormatter(format="0,")

def generate_numbers(n, low, high, increment):
    add = 0
    for i in range(n):
        add += increment
        yield random.randint(low, high) + add

def main():
    gen = generate_numbers(365, 6, 10, .005)
    x = []
    y =[]
    for counter, i in enumerate(gen):
        #print('{x},{y}'.format(x = counter, y = i))
        x.append(counter)
        y.append(i)
    p = figure(plot_width=400, plot_height=400, title = "original")
    line_plot(p, x, y)
    show(p)
    y = savgol_filter(y, 61, 8)
    p2 = figure(plot_width=400, plot_height=400, title = "smoothed 3")
    line_plot(p2, x, y)
    show(p2)

if __name__ == '__main__':
    main()
