import SimpleHTTPServer
import SocketServer
import sys

PORT = 8080
    
def main(argv):
    global PORT
    try:
        PORT = int(argv[0])
    except:
        pass
    
    print "serving at port", PORT, "Open in your browser: http://localhost:%s/"%PORT
    print "If you need to kill the connection: fuser  -n tcp -k", PORT
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    httpd.serve_forever()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])