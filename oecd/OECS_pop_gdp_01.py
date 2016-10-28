import string
import numpy as np
import csv
import pylab as pl
pl.switch_backend('TkAgg')

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

## data in x: population
year_ = '2010'
var_ = 'POP'

i_year=0
i_var=0
i_val=0

i_id=0
i_city=1

dict_data_x = {}

with open('raw_data/CITIES_population_raw.csv', 'rb') as csvfile:
    x = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in x:
#         print ', '.join(row)
        if i == 0:
            list_header = row
            i_year = list_header.index('Year')
            i_var = list_header.index('VAR')
            i_val = list_header.index('Value')
        else:
            year = row[i_year]
            var = row[i_var]
#             print year,var
            if year == year_ and var == var_:
                id = row[i_id]
                if hasNumbers(id): ## check if the city-id has an integer number, otherwise it is a country
                    city = row[i_city]
                    val = row[i_val]
                    try:
                        dict_data_x[id] = {'val':int(val),'name':city}
                    except ValueError:
                        pass
        i+=1
## data in y: gdp
year_ = '2010'

i_year=0
i_var=0
i_val=0

i_id=0
i_city=1

dict_data_y = {}

var_ = 'GDP'
with open('raw_data/CITIES_gdp_raw.csv', 'rb') as csvfile:
# var_='PCT'
# with open('raw_data/CITIES_patents_raw.csv', 'rb') as csvfile:

    x = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in x:
#         print ', '.join(row)
        if i == 0:
            list_header = row
            i_year = list_header.index('Year')
            i_var = list_header.index('VAR')
            i_val = list_header.index('Value')
        else:
            year = row[i_year]
            var = row[i_var]

            if year == year_ and var == var_:
                id = row[i_id]
                if hasNumbers(id):
                    city = row[i_city]
                    val = row[i_val]
                    print id,city,val
                    try:
                        dict_data_y[id] = {'val':float(val),'name':city}
                    except ValueError:
                        pass
        i+=1


list_x = []
list_y = []
list_name = []
for city_id,city_x in dict_data_x.iteritems():
    try:
        city_y = dict_data_y[city_id]
        list_x += [city_x['val']]
        list_y += [city_y['val']]
        list_name += [city_x['name']]
    except KeyError:
        pass
list_x = np.array(list_x)
list_y = np.array(list_y)
list_name = np.array(list_name)
indsort = np.argsort(list_x)
list_x = list_x[indsort][::-1]
list_y = list_y[indsort][::-1]
list_name = list_name[indsort][::-1]


f = open('OECD_gdp_pop_2010','w')
f.write('city\tpopulation\tgdp_in_million_USD\n')
for i in xrange(len(list_name)):
    f.write('%s\t%s\t%s\n'%(list_name[i],list_x[i],list_y[i]))
f.close()

# pl.plot(np.sort(list_pop)[::-1],lw=0,marker='o')
pl.plot(list_x,list_y,marker='o',lw=0)
pl.plot(list_x,0.01*list_x,lw=1,ls='--',color='black')

pl.xscale('log')
pl.yscale('log')

pl.show()