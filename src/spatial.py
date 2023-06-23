from math import *
import numpy as np
from scipy import optimize
import scipy as sp


## Function to import the data:

import brazil,usa,australia

def getData(country="USA",data="gdp"):
    "Load data from requested country and dataset"
    if country=="Brazil":
        if data=="gdp":
            x,y,l,names=brazil.gdplocation(names=True)
        if data=="external":
            x,y,l,names=brazil.extlocation(names=True)
        if data=="aids":
            x,y,l,names=brazil.aidslocation(names=True)
        
    if country=="USA":
        if data=="gdp":
            x,y,l,names=usa.gdplocation(names=True)
        if data=="roads":
            x,y,l,names=usa.mileslocation(names=True)
    if country == "Australia":
        if data=="area":
            x,y,l,names=australia.area(locations=True)
        if data=="education":
            x,y,l,names=australia.education(locations=True)
        if data=="income":
            x,y,l,names=australia.income(locations=True)
    try:
        return x,y,l,names
    except:
        print("Error: data not available!")
        return 0



#################### Functions to compute matrix for the different model ####################

def amatModel(dmat,modelname="percapita",alpha=10):
    "Choose the name of the model, return the distance matrix for fixed alpha; Parameters should contain the parameters of the model, e.g., [alpha,gamma] for the gravitational model"
    if modelname == "percapita":
        return np.matrix(np.identity(len(dmat)))
    if modelname=="city":
        return np.matrix(np.identity(len(dmat)))
    if modelname=="gravitational":
        return aModelG(dmat,alpha)
    if modelname=="exponential":
        return aModelE(dmat,alpha)
    
###########################################################################

# Functions to compute matrix of geodesic distances

def d(i,l):
    "Return the distancesbetwen point i and vector l in km (input is [lat,lon] in decimals"
    earthradius = 6371.0088 # Mean radius according to Wikipdeia and International Union of Geodesy and Geophysics
    lat=np.radians(np.swapaxes(l,0,1)[0]) # array with latitudes
    lon=np.radians(np.swapaxes(l,0,1)[1]) # array with longitudes
    lati =np.radians(np.repeat(i[0],len(l))) # np array of length entries with latitude of i
    loni = np.radians(np.repeat(i[1],len(l))) # np array of length entries with longitude of i
    
    angles=np.power(np.sin(lat-lati),2)+np.cos(lat)*np.cos(lati)*np.power(np.sin((lon-loni)/2),2)
    return 2*earthradius*np.arcsin(np.sqrt(angles))

def dmatrix(l):
    "Return matrix of distances between cities"
    result=[]
    for i in l:
        result.append(d(i,l))
    return np.matrix(result)

###############################################################
# Functions to compute the matrix of interactions 

def aModelG(dmat,alpha,gamma=2):
    "Gets a matrix of distances, returns a matrix aii for model gravitation with exponent gamma and extra parameter alpha"
    return np.divide(1,1+np.power(dmat/alpha,gamma))

def aModelE(dmat,alpha):
    "Gets a matrix of distances, returns a matrix aii for model exponential distance"
    return np.exp(-dmat*np.log(2)/alpha)


####################### Likelihood functions ########################

# the minus log likelihood function involves only the third, relevant term of the likelihood. The additional term are computed in the Description Length functions below

def minus_log_likelihood_beta(beta,x,y,amat):
    "Minus log-likelihood suited for fixed alpha, varying bet (the amat matrix is given, not changing)"
    A = np.array(x*amat) # check with np.matrix times np.array multiplication
    prnon = x*np.power(A,beta-1)
    p=prnon/np.sum(prnon)
    logL=y*np.log(p)
    return -np.sum(logL)


def minus_log_likelihood_alpha(alpha,x,y,l,modelname,beta="ML"):
    "Minus log-likelihood suited for fixed beta, choose beta='ML' if maximum likelihood beta is to be used "
    dmat=dmatrix(l)
    amat=amatModel(dmat,modelname,alpha)
    A = np.array(x*amat) # check with np.matrix times np.array multiplication
    if beta=="ML":
        res=sp.optimize.minimize_scalar(fun=minus_log_likelihood_beta,args=(x,y,amat),method="bounded",bounds=[0,2])
        beta=res.x
    prnon = x*np.power(A,beta-1)
    p=prnon/np.sum(prnon)
    logL=y*np.log(p)
    return -np.sum(logL)


def log_likelihood_amat(beta,x,y,amat):
    "Log-likelihood suited for fixed alpha (the amat matrix is given, not changing), based on Stirling's approximation"
    A = np.array(x*amat) # check with np.matrix times np.array multiplication
    prnon = x*np.power(A,beta-1)
    p=prnon/np.sum(prnon)
    logL=y*np.log(p)
    return np.sum(logL)


def log_likelihood_alphabeta(alpha,beta,x,y,l,model):
    "Log-likelihood suited for fixed alpha (the amat matrix is given, not changing), based on Stirling's approximation"
    dmat = dmatrix(l)
    amat = amatModel(dmat,model,alpha)
    return log_likelihood_amat(beta,x,y,amat)

    
    
####################################
# Functions to find maxima of likelihood functions (minima of - log likelihood)

def MLparameters(x,y,l,model):
    "Returns alpha,beta, and -logLikelihood that maximize likelihood of the model"
    dmat = dmatrix(l)
    # Alpha maximum is ten times the maximum distance
    alphamax = np.max(dmat)

    if model == "percapita":
        amat=amatModel(dmat,model)
        return 0,1,minus_log_likelihood_beta(1,x,y,amat)
    if model == "city":
        amat = amatModel(dmat,"city")
        res=sp.optimize.minimize_scalar(fun=minus_log_likelihood_beta,args=(x,y,amat),method="bounded",bounds=[0,2])
        return 0,res.x,res.fun
    else:
    #Optimize in alpha, choosing beta to be the Maximum likelihood value for fixed alpha
        res=sp.optimize.minimize_scalar(fun=minus_log_likelihood_alpha,args=(x,y,l,model),method="bounded",bounds=[0,alphamax])
        restest=sp.optimize.minimize_scalar(fun=minus_log_likelihood_alpha,args=(x,y,l,model),method="bounded",bounds=[0,500])
        if restest.fun < res.fun:
            res = restest
        if res.success:
            alpha = res.x
            amat=amatModel(dmat,model,alpha)
            res2=sp.optimize.minimize_scalar(fun=minus_log_likelihood_beta,args=(x,y,amat),method="bounded",bounds=[0,2])
            beta=res2.x
            nloglike = res2.fun
            return alpha,beta,nloglike
        else:
            print("Error, minimum not found")
            return "error","error","error"


#### Functions to compute the description length #####################
    

def integratedL(data,model,par,optimal=[]):
    '''Compute the integral of the relative likelihood for the given model and data, with resolution par; the Maximum Likelihood values can be provided as "optimal" to facilitated computations'''
    x=data[0]
    y=data[1]
    l=data[2]
    if len(optimal)!=3:
            optimal = list(MLparameters(x,y,l,model))
    alphaML=optimal[0]
    betaML=optimal[1]
    logLML=optimal[2]
    if logLML>0:
        logLML=-logLML
    
    if model=="percapita":
    # Nothing to be done, the difference to the logML is zero
        return 0

    amin=max(-par[0],-alphaML)
    amax=min(par[0],6380-alphaML)
    bmin=max(-par[1],0-betaML)
    bmax=min(par[1],2-betaML)
    eps=10**-6
    
    if model=="city":
        #integrate over beta only
        gbeta = lambda be: np.exp(log_likelihood_alphabeta(alphaML,betaML+be,x,y,l,model)-logLML)
        I=sp.integrate.quad(gbeta,bmin,bmax,epsrel=eps)
        return I
    
    if model=="gravitational" or model=="exponential":
        #integrate over alpha and beta; first term of par is the variation in alpha, second is the variation in beta, third is precision
        g2 =  lambda ae,be: np.exp(log_likelihood_alphabeta(alphaML+ae,betaML+be,x,y,l,model)-logLML)
        I=sp.integrate.dblquad(g2,bmin,bmax,lambda be:amin,lambda be:amax,epsrel=eps,epsabs=eps)
        return I


def logLikelihood12(y):
    "compute the two terms of the log-likelihood that depend only on the data y"
    Y = np.sum(y)
    logL12 = Y*np.log(Y)-Y-np.sum(y[y>0]*np.log(y[y>0])-y[y>0])
    return logL12


def negLogPrior(model):
    "Returns the prior probability of the model"
    if model=="percapita" or model=="P":
        prior=-np.log(1/4)
    if model=="city" or model=="C":
        prior=-np.log(1/4)-np.log(1/2)
    if model=="gravitational" or model=="exponential" or model=="G" or model=="E":
        prior=-np.log(1/4)-np.log(1/2)-np.log(1/6371) #where 6371km is the radius of the earth
    try:
        return prior
    except:
        print("Error computing prior, no model found")
        return 0


def DL(y,model,logI,logLML):
    "Computes the description length from I (the integral of the relative likelihood computed from integratedL) and the Maximum Likelihood (logLML)"
    if logLML>0:
        logLML=-logLML
    if logI>0:
        logI=-logI
    # Two fixed terms of the log-likelihood
    logL12=logLikelihood12(y)
    if logL12>0:
        logL12=-logL12
    #Prior probability
    logPrior = negLogPrior(model)
    if logPrior>0:
        logPrior=-logPrior
    #
    DL=-logI-logLML-logL12-logPrior
    return DL

