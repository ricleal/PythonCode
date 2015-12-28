'''
Created on Jul 20, 2012

@author: leal
'''

import numpy as np

class Crystal(object):
    
    def __init__(self, a,b,c,alpha,beta,gamma):
        
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
        
        # reciprocal latice vectors
        ar=b*c*sinAlpha/vol
        br=a*c*sinBeta/vol
        cr=a*b*sinGamma/vol
    
        cosalphar=(cosBeta*cosGamma-cosAlpha)/(sinBeta*sinGamma)
        cosbetar=(cosAlpha*cosGamma-cosBeta)/(sinAlpha*sinGamma)
        cosgamar=(cosAlpha*cosBeta-cosGamma)/(sinAlpha*sinBeta)
    
        # reciprocal latice angles
        alphar=np.arccos(cosalphar)
        betar=np.arccos(cosbetar)
        gamar=np.arccos(cosgamar)
        
        self.ar = ar
        self.br = br
        self.cr = cr
        
        self.am = np.matrix([[ar, br*np.cos(gamar), cr*np.cos(betar)],
                    [ 0.0, br*np.sin(gamar), -cr*np.sin(betar)*cosAlpha],
                    [ 0.0, 0.0, 1.0/c]])
    
    def orthogonal_matrix(self):
        return self.am

    def d(self, h, k , l):
        return 1 / np.abs( h*self.ar + k*self.br + l*self.cr )




def test():
    c = Crystal(65.,61.,89.,90.,90.,120.)
    mat = c.orthogonal_matrix()
    
    for i in range(10):
        for j in range(10):
            for k in range(10):
                p = np.matrix([i,j,k])
                latticePoint = p*mat
                print p, ' -> ', latticePoint, c.d(i,j,k)

if __name__ == '__main__':
    test()