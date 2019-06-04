from scipy import stats

def describe_data(data, pretty_print = True, roun = 0):
    def format_num(x):
        return '{:0,}'.format(round(x,roun))
    d ={}
    nobs, minmax, mean, variance, skewness, kurtosis =  stats.describe(data)
    median = np.median(data)
    q1 = np.quantile(data, .25)
    q3 = np.quantile(data, .75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    if lower < minmax[0]:
        lower = 0
    upper = q3 + 1.5 * iqr
    d['nobs'] = nobs
    d['min'] = minmax[0]
    d['max'] = minmax[1]
    d['variance'] = variance
    d['kurtosis'] = kurtosis
    d['skewness'] = skewness
    d['median'] = median

    d['upper_quantile'] = upper
    d['lower_quantile'] = lower
    if pretty_print:
        d['lower_quantile'] = format_num(d['lower_quantile'])
        d['upper_quantile'] = format_num(d['upper_quantile'])
        d['median'] = format_num(d['median'])
        d['max'] = format_num(d['max'])
    if pretty_print:
        return pp.pformat(d)
    return d

print(describe_data(per_day))
