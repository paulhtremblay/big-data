import random

def resample(l):
    final = []
    for i in range(len(l)):
        final.append(random.choice(l))
    return final

def repeat_resample(sample_a, sample_b, num_iter = 1000):
    difference_in_means = []
    for i in range(num_iter):
        resample_a = resample(sample_a)
        resample_b = resample(sample_b)
        difference = np.mean(resample_a) - np.mean(resample_b)
        difference_in_means.append(difference)
    return difference_in_means
