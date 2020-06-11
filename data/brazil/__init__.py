from numpy import array

from . import data as _data


def gdp(year, flush=False):
    data = _data.raw_gdp_data(year, flush)
    data = sorted((data[x]['population'], data[x]['gdp']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])


def aids(year, flush=False):
    data = _data.raw_aids_data(year, flush)
    data = sorted((data[x]['population'], data[x]['aids']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])


def externalCauses(year, flush=False):
    data = _data.raw_externalCauses_data(year, flush)
    data = sorted((data[x]['population'], data[x]['externalCauses']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])
