import numpy # numerical python (matrices etc)
import pylab # plotting
import scipy.stats.stats # scientific python

'''
From: https://wiki.pha.jhu.edu/advlab_wiki/index.php/Analysis_4
'''

# load data (unpack = read in by column)
time, alt0, alt1, alt2, alt3, alt4 = numpy.loadtxt('altitudes.txt', unpack=True)

#Get mean and variance: fancier ways to do this
mean = (alt0 + alt1 + alt2 + alt3 + alt4)/5
var  = ((alt0-mean)**2 + (alt1-mean)**2 + (alt2-mean)**2 + \
        (alt3-mean)**2 + (alt4-mean)**2)/4  # 
std  = numpy.sqrt( var )
var_on_mean = var/4
std_on_mean = numpy.sqrt(var_on_mean)
print 'time', time
print 'mean', mean
print 'std on mean', std_on_mean

#Plot (maybe skip this in the presentation)
pylab.subplot(2, 1, 1)
pylab.title("Raw Data")
pylab.plot(time, alt0,  'b.') 
pylab.plot(time, alt1,  'rx' )
pylab.plot(time, alt2,  'g*') 
pylab.plot(time, alt3,  'y^') 
pylab.plot(time, alt4,  'c+') 
pylab.errorbar(time, mean, std, fmt ='o', color='black')
font_size= 16
pylab.xlabel('Time (s)', fontsize=font_size)
pylab.ylabel('Altitude (m)', fontsize=font_size)
ax = pylab.gca()
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(font_size)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(font_size)
pylab.xlim([-.5, 4.5])
#pylab.savefig('data.png')

# Fit the data
# 
# Model is  
# d = a*t**2 + b*t + c <=> [t**2,t,1][a] = M x
#                                    [b]
#                                    [c]
#
# Maximimum Likelihood solution  x_ml = (MT N_inv M)^{-1} MT N_inv data
#

data = mean
print "data shape", data.shape
N_inv = numpy.diag(1/var_on_mean)  # diag function creates a diagonal matrix
print "N_inv shape", N_inv.shape

# Construct time matix
M = numpy.array([time**2, time, numpy.ones(len(time))]).transpose()
print "M shape", M.shape
MT = M.transpose()
print "MT shape", MT.shape

#Compute MT N_inv M
inv_cov = numpy.dot(MT,numpy.dot(N_inv,M))
cov     = numpy.linalg.inv(inv_cov)

#Compute MT N_inv data
rhs = numpy.dot(MT, numpy.dot( N_inv, data )) #rhs of equation

#Compute ML solution
x_ml = numpy.dot(cov, rhs)

print "a,b,c = ", x_ml
print "var(a,b,c) = ", cov[0,0], cov[1,1], cov[2,2]

#Final plot
#pylab.clf()
pylab.subplot(2, 1, 2)
pylab.title("Fitting")
pylab.errorbar(time, mean, std_on_mean, fmt ='o', color='black', label='data')
t_model = numpy.arange(-.4,4.5,.1)
alt_model = x_ml[0]*t_model**2 + x_ml[1]*t_model + x_ml[2]
pylab.plot(t_model, alt_model, label = 'model')
pylab.legend()
pylab.xlabel('Time (s)', fontsize=font_size)
pylab.ylabel('Altitude (m)', fontsize=font_size)
#pylab.savefig("data_with_model.png")


#Chi-squared

residual = data - numpy.dot(M, x_ml)
print residual
print residual**2
print var
chisq = numpy.sum(residual**2 / var_on_mean)
dof = len(residual)-3 # 3 parameters
print "chisq =", chisq, "with", dof, "dof"
print "PTE = ", scipy.stats.stats.chisqprob(chisq, dof)

pylab.show()