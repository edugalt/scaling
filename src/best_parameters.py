from random import randint, random
from scipy.stats import t
from scipy import std, average, sum
from scipy import optimize
import numpy as np
from math import isnan


class ConvergenceFailed(Exception):

    def __init__(self, msg, max_failures):
        super(ConvergenceFailed, self).__init__(self, msg)
        self.max_failures = max_failures


def mls_best_fit(x, y):
    """
    least square fit of y=alpha +beta x. Should be equivalent to:

    >>> A = np.vstack([x, np.ones(len(x))]).T
    >>> m, c = np.linalg.lstsq(A, y)[0]
    """
    #http://en.wikipedia.org/wiki/Simple_linear_regression
    #http://en.wikipedia.org/wiki/Student%27s_t-distribution
    sx = std(x)
    sy = std(y)
    ax = average(x)
    ay = average(y)
    rxy = (average(x*y) - ax*ay)/np.sqrt((average(x*x) - ax*ax)*(average(y*y) - ay*ay))
    beta = rxy*sy/sx
    alpha = ay - beta*ax

    epsilon2 = (y - alpha - beta*x)**2
    xdif2 = (x - ax)**2
    sbeta = np.sqrt(np.sum(epsilon2)/(np.sum(xdif2)*(len(x) - 2)))
    tstar = t.ppf(1 - 0.05/2, len(x)-2)
    return beta, sbeta*tstar, alpha


def minimize(model, x, y, parameters=None, disp=True):
    """
    Calculates the best parameters for a model using a minimization method +
    a random search in parameter space.

    The optional argument `parameters` is a dictionary with three optional keys:
     * `required_successes`: the number of success minimizations after the first minimum
       found required to accept that minimum as correct (default: 20)
     * `max_failures`: the maximum number of failures accepted before the claiming
       that the minimization procedure failed (default: `2*required_successes`)
     * `max_iterations`: maximum number of iterations of the minimization algorithm
        (default: 500)
     * `callback`: a function of 1 parameter (with a tuple of parameters) called
       on every iteration of the minimization.

    Returns (best_parameters, best_log_likelihood), the tuple that minimizes
    the set of all `min_successes` tuples.
    """
    if parameters is None:
        parameters = {}

    required_successes = parameters.get('required_successes', 20)
    max_failures = parameters.get('max_failures', 2*required_successes)
    max_iterations = parameters.get('max_iterations', 500)
    callback = parameters.get('callback', lambda params: params)

    best_parameters = []
    best_result = float("inf")
    successes = 0
    failures = 0
    while successes < required_successes:
        # actual optimization
        x0 = model.get_random_parameters(x, y)
        result = optimize.minimize(
            fun=model.minus_log_likelihood,
            x0=x0,
            args=(x, y),
            bounds=model.bounds,
            options={'disp': disp, 'maxiter': max_iterations},
            callback=callback)
        assert(not isnan(result.fun))

        if result.success:
            if disp:
                print('Success:', result.x, result.fun)

            successes += 1

            if result.fun < best_result:  # if new minimum, store and reset.
                best_parameters = result.x
                best_result = result.fun
                successes = 0
                failures = 0
        else:
            if disp:
                print('Failed:', result.x, result.fun)

            failures += 1

            if failures > max_failures:
                raise ConvergenceFailed('Convergence of minimization failed.',
                                        max_failures)

    return best_parameters, best_result


def minimize_with_errors(model, x, y, parameters=None, samples=100, disp=True):
    """
    Returns the best fit parameters using maximum likelihood and respective errors
    using bootstrap with replacement.

    - `model`: the model; it must be an instance of `NormalModel` or subclasses.
    - `parameters`: extra parameters passed to minimize
    - `samples`: is the number of samples to estimate the error with bootstrap.

    Returns (best_parameters, parameters_errors, likelihood), where parameters_errors are
    defined as 2x the standard deviation of the bootstrapping.
    """
    best_params, likelihood = minimize(model, x, y, disp=disp, parameters=parameters)
    if disp:
        print('\n Best parameters finished: \n', best_params)

    error_estimate = 0
    for run in range(samples):
        # create the sample
        # randint(a, b) returns in closed interval [a, b], thus the len(x) - 1
        indexes = [randint(0, len(x) - 1) for _ in range(len(x))]
        sample_x = np.array([x[index] for index in indexes])
        sample_y = np.array([y[index] for index in indexes])

        # try the sample. If it fails, repeat with another sample.
        try:
            params, _ = minimize(model, sample_x, sample_y, disp=False, parameters=parameters)
            error_estimate += (best_params - params)**2
            if disp:
                print('Bootstrap run:', run+1, ' out of ', samples,'finished', params)
        except ConvergenceFailed:
            run -= 1

    if samples == 0:
        return best_params, [None for _ in best_params], likelihood
    return best_params, 2*np.sqrt(error_estimate/samples), likelihood


########### Model Gaussian error + Taylor Law ###########
# this model assumes P(y|x) to be a normal distribution with:
#   \mu(x) = \alpha*x^\beta
#   \sigma(x) = c*\mu^d


class NormalModel(object):
    """
    A class Model is used in the minimization procedure. The model has `bounds`
    that define the parameter space, has a `minus_log_likelihood` that defines
    the likelihood, and has a `get_random_parameters` that returns a random
    realization of the parameters, which defines the ensemble of initial conditions
    used in the minimize function.
    """
    def __init__(self, bounds):
        self.bounds = bounds

    @staticmethod
    def minus_log_likelihood(params, x, y):
        """
        Returns the log-likelihood evaluated at x,y with
        * \mu = \alpha*x^\beta
        * \sigma = c*\mu^d
        """
        alpha = params[0]
        beta = params[1]
        c = params[2]
        d = params[3]
        mu = alpha*np.power(x, beta)
        sigma = c*np.power(mu, d)

        try:
            minus_log = np.log(sigma*np.sqrt(2.*np.pi)) + ((y - mu)**2)/(2.*sigma**2)
        except:
            print(alpha, beta, c, d)
            print(np.min(sigma), np.max(sigma))
            print(np.min(mu), np.max(mu))
            raise
        return sum(minus_log)

    @staticmethod
    def _check_initial(value, bounds):
        """
        Sends the parameter to the correct bounds defined in the function call.
        """
        value_min = bounds[0]
        value_max = bounds[1]
        if value_max is None:
            if value_min is not None and value < value_min:
                return value_min + random()
        else:
            if value < value_min or value > value_max:
                return value_min + random()*(value_max - value_min)
        return value

    def get_random_parameters(self, x, y):
        """
        Returns a realization of the parameters given by an heuristic to
        minimize the likelihood
        """
        # Initial guesses: heuristic + check bounds
        scale = 1.0*max(1, min(y))/min(x)  # a scale for \alpha

        alpha = scale*pow(10, -1 + 2.0*random())  # [scale/10, 10*scale]
        alpha = self._check_initial(alpha, self.bounds[0])
        beta = 0.5 + 1.0*random()                 # [0.5, 1.5]
        beta = self._check_initial(beta, self.bounds[1])
        c = pow(10, -2 + 4.0*random())            # [10^-2, 10^2]
        c = self._check_initial(c, self.bounds[2])
        d = 0.5 + 1.0*random()                    # [0.5, 1.5]
        d = self._check_initial(d, self.bounds[3])

        return [alpha, beta, c, d]


########### Model Log-normal error ###########
# this model assumes P(y|x) to be a log-normal with:
#   log_exp = \log(a) + b*log_x
#   \sigma(x)^2 = \log(1 + c*exp(log_exp*(d-2)))
#   \mu(x) = log_exp - \sigma(x)^2/2
# because it guarantees that:
# - E(y) = a*x**b
# - Var(y) = c*<y>**d


class LogNormalModel(NormalModel):

    @staticmethod
    def minus_log_likelihood(params, log_x, log_y):
        a, b, c, d = params[0], params[1], params[2], params[3]

        log_mean = np.log(a) + b*log_x

        # numerically, value can be very small. If that is the case, the
        # Likelihood is practically 0
        value = c*np.exp(log_mean*(d - 2))
        if np.min(value) <= 10**-10:
            return 10**10

        sigma2 = np.log(1 + value)
        if np.min(sigma2) < 0:
            raise ValueError(value)

        mu = log_mean - 0.5*sigma2

        minus_log = log_y + 0.5*np.log(sigma2*2.*np.pi) + \
            ((log_y - mu)**2)/(2.*sigma2)
        return np.sum(minus_log)

    def get_random_parameters(self, log_x, log_y):
        """
        Returns a realization of the parameters given by an heuristic to
        minimize the likelihood.
        """
        # Initial guesses: heuristic + check bounds
        scale = 1.0*max(1, min(log_y))/min(log_x) # a scale for \alpha

        a = scale*pow(10, -1 + 2.0*random())  # [scale/10, 10*scale]
        a = self._check_initial(a, self.bounds[0])
        b = 0.5 + 1.0*random()                 # [0.5, 1.5]
        b = self._check_initial(b, self.bounds[1])
        c = 5.0*random()                        # [0, 5]
        c = self._check_initial(c, self.bounds[2])
        d = 1 + 2.0*random()                      # [1, 3]
        d = self._check_initial(d, self.bounds[3])

        return [a, b, c, d]


########### Population model ###########


class PopulationModel(NormalModel):

    @staticmethod
    def minus_log_likelihood(params, x, y):
        gamma = params[0]
        prnon = x**gamma
        p = prnon/np.sum(prnon)
        logL = y*np.log(p)
        return -np.sum(logL)

    def get_random_parameters(self, x, y):
        gamma = self.bounds[0][0] + (self.bounds[0][1] - self.bounds[0][0])*random()
        return [gamma]
