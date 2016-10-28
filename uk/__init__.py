import numpy as np


def row(rowname):
    f = open("uk/raw_data/SumsP50D14F30.txt", "r")
    line = f.readline()
    entry = line.strip("\n").split("\t")
    rowfixed = 0
    for i in range(len(entry)):
        if entry[i] == rowname:
            rowfixed = i

    if rowfixed == 0:
        print('Wrong name: ', rowname, '\n Available are: \n d_Work	AgricultHF	Manufact	Construct	HotelRest	FinanceInt	RealEstate	Admin	Education	Income	NetIncome	NIncBH	NIncAH	Households	CarsVans	Dwellings	OccuDwell	UnDwell	UnSecDwell	Employed	Managers	Profess	technical	Admin2	SkillTrd	Service	Sales	plant	Basic	Coach	Train	Patents	Morphology')
        return 0

    line = f.readline()
    x = []
    y = []
    while len(line) > 1:
        entry = line.strip("\n").split("\t")
        x.append(int(float(entry[1])))
        y.append(float(entry[rowfixed]))
        line = f.readline()
    return np.array(x), np.array(y)
