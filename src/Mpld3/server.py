import SimpleHTTPServer
import SocketServer

PORT = 8080

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "serving at port", PORT, "Open in your browser: http://localhost:%s/"%PORT
print "If you need to kill the connection: fuser  -n tcp -k", PORT
httpd.serve_forever()
