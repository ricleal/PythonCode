'''
From: https://wiki.pha.jhu.edu/advlab_wiki/index.php/Analysis_5
'''

import numpy # numerics (matrix operations, etc)
import scipy.optimize, scipy.stats.stats #Fitting and Statistics
import pylab # Plotting

#Read in the data and check (print) that we read in correctly
x, counts = numpy.loadtxt('counts.txt', unpack=True)
print x
print counts

#Because these are counts, we can use poisson statistics to define
#the standard deviation
std = numpy.sqrt(counts)

#Plot Data

pylab.subplot(2, 1, 1)
pylab.title("Raw Data")
pylab.errorbar(x,counts,std, fmt='o')
pylab.xlabel('x (units)')
pylab.ylabel('Counts')
# pylab.savefig('data.png')
# pylab.clf()

#Define a function that we want to fit
def gaussian_with_background(x,A,B,C,D,E):
    return A*numpy.exp(-(x-B)**2/(2.*C**2)) + D*x + E

#Call the non-linear (Levenburg-Marquardt-based) fitting routine
#scipy.optimize.curve_fit
#http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
#returns answer and covariance

ans, cov = scipy.optimize.curve_fit(gaussian_with_background, x, counts, sigma=std)

print "A=", ans[0], "+/-", numpy.sqrt(cov[0][0])
print "B=", ans[1], "+/-", numpy.sqrt(cov[1][1])
print "C=", ans[2], "+/-", numpy.sqrt(cov[2][2])
print "D=", ans[3], "+/-", numpy.sqrt(cov[3][3])
print "E=", ans[4], "+/-", numpy.sqrt(cov[4][4])

#Write out result for later reference
# numpy.savetxt('counts_best_fit.txt', ans)
# numpy.savetxt('counts_cov.txt', cov)

#Plot data, best-fit model, and residual
model = gaussian_with_background(x,ans[0], ans[1], ans[2], ans[3], ans[4])
pylab.subplot(2, 1, 2)
pylab.title("Fitting")
pylab.plot(x, model, label='Model')
pylab.errorbar(x, counts, std, label='Data', fmt='o')
residual = counts - model
pylab.errorbar(x, residual, std, label='Residual', fmt='o')
pylab.legend()
pylab.xlabel('x (units)')
pylab.ylabel('Counts')
#pylab.savefig('counts_with_fit.png')
#pylab.clf()

#compute model chi-sq
chisq = (residual**2/std**2).sum()
dof = len(counts)-len(ans)
print 'Chi-Sq =', chisq
print 'dof = ', dof
print 'PTE = ', scipy.stats.stats.chisqprob(chisq,dof)

pylab.show()
