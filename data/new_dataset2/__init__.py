import numpy as np


def index():
    v = []
    with open('../data/new_dataset2/generic_dataset.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            try:
                v.append(list(map(float, line[:])))
            except:
                print("Warning, ignoring line: ",line)
    v = np.array(v).transpose()
    return v[0, :], v[1, :]
