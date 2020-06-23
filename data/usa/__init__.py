import os.path
from numpy import array
from io import open
import numpy as np


def gdp():
     f=open("../data/usa/USmetro_gdp_pop_2013","r")

     line=f.readline()
     line=f.readline()
     x=[]
     y=[]
     while len(line)>1:
          entry=line.strip("\n").split("\t")
          x.append(int(entry[1]))
          y.append(float(entry[2]))
          line=f.readline()
     return np.array(x),np.array(y)


def miles():
     f=open("../data/usa/metropolitan-miles.csv","r")
     line=f.readline()
     x=[]
     y=[]
     while len(line)>1:
 #         print 'oi:',line,'->',
          line=line[1:-2]
          entry=line.strip("\n").split('",')
          if len(entry)==3:
              xe=entry[1].strip(" ").replace(',','')
              ye=entry[2].strip(" ").replace(',','')
              if not xe.isalnum():
                  xe=xe[1:]
              if not ye.isalnum():
                  ye=ye[1:]
#              print "mid",xe,ye,len(xe),len(ye)
              if len(xe)>0 and len(ye)>0:
                  x.append(int(xe))
                  y.append(float(ye))
#              else:
#                  print 'Not added 2',line
#          else:
#              print 'Not added:',line
#          print xe,ye
          line=f.readline()
     return np.array(x),np.array(y)


def gdplocation(names=False):
    dictLocation={}
    fileLoc = open(os.path.dirname(__file__)+"/USA-locations.csv","r")
#    fileLoc = open("./USA-locations.csv","r")
    fileLines = fileLoc.readlines()
    for line in fileLines:
        e=line.split(",")
        cityname=e[0].strip('"')
        while cityname in dictLocation.keys():
            cityname=cityname+"+"
        dictLocation[cityname]=[float(e[6]),float(e[7].strip("\n"))]
    
    dictPopGdp={}
    filePop = open(os.path.dirname(__file__)+"/USmetro_gdp_pop_2013","r")
    fileLines = filePop.readlines()
    for line in fileLines[1:]:
        e=line.split()
        cityname=e[0].split(",")[0].replace("_"," ")
        while cityname in dictPopGdp:
            cityname=cityname+"+"
        dictPopGdp[cityname]=[int(e[1]),float(e[2])]

    data=sorted([(dictPopGdp[k][0],dictPopGdp[k][1],dictLocation[k][0],dictLocation[k][1],k) for k in dictLocation])
    data=data[::-1] # reverse the data
    population = array([d[0] for d in data])
    gdp = array([d[1] for d in data])
    l = array([[d[2],d[3]] for d in data])
    nam = array([d[4] for d in data])

    if names:
        return population,gdp,l,nam
    else:
        return population,gdp,l

def mileslocation(names=False):
    data=[]
    f = open(os.path.dirname(__file__)+"/miles-location.csv","r")
    fileLines = f.readlines()
    for line in fileLines:
        e=line.split(",")
        data.append([float(e[1]),float(e[2]),float(e[3].strip(" [")),float(e[4].strip("]\n")),e[0]])
    data = sorted(data)[::-1]


    population = array([d[0] for d in data])
    miles = array([d[1] for d in data])
    l = array([[d[2],d[3]] for d in data])
    nam = array([d[4] for d in data])
    
    if names:
        return population,miles,l,nam
    else:
        return population,miles,l
