#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
from bokeh.io import show
from bokeh.plotting import figure
from  big_data_tools.bokeh_tools.box_plot import box_plot
from bokeh.layouts import gridplot
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


# In[ ]:


def get_groups_for_tukey(data):
    groups = []
    for i in data.index:
        for j in data.loc[i]:
            groups.append(i)
    return groups
def get_values_for_tukey(data):
    values = []
    for i in data.index:
        for j in data.loc[i]:
            values.append(j)
    return values


# In[2]:


def get_data_2():
    d = [
        ['1', '1', 65],
        ['1', '2', 49],
        ['1', '3', 50],
        ['2', '1', 53],
        ['2', '2', 51],
        ['2', '3', 48],
        ['3', '1', 47],
        ['3', '2', 45],
        ['3', '3', 50],
        ['4', '1', 51],
        ['4', '2', 43],
        ['4', '3', 52],
    ]
    df = pd.DataFrame(d,   
                     columns = ['coating', 'soil', 'corrosion'])
    return df

def box_ex2():
    df = get_data_2()
    p_box1 = box_plot(cats =['1', '2', '3', '4'],
                      data = [
                       list(df[df.coating == '1'].corrosion),
                       list(df[df.coating == '2'].corrosion),
                       list(df[df.coating == '3'].corrosion),
                       list(df[df.coating == '3'].corrosion),
                      ]
    )
    p_box2 = box_plot(cats =['1', '2', '3'],
                      data = [
                       list(df[df.soil == '1'].corrosion),
                       list(df[df.soil == '2'].corrosion),
                       list(df[df.soil == '3'].corrosion)
                      ]
    )
    grid = gridplot([p_box1, p_box2
        ],
        ncols = 2)
    show(grid)
#box_ex2()


# In[3]:


def anova_ex2():
    data = get_data_2()
    formula = 'corrosion ~ C(soil) + C(coating) + C(soil):C(coating)'
    model = ols(formula, data).fit()
    aov_table = anova_lm(model, typ=2)
    print(aov_table)
anova_ex2()


# In[ ]:


def get_data_ex3():
    d1 = [200, 226, 240, 261]
    d2 = [278, 312, 330, 381]
    d3 = [369, 416, 462, 517]
    d4 = [500, 575, 645, 733]
    df = pd.DataFrame([d1, d2, d3,d4],  index = ['200', '400', '700', '1100'], 
                     columns = ['190', '250', '300', '400'])
    return df


# In[ ]:


def get_data_pen():
    d1 = [.97, .48, .48, .46]
    d2 = [.77, .14, .22, .25]
    d3 = [.67, .39, .57, .19]
    df = pd.DataFrame([d1, d2, d3],  index = ['1', '2',  '3'], 
                     columns = ['1', '2', '3', '4'])
    return df


# In[ ]:




