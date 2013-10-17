'''
Created on Jul 20, 2012

@author: leal
'''

import numpy as np

def crystGen(cell):
    """
    c-------------------------------------------------
    c    Callculation of reciprocal lattice parameters and
    c     orthogonal matrix of crystal orientation
    c    Am(3,3) -  3*3 - matrics
    c       a*  b*cos(gama*)  c*cos(beta*)
    c       0   b*sin(gama*) -c*sin(beta*)cosAlpha
    c       0       0         1/c
    c
    c===================================================
    """

    a,b,c,alpha,beta,gamma = cell

    alpha = alpha * np.pi/180
    beta = beta * np.pi/180
    gamma = gamma * np.pi/180

    cosAlpha = np.cos(alpha)
    sinAlpha = np.sin(alpha)
    cosBeta = np.cos(beta)
    sinBeta = np.sin(beta)
    cosGamma = np.cos(gamma)
    sinGamma = np.sin(gamma)

    vol=a*b*c*np.sqrt(1.-cosAlpha**2-cosBeta**2-cosGamma**2+2.*cosAlpha*cosBeta*cosGamma)

    ar=b*c*sinAlpha/vol
    br=a*c*sinBeta/vol
    cr=a*b*sinGamma/vol

    cosalfar=(cosBeta*cosGamma-cosAlpha)/(sinBeta*sinGamma)
    cosbetar=(cosAlpha*cosGamma-cosBeta)/(sinAlpha*sinGamma)
    cosgamar=(cosAlpha*cosBeta-cosGamma)/(sinAlpha*sinBeta)

    alfar=np.arccos(cosalfar)
    betar=np.arccos(cosbetar)
    gamar=np.arccos(cosgamar)

    am = np.matrix([[ar, br*np.cos(gamar), cr*np.cos(betar)],
                    [ 0.0, br*np.sin(gamar), -cr*np.sin(betar)*cosAlpha],
                    [ 0.0, 0.0, 1.0/c]])

    #print am

    return am

if __name__ == '__main__':

    cell = np.array([1,1,1,90,90,90])
    orthogonalMatrix = crystGen(cell)
    print orthogonalMatrix
    
    for i in range(10):
        for j in range(10):
            for k in range(10):
                p = np.matrix([i,j,k])
                latticePoint = p*orthogonalMatrix
                print p, ' -> ', latticePoint
