import numpy as np
from best_parameters import minimize, PopulationModel


# best_fit = population_likelihood_best_fit


def chi2(y0, y1):
    return np.sum(np.power(y0 - y1, 2.0) / y1)


def chi2_gamma(x, y, gamma):
    y1 = np.power(x, gamma) / np.sum(np.power(x, gamma)) * np.sum(y)
    return chi2(y, y1)


def sample_pop_model(fx, n):
    sample = np.random.multinomial(n, fx)
    return sample


def pvalue_pop(x, y, params, bounds, samples=200):
    gamma0 = params[0]
    chi20 = chi2_gamma(x, y, gamma0)
    n = int(np.sum(y))  # number of tokens
    chi2s, gammas = [], []
    fx = np.power(x, gamma0)
    fx = fx / np.sum(fx)

    model = PopulationModel(bounds)

    for i in range(samples):
        sample = sample_pop_model(fx, n)
        gamma = minimize(model, x, sample, disp=False)
        gammas.append(gamma[0][0])
        chi21 = chi2_gamma(x, sample, gamma[0][0])
        chi2s.append(chi21)
    chi2s = np.array(chi2s)
    mask = (chi2s > chi20)
    p_value = len(chi2s[mask]) / float(len(chi2s))
    return p_value
