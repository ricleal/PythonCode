'''
Created on Jul 1, 2013

@author: leal

pysimplesoap



'''
from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler

def adder(a, b):
    "Add two values"
    return a + b

dispatcher = SoapDispatcher(
    'my_dispatcher',
    location="http://localhost:8008/",
    action='http://localhost:8008/',  # SOAPAction
    namespace="http://example.com/sample.wsdl", prefix="ns0",
    trace=True,
    ns=True)

# register the user function
dispatcher.register_function('Adder', adder,
    returns={'AddResult': int},
    args={'a': int, 'b': int})

application = WSGISOAPHandler(dispatcher)

if __name__ == "__main__":
    print "Starting server..."
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8008, application)
    httpd.serve_forever()
