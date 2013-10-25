'''
Created on Jul 16, 2012

@author: leal
'''

from soaplib.client import make_service_client
from test2_server import HelloService

client = make_service_client('http://localhost:8080/hello', HelloService())


inputMsg = 'Ricardo'
print 'Sending to server: ', inputMsg

retMsg = client.hello(inputMsg)
print 'Server sent back <' + retMsg + '>'

