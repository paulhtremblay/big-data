from numpy import array
from numpy import mean
import numpy as np
M = array([[1,2,3,4,5,6],[1,2,3,4,5,6]])
#print(M)
col_mean = mean(M, axis=0)
print(col_mean)
row_mean = mean(M, axis=1)
print(row_mean)
all_mean = mean(M)
print(all_mean)
l = [1, 2, 3]
p = [.2, .3,  .5]
e = 0
for count, i in enumerate(l):
    e += i * p[count]
print(e)
e = np.average(l, weights = p)
print(e)
