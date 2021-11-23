# Overview

This repository contains both data and code from the papers:

- Spatial Interctions in urban scaling laws, by Eduardo G. Altmann, [PLOS ONE 15, e0243390 (2020)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390]).

- Is this scaling non-linear? by
Jorge C. Leitão, José M. Miotto, Martin Gerlach, and Eduardo G. Altmann, [
Royal Society Open Science 3, 150649 (2016)](http://rsos.royalsocietypublishing.org/content/3/7/150649)

and also results for COVID-19 data performed by [Jimena Espinoza](https://github.com/jimenaspi)

## Notebook and Examples

The usage is illustrated in jupyter notebooks in the folder ./notebook/

- Notebook-FittingModels.ipynb shows how to perform different fittings as dicussed in the 2016 paper.

- Notebook-SpatialModels.ipynb shows how to analyze the spatial models discussed in the 2020 paper.

- Notebook-covid19_results.ipynb shows the results for COVID-19 data from 2021.

## Data

The data consists of Python packages (e.g. `brazil`). Each package has functions
that return the data there, defined in the `__init__.py` of the package.
The data is always a tuple (x, y) of numpy arrays of the same size, where x is always population.

For example, to get the population-gdp of brazilian cities from 2010 use:

    import brazil
    x, y = brazil.gdp(2010)

## Installation

Copy the files to a directory and install the dependencies (numpy, scipy, matplotlib), e.g. running 

    pip install -r requirements.txt

## Further information on the 2020 paper (Spatial models):

To analyse a new dataset:

- Start from Notebook-SpatialModels.ipynb
- Import your resuts as x (population), y (observable), l (latitude and longitude of city)
- Choose the model of interest and run the notebook

## Further information on the 2016 paper (Fitting scaling laws):

### Data
New data can be added as .csv file to the files

new_dataset/generic_dataset.txt	   (for three columns: city name, population, observable)

or

new_dataset2/generic_dataset.txt	(for two columsn: population,observable)


### Likelihood and minimisation

The module `best_parameters.py` contains the definition of the likelihood functions of each model,
the minimization algorithm and the parameters we use in it.

The bootstrap used to estimate error bars is also defined in this module, at `minimize_with_errors`.
The bootstrap for the person model is implemented in `pvalue_population.py`. 

### Analysis

The different analysis we perform, as well as the list of databases we use, are defined in `analysis.py`.
The general setting is defined in `LikelihoodAnalysis` and respective methods.

For example, to get beta estimated by Log-Normal with free \delta and other statistical information, use

    from analysis import LogNormalAnalysis
    >>> analysis = LogNormalAnalysis('brazil_aids_2010', required_successes=512)
    >>> analysis.beta[0]
    >>> analysis.p_value
    >>> analysis.bic
 
These results are pre-computed and stored in a JSON file at `_results`.

### Running an analysis for your data

In case you want to run your model against a new dataset, copy paste the dataset to 
`new_dataset/generic_dataset.txt` as a list of the form `id,x,y` or
'new_dataset2/generic_dataset.txt' as a list of the form 'x,y'.

You can run the Notebook in Jupyter (Ipython3) or 
run `python -m analyze.py`. For example,

    MODEL=LogNormalAnalysis ERROR_SAMPLES=10 python -m analyze

runs the `LogNormal` model with 10 samples for bootstrap on the new dataset. 
It prints the best \beta, the bootstrap error for beta, p_value, and BIC for the specific model 
(the script explains how to select the model). Check the file `analyze.py` for more details.

### Reproduce the results in the paper

### Compute the numerical data

In case you want to reproduce some of the results stored in `_results`, you can delete the respective 
analysis in the directory and run (may take some time)

    python -m analysis_run

this requires some environment variables that are documented when you run it.

