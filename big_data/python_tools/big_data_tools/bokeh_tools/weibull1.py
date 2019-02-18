from bokeh.plotting  import figure, show
import numpy as np

def weib(x,n,a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

def make_pdf(size, a):
    x = np.arange(1, size)
    x =  np.arange(1,100.)/50.
    w = weib(x, 1, a)
    p = figure()
    p.line(x, w)
    show(p)

def make_dist(a, size):
    s = np.random.weibull(a, size)
    p = figure()
    hist, edges = np.histogram(s)
    p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)
    show(p)


if __name__ == '__main__':
    make_pdf(100, .5)
