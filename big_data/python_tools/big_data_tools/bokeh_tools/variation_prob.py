import numpy as np

size = 1000
l1 = np.random.normal(loc = 520, scale = 10, size = size)
l2 = np.random.normal(loc = 520, scale = 10, size = size)
print('var of same list is {var}'.format
        (var = np.var(l1 + l1)))
cov5 = np.cov(l1, l1)[1, 0]
print('cov of same list is {cov} '.format(
    cov = np.cov(l1, l1)[1,0]
    ))
print('variation of single list is {var}'.format(
    var = np.var(l1)
    ))
print('var + var + 2cov = {the_sum}'.format(
    the_sum = np.var(l1) + np.var(l1) + 2 * np.cov(l1, l1)[1,0])
    )
