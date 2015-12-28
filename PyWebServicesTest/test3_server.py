'''
Created on Jul 16, 2012

@author: leal
'''

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
import pprint as pp



### General functions to call remotely

def adder(a,b):
    "Add two values"
    return a+b

def multiplier(a,b):
    "Multiply two values"
    return a*b

#######################


dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8080/",
    action = 'http://localhost:8080/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# register the user function
dispatcher.register_function('Adder', adder,
    returns={'AddResult': int}, 
    args={'a': int,'b': int},
    doc = 'Add two values...')

dispatcher.register_function('Multiplier', multiplier,
    returns={'MultResult': int}, 
    args={'a': int,'b': int},
    doc = 'Multiply two values...')

### Print registered methods
print 'List of Registered methods' 
pp.pprint(dispatcher.list_methods(), indent=2, width=1)


### Start the webserver in port 8080
print "Starting server..."
httpd = HTTPServer(("", 8080), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()

