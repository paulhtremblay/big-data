from bokeh.io import  show
from bokeh.plotting import figure
import datetime
import argparse
from bokeh.models import NumeralTickFormatter


def line_plot(p, x, y, line_width = 2, legend=None):
    p.line(x,y, line_width =line_width,legend=legend )
    p.yaxis.formatter=NumeralTickFormatter(format="0,")
    show(p)

