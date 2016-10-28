import numpy as np


def index():
    v = []
    with open('new_dataset/generic_dataset.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip("\n").split(',')  # split data
            v.append(list(map(int, line[1:])))
    v = np.array(v).transpose()
    return v[0, :], v[1, :]
