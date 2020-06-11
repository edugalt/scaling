import numpy as np

def read_file(file_name):
    """
    """
    v = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            v.append(list(map(int, line.strip("\n").split("\t")[1:])))
    v = np.array(v).transpose()
    return v[0,:], v[1,:]


def cinemaSeats():
    file_name = '../data/eurostat/EUROSTAT_culture1_pop_2011'
    return read_file(file_name)


def cinemaAttendance():
    file_name = '../data/eurostat/EUROSTAT_culture2_pop_2011'
    return read_file(file_name)


def museumVisitors():
    file_name = '../data/eurostat/EUROSTAT_culture3_pop_2011'
    return read_file(file_name)


def theaters():
    file_name = '../data/eurostat/EUROSTAT_culture4_pop_2011'
    return read_file(file_name)


def libraries():
    file_name = '../data/eurostat/EUROSTAT_culture5_pop_2011'
    return read_file(file_name)
