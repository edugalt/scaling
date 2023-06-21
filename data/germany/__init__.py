import numpy as np

def gdp():
     f=open("../data/germany/GERcity_gdp_pop_2012","r")

     line=f.readline()
     line=f.readline()
     x=[]
     y=[]
     while len(line)>1:
          entry=line.strip("\n").split("\t")
          x.append(int(entry[1]))
          y.append(int(entry[2]))
          line=f.readline()
     return np.array(x),np.array(y)
