from collections import OrderedDict
import numpy as np
from bokeh.plotting import figure
import pandas as pd

import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_quantiles(data):
    # data is a list of lists
    final = []
    for i in data:
        q1 = np.percentile(i, 25)
        q2 = np.percentile(i, 50)
        q3 = np.percentile(i, 75)
        iqr = q3 - q1
        final.append((q1 - 1.5*iqr, q3 + 1.5*iqr,q1, q2,  q3,  [x for x in i if x < q1 - (1.5 * iqr) or x >q3 + (1.5 * iqr)  ]))
    return final


def make_box_raw(p, cats, upper, lower, q1, q2, q3, out):
    p.segment(cats, lower, cats, upper)
    p.vbar(cats, 0.7, q1, q2, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q2, q3, fill_color="#3B8686", line_color="black")
    p.rect(cats, lower, 0.2, 0.01, line_color="black")
    p.rect(cats, upper, 0.2, 0.01, line_color="black")
    for k, v in out.items():
        for point in v:
            p.circle([k], [point], size=6, color="#F38630", fill_alpha=0.6)
    return p

def zip_data(cats, data):
    zip_data = list(zip(*data))
    outs = OrderedDict()
    for counter, i in enumerate(cats):
        if len(zip_data[5][counter]) != 0:
            outs[i] = zip_data[5][counter]
    return zip_data, outs

def box_plot(data, cats = None, p = None, df_type = None):
    """
    Simple List
    ============
    cats: a list of labels
    data: a list of lists
    Example:
    cats = ['a', 'b']
    data = [[1, 2, 3], [4, 5, 6]]
    
    Data Frame
    ============
    data = df, df_type = 'index'
    OR
    data = df, df_type = 'columns'
    
    Pandas Series
    ==============
    data =  [df['s1'], df['s2'], df['s3']]

    Returns: p, the figure()
    """
    if isinstance(data, list) and isinstance(data[0], pd.core.series.Series ):
        cats = []
        for i in data:
            cats.append(i.name)
    elif isinstance(data, pd.core.frame.DataFrame):
        assert df_type != None
        if df_type == 'index':
            cats = data.index.to_list()
        elif df_type == 'columns':
            cats = data.columns.to_list()
        else:
            raise ValueError('df_type must be "columns" or "index')
        if df_type == 'index':
            _data = []
            for index, rows in data.iterrows():
                _data.append(rows.values)
            data = _data
        elif df_type == 'columns':
            _data = []
            names = list(data)
            for i in list(data):
                _data.append(data[i].values)
            data = _data
    else:
        assert len(cats) == len(data)
        assert isinstance(cats, list)
        assert isinstance(data, list)
    if not p:
        p = figure(tools="save", background_fill_color="#EFE8E2", x_range=cats)
    f, outs = zip_data(cats, get_quantiles(data))
    return make_box_raw(p, cats, f[0], f[1], f[2], f[3], f[4], outs)


