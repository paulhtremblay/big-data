import numpy as np

def manual_point_est(l):
    mean = np.mean(l)
    print(mean)
    s = 0
    mean_squared = 0
    for i in l:
        s += (mean - i) * (mean - i) 
        mean_squared += i * i * 1/len(l)
    s2 = mean_squared - mean * mean
    print(s2)
    return s * 1/len(l)


def point_est(l):
    v = np.var(l)
    v2 = manual_point_est(l)
    print(v)
    print(v2)

if __name__ == '__main__':
    point_est([1, 2, 3])
