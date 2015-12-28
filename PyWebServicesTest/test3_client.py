'''
Created on Jul 16, 2012

@author: leal
'''

from pysimplesoap.client import SoapClient
import time

# create a simple consumer
client = SoapClient(
    location = "http://localhost:8080/",
    action = 'http://localhost:8080/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", 
    soap_ns='soap',
    trace = False,
    ns = False)

#############

# Local functions ro compare:
def localAdder(a,b):
    "Add two values"
    return a+b

def localMultiplier(a,b):
    "Multiply two values"
    return a*b

#############

print '** 1st Remote Call'
t0 = time.time()
# call the remote method
response = client.Adder(a=3, b=2)
# extract and convert the returned value
result = response.AddResult
remoteTime = float(time.time()-t0)
print 'Adder time = %.2e: '% remoteTime
print 'AddResult:', int(result)

print '** 2nd Remote Call'
t0 = time.time()
# call the remote method
response = client.Adder(a=4, b=5)
# extract and convert the returned value
result = response.AddResult
remoteTime = float(time.time()-t0)
print 'Adder time = %.2e: '% remoteTime
print 'AddResult:', int(result)

print '** Local Call'
# local
t0 = time.time()
result = localAdder(a=3, b=2)
localTime = float(time.time()-t0)
print 'Local Adder time = %.2e: '% localTime
print 'Local AddResult:', int(result)

print 'Local is %.1f times faster'% (remoteTime/localTime)


#############

print '** Remote multiplication...'

# call the remote method
response = client.Multiplier(a=3, b=2)
# extract and convert the returned value
result = response.MultResult
print 'MultResult:', int(result)
