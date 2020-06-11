import string
import numpy as np
import csv
import pylab as pl
pl.switch_backend('TkAgg')


year_ = '2011'


countries = ['Belgium','Bulgaria','Czech Republic','Denmark','Germany','Estonia','Ireland','Greece','Spain','France','Italy','Cyprus','Latvia','Lithuania','Luxembourg','Hungary','Netherlands','Austria','Poland','Portugal','Romania','Slovenia','Slovakia','Finland','Sweden','United Kingdom','Turkey','Norge','Schweiz/Suisse']
#'(greater city)'
## data in x: population
var_ = 'Population on the 1st of January, total'

i_year=0
i_var=0
i_val=0

# i_id=0
i_city=1

dict_data_x = {}

with open('raw_data/urb_cpop1/urb_cpop1_1_Data.csv', 'rb') as csvfile:
    x = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in x:
#         print ', '.join(row)
        if i == 0:
            list_header = row
            i_year = list_header.index('TIME')
            i_var = list_header.index('INDIC_UR')
            i_val = list_header.index('Value')
        else:
            year = row[i_year]
            var = row[i_var]
#             print year,var
            if year == year_ and var == var_:
                city = row[i_city]
                if city not in countries and '(greater city)' not in city:
                    val = row[i_val]
                    try:
                        dict_data_x[city] = {'val':int(string.replace(val,',',''))}
                    except ValueError:
                        pass
        i+=1
        
        
## data in y: cultural output
# var_ = 'Number of cinema seats (total capacity)'
# var_ = 'Cinema attendance (per year)'
# var_ = 'Number of museum visitors (per year)'
# var_ = 'Number of theatres'
# var_ = 'Number of public libraries (all distribution points)'
i_year=0
i_var=0
i_val=0

# i_id=0
i_city=1
list_var_ = ['Number of cinema seats (total capacity)','Cinema attendance (per year)','Number of museum visitors (per year)','Number of theatres','Number of public libraries (all distribution points)']
for i_var_,var_ in enumerate(list_var_):




    dict_data_y = {}
    with open('raw_data/urb_ctour/urb_ctour_1_Data.csv', 'rb') as csvfile:
        x = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in x:
    #         print ', '.join(row)
            if i == 0:
                list_header = row
                i_year = list_header.index('TIME')
                i_var = list_header.index('INDIC_UR')
                i_val = list_header.index('Value')
            else:
                year = row[i_year]
                var = row[i_var]
    #             print year,var
                if year == year_ and var == var_:
                    city = row[i_city]
                    if city not in countries and '(greater city)' not in city:
                        val = row[i_val]
                        try:
                            dict_data_y[city] = {'val':int(string.replace(val,',',''))}
                        except ValueError:
                            pass
            i+=1
    # 
    # 
    list_x = []
    list_y = []
    list_name = []
    for city_id,city_x in dict_data_x.iteritems():
        try:
            city_y = dict_data_y[city_id]
            list_x += [city_x['val']]
            list_y += [city_y['val']]
            list_name += [city_id]
        except KeyError:
            pass
    list_x = np.array(list_x)
    list_y = np.array(list_y)
    list_name = np.array(list_name)
    indsort = np.argsort(list_x)
    list_x = list_x[indsort][::-1]
    list_y = list_y[indsort][::-1]
    list_name = list_name[indsort][::-1]
    print len(list_name)
    
    f = open('EUROSTAT_culture%s_pop_%s'%(str(i_var_+1),str(year_)),'w')
    f.write('city\tpopulation\t%s\n'%(string.replace(var_,' ','_')))
    for i in xrange(len(list_name)):
        f.write('%s\t%s\t%s\n'%(string.replace(list_name[i],' ','_'),list_x[i],list_y[i]))
    f.close()
    
#     # pl.plot(np.sort(list_pop)[::-1],lw=0,marker='o')
#     pl.plot(list_x,list_y,marker='o',lw=0)
#     pl.plot(list_x,0.01*list_x,lw=1,ls='--',color='black')
# 
#     pl.xscale('log')
#     pl.yscale('log')
# 
#     pl.show()