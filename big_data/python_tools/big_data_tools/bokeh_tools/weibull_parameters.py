#!/usr/bin/env python
# coding: utf-8

# In[100]:


from scipy import stats
import numpy as np
import math
from scipy.optimize import bisect
from bokeh.plotting  import figure, show


# In[129]:


#create a dist
c = .9
scale = 10
loc = 10
rv = stats.weibull_min.rvs(c=c, scale = scale, loc = loc, size = 50)
ex = scale * math.gamma(1 + 1/c) + loc
m =np.mean(rv)
print(ex, m, min(rv))


# In[130]:


def sum__x_sq_div_mean_x_sq(rv):
    s = 0
    for i in rv:
        s += (i * i)/(np.mean(rv) * np.mean(rv))
    return s/(len(rv))


# In[131]:


#fix the location at zero
the_min = np.min(rv)
rv_min = rv - the_min
k = sum__x_sq_div_mean_x_sq(rv_min)


# In[132]:


def alpha_fun (x, k):
    # x is variable
    # k is constant from sum__x_sq_div_mean_x_sq
    return math.gamma(1 + 2/x)/(math.gamma(1 +1/x) * math.gamma(1 + 1/x)) - k
g = lambda x: alpha_fun(x, k)


# In[133]:


def beta_fun(rv, alpha):
    return np.mean(rv)/(math.gamma(1 + 1/alpha))


# In[134]:


# what the graph looks like
x = np.linspace(.3,30, 100)
y = [g(x) for x in x]
p = figure()
p.line(x,y)
#show(p)


# In[135]:


alpha_hat = bisect(g, .3, 30)
beta_hat = beta_fun(rv_min, alpha_hat)
print(alpha_hat, beta_hat)


# In[136]:


#plot
hist, edges = np.histogram(rv, density=True, bins=20)
p = figure()
p.quad(top = hist, bottom=0, left=edges[:-1], right=edges[1:], alpha = .4)


x = np.linspace(stats.weibull_min.ppf(0.01, c = alpha_hat, scale= beta_hat, loc= min(rv)),
 stats.weibull_min.ppf(0.99, c = alpha_hat, scale = beta_hat, loc=min(rv)), 100)
y =  stats.weibull_min.pdf(x, c = alpha_hat, scale = beta_hat, loc = min(rv))
p.line(x,y)
show(p)


# In[128]:


stats.weibull_min.ppf(.00001, c= alpha_hat, scale=beta_hat, loc = min(rv))


# In[127]:


np.percentile(rv, .001)


# In[ ]:




