import string
import numpy as np
import csv

dict_data = {}

## GDP
tag = '(Metropolitan Statistical Area)'
year_gdp=2013
i=0
with open('raw_data/US_metro_gdp_%s.csv'%str(year_gdp), 'rb') as csvfile:
    x = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in x:
        try:
            if tag in row[1]:
                id = int(row[0])
                city = string.rstrip(string.split(row[1],tag)[0])
                gdp = float(row[2]) 
#                 print id,city,gdp
                dict_data[city] = {'gdp': gdp}
            i+=1
#             if i==10:
#                 break
        except IndexError:
            pass
## POP
tag = 'Metro Area'

year_pop=2013
i=0
with open('raw_data/US_metro_pop_%s.csv'%str(year_pop), 'rb') as csvfile:
    x = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in x:
        if tag in row[0]:
            city = string.strip(string.split(row[0],tag)[0])
            pop = int(string.replace(row[3],',',''))
            print city
            try:
                dict_data[city]['pop'] = pop
                print dict_data[city],pop
            except KeyError:
                pass
#             print city,pop
#         print row
        i+=1
#         if i==10:
#             break


gdp = []
pop = []
city = []
for city_,data_ in dict_data.iteritems():
    gdp += [data_['gdp']]
    pop += [data_['pop']]
    city += [city_]
gdp=np.array(gdp)
pop=np.array(pop)
city=np.array(city)
indsort = np.argsort(pop)
pop=pop[indsort][::-1]
gdp=gdp[indsort][::-1]
city=city[indsort][::-1]

f = open('USmetro_gdp_pop_2013','w')
f.write('city\tpopulation\tgdp_in_million_USD\n')
for i in xrange(len(city)):
    f.write('%s\t%s\t%s\n'%(string.replace(city[i],' ','_'),pop[i],gdp[i]))
f.close()
