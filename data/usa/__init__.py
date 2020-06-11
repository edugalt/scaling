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
