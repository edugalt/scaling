import numpy as np

def gdp():
     f=open("oecd/OECD_gdp_pop_2010","r")

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

def patents():
     f=open("oecd/OECD_patents_pop_2008","r")

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

