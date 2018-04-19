import math
from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png

def _get_no_indices_data():
    return  ([1000, 2000, 3000,
    4000, 5000, 6000, 7000, 8000, 10000,
    15000, 20000, 25000, 30000, 60000,],
    [ 0.2, 0.6, 1.4, 2.1,
    3.3, 4.8, 7.3, 10.4, 13.0, 24.8,
    55.4, 70.1, 118.1, 398.5])

def _get_indices_data():
    return ([ 100000, 200000, 300000, 400000,
    600000, 700000, 800000, 900000, 1000000,
    1400000, 1800000 ],
    [ 0.3, 4.0, 7.8, 11.4, 16.8, 20.9,
    24.9, 23.4, 25.7, 39.3, 52.2]
    )

def no_indices():
    no_index = _get_no_indices_data()
    index = _get_indices_data()
    output_file("indices_sql1.html")
    p = figure(title="Without Indices", x_axis_label='num rows', y_axis_label='seconds', 
            plot_width=1000, plot_height=1000)
    p.line(no_index[0], no_index[1], line_width=2, color="blue",
    legend="Actual")
    fitted = [.00000025/2* x * x for x in no_index[0]]
    p.line(no_index[0], fitted, line_width=2, color="red", legend="fitted")
    show(p)

def indices():
    c = 2.01342786663877e-06
    index = _get_indices_data()
    output_file("indices_sql2.html")
    p = figure(title="With Indices", x_axis_label='num rows', y_axis_label='seconds', 
            plot_width=1000, plot_height=1000)
    p.line(index[0], index[1], line_width=2, color="blue",
    legend="Actual")
    fitted = [math.log(x) * x * c  for x in index[0]]
    p.line(index[0], fitted, line_width=2, color="red", legend="fitted")
    show(p)


def main():
    no_indices()
    indices()

if __name__ == '__main__':
    main()

