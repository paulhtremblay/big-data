import math
from scipy.stats import probplot
import scipy.stats
import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def make_lognormal():
    pd_series = np.random.lognormal(mean=0.0, sigma=1.0, size=1000)
    series1 = probplot(pd_series, dist="lognorm", sparams= (1,))
    p = figure(title="Log Normal QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p.scatter(series1[0][0],series1[0][1], fill_color="red")
    p.line(x,y2, line_width =2)
    return p

def generic(data, dist, sparams = None, title= None):
    if not title:
        title = "{dist} QQ Plot".format(dist = dist)
    series = probplot(data, dist=dist, sparams= sparams)
    p = figure(title=title)
    x = series[0][0]
    y = series[0][1]
    slope = series[1][0]
    intercept = series[1][1]
    y2 = [z * slope + intercept for z in x]
    p.scatter(series[0][0],series[0][1], fill_color="red")
    p.line(x,y2, line_width =2)
    return p

def make_weibull():
    a = .5
    pd_series = np.random.weibull(a = a, size = 1000)
    series1 = probplot(pd_series, dist="weibull_min", sparams= (a,))
    p1 = figure(title="Weibull QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p1.scatter(series1[0][0],series1[0][1], fill_color="red")
    p1.line(x,y2, line_width =2)
    return p1

def make_normal():
    pd_series = np.random.normal(size = 100)
    series1 = probplot(pd_series, dist="norm")
    p1 = figure(title="Normal QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p1.scatter(series1[0][0],series1[0][1], fill_color="red")
    p1.line(x,y2, line_width =2)
    return p1


def make_exp():
    pd_series = np.random.exponential(size = 100)
    series1 = probplot(pd_series, dist=scipy.stats.expon)
    p1 = figure(title="Exponential QQ-Plot", background_fill_color="#E8DDCB")
    x = series1[0][0]
    y = series1[0][1]
    slope = series1[1][0]
    intercept = series1[1][1]
    y2 = [z * slope + intercept for z in x]
    p1.scatter(series1[0][0],series1[0][1], fill_color="red")
    p1.line(x,y2, line_width =2)
    return p1

def main():
    p_weibul = make_weibull()
    p_normal =  make_normal()
    p_expon = make_exp()
    p_lognormal = make_lognormal()
    data = np.random.weibull(a = .5, size = 1000)
    p_generic = generic(data = data, dist = "weibull_min", sparams = .5,)
    data2 = np.random.normal(size = 100)
    p_generic_norm = generic(data = data2, dist = "norm")
    grid = gridplot([p_normal, p_expon, p_weibul, 
        p_lognormal, p_generic, p_generic_norm], ncols = 2, height=500, 
            width = 500)
    show(grid)

if __name__ == '__main__':
    main()
    """
    ['__all__', '__builtins__', '__cached__', 
    '__doc__'
 '__file__'
 '__loader__'
 '__name__'
 '__package__'
 '__spec__'
 '_continuous_distns'
 '_discrete_distns'
 'absolute_import'
 'alpha'
 'alpha_gen'
 'anglit'
 'anglit_gen'
 'arcsine'
 'arcsine_gen'
 'argus'
 'argus_gen'
 'bernoulli'
 'bernoulli_gen'
 'beta'
 'beta_gen'
 'betaprime'
 'betaprime_gen'
 'binom'
 'binom_gen'
 'boltzmann'
 'boltzmann_gen'
 'bradford'
 'bradford_gen'
 'burr'
 'burr12'
 'burr12_gen'
 'burr_gen'
 'cauchy'
 'cauchy_gen'
 'chi'
 'chi2'
 'chi2_gen'
 'chi_gen'
 'cosine'
 'cosine_gen'
 'crystalball'
 'crystalball_gen'
 'dgamma'
 'dgamma_gen'
 'division'
 'dlaplace'
 'dlaplace_gen'
 'dweibull'
 'dweibull_gen'
 'entropy'
 'erlang'
 'erlang_gen'
 'expon'
 'expon_gen'
 'exponnorm'
 'exponnorm_gen'
 'exponpow'
 'exponpow_gen'
 'exponweib'
 'exponweib_gen'
 'f'
 'f_gen'
 'fatiguelife'
 'fatiguelife_gen'
 'fisk'
 'fisk_gen'
 'foldcauchy'
 'foldcauchy_gen'
 'foldnorm'
 'foldnorm_gen'
 'frechet_l'
 'frechet_l_gen'
 'frechet_r'
 'frechet_r_gen'
 'gamma'
 'gamma_gen'
 'gausshyper'
 'gausshyper_gen'
 'genexpon'
 'genexpon_gen'
 'genextreme'
 'genextreme_gen'
 'gengamma'
 'gengamma_gen'
 'genhalflogistic'
 'genhalflogistic_gen'
 'genlogistic'
 'genlogistic_gen'
 'gennorm'
 'gennorm_gen'
 'genpareto'
 'genpareto_gen'
 'geom'
 'geom_gen'
 'gilbrat'
 'gilbrat_gen'
 'gompertz'
 'gompertz_gen'
 'gumbel_l'
 'gumbel_l_gen'
 'gumbel_r'
 'gumbel_r_gen'
 'halfcauchy'
 'halfcauchy_gen'
 'halfgennorm'
 'halfgennorm_gen'
 'halflogistic'
 'halflogistic_gen'
 'halfnorm'
 'halfnorm_gen'
 'hypergeom'
 'hypergeom_gen'
 'hypsecant'
 'hypsecant_gen'
 'invgamma'
 'invgamma_gen'
 'invgauss'
 'invgauss_gen'
 'invweibull'
 'invweibull_gen'
 'johnsonsb'
 'johnsonsb_gen'
 'johnsonsu'
 'johnsonsu_gen'
 'kappa3'
 'kappa3_gen'
 'kappa4'
 'kappa4_gen'
 'ksone'
 'ksone_gen'
 'kstwobign'
 'kstwobign_gen'
 'laplace'
 'laplace_gen'
 'levy'
 'levy_gen'
 'levy_l'
 'levy_l_gen'
 'levy_stable'
 'levy_stable_gen'
 'loggamma'
 'loggamma_gen'
 'logistic'
 'logistic_gen'
 'loglaplace'
 'loglaplace_gen'
 'lognorm'
 'lognorm_gen'
 'logser'
 'logser_gen'
 'lomax'
 'lomax_gen'
 'maxwell'
 'maxwell_gen'
 'mielke'
 'mielke_gen'
 'moyal'
 'moyal_gen'
 'nakagami'
 'nakagami_gen'
 'nbinom'
 'nbinom_gen'
 'ncf'
 'ncf_gen'
 'nct'
 'nct_gen'
 'ncx2'
 'ncx2_gen'
 'norm'
 'norm_gen'
 'norminvgauss'
 'norminvgauss_gen'
 'pareto'
 'pareto_gen'
 'pearson3'
 'pearson3_gen'
 'planck'
 'planck_gen'
 'poisson'
 'poisson_gen'
 'powerlaw'
 'powerlaw_gen'
 'powerlognorm'
 'powerlognorm_gen'
 'powernorm'
 'powernorm_gen'
 'print_function'
 'randint'
 'randint_gen'
 'rayleigh'
 'rayleigh_gen'
 'rdist'
 'rdist_gen'
 'recipinvgauss'
 'recipinvgauss_gen'
 'reciprocal'
 'reciprocal_gen'
 'rice'
 'rice_gen'
 'rv_continuous'
 'rv_discrete'
 'rv_frozen'
 'rv_histogram'
 'semicircular'
 'semicircular_gen'
 'skellam'
 'skellam_gen'
 'skew_norm_gen'
 'skewnorm'
 't'
 't_gen'
 'trapz'
 'trapz_gen'
 'triang'
 'triang_gen'
 'truncexpon'
 'truncexpon_gen'
 'truncnorm'
 'truncnorm_gen'
 'tukeylambda'
 'tukeylambda_gen'
 'uniform'
 'uniform_gen'
 'vonmises'
 'vonmises_gen'
 'vonmises_line'
 'wald'
 'wald_gen'
 'weibull_max'
 'weibull_max_gen'
 'weibull_min'
 'weibull_min_gen'
 'wrapcauchy'
 'wrapcauchy_gen'
 'zipf'
 'zipf_gen']
    """
