from numpy import array

from . import data as _data


def gdp(year, flush=False):
    data = _data.raw_gdp_data(year, flush)
    data = sorted((data[x]['population'], data[x]['gdp']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])

def gdplocation(year=2010,flush=False,names=False):
    data = _data.raw_gdploc_data(year,flush)


    if names:
        data = sorted((data[x]['population'], data[x]['gdp'],data[x]['location'],data[x]['name']) for x in data)[::-1]
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data]),array([x[3] for x in data])

    else:
        data = sorted((data[x]['population'], data[x]['gdp'],data[x]['location']) for x in data)
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data])

def aids(year, flush=False):
    data = _data.raw_aids_data(year, flush)
    data = sorted((data[x]['population'], data[x]['aids']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])


def externalCauses(year, flush=False):
    data = _data.raw_externalCauses_data(year, flush)
    data = sorted((data[x]['population'], data[x]['externalCauses']) for x in data)

    return array([x[0] for x in data]), array([x[1] for x in data])

    
def aidslocation(year=2010,flush=False,names=False):
    data = _data.raw_aidsloc_data(year,flush)


    if names:
        data = sorted((data[x]['population'], data[x]['aids'],data[x]['location'],data[x]['name']) for x in data)[::-1]
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data]),array([x[3] for x in data])

    else:
        data = sorted((data[x]['population'], data[x]['aids'],data[x]['location']) for x in data)
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data])


def extlocation(year=2010,flush=False,names=False):
    data = _data.raw_extloc_data(year,flush)


    if names:
        data = sorted((data[x]['population'], data[x]['ext'],data[x]['location'],data[x]['name']) for x in data)[::-1]
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data]),array([x[3] for x in data])

    else:
        data = sorted((data[x]['population'], data[x]['ext'],data[x]['location']) for x in data)
        return array([x[0] for x in data]), array([x[1] for x in data]),array([x[2] for x in data])
