#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Michelle
#
# Created:     05/11/2014
# Copyright:   (c) Michelle 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np

def Spectrum(ktemp,constant,power,pivot,equation):
    """Creates the spectrum of phi using a powerlaw
    ktemp -> float
    constant -> float
    power -> float
    equation -> 1=Ck^n, 2=Ck^(n-1)
    return Spectrum -> float"""
    if equation == 3:
        temp = np.multiply(constant,pow(ktemp/pivot,1-power))
    elif equation == 2:
        temp = np.multiply(constant,pow(ktemp/pivot,power-1))
    else: # default Ck^n
        temp = np.multiply(constant,pow(ktemp/pivot,power))
    temp[np.isnan(temp)] = 0.0
    temp[np.isinf(temp)] = 0.0
    return temp


def SigmaNSquared(ktemp,Spectrumtemp):
    """
    Calculates sigma squared for the given power spectrum. M{P*2*np.pi^2*k^3}

    @type         ktemp: float
    @param        ktemp:
    @type  Spectrumtemp: float
    @param Spectrumtemp:
    @type         Ltemp: float
    @param        Ltemp: the size of the box

    @rtype:              float
    @return:
    """
    temp = np.divide(Spectrumtemp,8.0*np.pi*pow(ktemp,3))#*pow(100/663,-3)) #/(2*np.pi)
    temp[np.isnan(temp)] = 0.0
    temp[np.isinf(temp)] = 0.0

    return temp
    
    
def Radius(Ntemp,factortemp):
    x = np.multiply(np.arange(0,Ntemp/2+1,1),factortemp)
    yy,zz,xx = np.meshgrid(x,x,x)
    radius = np.sqrt(pow(xx,2)+pow(yy,2)+pow(zz,2))

    q = radius.flat
    radius = list(q)
    r = list(set(radius))
    r.sort()

    return np.array(r)