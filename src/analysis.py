"""
This module collects the different analysis and different databases we have so far
and computes all the combinations.

DATABASES is a dictionary that the databases. You can add new databases to
this dictionary (see existing examples)

The class `MLSAnalysis` and subclasses compute and store the minimum least square.
The class `LikelihoodAnalysis` and subclasses compute and store the Likelihood analysis.

Examples:

>>> result = FixedDAnalysis('brazil_aids_2010')
>>> print(result.beta)  # (value, error)
>>> print(result.p_value) # the p-value of the model.
>>> result = FixedDAnalysis('brazil_aids_2010')
>>> print(result.beta)  # (value, error) with d = 0.5 fixed.

Since the analysis of the likelihood are taking a lot of time, we are storing
the result in a file so we retrieve it if it already exists. Erase `_data` to force
a new calculation (e.g. if the analysis/database changes).

The objective is to have the analysis ready to add to a table of databases.
"""
import numpy as np
import scipy.stats
import scipy.stats.mstats

from brazil.data import cache
import brazil, eurostat, usa, oecd, uk, new_dataset, new_dataset2, covid19, australia, germany
from best_parameters import mls_best_fit, minimize_with_errors, \
    NormalModel, LogNormalModel, PopulationModel
from pvalue_population import pvalue_pop


MIN_VALUE = 10**-8
            

def sort_data(x, y):
    """
    Sorts the data by increasing x while keeping the respective y.
    """
    idx = x.argsort()
    return x[idx], y[idx]


def remove_zero_y(x, y):
    """
    Removes entries of both x,y where y <= 0.
    """
    x = list(x)
    y = list(y)
    idx = []
    for i, y_i in enumerate(y[:]):
        if y_i <= 0:
            idx.append(i)
    for i in reversed(idx):
        del x[i]
        del y[i]
    return np.array(x), np.array(y)


# lambda's so we don't load all databases to the dictionary.
# Use `DATABASES['...']()` to load it, returning the tuple (x, y).
DATABASES = {'brazil_aids_2010': lambda: remove_zero_y(*sort_data(*brazil.aids(2010))),
             'brazil_gdp_2010': lambda: remove_zero_y(*sort_data(*brazil.gdp(2010))),
             'brazil_externalCauses_2010': lambda: remove_zero_y(*sort_data(*brazil.externalCauses(2010))),
             'oecd_gdp': lambda: remove_zero_y(*sort_data(*oecd.gdp())),
             'oecd_patents': lambda: remove_zero_y(*sort_data(*oecd.patents())),
             'usa_gdp': lambda: remove_zero_y(*sort_data(*usa.gdp())),
             'usa_miles': lambda: remove_zero_y(*sort_data(*usa.miles())),
             'eurostat_cinema_seats': lambda: remove_zero_y(*sort_data(*eurostat.cinemaSeats())),
             'eurostat_cinema_attendance': lambda: remove_zero_y(*sort_data(*eurostat.cinemaAttendance())),
             'eurostat_museum_visitors': lambda: remove_zero_y(*sort_data(*eurostat.museumVisitors())),
             'eurostat_theaters': lambda: remove_zero_y(*sort_data(*eurostat.theaters())),
             'eurostat_libraries': lambda: remove_zero_y(*sort_data(*eurostat.libraries())),
             'uk_patents': lambda: remove_zero_y(*sort_data(*uk.row('Patents'))),
             'uk_income': lambda: remove_zero_y(*sort_data(*uk.row('Income'))),
             'uk_train': lambda: remove_zero_y(*sort_data(*uk.row('Train'))),
             'new_dataset': lambda: remove_zero_y(*sort_data(*new_dataset.index())),
             'new_dataset2': lambda: remove_zero_y(*sort_data(*new_dataset2.index())),
             'covid19_USA': lambda: remove_zero_y(*sort_data(*covid19.covid19_USA())),
             'covid19_NSW': lambda: remove_zero_y(*sort_data(*covid19.covid19_NSW())),
             'covid19_chile': lambda: remove_zero_y(*sort_data(*covid19.covid19_chile())),
             'covid19_brazil': lambda: remove_zero_y(*sort_data(*covid19.covid19_brazil())),
             'australia_area':lambda: remove_zero_y(*sort_data(*australia.area())),
             'australia_income':lambda: remove_zero_y(*sort_data(*australia.income())),
             'australia_education':lambda: remove_zero_y(*sort_data(*australia.education())),
             'germany_gdp':lambda: remove_zero_y(*sort_data(*germany.gdp())),
             }

class Analysis(object):
    """
    A general class that holds data and statistics of it.
    """
    def __init__(self, dataset):
        self.dataset = dataset
        self.x, self.y = DATABASES[dataset]()

    def __str__(self):
        return self.__class__.__name__

class xy(Analysis):
    def __init__(self,dataset):
        self.x, self.y = DATABASES[dataset]()
    

class MLSAnalysis(Analysis):
    """
    A MLS where we use all the data
    """
    def __init__(self, dataset, cut=0):
        super(MLSAnalysis, self).__init__(dataset)
        self.cut = cut
        beta, self.error, c = mls_best_fit(np.log(self.x[cut:]), np.log(self.y[cut:]))
        self.params = [beta, c]

    @property
    def beta(self):
        return self.params[0], self.error


class MLSMedianAnalysis(MLSAnalysis):
    """
    A MLS where we only use the upper half (above median) of the data.
    """
    def __init__(self, dataset):
        x, _ = DATABASES[dataset]()
        super(MLSMedianAnalysis, self).__init__(dataset, int(len(x)/2.0))


class LikelihoodAnalysis(Analysis):
    """
    Contains all information of a likelihood analysis using Taylor's law.

    set the data using `x, y`; define the model using `bounds`.

    It computes `params`, `errors` and `likelihood_ratio`.
    """
    Model = NormalModel
    samples = 100

    def __init__(self, dataset, bounds, required_successes=16):
        super(LikelihoodAnalysis, self).__init__(dataset)
        self.bounds = bounds
        self._required_successes = required_successes
        result = self._mle_calculation(self._cache_name)

        self.params = np.array(result['params'])
        self.errors = np.array(result['errors'])
        self.minus_log_likelihood = result['-log_likelihood']

        self.p_value = self._p_value_calculation(self._cache_name)['p_value']

    @property
    def _cache_name(self):
        return '%s_%s_%d_%d' % (self, self.dataset, self._required_successes, self.samples)

    def _p_value_calculation(self, cache_file):
        """
        Computes the p-value of the null hypotheses that the data was generated by the model.
        Our model assumes that:

        1. P(y|x) is normally distributed with mu(x) and sigma(x) which implies
        that z = (y - mu(x))/sigma(x) are normally distributed.
        We use the D'Agostino and Pearson K^2 test to test this assumption.

        2. z = (y - mu(x))/sigma(x) are uncorrelated. We use the spearman's correlation
        test to test this assumption.

        Since the statistics used in the tests are uncorrelated, we extend the
        K^2 test by combining the three statistics.

        p < \alpha implies that the null hypothesis is rejected.
        """

        # this ignore should not be here, but a bug in numpy forces it to be
        # See https://github.com/numpy/numpy/issues/4895
        with np.errstate(under='ignore'):
            # Combine the D'Agostino normality K^2 test (s, k) with
            # the spearman's correlation test (sr).

            # copy of scipy.stats.mstats.normaltest
            s, _ = scipy.stats.mstats.skewtest(self.z_scores)
            k, _ = scipy.stats.mstats.kurtosistest(self.z_scores)

            # compute statistic that is normally distributed, see
            # https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient
            rs, _ = scipy.stats.spearmanr(self.x, self.z_scores)
            sr = np.sqrt((len(self.z_scores) - 3) / 1.06) * np.arctan(rs)

            # merge the 3 statistics and compute its probability
            k3 = s*s + k*k + sr*sr

            return {'p_value': scipy.stats.distributions.chi2.sf(k3, 3)}

    @cache('_results/mle_{1}.json')
    def _mle_calculation(self, cache_file):
        """
        This computes:
            1. the best parameters using Max. likelihood,
            2. the -log_likelihood obtained,
            3. the respective error bars using bootstrap.

        It stores the result in a json so we only have to run this once every
        code change.
        """
        model = self.Model(self.bounds)

        params, errors, minus_log_likelihood = minimize_with_errors(
            model, self.x, self.y, samples=self.samples,
            parameters={'required_successes': self._required_successes},
            disp=False)

        return {'params': list(params), 'errors': list(errors),
                '-log_likelihood': minus_log_likelihood}

    @property
    def z_scores(self):
        """
        The z-scores of the normal variable
        """
        return (self.y - self.mean)/self.std

    @property
    def beta(self):
        """
        The scaling exponent of y with x and respective error estimate
        via bootstrap.
        """
        return self.params[1], self.errors[1]

    @property
    def delta(self):
        # in this model the delta is of sigma, not of var
        return 2*self.params[3]

    @property
    def mean(self):
        """
        The mean of y.
        """
        a, b, _, _ = tuple(self.params)
        return a*np.power(self.x, b)

    @property
    def std(self):
        """
        The std of y.
        """
        _, _, c, d = tuple(self.params)
        return c*np.power(self.mean, d)

    @property
    def n_parameters(self):
        """
        Number of free parameters.
        """
        return sum([bounds[0] != bounds[1] or
                    bounds[0] is None or
                    bounds[1] is None
                    for bounds in self.bounds])

    @property
    def data_size(self):
        return len(self.x)

    @property
    def bic(self):
        # Bayesian information criterion, see e.g.
        # https://en.wikipedia.org/wiki/Bayesian_information_criterion
        return 2*self.minus_log_likelihood + self.n_parameters*np.log(self.data_size)

    def model_error_bars(self, sigmas=1):
        """
        The errors bars computed from the model.
        """
        return [sigmas*self.std, sigmas*self.std]

# The analysis
# Each analysis has the counter-part with fixed \beta=1.


class FixedDAnalysis(LikelihoodAnalysis):
    description = r'Gaussian fluctuations with \delta = 0.5'
    def __init__(self, dataset, required_successes=16):
        super(FixedDAnalysis, self).__init__(dataset,
                                             ([MIN_VALUE, None], [0.01, 3],
                                              [MIN_VALUE, None], [0.5, 0.5]),
                                             required_successes)


class FixedDFixedBetaAnalysis(LikelihoodAnalysis):
    description = r'Gaussian fluctuations with \beta = 1 and \delta = 0.5'
    def __init__(self, dataset, required_successes=16):
        super(FixedDFixedBetaAnalysis, self).__init__(
            dataset, ([MIN_VALUE, None], [1, 1], [MIN_VALUE, None], [0.5, 0.5]),
            required_successes)


class ConstrainedDAnalysis(LikelihoodAnalysis):
    description = r'Gaussian fluctuations with free \delta'
    def __init__(self, dataset, required_successes=16):
        super(ConstrainedDAnalysis, self).__init__(dataset,
                                                   ([MIN_VALUE, None], [0.01, 3],
                                                    [MIN_VALUE, None], [0.5, 1.0]),
                                                   required_successes)


class ConstrainedDFixedBetaAnalysis(LikelihoodAnalysis):
    description = r'Gaussian fluctuations with \beta = 1 and free \delta'
    def __init__(self, dataset, required_successes=16):
        super(ConstrainedDFixedBetaAnalysis, self).__init__(
            dataset, ([MIN_VALUE, None], [1, 1], [MIN_VALUE, None], [0.5, 1.0]),
            required_successes)


class PopulationAnalysis(LikelihoodAnalysis):
    """
    Analysis of the population model.
    """
    Model = PopulationModel
    description = r'People model with free \delta'

    def __init__(self, dataset, required_successes):
        # ([0.01, 3],) is the same as we use for beta.
        super(PopulationAnalysis, self).__init__(dataset, ([0.01, 3],), required_successes)

    @cache('_results/pvalue_{1}.json')
    def _p_value_calculation(self, cache_file):
        return {'p_value': pvalue_pop(self.x, self.y, self.params, ([0.01, 3],))}

    @property
    def beta(self):
        return self.params[0], self.errors[0]

    @property
    def bic(self):
        # Bayesian information criterion, see e.g.
        # https://en.wikipedia.org/wiki/Bayesian_information_criterion
        y = self.y
        Y = np.sum(y)

        lnY_factorial = Y*np.log(Y) - Y
        sum_lny_factorial = np.sum(y*np.log(y) - y)

        return super(PopulationAnalysis, self).bic + \
               2*(lnY_factorial - sum_lny_factorial)

    @property
    def delta(self):
        return 1

    @property
    def data_size(self):
        return np.sum(self.y)

    @property
    def mean(self):
        """
        The mean of this model is y*p_i, where y is the total number of tokens.
        """
        prnon = self.x**self.params[0]
        p = prnon/np.sum(prnon)
        y = np.sum(self.y)
        return y*p

    @property
    def std(self):
        prnon = self.x**self.params[0]
        p = prnon/np.sum(prnon)
        y = np.sum(self.y)
        return np.sqrt(y*p*(1-p))


class PopulationFixedGammaAnalysis(PopulationAnalysis):
    description = r'People model with \delta = 1'
    def __init__(self, dataset, required_successes):
        # ([0.01, 3],) is the same as we use for beta.
        super(PopulationAnalysis, self).__init__(dataset, ([1, 1],), required_successes)



        
class LogNormalAnalysis(LikelihoodAnalysis):
    description = r'Log normal fluctuations with a general \delta'
    Model = LogNormalModel

    def __init__(self, dataset, bounds=([MIN_VALUE, None],
                                        [0.01, 3],
                                        [MIN_VALUE, None],
                                        [1, 3]),
                 required_successes=16):
        super(LikelihoodAnalysis, self).__init__(dataset)
        self.x = np.log(self.x)
        self.y = np.log(self.y)
        self.bounds = bounds
        self._required_successes = required_successes

        result = self._mle_calculation(self._cache_name)

        self.params = np.array(result['params'])
        self.errors = np.array(result['errors'])
        self.minus_log_likelihood = result['-log_likelihood']

        self.p_value = self._p_value_calculation(self._cache_name)['p_value']

    @property
    def mean_log(self):
        """
        Median of y.
        """
        a, b, _, _ = tuple(self.params)
        return np.log(a) + b*self.x - self.var_log/2

    @property
    def var_log(self):
        """
        Variance of log_y.
        """
        _, _, c, d = tuple(self.params)
        return np.log(1 + c * np.power(self.mean, (d - 2)))

    @property
    def z_scores(self):
        """
        The z-scores of the normal variable, log_y
        """
        return (self.y - self.mean_log)/self.var_log

    @property
    def mean(self):
        a, b, _, _ = tuple(self.params)
        x = np.exp(self.x)  # self.x is log_x, see __init__.
        return a*np.power(x, b)

    @property
    def std(self):
        _, _, c, d = tuple(self.params)
        x = np.exp(self.x)  # self.x is log_x, see __init__.
        return np.sqrt(c*np.power(x, d))

    @property
    def beta(self):
        _, b, _, _ = tuple(self.params)
        _, Sb, _, _ = tuple(self.errors)
        return b, Sb

    @property
    def delta(self):
        return self.params[3]

    def model_error_bars(self, sigmas=1):
        return [self.mean - np.exp(self.mean_log - sigmas*np.sqrt(self.var_log)),
                np.exp(self.mean_log + sigmas*np.sqrt(self.var_log)) - self.mean]


class LogNormalFixedBetaAnalysis(LogNormalAnalysis):
    description = r'Log normal fluctuations with \beta = 1'
    def __init__(self, dataset, required_successes=16):
        super(LogNormalFixedBetaAnalysis, self).__init__(
            dataset, ([MIN_VALUE, None], [1, 1], [MIN_VALUE, None], [1, 3]),
            required_successes)


class LogNormalFixedDAnalysis(LogNormalAnalysis):
    description = r'Log normal fluctuations with \delta = 1'
    def __init__(self, dataset, required_successes=16):
        super(LogNormalFixedDAnalysis, self).__init__(
            dataset, ([MIN_VALUE, None], [0.01, 3], [MIN_VALUE, None], [2, 2]),
            required_successes)


class LogNormalFixedDFixedBetaAnalysis(LogNormalAnalysis):
    description = r'Log normal fluctuations with \beta = \delta = 1'
    def __init__(self, dataset, required_successes=16):
        super(LogNormalFixedDFixedBetaAnalysis, self).__init__(
            dataset, ([MIN_VALUE, None], [1, 1], [MIN_VALUE, None], [2, 2]),
            required_successes)


MODELS = dict((x.__name__, x) for x in [
    ConstrainedDAnalysis, ConstrainedDFixedBetaAnalysis,
    FixedDAnalysis, FixedDFixedBetaAnalysis,
    LogNormalAnalysis, LogNormalFixedBetaAnalysis,
    LogNormalFixedDAnalysis, LogNormalFixedDFixedBetaAnalysis,
    PopulationAnalysis, PopulationFixedGammaAnalysis
])


MODEL_TO_MODEL = {'FixedDAnalysis': 'FixedDFixedBetaAnalysis',
                  'ConstrainedDAnalysis': 'ConstrainedDFixedBetaAnalysis',
                  'LogNormalAnalysis': 'LogNormalFixedBetaAnalysis',
                  'LogNormalFixedDAnalysis': 'LogNormalFixedDFixedBetaAnalysis',
                  'PopulationAnalysis': 'PopulationFixedGammaAnalysis'}


FREE_MODEL_TO_FIXED_MODEL = {
    'ConstrainedDAnalysis': 'FixedDAnalysis',
    'LogNormalAnalysis': 'LogNormalFixedDAnalysis',
}

FIXED_MODEL_TO_FREE_MODEL = {
    'FixedDAnalysis': 'ConstrainedDAnalysis',
    'LogNormalFixedDAnalysis': 'LogNormalAnalysis',
}
