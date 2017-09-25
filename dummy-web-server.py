#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost:8080

Send a HEAD request::
    curl -I http://localhost:8080

Send a POST request::
    curl -d '["foo", {"bar":["baz", null, 1.0, 2]}]' http://localhost:8080

"""

import SimpleHTTPServer
import SocketServer
import json

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        try:
            data = json.loads(post_body)
        except ValueError:
            data = post_body
        self.wfile.write(
            "<html><body><h1>POST:\n{}\n</h1></body></html>".format(
                data))


Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()
