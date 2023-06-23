import numpy as np

import pandas as pd

def sort_dataC(x, y,c,loc):
    """
    Sorts the data by increasing x while keeping the respective y and city name.
    """
    idx = x.argsort()
    return x[idx], y[idx],c[idx],loc[idx]


def location(cities,dictLoc):
    """
returns an array of cities with location and and array of locations, found in dictLoc    
    """
    citiesLoc=[]
    locCities=[]
    for c in cities:
        if c in dictLoc.keys():
            citiesLoc.append(c)
            locCities.append(dictLoc[c])
        else:
            for i in dictLoc.keys():
                if i[:5] == c[:5]:
                 #   print(c,"\t => \t",i)
                    citiesLoc.append(c)
                    locCities.append(dictLoc[i])
    return(citiesLoc,locCities)


def dictLocation():
     loc = pd.read_excel('../data/australia/SUA_LatLong.xlsx')
     dictLoc={}
     for i in range(len(loc)):
          dictLoc[loc.City[i].replace("-"," - ")]=[loc.Latitude[i],loc.Longitude[i]]
     return(dictLoc)

def dictAreas():
     areas = pd.read_excel('../data/australia/SUA_association_2016_2021.xlsx')
     dictArea21={}
     for i in range(len(areas)):
          if str(areas.SUA_NAME_2021[i]).startswith("Not in any "):
               pass
          else:
               dictArea21[areas.SUA_NAME_2021[i]]=areas.AREA_ALBERS_SQKM_2021[i]
     return(dictArea21)



def dictIncomeAndPopulation():
     pop = pd.read_csv('../data/australia/top2021.csv')
     dictIncome={}
     dictPop={}
     for i in range(len(pop)):
          if str(pop.SUA[i]).startswith("Not in any "):
               pass
          else:
               dictPop[pop.SUA[i]]=pop.Population[i]
               dictIncome[pop.SUA[i]]=pop.Income[i]
     return(dictIncome,dictPop)

def dictEducationAndPopulation():
     pop = pd.read_csv('../data/australia/top2021.csv')
     dictE={}
     dictPop={}
     for i in range(len(pop)):
          if str(pop.SUA[i]).startswith("Not in any "):
               pass
          else:
               dictPop[pop.SUA[i]]=pop.Population[i]
               dictE[pop.SUA[i]]=pop.Education[i]
     return(dictE,dictPop)


def income(locations=False):
    dictI,dictP=dictIncomeAndPopulation()
    x,y=[],[]
    names=list(dictP.keys())
    if(locations):
        dictLoc=dictLocation()
        namesLoc,loc = location(names,dictLoc)   
        for i in range(len(namesLoc)):
            c=namesLoc[i]
            x.append(dictP[c])
            y.append(dictI[c])
        return sort_dataC(np.array(x),np.array(y),np.array(loc),np.array(namesLoc))
    else:
        for c in dictP.keys():
            x.append(dictP[c])
            y.append(dictI[c])
        return np.array(x),np.array(y)

def education(locations=False):
    dictE,dictP=dictIncomeAndPopulation()
    x,y=[],[]
    names=list(dictP.keys())
    if(locations):
        dictLoc=dictLocation()
        namesLoc,loc = location(names,dictLoc)   
        for i in range(len(namesLoc)):
            c=namesLoc[i]
            x.append(dictP[c])
            y.append(dictE[c])
        return sort_dataC(np.array(x),np.array(y),np.array(loc),np.array(namesLoc))

    else:
        for c in dictP.keys():
            x.append(dictP[c])
            y.append(dictE[c])
        return np.array(x),np.array(y)


def area(locations=False):
    dictE,dictP=dictIncomeAndPopulation()
    dictA=dictAreas()
    x,y=[],[]
    names=list(dictP.keys())
    if(locations):
        dictLoc=dictLocation()
        namesLoc,loc = location(names,dictLoc)   
        for i in range(len(namesLoc)):
            c=namesLoc[i]
            x.append(dictP[c])
            y.append(dictA[c])
        return sort_dataC(np.array(x),np.array(y),np.array(loc),np.array(namesLoc))
    else:
        for c in dictP.keys():
            x.append(dictP[c])
            y.append(dictA[c])
        return np.array(x),np.array(y)
     
