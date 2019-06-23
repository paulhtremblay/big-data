#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from scipy import stats


# In[ ]:


def get_ss_by_factor(df, factor_main, factor_second, target):
    df_means = df.groupby(by = [factor_main, factor_second]).mean()
    g_m = df.mean()
    total = 0
    for i in df[factor_main].unique():
        mean_g = df[df[factor_main]==i].mean()
        total +=  sum([(g_m - mean_g)**2 for x in df[df[factor_main]==i][target]])
    return total  


# In[ ]:


def get_ss_within(df, first_factor, second_factor, target):
    s = 0
    def get_combos():
        first = df[first_factor].unique()
        second = df[second_factor].unique()
        combos = []
        for i in first:
            for j in second:
                combos.append((i,j))
        return combos
    def get_mean(age, gender):
        f = df[df[first_factor]==age]
        s = f[f[second_factor]==gender]
        return s
    data = get_combos()
    for i in data:
        df_first = get_mean(i[0], i[1])
        mean = df_first.mean()
        s += sum([(x - mean)**2 for x in df_first[target]])
    return s


# In[ ]:


def get_ss_total(df, target):
    g_m = df.mean()
    return sum([(x-g_m)**2 for x in df[target]])


# In[ ]:


def get_ss_both_factors(df, ss_first, ss_second, ss_within, ss_total):
    return ss_total - (ss_gender + ss_age + ss_within)


# In[ ]:


def get_df(df, target):
    cols = list(df.columns)
    cols.remove(target)
    df_first =  len(list(df[cols[0]].unique())) - 1
    df_second = len(list(df[cols[1]].unique())) - 1
    df_within = len(df[target]) - (len(df[cols[0]].unique())*len(df[cols[1]].unique()))
    df_both_factors = df_first * df_second
    return df_first, df_second, df_within, df_both_factors


# In[ ]:


def do_anova(df, target):
    cols = list(df.columns)
    cols.remove(target)
    print(cols)
    print(df)
    ss_first = get_ss_by_factor(df, cols[0], cols[1], target)
    print(ss_first)
    return
    ss_second = get_ss_by_factor(df, cols[1], cols[0], target)
    ss_within = get_ss_within(df, cols[0], cols[1], target)
    ss_total  = get_ss_total(df, target)
    ss_both_factors = ss_total - (ss_first + ss_second + ss_within)
    df_first, df_second, df_within, df_both_factors = get_df(df, target)
    mean_first = ss_first/df_first
    mean_second = ss_second/df_second
    mean_ss_within = ss_within/df_within
    mean_both_factors = ss_both_factors/df_both_factors
    first_f_score = mean_first/mean_ss_within
    second_f_score = mean_second/mean_ss_within
    both_factors_f_score = mean_both_factors/mean_ss_within
    p_first = stats.f.sf(first_f_score, df_first, df_within)
    p_second = stats.f.sf(second_f_score, df_second, df_within)
    p_both_factors = stats.f.sf(both_factors_f_score, df_both_factors, df_within)
    return ('within', both_factors_f_score, p_both_factors),\
            (cols[0], first_f_score, p_first),\
            (cols[1], second_f_score, p_second)
    """
    return ('within', float(both_factors_f_score), float(p_both_factors))\, 
            (cols[0], float(first_f_score), float(p_first)),\
            (cols[1], float(second_f_score), float(p_second))
    """


