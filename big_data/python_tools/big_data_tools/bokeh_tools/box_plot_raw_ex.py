import sys
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file


def make_box_raw(p, cats, upper, lower, q1, q2, q3, out):
    p.segment(cats, lower, cats, upper)
    p.vbar(cats, 0.7, q1, q2, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q2, q3, fill_color="#3B8686", line_color="black")
    p.rect(cats, lower, 0.2, 0.01, line_color="black")
    p.rect(cats, upper, 0.2, 0.01, line_color="black")
    for k, v in out.items():
        for point in v:
            p.circle([k], [point], size=6, color="#F38630", fill_alpha=0.6)
    show(p)


def main():
    cats = ['a', 'b', 'c']
    lower = (1,2,3)
    upper = (5, 7,8)
    q1 = (2,3,4)
    q2 = (3,4,5)
    q3 = (4,5,6)
    out = OrderedDict()
    out['a'] = [9,10]
    out['c'] = [11]
    p = figure(tools="save", background_fill_color="#EFE8E2", title="box plot", x_range=cats)
    make_box_raw(p, cats, upper,lower, q1, q2, q3, out)

if __name__ == '__main__':
    main()
