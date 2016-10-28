from __future__ import unicode_literals

import json
import os.path
from io import open


def cache(file_name_format):
    """
    A decorator to cache the result of the function into a file. The result
    must be a dictionary. The result storage is in json.

    The decorator argument is the file name format. The format must contain the
    same number of positional arguments as the function

    E.g. 'd_{0}_{1}.json' for a function of 2 arguments.
    """
    def cache_function(function):
        def func_wrapper(*args, **kwargs):
            file_name = file_name_format.format(*args, **kwargs)
            try:
                if 'flush' in kwargs and kwargs['flush']:
                    raise IOError
                with open(file_name, 'r', encoding='utf8') as cache_file:
                    data = json.load(cache_file)
            except IOError:
                data = function(*args, **kwargs)
                with open(file_name, 'w', encoding='utf8') as cache_file:
                    cache_file.write(json.dumps(data, ensure_ascii=False, indent=2,
                                                separators=(',', ': '),
                                                sort_keys=True))

            return data
        return func_wrapper
    return cache_function


def get_population(year):
    assert(1996 <= year <= 2012)
    with open(os.path.dirname(__file__) + '/raw_data/population-1996-2012.dat',
              'r', encoding='utf-8') as f:
        data = f.readlines()

    # choose the right column
    year_to_column = dict((1996 + i, i + 1) for i in range(17))  # [1996, 2012] -> [1, 17]
    column = year_to_column[year]

    column_names = data[0].split(';')
    assert(int(column_names[column][1:-1]) == year)

    # build the city names and numbers
    result = {}
    for row in data[1:-2]:
        columns = row.split(";")
        first_column = columns[0]
        city_number = first_column[1:7]
        city_name = first_column[8:-1]
        assert('"' not in city_name)
        assert('"' not in city_number)

        # see data README why the replace.
        city_population = int(columns[column].replace('-', '0'))
        
        if city_population > 0:
            result[city_number] = {'name': city_name, 'population': city_population}

    return result


def get_gdp(year):
    assert(2000 <= year <= 2012)
    with open(os.path.dirname(__file__) + '/raw_data/gdp-2000-2012.dat',
              'r', encoding='utf-8') as f:
        data = f.readlines()

    # choose the right column
    year_to_column = dict((2000 + i, i + 1) for i in range(13))  # [2000, 2012] -> [1, 13]
    column = year_to_column[year]

    column_names = data[0].split(';')
    assert(int(column_names[column][1:-1]) == year)

    # build the city name, number and gdp (-1 == Total)
    result = {}
    for row in data[1:-2]:
        columns = row.split(";")
        first_column = columns[0]
        city_number = first_column[1:7]
        city_name = first_column[8:-1]
        assert('"' not in city_name)
        assert('"' not in city_number)

        # see data README why the first replace; PT uses ',' instead of '.'
        city_gdp = int(float(columns[column].replace('-', '0').replace(',', '.')))

        result[city_number] = {'name': city_name, 'gdp': city_gdp}

    return result

def get_aids(year):
    assert(1996 <= year <= 2012)
    with open(os.path.dirname(__file__) + '/raw_data/aids-1996-2012.dat',
              'r', encoding='utf-8') as f:
        data = f.readlines()

    # choose the right column
    year_to_column = dict((1996 + i, i + 1) for i in range(17))  # [1996, 2012] -> [1, 17]
    column = year_to_column[year]

    column_names = data[0].split(';')
    assert(int(column_names[column][1:-1]) == year)

    # build the city name, number and gdp (-1 == Total)
    result = {}
    for row in data[1:-2]:
        columns = row.split(";")
        first_column = columns[0]
        city_number = first_column[1:7]
        city_name = first_column[8:-1]
        assert('"' not in city_name)
        assert('"' not in city_number)

        # see data README why the first replace; PT uses ',' instead of '.'
        city_aids = int(float(columns[column].replace('-', '0').replace(',', '.')))

        result[city_number] = {'name': city_name, 'aids': city_aids}

    return result

def get_externalCauses(year):
    assert(1996 <= year <= 2012)
    with open(os.path.dirname(__file__) + '/raw_data/externalCauses-1996-2012.dat',
              'r', encoding='utf-8') as f:
        data = f.readlines()

    # choose the right column
    year_to_column = dict((1996 + i, i + 1) for i in range(17))  # [1996, 2012] -> [1, 17]
    column = year_to_column[year]

    column_names = data[0].split(';')
    assert(int(column_names[column][1:-1]) == year)

    # build the city name, number and gdp (-1 == Total)
    result = {}
    for row in data[1:-2]:
        columns = row.split(";")
        first_column = columns[0]
        city_number = first_column[1:7]
        city_name = first_column[8:-1]
        assert('"' not in city_name)
        assert('"' not in city_number)

        # see data README why the first replace; PT uses ',' instead of '.'
        city_externalCauses = int(float(columns[column].replace('-', '0').replace(',', '.')))

        result[city_number] = {'name': city_name, 'externalCauses': city_externalCauses}

    return result


@cache(os.path.dirname(__file__) + '/json/data-GDP{0}.json')
def raw_gdp_data(year, flush=False):
    population = get_population(year)
    gdp = get_gdp(year)
    # add gdp to the population dictionary
    common = set(population.keys()).intersection(set(gdp.keys()))

    result = {}
    for city in common:
        result[city] = population[city]
        result[city]['gdp'] = gdp[city]['gdp']

    return result

@cache(os.path.dirname(__file__) + '/json/data-aids{0}.json')
def raw_aids_data(year, flush=False):
    population = get_population(year)
    aids = get_aids(year)
    common = set(population.keys()).intersection(set(aids.keys()))

    result = {}
    for city in common:
        result[city] = population[city]
        result[city]['aids'] = aids[city]['aids']

    return result

@cache(os.path.dirname(__file__) + '/json/data-externalCauses{0}.json')
def raw_externalCauses_data(year, flush=False):
    population = get_population(year)
    externalCauses = get_externalCauses(year)
    common = set(population.keys()).intersection(set(externalCauses.keys()))

    result = {}
    for city in common:
        result[city] = population[city]
        result[city]['externalCauses'] = externalCauses[city]['externalCauses']

    return result


@cache(os.path.dirname(__file__) + '/json/data-growth{0}.json')
def raw_growth_data(year, flush=False):
    population = get_population(year)
    old_population = get_population(year - 1)
    # add gdp to the population dictionary
    common = set(population.keys()).intersection(set(old_population.keys()))

    result = {}
    for city in common:
        result[city] = population[city]
        result[city]['growth'] = population[city]['population'] - \
            old_population[city]['population']

    return result
