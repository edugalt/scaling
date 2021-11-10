import numpy as np

def covid19_USA():
    v = []
    with open('../data/covid19/raw_data/covid19_USA.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            v.append(list(map(int, line[1:])))
    v = np.array(v).transpose()
    return v[0, :], v[1, :]

def covid19_NSW():
    v = []
    with open('../data/covid19/raw_data/covid19_NSW.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            v.append(list(map(int, line[1:])))
    v = np.array(v).transpose()
    return v[0, :], v[1, :]

def covid19_brazil():
    v = []
    with open('../data/covid19/raw_data/covid19_brazil.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            v.append(list(map(int, line[1:])))
    v = np.array(v).transpose()
    return v[0, :], v[1, :]

def covid19_chile():
    v = []
    with open('../data/covid19/raw_data/covid19_chile.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            v.append(list(map(int, line[1:])))
    v = np.array(v).transpose()
    return v[0, :], v[1, :]