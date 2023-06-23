# An inferential approach to Urban Scaling Laws

This repository contains data and the Python implementation of probabilistic models to investigate <i> Urban scaling laws</i> [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649)[[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390). These statistical laws state that many observables $y_i$ (e.g., GDP) of $i=1, 2, \ldots, N$ urban areas in a country (or region) scale with the population $x_i$ as

$$ y_i \sim x_i^{\beta},$$

with $0<\beta<2$. The primary interest is to compare different models, test the validity of the urban scaling law, and estimate the scaling paramter $\beta$.


## Models

For the application of models based on cities (C), see Ref. [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649)  and the [Jupyter Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels.ipynb) (or [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels-Colab.ipynb)).

For the application of models based on the attribution of tokens to individuals (I), which account also for the spatial interaction between urban areas, see Ref. [[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390)|the [Jupyter Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-SpatialModels.ipynb)  (or [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-SpatialModels-Colab.ipynb)).


|Model |  Parameters | Spatial interaction (Y/N)? | Cities(C) or Individuals(I) |Formula| Description/Reference|
|-|-|-|-|-|-|
|Per-capita |$\emptyset$ | N| C,I |  $y_i = x_i \frac{\sum y_i}{\sum x_i}$ | Fixed per-capita rate $\beta=1$ [[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390)|
|Least-square|$\beta,A$ |N| C | $\log(y) = A +\beta \log(x)$ | Least-squared fitting of log-transformed variables [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649) |
|Gaussian| $\beta,\alpha,\gamma,\delta$| N | C | $\mathbb{E}(y\mid x) = \alpha x^{\beta}, \mathbb{V}(y\mid x) = \gamma \mathbb{E}(y\mid x)^{\delta}$   |  Gaussian $P(y\mid x)$ [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649)|
|Log-normal |$\beta,\alpha,\gamma,\delta$| N | C| $\mathbb{E}(y\mid x) = \alpha x^{\beta}, \mathbb{V}(y\mid x) = \gamma \mathbb{E}(y\mid x)^{\delta}$ | Log-normal $P(y\mid x)$ [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649)|
|Persons |$\beta$ | N | I |  $p(j) \sim x_{c(j)}^{\beta-1}$  | Tokens are attributed to individuals with probability $p(j)$ [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649)[[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390)|
|Gravitational|$\beta,\alpha_G$ | Y | I |$a_G = \frac{1}{1+ \left(\frac{d}{\alpha_G}\right)^2}$| Tokens to individuals with prob. $p(j)$, who interact according to $a_G$ depending on distance $d$ [[1]](https://royalsocietypublishing.org/doi/10.1098/rsos.150649) [[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390)|
|Exponential|$\beta,\alpha_E$ |Y|I | $a_E = e^{- d \ln(2) / \alpha_E}$|Tokens to individuals with prob. $p(j)$, who interact according to $a_E$ depending on distance $d$ [[2]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390)|


## Data

The datasets listed below are available for investigation. The column "tag" indicates the key to be used to call this data in our code (e.g., in the [notebook](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels-Colab.ipynb)). The column "Location?" indicates whether the latitude and logitude is available (Y/N). An example of the analysis of COVID19 cases can be found [here](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-covid19_results.ipynb).

| Region: | Tag: | N	| Location? | Year | Description| Source |
| --------|------|------------------------|--------------------| -------| ------|------|
|Australia ||||||
|| covid19_NSW |	144 | N | 2021 | COVID19 cases in the state of NSW |[NSW](https://data.nsw.gov.au/data/dataset/covid-19-cases-by-location/resource/21304414-1ff1-4243-a5d2-f52778048b29) |
|| australia_area | 102 | Y | 2021 | Area | [Australian Bureau of Statistics](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files) |
|| australia_education | 102 | Y | 2021 | Top bracket in Eduction | [Census, Australian Bureau of Statistics](https://tablebuilder.abs.gov.au/)|
|| australia_income | 102 | Y | 2021 | Top bracket in Income | [Census, Australian Bureau of Statistics](https://tablebuilder.abs.gov.au/)|
|Brazil | 				
| | brazil_aids_2010 | 1812	| Y |	2010 | AIDS cases | Brazilian Health Ministry |
||	brazil_externalCauses_2010 | 5286 |	Y	| 2010|Death by external causes| Brazilian Health Ministry |
||	brazil_gdp_2010	| 5565 |	Y |	2010|GDP| Brazilian Health Ministry |
||	covid19_brazil	|5570	|N	|2021|COVID19 cases|[Brasil.io](https://brasil.io/dataset/covid19/files/) and [wcota](https://github.com/wcota/covid19br/blob/master/cases-brazil-cities.csv)|
|Chile|				
||	covid19_chile	|346|	N|	2021| COVID19 cases|[MinCiencia](https://github.com/MinCiencia/Datos-COVID19)|
|Europe|
||	eurostat_cinema_seats	| 418	|N	|2011|Cinema seats |[Eurostat](https://ec.europa.eu/eurostat/web/cities/data/database)|
||	eurostat_cinema_attendance	|221|	N| 2011|Attendance to cinemas|[Eurostat](https://ec.europa.eu/eurostat/web/cities/data/database)|
||	eurostat_museum_visitors	|443|	N|	2011|Visitors to museums|[Eurostat](https://ec.europa.eu/eurostat/web/cities/data/database)|
||	eurostat_theaters	|398	|N|	2011|Theaters|[Eurostat](https://ec.europa.eu/eurostat/web/cities/data/database)|
||	eurostat_libraries	|597	|N	|2011|Libraries|[Eurostat](https://ec.europa.eu/eurostat/web/cities/data/database)|
|Germany | 				
| | germany_gdp |108	| N |	2012 | GDP | [German Statistical Office](https://www.destatis.de/EN/Themes/Countries-Regions/Regional-Statistics/_node.html)|
|OECD|				
||	oecd_gdp	|275	|N	|2010|GDP |[OECD](http://dx.doi.org/10.1787/data-00531-en)|
|| oecd_patents	|218	|N	|2008| Patents filed |[OECD](http://dx.doi.org/10.1787/data-00531-en)|
|UK|				
||	uk_income	|100|	N|	2000 to 2011|Weekly income| [Arcaute et al.](http://dx.doi.org/doi:10.1098/rsif.2014.0745)|
||	uk_patents	|93|	N|	2000 to 2011|Patents filed|[Arcaute et al.](http://dx.doi.org/doi:10.1098/rsif.2014.0745)|
||	uk_train	|97|	N|	2000 to 2011|Train statiions|[Arcaute et al.](http://dx.doi.org/doi:10.1098/rsif.2014.0745)|
|USA				|
||	usa_gdp	|381|	Y	|2013| GDP | [BEA](www.bea.gov/itable/index_regional.cfm)|
||	usa_miles|	459|	Y|	2013 |  Length of roads in miles | [FHWA](www.fhwa.dot.gov/policyinformation/statistics/2013/)|
||	covid19_USA|	3131|	N|	2021 | Covid19 cases | [Kaggle](https://www.kaggle.com/sudalairajkumar/covid19-in-usa/version/102)|


The data is stored in the folder [data](https://github.com/edugalt/scaling/tree/master/data), where more information about its sources and filtering can be found. It consists of Python packages (e.g. `brazil`). Each package has functions
that return the data there, defined in the `__init__.py` of the package.
The data is always a tuple (x, y) of numpy arrays of the same size, where x is always population.

For example, to get the population-gdp of brazilian cities from 2010 use:

    import brazil
    x, y = brazil.gdp(2010)

For the spatial data, an additional array (l) indicates the location (latitude and longitude) of the urban area.

### Import your own data:

New data can be added as .csv file to

new_dataset/generic_dataset.txt	   (for three columns: city name, $x,y$)

or

new_dataset2/generic_dataset.txt	(for two columns: $x,y$)

For the spatial analysis, import your resuts as $x$ (population), $y$ (observable), $\ell$ (latitude and longitude) directly in the [notebook](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-SpatialModels-Colab.ipynb)


## Code

The easiset way to interact and run the code is through the Notebooks in the folder [notebooks](https://github.com/edugalt/scaling/tree/master/notebooks). Follow the link in the "Notebook-*-Colab.ipynb" files to run them in [Colab](colab.research.google.com/) or [download](https://github.com/edugalt/scaling/archive/refs/heads/master.zip) this repository and run using [Jupyter](http://jupyter.org/). The source Python code is in the folder [src](https://github.com/edugalt/scaling/tree/master/src)


### Likelihood and minimisation

All inference is performed based on the likelihood of different models. The module `best_parameters.py` contains the definition of the likelihood functions of the models,
the minimization algorithm, and the parameters we use in it.  The bootstrap used to estimate error bars is also defined in this module, at `minimize_with_errors`.
The bootstrap for the person model is implemented in `pvalue_population.py`. The likelihood and minimization of the spatial models appear in 'spatial.py'


### Analysis

The different analysis we perform, as well as the list of databases we use, are defined in `analysis.py`.
The general setting is defined in `LikelihoodAnalysis` and respective methods.

For example, to get beta estimated by Log-Normal with free \delta and other statistical information, use

    from analysis import LogNormalAnalysis
    >>> analysis = LogNormalAnalysis('brazil_aids_2010', required_successes=512)
    >>> analysis.beta[0]
    >>> analysis.p_value
    >>> analysis.bic

You can run the [Jupyter Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels.ipynb) (or [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels-Colab.ipynb)[Jupyter Notebook] or run `python -m analyze.py`. For example,

    MODEL=LogNormalAnalysis ERROR_SAMPLES=10 python -m analyze

runs the `LogNormal` model with 10 samples for bootstrap on the new dataset. 
It prints the best \beta, the bootstrap error for beta, p_value, and BIC for the specific model 
(the script explains how to select the model). 


Pre-computed results are stored at `_results`. In case you want to reproduce some of the results stored in `_results`, you can delete the respective 
analysis in the directory and run (may take some time)

    python -m analysis_run

this requires some environment variables that are documented when you run it.


# References

This repository contains both data and code from the papers:


[1] Is this scaling non-linear? by Jorge C. Leitão, José M. Miotto, Martin Gerlach, and [Eduardo G. Altmann](https://www.maths.usyd.edu.au/u/ega/), [Royal Society Open Science 3, 150649 (2016)](https://royalsocietypublishing.org/doi/10.1098/rsos.150649).  | [See Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels.ipynb) | [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-FittingModels-Colab.ipynb)

[2] Spatial Interctions in urban scaling laws, by [Eduardo G. Altmann](https://www.maths.usyd.edu.au/u/ega/), [PLOS ONE 15, e0243390 (2020)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243390]). | [See Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-SpatialModels.ipynb) | [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-SpatialModels-Colab.ipynb)

and also results for COVID-19 data performed by [Jimena Espinoza](https://github.com/jimenaspi) in Semester 2 2021| [See Notebook](https://github.com/edugalt/scaling/blob/master/notebooks/Notebook-covid19_results.ipynb) | [Open Notebook in Colab](https://colab.research.google.com/github/edugalt/scaling/blob/master/notebooks/Notebook-covid19-Colab.ipynb). 

Contributions with data and models are welcome. If results of this repository are used, please cite the corresponding publications as well.
