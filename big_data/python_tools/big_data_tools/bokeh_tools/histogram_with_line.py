import numpy as np
mu = 0
sigma = .5
pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
print(pdf)

